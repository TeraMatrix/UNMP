var pingFormStatus = 0;				/* { 0:form for add and upadate not present, 1:form for add and upadate not present } */
var snmpFormStatus = 0;				/* { 0:form for add and upadate not present, 1:form for add and upadate not present } */
var upnpFormStatus = 0;				/* { 0:form for add and upadate not present, 1:form for add and upadate not present } */

var formStatus = 0;				/* { 0:form for add and upadate not present, 1:form for add and upadate not present } */

/* Add Host */
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
var hostDefaultDetails = null;
var $tooltip = null;

/* Discovered Host */
var $gridViewDiscoveredHostTableObj = null;
var $gridViewDiscoveredHostDataTable = null;
var $gridViewDiscoveredHostFetched = 0;
var $gridViewDiscoveredHostSelectedTr = [];		/* Datatable selected rows Array */


var $gridViewDiv = null;
var $formDiv = null;
var $spinLoading = null;
var $spinMainLoading  = null;


// ping
var pingDefaultDetails = null;
var pingFormFetched = 0;
var $pForm = null;
var $pFormInput = null;
var $tooltipPing = null;

// snmp
var snmpDefaultDetails = null;
var snmpFormFetched = 0;
var $sForm = null;
var $sFormInput = null;
var $sFormSelect = null;
var $tooltipSnmp = null;

// upnp
var upnpDefaultDetails = null;
var upnpFormFetched = 0;
var $uForm = null;
var $uFormInput = null;
var $tooltipUpnp = null;

var currentTab = null; 				// host_list,ping,snmp,upnp, etc.

//selected host details
var selectedHostName = null;
var selectedHostAlias = null;
var selectedIpAddress = null;
var selectedMacAddress = null;
var selectedDeviceType = null;

// for default values
var pingDefaultDetails = null;
var snmpDefaultDetails = null;
var upnpDefaultDetails = null;

var messages = {
	"add":"Host added Successfully",
	"del":"Selected host(s) deleted Successfully",
	"delConfirm":"Are you sure want to delete the selected host(s)?",
	"duplicateError":"Please Enter Different Host Alias, IP  and MAC",
	"noneSelectedError":"Select Atleast one Host.",
	"multiSelectedError":"Select only single Host.",
	"localhostDelError":"You Could not delete this Host because This is the Localhost.",
	"localhostEditError":"You Could not Edit this Host because This is The Localhost.",
	"validationError":"Some Fields are Missing or Incorrect.",
	"dbError":"Some Database Error occurred, Please Contact Your Administrator.",
	"noRecordError":"No Record Exist, May be host already deleted, Please reload this page.",
	"sysError":"UNMP Server has encountered an error. Please retry after some time.",
	"unknownError":"UNMP Server has encountered an error. Please retry after some time.",
	"loadDefaultSettingWarn":"Loading of Default Setting Failed",
	"noNmsInctanceError":"This UNMP Instance Does not Present in Database, Please Contact Your Administrator.",
	"ping_start":"PING Discovery Start Successfully, You will get discoverd host within 60 secs.",
	"ping_pause":"PING Discovery Paused",
	"ping_restart":"PING Discovery Restart Successfully",
	"ping_stop":"PING Discovery Stopped",
	"ping_complete":"PING Discovery Completed Successfully",
	"snmp_start":"SNMP Discovery Start Successfully, You will get discoverd host within 60 secs.",
	"snmp_pause":"SNMP Discovery Paused",
	"snmp_restart":"SNMP Discovery Restart Successfully",
	"snmp_stop":"SNMP Discovery Stopped",
	"snmp_complete":"SNMP Discovery Completed Successfully",
	"upnp_start":"UPNP Discovery Start Successfully, You will get discoverd host within 60 secs.",
	"upnp_pause":"UPNP Discovery Paused",
	"upnp_restart":"UPNP Discovery Restart Successfully",
	"upnp_stop":"UPNP Discovery Stopped",
	"upnp_complete":"UPNP Discovery Completed Successfully",
	"rangeError":"IP Range Start Should be Less than IP Range End.",
	"raMacMissing":"RA MAC is Required for UBR and UBRe Type Device",
	"raMacWarning":"RA MAC should be correct otherwise you may get error in monitoring and configuration of device.",
	"raMacError":"Enter correct format of MAC Address.",
	"masterMacMissing":"Master MAC is Required for UBR and UBRe Slave device",
	"masterMacWarning":"Master MAC should be correct otherwise you may get error in monitoring and configuration of device.",
	"masterMacError":"Please Choose correct Master.",
	"licenseError":"Maximum number of allowed host have reached. To Complete this action you need to upgrade your license please contact sales team."
};
var actionName = null;

