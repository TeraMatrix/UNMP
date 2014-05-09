var formStatus = 0;				/* { 0:form for add and upadate not present, 1:form for add and upadate not present } */

/* Active Host */
var $gridViewActiveHostTableObj = null;
var $gridViewActiveHostDataTable = null;
var $gridViewActiveHostFetched = 0;
var $gridViewActiveHostSelectedTr = [];			/* Datatable selected rows Array */

/* Disable Host */
var $gridViewDisableHostTableObj = null;
var $gridViewDisableHostDataTable = null;
var $gridViewDisableHostFetched = 0;
var $gridViewDisableHostSelectedTr = [];		/* Datatable selected rows Array */

/* Discovered Host */
var $gridViewDiscoveredHostTableObj = null;
var $gridViewDiscoveredHostDataTable = null;
var $gridViewDiscoveredHostFetched = 0;
var $gridViewDiscoveredHostSelectedTr = [];		/* Datatable selected rows Array */

/* Deleted Host */
var $gridViewDeletedHostTableObj = null;
var $gridViewDeletedHostDataTable = null;
var $gridViewDeletedHostFetched = 0;
var $gridViewDeletedHostSelectedTr = [];		/* Datatable selected rows Array */

var $gridViewDiv = null;
var $formDiv = null;
var $spinLoading = null;
var $spinMainLoading  = null;
var $form = null;
var $formTitle = null;
var $formInput = null;
var $formPassword = null;
var $formTextarea = null;
var $formCheckbox = null;
var $formSelectList = null;
var $formAddButton = null;
var $formEditButton = null;
var $RaMacDiv = null;
var $MasterSlaveDiv = null;
var $tooltip = null;
var hostDefaultDetails = null;
var currentTab = null; 				// active,disable,discovered,deleted, etc. 


// Header buttons
var $addButtonHead = null;
var $editButtonHead = null;
var $delButtonHead = null;

//selected host details
var selectedHostName = null;
var selectedHostAlias = null;
var selectedIpAddress = null;
var selectedMacAddress = null;
var selectedDeviceType = null;

var messages = {
	"add":"Host added successfully.",
	"edit":"Host details updated successfully.",
	"del":"Selected host(s) deleted successfully",
	"delConfirm":"Are you sure want to delete the selected host(s)?",
	"duplicateError":"Please enter a different Host Name, Host Alias, IP  and MAC",
	"noneSelectedError":"Please select atleast one Host",
	"multiSelectedError":"Please select a single Host.",
	"localhostDelError":"Deletion of localhost is restricted",
	"localhostEditError":"Update of localhost is restricted",
	"validationError":"Invalid host details are entered, please recheck",
	"dbError":"UNMP Database Server is busy at the moment, please try again later ",
	"noRecordError":"No such record found",
	"sysError":"UNMP Server is busy at the moment, please try again later",
	"unknownError":"UNMP Server is busy at the moment, please try again later ",
	"licenseError":"To successfully complete this action please upgrade your license.",
	"loadDefaultSettingWarn":"UNMP Server is busy at the moment, please try again later",
	"noNmsInctanceError":"UNMP Server is busy at the moment, please try again later.",
	"nagiosConfigError":"UNMP Server is busy at the moment, please try again later time.",
	"changeIpAddressConfirm":"Do You want to change the network configuration of the device?",
	"changeIpAddressError":"Failed to change the network details of the device. Please try again",
	"raMacMissing":"RA MAC is required for UBR and UBRe type devices",
	"raMacWarning":"Note: Incorrect RA MAC will cause a failure of device configuration",
	"raMacError":"Please recheck the MAC address.",
	"masterMacMissing":"Master node’s MAC is required for UBR and UBRe Slave device",
	"masterMacWarning":" Note: Incorrect RA MAC will cause a failure of device configuration ",
	"masterMacError":"Please choose a correct device Master.",
	"licenseDeviceError":"Maximum limit of allowed host for this device type is reached",
	"addDeletedHost":"Do you want to restore the selected host(s)?"
};
var actionName = null;
var oldIpAddress = null;
var oldNetmask = null;
var oldGateway = null;
var oldDhcp = null;
var oldPriIp = null;
var oldSecIp = null;

$(function(){

	/* header button object*/
	$addButtonHead = $("#add_host").parent();
	$editButtonHead = $("#edit_host").parent();
	$delButtonHead = $("#del_host").parent();

	/* create object of divs */
	$gridViewDiv = $("div#grid_view_div");
	$formDiv = $("div#form_div");
	
	/* show grid view only hide other */
	$gridViewDiv.show();
	$formDiv.hide();
	
	// spin loading object
	$spinLoading = $("div#spin_loading");		// create object that hold loading circle
	$spinMainLoading = $("div#main_loading");	// create object that hold loading squire
	
	// page tip [for page tip write this code on each page please dont forget to change "href" value because this link create your help tip page]
	$("#page_tip").colorbox(
	{
		href:"help_inventory_host.py",
		title: "Help",
		opacity: 0.4,
		maxWidth: "80%",
		width:"600px",
		height:"400px"
	});
	$("div.yo-tabs","div#container_body").yoTabs();
	
	/* Add Data Table Tr Selecter Click Handler*/
	dataTableClickHandler();
		
	/* Call Active Host Data Table */
	$gridViewActiveHostTableObj = $("table#grid_view_active_host");
	//gridViewActiveHost();
	
	/* Call Active Host Data Table */
	$gridViewDisableHostTableObj = $("table#grid_view_disable_host");
	//gridViewDisableHost();
	
	/* Call Active Host Data Table */
	$gridViewDiscoveredHostTableObj = $("table#grid_view_discovered_host");
	//gridViewDeletedHost();
	
	/* Call Active Host Data Table */
	$gridViewDeletedHostTableObj = $("table#grid_view_deleted_host");
	//gridViewDiscoveredHost();
	
	/* Bind Function With Tabs */
	
	/* Active Host Tab*/
	$("a#active_host_tab").click(function(e){
		e.preventDefault();
		currentTab = "active";
		if($gridViewActiveHostFetched == 0)
		{
			gridViewActiveHost();
		}
		$addButtonHead.show();
		$editButtonHead.show();
		$delButtonHead.show();
	});
	
	/* Disable Host Tab*/
	$("a#disable_host_tab").click(function(e){
		e.preventDefault();
		currentTab = "disable";
		if($gridViewDisableHostFetched == 0)
		{
			gridViewDisableHost();
		}
		$addButtonHead.show();
		$editButtonHead.show();
		$delButtonHead.show();
	});
	
	/* Discovered Host Tab*/
	$("a#discovered_host_tab").click(function(e){
		e.preventDefault();
		currentTab = "discovered";
		if($gridViewDiscoveredHostFetched == 0)
		{
			gridViewDiscoveredHost();
		}
		$addButtonHead.show();
		$editButtonHead.hide();
		$delButtonHead.show();
	});
	
	/* Deleted Host Tab*/
	$("a#deleted_host_tab").click(function(e){
		e.preventDefault();
		currentTab = "deleted";
		if($gridViewDeletedHostFetched == 0)
		{
			gridViewDeletedHost();
		}
		$addButtonHead.hide();
		$editButtonHead.hide();
		$delButtonHead.show();
	});
	
	/* It Shows Active Host as Default Host Grid View */
	$("a#active_host_tab").click();
});

