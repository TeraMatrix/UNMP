var aSelected = [];				/* Datatable selected rows Array */
var formStatus = 0;				/* { 0:form for add and upadate not present, 1:form for add and upadate not present } */
var $gridViewDiv = null;
var $formDiv = null;
var $spinLoading = null;
var $spinMainLoading  = null;
var $form = null;
var $formTitle = null;
var $formInput = null;
var $formAddButton = null;
var $formEditButton = null;
var $tooltip = null;
var service_time=[];
var service_hosts=[];
var service_name=[];
var details=[];
var messages = {
	"add":"Hostgroup Added Successfully",
	"edit":"Hostgroup Details Edit Successfully",
	"del":"Selected Hostgroup(s) Deleted Successfully",
	"delConfirm":"Are You Sure, You want to Delete Selected Hostgroup(s)?",
	"duplicateError":"Please Enter Different Hostgroup Name and Hostgroup Alias, They are Already Exist.",
	"noneSelectedError":"Select Atleast one Hostgroup.",
	"multiSelectedError":"Select only single Hostgroup.",
	"defaultDelError":"You Could not delete this Hostgroup because This is Default Group.",
	"defaultEditError":"You Could not Edit this Hostgroup because This is Default Group.",
	"validationError":"Some Fields are Missing or Incorrect.",
	"dbError":"Some Database Error occurred, Please Contact Your Administrator.",
	"noRecordError":"No Record Exist, May be hostgroup already deleted, Please reload this page.",
	"sysError":"Some System Error occurred, Please Contact Your Administrator.",
	"unknownError":"Some Unknown/Critical Error occurred, Please Contact Your Administrator."
};
var actionName = null;

$(function(){
	// spin loading object
	$spinLoading = $("div#spin_loading");		// create object that hold loading circle
	$spinMainLoading = $("div#main_loading");	// create object that hold loading squire
	/* create object of divs */
	$gridViewDiv = $("div#grid_view_div");
	$formDiv = $("div#form_div");	
	
	/* show grid view only hide other */
	$gridViewDiv.show();
	$formDiv.show();
	

	// page tip [for page tip write this code on each page please dont forget to change "href" value because this link create your help tip page]
	$("#page_tip").colorbox(
	{
		href:"help_inventory_service.py",
		title: "Page Tip",
		opacity: 0.4,
		maxWidth: "80%",
		width:"450px",
		height:"350px"
	});
	
	/* create grid view */
	gridViewHostgroup();

	/* Click event handler for grid view */
	/*$('#grid_view tbody tr').live('click', function () {
		var id = this.id;
		var index = jQuery.inArray(id, aSelected);
		
		if ( index === -1 ) {
			aSelected.push( id );
		} else {
			aSelected.splice( index, 1 );
		}
		
		$(this).toggleClass('row_selected');
	});*/
});

function gridViewHostgroup()
{
	$('.n-tip-image').tipsy({gravity: 'n',html: true});
	oTable = $('#grid_view').dataTable({
				"bServerSide": true,
				"sAjaxSource": "grid_view_service.py",
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true,
				"bStateSave": false,
				"bLengthChange":true,
				"aoColumns": [
				    {"sWidth": "0%" },
				    {"sWidth": "0%" },
				    {"sWidth": "10%" },
				    {"sWidth": "10%" },
				    {"sWidth": "10%" },
				    {"sWidth": "10%" },
				    {"sWidth": "55%" },
				    {"sWidth": "5%" }
				],
				 "fnServerData": function(sSource,aoData,fnCallback){
				$.getJSON( sSource, aoData, function (json) { 
				fnCallback(json);
				$('.n-tip-image').tipsy({gravity: 'n',html: true});
			});
		}
			});
			oTable.fnSetColumnVis( 0, false,false );
			oTable.fnSetColumnVis( 1, false,false );
}



function addService()
{
	$.prompt("Add Service",{prefix:'jqismooth'});
}

function editService(host_id,is_localhost)
{
	var flag_change=false;
	if(is_localhost==1)
	{
	$.prompt("Services of localhost are not editable.",{prefix:'jqismooth'});
	//return false;
	}
	else
	{
	$.colorbox(
	{
		href:"edit_service_details.py?host_id="+host_id,
		//iframe:true,
		title : "Edit Service Time",
		opacity: 0.4,
		maxWidth: "90%",
		width:"500px",
		height:"300px",
		onComplete:function(){
			var service_names=$("#service_names").val().split(",");
			for(var i=0;i<service_names.length-1;i++)
			{
			id=service_names[i].replace(/ /g,'_');
			$("#"+id).multiselect({selectedList: 1,multiple:false,noneSelectedText: 'Select Time',minWidth:50});
			if(service_names[i].toLowerCase().indexOf("uptime")!=-1)
			{
				$("#"+id).multiselect("disable");
			}
			else
			{
				$("#"+id).bind("multiselectclick", function(event, ui){
					var sel=$("#"+id).val();
					if(sel!=ui.value)
					{
						service_hosts.push(host_id);
						service_time.push(ui.value);
						service_name.push(id);
						$("#apply_changes_services_button").removeAttr('disabled');
						$("#service_box_"+host_id+"_"+id).html(ui.value);
						flag_change=true;
					}
				});
			}
		}
		
		},
		onClosed:function(){
			if(flag_change==true)
			{
				$().toastmessage('showWarningToast', "Please save changes by clicking on Apply Changes.");
			}
		},
		overlayClose:false
	});
	}
}

function viewServiceDetails(host_id,host_alias)
{
	$.colorbox(
	{
		href:"view_service_details_example.py?host_id="+host_id,
		//iframe:true,
		title : host_alias+" service details",
		opacity: 0.4,
		maxWidth: "90%",
		width:"1100px",
		height:"300px",
		overlayClose:false
	});
}

function applyChanges()
{
	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"get",
		url:"apply_service_changes.py?service_hosts="+service_hosts+"&service_time="+service_time+"&service_name="+service_name,
		cache:false,
		success:function(result){
				result=eval("("+result+")");
				if(result.success==0 || result.success=='0')
				{
					spinStop($spinLoading,$spinMainLoading);
					$().toastmessage('showSuccessToast', "Servcies modified Successfully.");
				}
				else 
				{
					spinStop($spinLoading,$spinMainLoading);
					$().toastmessage('showErrorToast', 'Services couldnt be modified currently.');
				}
		}
	});
}

function delService()
{
	$.prompt("Delete Service",{prefix:'jqismooth'});
}