function hideAllToolTip()
{
	/* this is bcoz when validation unsuccess and you click on cancel button then tooltip visible so this code will hide that. */
	if($tooltip)
		$tooltip.tooltip().hide();
	if($tooltipPing)
		$tooltipPing.tooltip().hide();
	if($tooltipSnmp)
		$tooltipSnmp.tooltip().hide();
	if($tooltipUpnp)
		$tooltipUpnp.tooltip().hide();
}
$(function(){
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
		href:"help_inventory_discovery.py",
		title: "Page Tip",
		opacity: 0.4,
		maxWidth: "80%",
		width:"600px",
		height:"350px"
	});
	$("div.yo-tabs").yoTabs();
	
	/* Add Data Table Tr Selecter Click Handler*/
	dataTableClickHandler();
	
	/* Call Active Host Data Table */
	$gridViewDiscoveredHostTableObj = $("table#grid_view_discovered_host");
	//gridViewDeletedHost();
	
	/* Active Host Tab*/
	$("a#discovered_host_tab").click(function(e){
		e.preventDefault();
		currentTab = "host_list";
		if($gridViewDiscoveredHostFetched == 0)
		{
			gridViewDiscoveredHost();
		}
		hideAllToolTip();
	});
	
	/* PING Tab*/
	$("a#ping_tab").click(function(e){
		e.preventDefault();
		currentTab = "ping";
		if(pingFormFetched == 0)
		{
			pingForm();
		}
		else
		{
			//applyPingDefaultValues();
		}
		hideAllToolTip();
	});
	
	/* SNMP Tab*/
	$("a#snmp_tab").click(function(e){
		e.preventDefault();
		currentTab = "snmp";
		if(snmpFormFetched == 0)
		{
			snmpForm();
		}
		else
		{
			//applySnmpDefaultValues();
		}
		hideAllToolTip();
	});
	
	/* UPNP Tab*/
	$("a#upnp_tab").click(function(e){
		e.preventDefault();
		currentTab = "upnp";
		if(upnpFormFetched == 0)
		{
			upnpForm();
		}
		else
		{
			//applyUpnpDefaultValues();
		}
		hideAllToolTip();
	});
	
	/* It Shows Active Host as Default Host Grid View */
	$("a#discovered_host_tab").click();
});

function dataTableClickHandler()
{
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
				"bStateSave": false,
				"bLengthChange":true,
				"aoColumns": [
				    {"sWidth": "0%" },
				    {"sWidth": "15%" },
				    {"sWidth": "20%" },
				    {"sWidth": "20%" },
				    {"sWidth": "15%" },
				    {"sWidth": "30%" }
				]
			});
			$gridViewDiscoveredHostDataTable.fnSetColumnVis( 0, false,false );
			//$gridViewDeletedHostDataTable.fnSetColumnVis( 1, false,false );