function dataTableClickHandler()
{
	/* Click event handler for active host grid view */
	$("table#grid_view_active_host tbody tr").live('click', function (event) {
		var id = this.id;
		if(event.target.nodeName.toLowerCase() != 'img')
		{
			var index = jQuery.inArray(id, $gridViewActiveHostSelectedTr);
		
			if ( index === -1 ) {
				$gridViewActiveHostSelectedTr.push( id );
			} else {
				$gridViewActiveHostSelectedTr.splice( index, 1 );
			}
		
			$(this).toggleClass('row_selected');
		}
	});
	/* Click event handler for disable host grid view */
	$("table#grid_view_disable_host tbody tr").live('click', function (event) {
		var id = this.id;
		if(event.target.nodeName.toLowerCase() != 'img')
		{
			var index = jQuery.inArray(id, $gridViewDisableHostSelectedTr);
		
			if ( index === -1 ) {
				$gridViewDisableHostSelectedTr.push( id );
			} else {
				$gridViewDisableHostSelectedTr.splice( index, 1 );
			}
		
			$(this).toggleClass('row_selected');
		}
	});
	/* Click event handler for discovered host grid view */
	$("table#grid_view_discovered_host tbody tr").live('click', function () {
		var id = this.id;
		var index = jQuery.inArray(id, $gridViewDiscoveredHostSelectedTr);
		
		if ( index === -1 ) {
			$gridViewDiscoveredHostSelectedTr.push( id );
		} else {
			$gridViewDiscoveredHostSelectedTr.splice( index, 1 );
		}
		
		$(this).toggleClass('row_selected');
	});
	/* Click event handler for deleted host grid view */
	$("table#grid_view_deleted_host tbody tr").live('click', function () {
		//if($(event.target))
		//alert(event.target);
		var id = this.id;
		var index = jQuery.inArray(id, $gridViewDeletedHostSelectedTr);
		
		if ( index === -1 ) {
			$gridViewDeletedHostSelectedTr.push( id );
		} else {
			$gridViewDeletedHostSelectedTr.splice( index, 1 );
		}
		
		$(this).toggleClass('row_selected');
	});
}


function gridViewActiveHost()
{
	//spinStart($spinLoading,$spinMainLoading);
	$gridViewActiveHostDataTable = $gridViewActiveHostTableObj.dataTable({
				"bServerSide": true,
				"sAjaxSource": "grid_view_active_host.py",
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true,
				"bStateSave": false,
				"fnServerData": function(sSource,aoData,fnCallback){
					$.getJSON( sSource, aoData, function (json) { 
						/**
						 * Insert an extra argument to the request: rm.
						 * It's the the name of the CGI form parameter that
						 * contains the run mode name. Its value is the
						 * runmode, that produces the json output for
						 * datatables.
						 **/
						fnCallback(json)
						$('img.host_opr').tipsy({gravity: 'n'}); // n | s | e | w
					});
				}
			});
			
			$gridViewActiveHostDataTable.fnSetColumnVis( 0, false,false );
			$gridViewActiveHostDataTable.fnSetColumnVis( 1, false,false );
			//oTable.fnSetColumnVis( 2, false,false );
	/*$.ajax({
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
				"oLanguage":{
					"sInfo":"_START_ - _END_ of _TOTAL_",
					"sInfoEmpty":"0 - 0 of 0",
					"sInfoFiltered":"(of _MAX_)"
				},
				"fnRowCallback": function( nRow, aData, iDisplayIndex ) {
					if ( jQuery.inArray(aData.DT_RowId, $gridViewActiveHostSelectedTr) !== -1 ) {
						$(nRow).addClass('row_selected');
					}
					return nRow;
				},
				"aoColumns": [
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 0 ] },
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 1 ] },
					{ "sTitle": "Host Name" , "sClass": "center", "sWidth": "18%"},
					{ "sTitle": "Host Alias" , "sClass": "center", "sWidth": "20%"},
					{ "sTitle": "IP Address", "sClass": "center", "sWidth": "18%" },
					{ "sTitle": "Device Type", "sClass": "center", "sWidth": "18%" },
					{ "sTitle": "MAC Address", "sClass": "center", "sWidth": "17%" },
					{ "sTitle": " ", "sWidth": "9%" }
				]
			});*/
			//$gridViewActiveHostDataTable.fnDraw();
			//spinStop($spinLoading,$spinMainLoading);
		/*}
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
				"bStateSave": false,
				"bLengthChange":true,
				"fnServerData": function(sSource,aoData,fnCallback){
					$.getJSON( sSource, aoData, function (json) { 
						/**
						 * Insert an extra argument to the request: rm.
						 * It's the the name of the CGI form parameter that
						 * contains the run mode name. Its value is the
						 * runmode, that produces the json output for
						 * datatables.
						 **/
						fnCallback(json)
						$('img.host_opr').tipsy({gravity: 'n'}); // n | s | e | w
					});
				}
			});
			$gridViewDisableHostDataTable.fnSetColumnVis( 0, false,false );
			$gridViewDisableHostDataTable.fnSetColumnVis( 1, false,false );
			//$gridViewDisableHostDataTable.fnDraw();
			//spinStop($spinLoading,$spinMainLoading);
		/*}
	});*/
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
				"oLanguage":{
					"sInfo":"_START_ - _END_ of _TOTAL_",
					"sInfoEmpty":"0 - 0 of 0",
					"sInfoFiltered":"(of _MAX_)"
				},
				"fnRowCallback": function( nRow, aData, iDisplayIndex ) {
					if ( jQuery.inArray(aData.DT_RowId, $gridViewDisableHostSelectedTr) !== -1 ) {
						$(nRow).addClass('row_selected');
					}
					return nRow;
				},
				"aoColumns": [
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 0 ] },
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 1 ] },
					{ "sTitle": "Host Name" , "sClass": "center", "sWidth": "18%"},
					{ "sTitle": "Host Alias" , "sClass": "center", "sWidth": "20%"},
					{ "sTitle": "IP Address", "sClass": "center", "sWidth": "18%" },
					{ "sTitle": "Device Type", "sClass": "center", "sWidth": "18%" },
					{ "sTitle": "MAC Address", "sClass": "center", "sWidth": "17%" },
					{ "sTitle": " ", "sWidth": "9%" }
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
				"bServerSide": true,
				"sAjaxSource": "grid_view_discovered_host.py",
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true,
				"bStateSave": false
			});
			$gridViewDiscoveredHostDataTable.fnSetColumnVis( 0, false,false );
	/*spinStart($spinLoading,$spinMainLoading);
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
				"oLanguage":{
					"sInfo":"_START_ - _END_ of _TOTAL_",
					"sInfoEmpty":"0 - 0 of 0",
					"sInfoFiltered":"(of _MAX_)"
				},
				"fnRowCallback": function( nRow, aData, iDisplayIndex ) {
					if ( jQuery.inArray(aData.DT_RowId, $gridViewDiscoveredHostSelectedTr) !== -1 ) {
						$(nRow).addClass('row_selected');
					}
					return nRow;
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
				"bServerSide": true,
				"sAjaxSource": "grid_view_deleted_host.py",
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true,
				"bStateSave": false
			});
			$gridViewDeletedHostDataTable.fnSetColumnVis( 0, false,false );
			$gridViewDeletedHostDataTable.fnSetColumnVis( 1, false,false );
/*
	spinStart($spinLoading,$spinMainLoading);
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
				"oLanguage":{
					"sInfo":"_START_ - _END_ of _TOTAL_",
					"sInfoEmpty":"0 - 0 of 0",
					"sInfoFiltered":"(of _MAX_)"
				},
				"fnRowCallback": function( nRow, aData, iDisplayIndex ) {
					if ( jQuery.inArray(aData.DT_RowId, $gridViewDeletedHostSelectedTr) !== -1 ) {
						$(nRow).addClass('row_selected');
					}
					return nRow;
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




function oduMasterList(deviceTypeId,master_id)
{
	$.ajax({
		type:"get",
		url:"odu_master_list.py?device_type_id=" + String(deviceTypeId),
		cache:false,
		success:function(result){
			var $result = $(result);
			$formSelectList.eq(2).html($result.html());
			$formSelectList.eq(2).val(master_id);
		}
	});
}
function showMasterMacDiv()
{
	var nodeType = $formSelectList.eq(1).val();
	try
	{
		if(parseInt(nodeType) == 1 || parseInt(nodeType) == 3)
		{
			oduMasterList($formSelectList.eq(0).val(),"")
			$MasterSlaveDiv.show();
		}
		else
		{
			$MasterSlaveDiv.hide();
		}
	}
	catch(err)
	{
		$MasterSlaveDiv.hide();
	}
}
function fetchRAMacAddress()
{
	var ip_address = $formInput.eq(2).val();
	if($formSelectList.eq(0).val() == "odu16")
	{
		ip_address = ip_address + ":" +$formInput.eq(10).val();
	}
	else if($formSelectList.eq(0).val() == "odu100")
	{
		//ip_address = ip_address;
		// do nothing
	}
	$("#ra_mac_loading").show();
	$("a#a_fetch_ra_mac").hide();
	$.ajax({
		type:"get",
		url:"get_odu_ra_mac_and_node_type.py?ip_address=" + ip_address + "&username=" + $formInput.eq(9).val() + "&password=" + $formPassword.eq(0).val() + "&community=" + $formInput.eq(11).val() + "&port=" + $formInput.eq(13).val() + "&device_type=" + $formSelectList.eq(0).val(),
		cache:false,
		success:function(result){
			//{"node_type":node_type,"ra_mac":ra_mac}
			//result = eval("(" + result + ")");
			
			$formSelectList.eq(1).val(result.node_type);
			$formInput.eq(4).val(result.ra_mac);
			//$formInput.eq(3).val(result.ra_mac);
			showMasterMacDiv();
			$("#ra_mac_loading").hide();
			$("a#a_fetch_ra_mac").show();
		}
	});
}
function fetchMasterMacAddress()
{
	$("#master_mac_loading").show();
	$("#a_fetch_master_mac").hide();
	$.ajax({
		type:"get",
		url:"get_master_mac_from_slave.py?ip_address=" + $formInput.eq(2).val() + ":" + $formInput.eq(10).val() + "&username=" + $formInput.eq(9).val() + "&password=" + $formPassword.eq(0).val() + "&community=" + $formInput.eq(11).val() + "&port=" + $formInput.eq(13).val(),
		cache:false,
		success:function(result){
			//{"node_type":node_type,"ra_mac":ra_mac}
			$formSelectList.eq(2).val(result);
			$("#master_mac_loading").hide();
			$("#a_fetch_master_mac").show();
		}
	});
}

function deviceTypeChange(deviceTypeSelectList)
{
	deviceTypeSelectList.change(function(){
		var selectedDeviceType = $(this).val();
		if(selectedDeviceType == "odu16" || selectedDeviceType == "odu100")
		{
			$RaMacDiv.show();
			showMasterMacDiv();
		}
		else
		{
			$RaMacDiv.hide();
			$MasterSlaveDiv.hide();
		}
		// spacial case which is you can remove when you get fetch all devices http and snmp cradentails separately
		if(actionName == "add")
		{
			if(selectedDeviceType == "ap25")
			{
				$formInput.eq(9).val("admin");
				$formPassword.eq(0).val("password");
				$formInput.eq(10).val("");
				$formInput.eq(11).val("public");
				$formInput.eq(12).val("private");
				$formInput.eq(13).val("161");
				$formInput.eq(14).val("162");
				$formSelectList.eq(8).val("2c");
			}
			else if(selectedDeviceType == "odu16")
			{
				$formInput.eq(9).val("admin");
				$formPassword.eq(0).val("vnlggn");
				$formInput.eq(10).val("5555");
				$formInput.eq(11).val("public");
				$formInput.eq(12).val("private");
				$formInput.eq(13).val("161");
				$formInput.eq(14).val("162");
				$formSelectList.eq(8).val("2c");
				fetchRAMacAddress();
			}
			else if(selectedDeviceType == "odu100")
			{
				$formInput.eq(9).val("admin");
				$formPassword.eq(0).val("public");
				$formInput.eq(10).val("");
				$formInput.eq(11).val("public");
				$formInput.eq(12).val("private");
				$formInput.eq(13).val("161");
				$formInput.eq(14).val("162");
				$formSelectList.eq(8).val("2c");
				fetchRAMacAddress();
			}
			else if(selectedDeviceType == "idu4")
			{
				$formInput.eq(9).val("admin");
				$formPassword.eq(0).val("vnlggn");
				$formInput.eq(10).val("5555");
				$formInput.eq(11).val("public");
				$formInput.eq(12).val("private");
				$formInput.eq(13).val("8001");
				$formInput.eq(14).val("8002");
				$formSelectList.eq(8).val("2c");
			}
			else if(selectedDeviceType == "idu8")
			{
				$formInput.eq(9).val("admin");
				$formPassword.eq(0).val("vnlggn");
				$formInput.eq(10).val("5555");
				$formInput.eq(11).val("public");
				$formInput.eq(12).val("private");
				$formInput.eq(13).val("8001");
				$formInput.eq(14).val("8002");
				$formSelectList.eq(8).val("2c");
			}
			else if(selectedDeviceType == "swt4")
			{
				$formInput.eq(9).val("admin");
				$formPassword.eq(0).val("public");
				$formInput.eq(10).val("");
				$formInput.eq(11).val("public");
				$formInput.eq(12).val("private");
				$formInput.eq(13).val("161");
				$formInput.eq(14).val("162");
				$formSelectList.eq(8).val("2c");
			}
			else
			{
				$formInput.eq(9).val("");
				$formPassword.eq(0).val("");
				$formInput.eq(10).val("");
				$formInput.eq(11).val("public");
				$formInput.eq(12).val("private");
				$formInput.eq(13).val("161");
				$formInput.eq(14).val("162");
				$formSelectList.eq(8).val("2c");
			}
		}
	});
}

function createForm(act,id)
{
	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"get",
		url:"form_host.py",
		cache:false,
		success:function(result){
			$formDiv.html(result);
			addFormToolTip();
			cancelForm();
			$form = $("form#form_host");
			$formTitle = $("form#form_host th#form_title");
			$formInput = $("form#form_host input[type='text']");
			$formPassword = $("form#form_host input[type='password']");
			$formTextarea = $("form#form_host textarea");
			$formCheckbox = $("form#form_host input[type='checkbox']");
			$formSelectList = $("form#form_host select");
			$formAddButton = $("form#form_host button[id='add_host']");
			$formEditButton = $("form#form_host button[id='edit_host']");
			$RaMacDiv = $("#ra_mac_div,#node_type_div","form#form_host");
			$MasterSlaveDiv = $("#master_slave_div","form#form_host");
			submitForm($form);
			if(act == "edit")
			{
				editForm(id);
			}
			else
			{
				addForm();
			}
			spinStop($spinLoading,$spinMainLoading);
			deviceTypeChange($formSelectList.eq(0));
			$formSelectList.eq(1).change(function(){
				showMasterMacDiv();
			});
		}
	});
}
function addFormToolTip()
{
	// add tool tip
	$tooltip = $("form#form_host input[type='text'],form#form_host input[type='password'],form#form_host input[type='checkbox'],form#form_host textarea,form#form_host select").tooltip({
		// place tooltip on the right edge
		position: "center right",
		// a little tweaking of the position
		offset: [-2, 10],
		// use the built-in fadeIn/fadeOut effect
		effect: "fade",
		// custom opacity setting
		opacity: 1.0
	});
}
function cancelForm()
{
	$("button#cancel_host").click(function(){
		hideForm();
	});
}
function showForm()
{
	$gridViewDiv.hide();
	$formDiv.show();
}
function hideForm()
{
	$gridViewDiv.show();
	$formDiv.hide();
	/* this is bcoz when validation unsuccess and you click on cancel button then tooltip visible so this code will hide that. */
	if($tooltip)
		$tooltip.tooltip().hide();
}
function submitForm($formObj)
{
	valiateForm($formObj);
	$formObj.submit(function(){
		var $formThis = $(this);
		if($formThis.valid())
		{
			spinStart($spinLoading,$spinMainLoading);
			var action = $formThis.attr("action");
			var method = $formThis.attr("method");
			var data = $formThis.serialize();
			/*
			 * Check Host Details in case device type is odu16 and oud100
			 */
			if($formSelectList.eq(0).val() == "odu16" ||$formSelectList.eq(0).val() == "odu100")
			{
				var raMacValue = $formInput.eq(4).val();
				if($.trim(raMacValue) == "")
				{
					$.prompt(messages["raMacMissing"],{prefix:'jqismooth'});
					spinStop($spinLoading,$spinMainLoading);
					return false;
				}
				else
				{
					if(raMacValue.match("^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$"))
					{
						var nodeType = $formSelectList.eq(1).val();;
						try
						{
							if(parseInt(nodeType) == 1 || parseInt(nodeType) == 3)
							{
								// check master mac
								var masterMacValue = $formSelectList.eq(2).val();
								if($.trim(masterMacValue) == "")
								{
									$.prompt(messages["masterMacMissing"],{prefix:'jqismooth'});
									spinStop($spinLoading,$spinMainLoading);
									return false;
								}
								else
								{
									// do nothing
									$.prompt(messages["raMacWarning"] + "<br/>" + messages["masterMacWarning"],{prefix:'jqismooth'});
								}
							}
							else
							{
								$.prompt(messages["raMacWarning"],{prefix:'jqismooth'});
							}
							
						}
						catch(err)
						{
							
						}
					}
					else
					{
						$.prompt(messages["raMacError"],{prefix:'jqismooth'});
						spinStop($spinLoading,$spinMainLoading);
						return false;
					}
				}
			}
			if(actionName == "edit")
			{
				if(oldIpAddress == $formInput.eq(2).val() && oldNetmask == $formInput.eq(5).val() && oldGateway == $formInput.eq(6).val() && oldDhcp == $formSelectList.eq(7).val() && oldPriIp == $formInput.eq(7).val()  && oldSecIp == $formInput.eq(8).val())
				{
					action += "?ip_update=0";
					submitAjaxCall(method,action,data);
				}
				else
				{
					$.prompt(messages["changeIpAddressConfirm"],{ buttons:{Yes:true,No:false}, prefix:'jqismooth',callback:function(v,m) { if(v != undefined && v==true){ action += "?ip_update=1"; } else { action += "?ip_update=0";} submitAjaxCall(method,action,data);} });
				}
			}
			else
			{
				submitAjaxCall(method,action,data);
			}
			
		}
		else
		{
			$().toastmessage('showErrorToast', messages["validationError"]);
		}
		return false;
	});
}
function submitAjaxCall(method,action,data)
{
	$.ajax({
		type:method,
		url:action,
		data:data,
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
				hideForm();
				$().toastmessage('showSuccessToast', messages[actionName]);
				if(currentTab == "active")
				{
					gridViewActiveHost();
					$gridViewDisableHostFetched = 0;
					$gridViewDiscoveredHostFetched = 0;
				}
				else if(currentTab == "disable")
				{
					gridViewDisableHost();
					$gridViewActiveHostFetched = 0;
					$gridViewDiscoveredHostFetched = 0;
				}
				else if(currentTab == "discovered")
				{
					gridViewDiscoveredHost();
					$gridViewDisableHostFetched = 0;
					$gridViewActiveHostFetched = 0;
				}
				update_host_parents();
			}
			else
			{
				$().toastmessage('showErrorToast', messages[result.msg]);
			}
			spinStop($spinLoading,$spinMainLoading);
		}
	});
}
function valiateForm($formObj)
{
	$formObj.validate({
		rules:{
			host_name:{
				required:true,
				alphaNumeric: true,
				noSpace: true
			},
			host_alias:{
				required:true,
				alphaNumeric: true
			},
			ip_address:{
				required:true,
				ipv4Address:true
			},
			mac_address:{
				required:true,
				macAddress:true
			},
			device_type:{
				required:true
			},
			host_state:{
				required:true
			},
			host_priority:{
				required:true
			},
			host_parent:{
				required:true
			},
			host_comment:{
				alphaNumeric: true
			},
			netmask:{
				//netmask:true,
				ipv4Address:true,
				required:true
			},
			gateway:{
				ipv4Address:true,
				required:true
			},
			primary_dns:{
				ipv4Address:true
			},
			secondary_dns:{
				ipv4Address:true
			},
			http_username:{
				alphaNumeric: true
			},
			http_password:{
				alphaNumeric: true
			},
			http_port:{
				number: true
			},
			read_community:{
				alphaNumeric: true
			},
			write_community:{
				alphaNumeric: true
			},
			snmp_version:{
				alphaNumeric: true
			},
			get_set_port:{
				number: true
			},
			trap_port:{
				number: true
			},
			longitude:{
				number: true
			},
			latitude:{
				number: true
			},
			serial_number:{
				alphaNumeric: true
			},
			hardware_version:{
				alphaNumeric: true
			},
			host_vendor:{
				required: true
			},
			host_os:{
				required: true
			}
		},
		messages:{
			host_name:{
				required:"Host name is a required field",
				alphaNumeric: "Host name should be alpha numeric",
				noSpace: "In host name space are not allowed"
			},
			host_alias:{
				required:"Host alias is a required field",
				alphaNumeric: "Host alias should be alpha numeric"
			},
			ip_address:{
				required:"IP address is a required field",
				ipv4Address:"Invalid IP address"
			},
			mac_address:{
				required:"MAC address is a required field",
				macAddress:"Invalid MAC address"
			},
			device_type:{
				required:"Device type is a required field"
			},
			host_state:{
				required:"Host state is a required field"
			},
			host_priority:{
				required:"Host priority is a required field"
			},
			host_parent:{
				required:"Host parent is a required field"
			},
			host_comment:{
				alphaNumeric: "Comment should be alhpa numeric"
			},
			netmask:{
				//netmask:"Invalid Netmask",
				ipv4Address:"Invalid Netmask",
				required:"Netmask is a required field"
			},
			gateway:{
				ipv4Address:"Invalid IP Address",
				required:"Gateway is a required field"
			},
			primary_dns:{
				ipv4Address:"Invalid IP Address"
			},
			secondary_dns:{
				ipv4Address:"Invalid IP Address"
			},
			http_username:{
				alphaNumeric: "Username should be alpha numeric"
			},
			http_password:{
				alphaNumeric: "Password should be alpha numeric"
			},
			http_port:{
				number: "Port should be a number"
			},
			read_community:{
				alphaNumeric: "Read community should be alpha numeric"
			},
			write_community:{
				alphaNumeric: "Write community should be alpha numeric"
			},
			snmp_version:{
				alphaNumeric: "SNMP version should be correct"
			},
			get_set_port:{
				number: "SNMP get/set port should be a number"
			},
			trap_port:{
				number: "SNMP trap port should be a number"
			},
			longitude:{
				number: "Longitude should be a number"
			},
			latitude:{
				number: "Latitude should be a number"
			},
			serial_number:{
				alphaNumeric: "Serial number should be a alpha numeric"
			},
			hardware_version:{
				alphaNumeric: "Hardware version should be a alpha numeric"
			},
			host_vendor:{
				required: "Host Vendor is a required field"
			},
			host_os:{
				required: "Host OS name is a required field"
			}
		}
	});
}
function addForm()
{
	if(currentTab == "discovered")
	{
		var selectedRow = new Array();
		selectedRow = fnGetSelected($gridViewDiscoveredHostDataTable)
		var rLength = selectedRow.length; 
		if(rLength==0)
		{
			$.prompt(messages["noneSelectedError"],{prefix:'jqismooth'});
		}
		else if(rLength == 1)
		{
			// get data
			for(var i = 0;i<selectedRow.length;i++)
			{
				var aData = [];
				var iRow = $gridViewDiscoveredHostDataTable.fnGetPosition(selectedRow[i]);
				aData = $gridViewDiscoveredHostDataTable.fnGetData(iRow);
		
				//selected host details
				selectedHostName = aData[2];
				selectedHostAlias = aData[2];
				selectedIpAddress = aData[2];
				selectedMacAddress = aData[3];
				selectedDeviceType = "";
			}
	
			$formTitle.html("Add Host");
			$form.attr("action","add_host.py");
			manage_host_parents(null);
			//$formInput.val("");
			//$formTextarea.val("");
			$formAddButton.css({"display":"inline-block"});
			$formEditButton.hide();
			showForm();		
			if(!hostDefaultDetails)
			{
				loadDefault();
			}
			else
			{
				setValues(hostDefaultDetails);
			}
		}
		else
		{
			$.prompt(messages["multiSelectedError"],{prefix:'jqismooth'});
		}
	}
	else if(currentTab == "deleted")
	{
		actionName = "addDeletedHost";
		var selectedRow = new Array();
		selectedRow = fnGetSelected($gridViewDeletedHostDataTable)
		var rLength = selectedRow.length;
		if(rLength==0)
		{
			$.prompt(messages["noneSelectedError"],{prefix:'jqismooth'});
		}
		else
		{
			$.prompt(messages[actionName],{ buttons:{Ok:true,Cancel:false}, prefix:'jqismooth',callback:function(){
				//$.prompt("asd",{prefix:'jqismooth'});
				var hostId = [];
				for(var i = 0;i<selectedRow.length;i++)
				{
					var iRow =  $gridViewDeletedHostDataTable.fnGetPosition(selectedRow[i]);
					var aData = $gridViewDeletedHostDataTable.fnGetData(iRow);
					hostId.push(String(aData[0]));
				}
				action = "add_deleted_host.py";
				method = "post";
				data = {"host_ids":String(hostId)};
				spinStart($spinLoading,$spinMainLoading);
				$.ajax({
					type:method,
					url:action,
					data:data,
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
							// update datatable 
							$().toastmessage('showSuccessToast', result.msg);
						}
						else
						{
							$().toastmessage('showErrorToast', messages[result.msg]);
						}
						spinStop($spinLoading,$spinMainLoading);
					}
				});
				alert("sdf");
			}});
		}		
	}
	else
	{
		$formTitle.html("Add Host");
		$form.attr("action","add_host.py");
		manage_host_parents(null);
		//$formInput.val("");
		//$formTextarea.val("");
		$formAddButton.css({"display":"inline-block"});
		$formEditButton.hide();
		showForm();		
		if(!hostDefaultDetails)
		{
			loadDefault();
		}
		else
		{
			setValues(hostDefaultDetails);
		}
	}
	
}
function loadDefault()
{
	$.ajax({
		type:"get",
		url:"host_default_details.py",
		cache:false,
		success:function(result){
			try
			{
				result = eval("(" + result + ")");
			}
			catch(err)
			{
				result = {success:1,msg:"loadDefaultSettingWarn"};
			}
			if(result.success == 0)
			{
				hostDefaultDetails = result.result;
				setValues(hostDefaultDetails);
			}
			else
			{
				$().toastmessage('showWarningToast', messages[result.msg]);
			}
		}
	});
}
function setValues(details)
{
	$form.find("input#host_id").val(details["host_id"]);
	//$form.find("input#node_type").val(details["node_type"]);
	$formInput.eq(0).val(details["host_name"]);
	$formInput.eq(1).val(details["host_alias"]);
	$formInput.eq(2).val(details["ip_address"]);
	$formInput.eq(3).val(details["mac_address"]);
	$formInput.eq(4).val(details["rc_mac"]);
	$formInput.eq(5).val(details["netmask"]);
	$formInput.eq(6).val(details["gateway"]);
	$formInput.eq(7).val(details["primary_dns"]);
	$formInput.eq(8).val(details["secondary_dns"]);
	$formInput.eq(9).val(details["http_username"]);
	$formInput.eq(10).val(details["http_port"]);
	$formInput.eq(11).val(details["read_community"]);
	$formInput.eq(12).val(details["write_community"]);
	$formInput.eq(13).val(details["get_set_port"]);
	$formInput.eq(14).val(details["trap_port"]);
	$formInput.eq(15).val(details["longitude"]);
	$formInput.eq(16).val(details["latitude"]);
	$formInput.eq(17).val(details["serial_number"]);
	$formInput.eq(18).val(details["hardware_version"]);
	
	$formPassword.eq(0).val(details["http_password"]);
	$formTextarea.eq(0).val(details["host_comment"]);
	$formCheckbox.eq(0).attr("checked",true);
	$formCheckbox.eq(0).attr("disabled",false);
	if(details["lock_position"] == 't')
		$formCheckbox.eq(1).attr("checked",true);
	else
		$formCheckbox.eq(1).attr("checked",false);
		
	$formSelectList.eq(0).val(details["device_type"]);
	//$formSelectList.eq(0).change();
	$formSelectList.eq(1).val(details["node_type"]);
	if(details["device_type"] == "odu16" || details["device_type"] == "odu100")
	{
		$RaMacDiv.show();
		if(!isNaN(parseInt(details["node_type"])) && parseInt(details["node_type"]) != 0)
		{
			oduMasterList(details["device_type"],details["master_mac"]);
			$MasterSlaveDiv.show();
		}
		else
		{
			$MasterSlaveDiv.hide();
			$formSelectList.eq(2).find("option").eq(0).attr("selected","selected");
		}
	}
	else
	{
		$RaMacDiv.hide();
		$MasterSlaveDiv.hide();
		$formSelectList.eq(2).find("option").eq(0).attr("selected","selected");
		//$formSelectList.eq(1).val(details["master_mac"]);
	}
	$formSelectList.eq(3).val(details["host_state"]);
	$formSelectList.eq(4).val(details["host_priority"]);
	if(details["host_parent"] == "")
	{
		$formSelectList.eq(5).find("option").eq(0).attr("selected","selected");
	}
	else
	{
		$formSelectList.eq(5).val(details["host_parent"]);
	}
	if(details["hostgroup"] == "")
	{
		$formSelectList.eq(6).find("option").eq(0).attr("selected","selected");
	}
	else
	{
		$formSelectList.eq(6).val(details["hostgroup"]);
	}
	if(details["dns_state"] == "")
	{
		$formSelectList.eq(7).find("option").eq(0).attr("selected","selected");
	}
	else
	{
		$formSelectList.eq(7).val(details["dns_state"]);
	}
	$formSelectList.eq(8).val(details["snmp_version"]);
	if(details["host_vendor"] == "")
	{
		$formSelectList.eq(9).find("option").eq(1).attr("selected","selected");
	}
	else
	{
		$formSelectList.eq(9).val(details["host_vendor"]);
	}
	if(details["host_os"] == "")
	{
		$formSelectList.eq(10).find("option").eq(1).attr("selected","selected");
	}
	else
	{
		$formSelectList.eq(10).val(details["host_os"]);
	}

	if(currentTab == "discovered")
	{
		$formInput.eq(0).val(selectedHostName);
		$formInput.eq(1).val(selectedHostAlias);
		$formInput.eq(2).val(selectedIpAddress);
		$formInput.eq(3).val(selectedMacAddress);
		$formSelectList.eq(0).val(selectedDeviceType);
		$formSelectList.eq(0).change();
	}

}
function editForm(id)
{
	$formTitle.html("Edit Host");
	$form.attr("action","edit_host.py");
	manage_host_parents(id);
	$formEditButton.css({"display":"inline-block"});
	$formAddButton.hide();
	$.ajax({
		type:"get",
		url:"get_host_by_id.py?host_id=" + id,
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
				hostDetails = result.result;
				oldIpAddress = hostDetails["ip_address"];
				oldNetmask = hostDetails["netmask"];
				oldGateway = hostDetails["gateway"];
				oldDhcp = hostDetails["dns_state"];
				oldPriIp = hostDetails["primary_dns"];
				oldSecIp = hostDetails["secondary_dns"];
				setValues(hostDetails);
				showForm();
				$formCheckbox.eq(0).attr("checked",false);
				$formCheckbox.eq(0).attr("disabled",true);
			}
			else
			{
				$().toastmessage('showErrorToast', messages[result.msg]);
			}
		}
	});
}
function addHost()
{
	actionName = "add";
	if(formStatus == 0)
	{
		createForm(actionName);
		formStatus = 1;		
	}
	else
	{
		addForm();
	}
}