/*
	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"post",
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

function pingForm()
{
	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"get",
		url:"ping_discovery_form.py",
		cache:false,
		success:function(result){
			$("div#content_2").html(result);
			pingFormFetched = 1;
			addPingFormToolTip();
			$pForm = $("form#form_ping");
			$pFormInput = $("form#form_ping input[type='text']");
			$("button#cancel_ping").click(function(){
				$("a#discovered_host_tab").click();
			});
			submitPingForm($pForm);
			applyPingDefaultValues();
			spinStop($spinLoading,$spinMainLoading);
		}
	});
}
function applyPingDefaultValues()
{
	if(pingDefaultDetails)
	{
		setPingDefaultValues(pingDefaultDetails);
	}
	else
	{
		loadPingDefaultDetails();
	}
}
function loadPingDefaultDetails()
{
	$.ajax({
		type:"get",
		url:"ping_default_details.py",
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
				pingDefaultDetails = result.result;
				setPingDefaultValues(pingDefaultDetails);
			}
			else
			{
				$().toastmessage('showWarningToast', messages[result.msg]);
			}
		}
	});
}

function setPingDefaultValues(details)
{
	$pFormInput.eq(0).val(details["ping_ip_base"]);
	$pFormInput.eq(1).val(details["ping_ip_base_start"]);
	$pFormInput.eq(2).val(details["ping_ip_base_end"]);
	$pFormInput.eq(3).val(details["ping_timeout"]);
}

function addPingFormToolTip()
{
	// add tool tip
	$tooltipPing = $("form#form_ping input[type='text']").tooltip({
		// place tooltip on the right edge
		position: "center right",
		// a little tweaking of the position
		offset: [-2, 10],
		// use the built-in fadeIn/fadeOut effect
		effect: "fade",
		// custom opacity setting
		opacity: 0.7
	});
}

function submitPingForm($formObj)
{
	validatePingForm($formObj);
	$formObj.submit(function(){
		var $formThis = $(this);
		if($formThis.valid())
		{
			if(parseInt($pFormInput.eq(1).val()) > parseInt($pFormInput.eq(2).val()))
			{
				$().toastmessage('showErrorToast', messages["rangeError"]);
				return false;
			}
			actionName = "ping_start";
			spinStart($spinLoading,$spinMainLoading);
			var action = $formThis.attr("action");
			var method = $formThis.attr("method");
			var data = $formThis.serialize();
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
						$().toastmessage('showSuccessToast', messages[actionName]);
						$gridViewDiscoveredHostFetched=0;
						run_ping(result.discovery_id);
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
			$().toastmessage('showErrorToast', messages["validationError"]);
		}
		return false;
	});
}
function validatePingForm($formObj)
{
	$formObj.validate({
		rules:{
			ping_ip_base:{
				required:true,
				classCIPChecker: true
			},
			ping_ip_base_start:{
				required:true,
				positiveNumber: true
			},
			ping_ip_base_end:{
				required:true,
				positiveNumber:true
			},
			ping_timeout:{
				required:true,
				positiveNumber:true
			}
		},
		messages:{
			ping_ip_base:{
				required:"Host Name is Required Field",
				classCIPChecker:"Enter Valid Class C Network IP"
			},
			ping_ip_base_start:{
				required:"IP Range Start is Reqired Filed",
				positiveNumber: "IP Range Start Should be Positive"
			},
			ping_ip_base_end:{
				required:"IP Range End is Reqired Filed",
				positiveNumber:"IP Range End Should be Positive"
			},
			ping_timeout:{
				required:"Timeot is Reqired Filed",
				positiveNumber:"Timeout Should be Positive"
			}
		}
	});	
}
function run_ping(discovery_id)
{
	$.ajax({
		type:"get",
		url:"run_ping_discovery.py?discovery_id=" + String(discovery_id),
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
						$().toastmessage('showSuccessToast', "Host Discovered Successfully");
						$("a#discovered_host_tab").click();
					}
					else
					{
						$().toastmessage('showErrorToast', messages[result.msg]);
					}			
		}
	})
}
function run_snmp(discovery_id)
{
	$.ajax({
		type:"get",
		url:"run_snmp_discovery.py?discovery_id=" + String(discovery_id),
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
						$().toastmessage('showSuccessToast', "Host Discovered Successfully");
						$("a#discovered_host_tab").click();
					}
					else
					{
						$().toastmessage('showErrorToast', messages[result.msg]);
					}			
		}
	})
}
function snmpForm()
{
	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"get",
		url:"snmp_discovery_form.py",
		cache:false,
		success:function(result){
			$("div#content_3").html(result);
			snmpFormFetched = 1;
			addSnmpFormToolTip();
			$sForm = $("form#form_snmp");
			$sFormInput = $("form#form_snmp input[type='text']");
			$sFormSelect = $("form#form_snmp select");
			$("button#cancel_snmp").click(function(){
				$("a#discovered_host_tab").click();
			});
			submitSnmpForm($sForm);
			applySnmpDefaultValues();
			spinStop($spinLoading,$spinMainLoading);
		}
	});
}

function applySnmpDefaultValues()
{
	if(snmpDefaultDetails)
	{
		setSnmpDefaultValues(snmpDefaultDetails);
	}
	else
	{
		loadSnmpDefaultDetails();
	}
}
function loadSnmpDefaultDetails()
{
	$.ajax({
		type:"get",
		url:"snmp_default_details.py",
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
				snmpDefaultDetails = result.result;
				setSnmpDefaultValues(snmpDefaultDetails);
			}
			else
			{
				$().toastmessage('showWarningToast', messages[result.msg]);
			}
		}
	});
}

function setSnmpDefaultValues(details)
{
	$sFormInput.eq(0).val(details["snmp_ip_base"]);
	$sFormInput.eq(1).val(details["snmp_ip_base_start"]);
	$sFormInput.eq(2).val(details["snmp_ip_base_end"]);
	$sFormInput.eq(3).val(details["snmp_timeout"]);
	$sFormInput.eq(4).val(details["snmp_community"]);
	$sFormInput.eq(5).val(details["snmp_port"]);
	$sFormSelect.eq(0).val(details["snmp_version"]);
}

function addSnmpFormToolTip()
{
	// add tool tip
	$tooltipSnmp = $("form#form_snmp input[type='text']").tooltip({
		// place tooltip on the right edge
		position: "center right",
		// a little tweaking of the position
		offset: [-2, 10],
		// use the built-in fadeIn/fadeOut effect
		effect: "fade",
		// custom opacity setting
		opacity: 0.7
	});
}

function submitSnmpForm($formObj)
{
	validateSnmpForm($formObj);
	$formObj.submit(function(){
		var $formThis = $(this);
		if($formThis.valid())
		{
			if(parseInt($sFormInput.eq(1).val()) > parseInt($sFormInput.eq(2).val()))
			{
				$().toastmessage('showErrorToast', messages["rangeError"]);
				return false;
			}
			actionName = "snmp_start";
			spinStart($spinLoading,$spinMainLoading);
			var action = $formThis.attr("action");
			var method = $formThis.attr("method");
			var data = $formThis.serialize();
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
						$().toastmessage('showSuccessToast', messages[actionName]);
						$gridViewDiscoveredHostFetched=0;
						run_snmp(result.discovery_id);
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
			$().toastmessage('showErrorToast', messages["validationError"]);
		}
		return false;
	});
}
function validateSnmpForm($formObj)
{
	$formObj.validate({
		rules:{
			snmp_ip_base:{
				required:true,
				classCIPChecker: true
			},
			snmp_ip_base_start:{
				required:true,
				positiveNumber: true
			},
			snmp_ip_base_end:{
				required:true,
				positiveNumber:true
			},
			snmp_timeout:{
				required:true,
				positiveNumber:true
			},
			snmp_community:{
				required:true,
				alphaNumeric:true
			},
			snmp_port:{
				required:true,
				positiveNumber:true
			},
			snmp_version:{
				required:true,
				alphaNumeric:true
			}
		},
		messages:{
			snmp_ip_base:{
				required:"Host Name is Required Field",
				classCIPChecker:"Enter Valid Class C Network IP"
			},
			snmp_ip_base_start:{
				required:"IP Range Start is Required Field",
				positiveNumber: "IP Range Start Should be Positive"
			},
			snmp_ip_base_end:{
				required:"IP Range End is Required Field",
				positiveNumber:"IP Range End Should be Positive"
			},
			snmp_timeout:{
				required:"Timeot is Required Field",
				positiveNumber:"Timeout Should be Positive"
			},
			snmp_community:{
				required:"Community is Required Field",
				alphaNumeric:"Community Should be Alpha Numeric"
			},
			snmp_port:{
				required:"SNMP Port Number is Required Field",
				positiveNumber:"SNMP Port Should be Positive Number"
			},
			snmp_version:{
				required:"SNMP Version is Required Filed",
				alphaNumeric:"SNMP Version Should be Alpha Numeric"
			}
		}
	});	
}
function run_upnp(discovery_id)
{
	$.ajax({
		type:"get",
		url:"run_upnp_discovery.py?discovery_id=" + String(discovery_id),
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
						$().toastmessage('showSuccessToast', "Host Discovered Successfully");
						$("a#discovered_host_tab").click();
					}
					else
					{
						$().toastmessage('showErrorToast', messages[result.msg]);
					}			
		}
	})
}

function upnpForm()
{
	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"get",
		url:"upnp_discovery_form.py",
		cache:false,
		success:function(result){
			$("div#content_4").html(result);
			upnpFormFetched = 1;
			addUpnpFormToolTip();
			$uForm = $("form#form_upnp");
			$uFormInput = $("form#form_upnp input[type='text']");
			$("button#cancel_upnp").click(function(){
				$("a#discovered_host_tab").click();
			});
			submitUpnpForm($uForm);
			applyUpnpDefaultValues();
			spinStop($spinLoading,$spinMainLoading);
		}
	});
}

function applyUpnpDefaultValues()
{
	if(upnpDefaultDetails)
	{
		setUpnpDefaultValues(upnpDefaultDetails);
	}
	else
	{
		loadUpnpDefaultDetails();
	}
}
function loadUpnpDefaultDetails()
{
	$.ajax({
		type:"get",
		url:"upnp_default_details.py",
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
				upnpDefaultDetails = result.result;
				setUpnpDefaultValues(upnpDefaultDetails);
			}
			else
			{
				$().toastmessage('showWarningToast', messages[result.msg]);
			}
		}
	});
}

function setUpnpDefaultValues(details)
{
	$uFormInput.eq(0).val(details["upnp_timeout"]);
}

function addUpnpFormToolTip()
{
	// add tool tip
	$tooltipUpnp = $("form#form_upnp input[type='text']").tooltip({
		// place tooltip on the right edge
		position: "center right",
		// a little tweaking of the position
		offset: [-2, 10],
		// use the built-in fadeIn/fadeOut effect
		effect: "fade",
		// custom opacity setting
		opacity: 0.7
	});
}

function submitUpnpForm($formObj)
{
	validateUpnpForm($formObj);
	$formObj.submit(function(){
		var $formThis = $(this);
		if($formThis.valid())
		{
			actionName = "upnp_start";
			spinStart($spinLoading,$spinMainLoading);
			var action = $formThis.attr("action");
			var method = $formThis.attr("method");
			var data = $formThis.serialize();
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
						$().toastmessage('showSuccessToast', messages[actionName]);
						$gridViewDiscoveredHostFetched=0;
						run_upnp(result.discovery_id);
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
			$().toastmessage('showErrorToast', messages["validationError"]);
		}
		return false;
	});
}
function validateUpnpForm($formObj)
{
	$formObj.validate({
		rules:{
			upnp_timeout:{
				required:true,
				positiveNumber:true
			}
		},
		messages:{
			upnp_timeout:{
				required:"Timeot is Required Field",
				positiveNumber:"Timeout Should be Positive"
			}
		}
	});	
}

function addHost()
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
	else
	{
		$.prompt(messages["multiSelectedError"],{prefix:'jqismooth'});
	}
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
			//{"node_type_success":1,"ra_mac_success":1,"node_type":"SNMP agent down or device not reachable","ra_mac":"SNMP agent down or device not reachable"}
			if(result.node_type_success == 1 && result.ra_mac_success == 1)
			{
				$().toastmessage('showErrorToast', result.node_type);
			}
			else if(result.node_type_success == 1)
			{
				$().toastmessage('showErrorToast', "Fetching node type: " + result.node_type);
				//$formSelectList.eq(1).val("");
				$formInput.eq(4).val(result.ra_mac);
			}
			else if(result.ra_mac_success == 1)
			{
				$().toastmessage('showErrorToast', "Fetching RA MAC: " + result.ra_mac);
				$formSelectList.eq(1).val(result.node_type);
				$formInput.eq(4).val("");
			}
			else
			{
				$formSelectList.eq(1).val(result.node_type);
				$formInput.eq(4).val(result.ra_mac);
			}
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
			//{"success":1,"result":"SNMP agent down or device not reachable"}
			if(result.success == 0)
			{
				$formSelectList.eq(2).val(result.result);
			}
			else
			{
				$().toastmessage('showErrorToast', result.result);
				$formSelectList.eq(2).val("");
			}
			$("#master_mac_loading").hide();
			$("#a_fetch_master_mac").show();
		}
	});
}
function fetchNetworkDetails()
{
	if($formSelectList.eq(0).val() != "")
	{
		$("#network_details_loading").show();
		$("#a_network_details_loading").hide();
		$.ajax({
			type:"get",
			url:"get_network_details.py?ip_address=" + $formInput.eq(2).val() + "&community=" + $formInput.eq(11).val() + "&port=" + $formInput.eq(13).val() + "&device_type=" + $formSelectList.eq(0).val(),
			cache:false,
			success:function(result){
				//{"success":1,"result":"SNMP agent down or device not reachable"}
				if(result.success == 0)
				{
					$formInput.eq(5).val(result.result.netmask);
					$formInput.eq(6).val(result.result.gateway);
					$formInput.eq(7).val(result.result.primary_dns);
					$formInput.eq(8).val(result.result.secondary_dns);
					$formSelectList.eq(7).val(result.result.dns_state == 0 && "Disabled" || "Enabled");
				}
				else
				{
					$().toastmessage('showErrorToast', result.result);
				
				}
			},
			complete:function(){
				$("#network_details_loading").hide();
				$("#a_network_details_loading").show();
			}
		});
	}
	else
	{
		$.prompt(messages["selectDeviceWarnForFetchNetworkDetails"],{prefix:'jqismooth'});
	}
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
		opacity: 0.7
	});
}
function addForm()
{
	
	$formTitle.html("Add Host");
	$form.attr("action","add_host.py");
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
function submitForm($formObj)
{
	valiateForm($formObj);
	$formObj.submit(function(){
		var $formThis = $(this);
		if($formThis.valid())
		{
			actionName = "add";
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
						var nodeType = $formSelectList.eq(1).val();
						try
						{
							if(parseInt(nodeType) == 1 || parseInt(nodeType) == 3)
							{
								// check master mac
								var masterMacValue = $formSelectList.eq(2).val();;
								if($.trim(masterMacValue) == "")
								{
									$.prompt(messages["masterMacMissing"],{prefix:'jqismooth'});
									spinStop($spinLoading,$spinMainLoading);
									return false;
								}
								else
								{
									// do nothing
									$.prompt(messages["raMacWarning"],{prefix:'jqismooth'});
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
						var selectedRow = new Array();
						selectedRow = fnGetSelected($gridViewDiscoveredHostDataTable)
						for(var i = 0;i<selectedRow.length;i++)
						{
							var aData = [];
							if(currentTab == "host_list")
							{
								var iRow = $gridViewDiscoveredHostDataTable.fnGetPosition(selectedRow[i]);
								$gridViewDiscoveredHostDataTable.fnDeleteRow(iRow);
							}
							else
							{
								$gridViewDiscoveredHostFetched = 0;
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
			$().toastmessage('showErrorToast', messages["validationError"]);
		}
		return false;
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
				required:"Host Name is Required Field",
				alphaNumeric: "Name should be alpha numeric",
				noSpace: "Space Not Allowed"
			},
			host_alias:{
				required:"Host Alias is Required Field",
				alphaNumeric: "Alias should be alpha numeric"
			},
			ip_address:{
				required:"IP Address is Required Field",
				ipv4Address:"Invalid IP Address"
			},
			mac_address:{
				required:"Mac Address is Required Field",
				macAddress:"Invalid Mac Address"
			},
			device_type:{
				required:"Device Type is Required Field"
			},
			host_state:{
				required:"Host State is Required Field"
			},
			host_priority:{
				required:"Host Priority is Required Field"
			},
			host_parent:{
				required:"Host Parent is Required Field"
			},
			host_comment:{
				alphaNumeric: "Comment should be alhpa numeric"
			},
			netmask:{
				//netmask:"Invalid Netmask",
			},
			gateway:{
				ipv4Address:"Invalid IP Address"
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
				alphaNumeric: "Read Community should be alpha numeric"
			},
			write_community:{
				alphaNumeric: "Write Community should be alpha numeric"
			},
			snmp_version:{
				alphaNumeric: "SNMP Version should be correct"
			},
			get_set_port:{
				number: "SNMP Get/Set Port should be a number"
			},
			trap_port:{
				number: "SNMP Trap Port should be a number"
			},
			longitude:{
				number: "Longitude should be a number"
			},
			latitude:{
				number: "Latitude should be a number"
			},
			serial_number:{
				alphaNumeric: "Serial Number should be a Alpha Numeric"
			},
			hardware_version:{
				alphaNumeric: "Hardware Version should be a Alpha Numeric"
			},
			host_vendor:{
				required: "Host Vendor is Required Field"
			},
			host_os:{
				required: "Host OS name is  Required Field"
			}
		}
	});
}

function setValues(details)
{
	$form.find("input#host_id").val(details["host_id"]);
	//$form.find("input#node_type").val(details["node_type"]);
	$formInput.eq(0).val(selectedHostName);
	$formInput.eq(1).val(selectedHostAlias);
	$formInput.eq(2).val(selectedIpAddress);
	$formInput.eq(3).val(selectedMacAddress);
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
	$formCheckbox.eq(0).attr("checked",false);
	if(details["lock_position"] == 't')
		$formCheckbox.eq(1).attr("checked",true);
	else
		$formCheckbox.eq(1).attr("checked",false);
		
	$formSelectList.eq(0).val(selectedDeviceType);
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
}

function cancelForm()
{
	$("button#cancel_host").click(function(){
		hideForm();
	});
}

function hideForm()
{
	$gridViewDiv.show();
	$formDiv.hide();
	hideAllToolTip();
}
function showForm()
{
	$gridViewDiv.hide();
	$formDiv.show();	
} 
function delHost()
{
	actionName = "delConfirm";
	hideForm();
	var selectedRow = new Array();
	selectedRow = fnGetSelected($gridViewDiscoveredHostDataTable)
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

function delHostCallback(v,m){
	actionName = "del"
	if(v != undefined && v==true)
	{
		var action = "delete_discovered_host.py";
		var method = "get";
		spinStart($spinLoading,$spinMainLoading);
		var selectedRow = new Array();
		selectedRow = fnGetSelected($gridViewDiscoveredHostDataTable)
		var rLength = selectedRow.length;
		var hostId = [];
		var discoveryType = [];
		for(var i = 0;i<selectedRow.length;i++)
		{
			var aData = [];
			var iRow = $gridViewDiscoveredHostDataTable.fnGetPosition(selectedRow[i]);
			aData = $gridViewDiscoveredHostDataTable.fnGetData(iRow);
			
			hostId.push(String(aData[0]));
			discoveryType.push(aData[1]);
		}
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
						if(currentTab == "host_list")
						{
							var iRow = $gridViewDiscoveredHostDataTable.fnGetPosition(selectedRow[i]);
							$gridViewDiscoveredHostDataTable.fnDeleteRow(iRow);
						}
						else
						{
							$gridViewDiscoveredHostFetched = 0;
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
		//$().toastmessage('showNoticeToast', "Remain Unchanged.");
	}
}

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