function editHost(id,isLocalhost)
{
	var selectedRow = new Array();
	if(currentTab == "active")
		selectedRow = fnGetSelected($gridViewActiveHostDataTable)
	else if(currentTab == "disable")
		selectedRow = fnGetSelected($gridViewDisableHostDataTable)
		
	var rLength = selectedRow.length; 
	if(rLength==0 && id == undefined && isLocalhost == undefined)
	{
		$.prompt(messages["noneSelectedError"],{prefix:'jqismooth'});
	}
	else if (rLength == 1 || (id != undefined && isLocalhost != undefined))
	{
		if(id == undefined && isLocalhost == undefined)
		{
			var aData = [];
			if(currentTab == "active")
			{
				var iRow = $gridViewActiveHostDataTable.fnGetPosition(selectedRow[0]);
				aData = $gridViewActiveHostDataTable.fnGetData(iRow);
			}
			else if(currentTab == "disable")
			{
				var iRow = $gridViewDisableHostDataTable.fnGetPosition(selectedRow[0]);
				aData = $gridViewDisableHostDataTable.fnGetData(iRow);
			}
			id = aData[0];
			isLocalhost = aData[1];
		}
		if(isLocalhost == 0)
		{
			actionName = "edit";
			if(formStatus == 0)
			{
				createForm(actionName,id);
				formStatus = 1;
			}
			else
			{
				editForm(id);
			}
		}
		else
		{
			$.prompt(messages["localhostEditError"],{prefix:'jqismooth'});
		}
	}
	else
	{
		$.prompt(messages["multiSelectedError"],{prefix:'jqismooth'});
	}
}

function delHost()
{
	actionName = "delConfirm";
	hideForm();
	var selectedRow = new Array();
	if(currentTab == "active")
		selectedRow = fnGetSelected($gridViewActiveHostDataTable)
	else if(currentTab == "disable")
		selectedRow = fnGetSelected($gridViewDisableHostDataTable)
	else if(currentTab == "discovered")
		selectedRow = fnGetSelected($gridViewDiscoveredHostDataTable)
	else if(currentTab == "deleted")
		selectedRow = fnGetSelected($gridViewDeletedHostDataTable)
		
	var rLength = selectedRow.length; 
	if(rLength==0)
	{
		$.prompt(messages["noneSelectedError"],{prefix:'jqismooth'});
	}
	else
	{
		$.prompt(messages[actionName],{ buttons:{Ok:true,Cancel:false}, prefix:'jqismooth',callback:delHostCallback });
	}	
}
function update_host_parents()
{
	$.ajax({
		type:"get",
		url:"host_parents.py",
		cache:false,
		success:function(result){
			$result = $(result);
			$formSelectList.eq(5).html($result.html());
		}
	});
}
function manage_host_parents(edited_host_id)
{
	$formSelectList.eq(5).find("option").attr("disabled",false);
	if(edited_host_id != null)
	{
		$formSelectList.eq(5).find("option[value='" + edited_host_id + "']").attr("disabled",true);
	}
}
function delHostCallback(v,m){
	actionName = "del"
	if(v != undefined && v==true)
	{
		var action = "del_host.py";
		var method = "get";
		spinStart($spinLoading,$spinMainLoading);
		var selectedRow = new Array();
		if(currentTab == "active")
			selectedRow = fnGetSelected($gridViewActiveHostDataTable)
		else if(currentTab == "disable")
			selectedRow = fnGetSelected($gridViewDisableHostDataTable)
		else if(currentTab == "discovered")
			selectedRow = fnGetSelected($gridViewDiscoveredHostDataTable)
		else if(currentTab == "deleted")
			selectedRow = fnGetSelected($gridViewDeletedHostDataTable)

		var rLength = selectedRow.length;
		var hostId = [];
		var discoveryType = [];
		var isLocalhost = false;
		for(var i = 0;i<selectedRow.length;i++)
		{
			var aData = [];
			if(currentTab == "active")
			{
				var iRow = $gridViewActiveHostDataTable.fnGetPosition(selectedRow[i]);
				aData = $gridViewActiveHostDataTable.fnGetData(iRow);
				action = "del_host.py";
				if(aData[1] == 0)
				{
					hostId.push(aData[0]);
				}
				else
				{
					isLocalhost = true;
					break;
				}
			}
			else if(currentTab == "disable")
			{
				var iRow = $gridViewDisableHostDataTable.fnGetPosition(selectedRow[i]);
				aData = $gridViewDisableHostDataTable.fnGetData(iRow);
				action = "del_host.py";
				if(aData[1] == 0)
				{
					hostId.push(aData[0]);
				}
				else
				{
					isLocalhost = true;
					break;
				}
			}
			else if(currentTab == "discovered")
			{
				var iRow =  $gridViewDiscoveredHostDataTable.fnGetPosition(selectedRow[i]);
				aData = $gridViewDiscoveredHostDataTable.fnGetData(iRow);
				action = "delete_discovered_host.py";
				hostId.push(String(aData[0]));
				discoveryType.push(aData[1]);
			}
			else if(currentTab == "deleted")
			{
				var iRow =   $gridViewDeletedHostDataTable.fnGetPosition(selectedRow[i]);
				aData = $gridViewDeletedHostDataTable.fnGetData(iRow);
				hostId.push(aData[0]);
				action = "del_deleted_host.py";
				if(aData[1] == 0)
				{
					hostId.push(aData[0]);
				}
				else
				{
					isLocalhost = true;
					break;
				}
			}
		}
		if(isLocalhost)
		{
			$.prompt(messages["localhostDelError"],{prefix:'jqismooth'});
			spinStop($spinLoading,$spinMainLoading);
		}
		else
		{
			if(currentTab == "discovered")
			{
				$.ajax({
					type:method,
					url:action + "?host_id=" + String(hostId) + "&discovery_type=" + String(discoveryType),
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
							hideForm();
							$().toastmessage('showSuccessToast', messages[actionName]);
							for(var i = 0;i<selectedRow.length;i++)
							{
								var aData = [];
								if(currentTab == "discovered")
								{
									var iRow = $gridViewDiscoveredHostDataTable.fnGetPosition(selectedRow[i]);
									$gridViewDiscoveredHostDataTable.fnDeleteRow(iRow);
								}
							}
						}
						else
						{
							$().toastmessage('showErrorToast', messages[result.msg]);
						}
						spinStop($spinLoading,$spinMainLoading);
					}
				});
			}
			else
			{
				$.ajax({
					type:method,
					url:action + "?host_ids=" + String(hostId),
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
							hideForm();
							$().toastmessage('showSuccessToast', messages[actionName]);
							for(var i = 0;i<selectedRow.length;i++)
							{
								var aData = [];
								if(currentTab == "active")
								{
									var iRow = $gridViewActiveHostDataTable.fnGetPosition(selectedRow[i]);
									$gridViewActiveHostDataTable.fnDeleteRow(iRow);
								}
								else if(currentTab == "disable")
								{
									var iRow = $gridViewDisableHostDataTable.fnGetPosition(selectedRow[i]);
									$gridViewDisableHostDataTable.fnDeleteRow(iRow);
								}
								else if(currentTab == "deleted")
								{
									var iRow = $gridViewDeletedHostDataTable.fnGetPosition(selectedRow[i]);
									$gridViewDeletedHostDataTable.fnDeleteRow(iRow);
									$gridViewDiscoveredHostFetched = 0;
								}
								$gridViewDeletedHostFetched = 0;
							}
							if(currentTab == "discovered")
							{
								gridViewDiscoveredHost();
							}
						}
						else
						{
							$().toastmessage('showErrorToast', messages[result.msg]);
						}
						spinStop($spinLoading,$spinMainLoading);
					}
				});
			}
		}
	}
	else
	{
		//$().toastmessage('showNoticeToast', "Remain Unchanged.");
	}
}
/*
 * I don't actually use this here, but it is provided as it might be useful and demonstrates
 * getting the TR nodes from DataTables
 */

function fnGetSelected( oTableLocal )
{
	var aReturn = new Array();
	var aTrs = oTableLocal.fnGetNodes();
	
	for ( var i=0 ; i<aTrs.length ; i++ )
	{
		if ( $(aTrs[i]).hasClass('row_selected') )
		{
			aReturn.push( aTrs[i]);
		}
	}
	return aReturn;
}

