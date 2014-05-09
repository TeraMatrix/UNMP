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
//var is_colorbox_open=false;
var eventRecursion=null;
var refresh_interval=15000;
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
	AutoRefresh(refresh_interval);
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
function AutoRefresh(interval) {
	//if(is_colorbox_open==false)
	//{
	//	eventRecursion=setTimeout("location.reload(true);",interval);
	updatetable();
	eventRecursion=setTimeout(function (){AutoRefresh(interval);},interval);
	 
	//}
	//else
	//{
	//	clearTimeout(eventRecursion);
	//}
}
function updatetable()
{
	var hosts_obj=$(".service-box.n-tip-image");
	var hosts_array=[];
	//alert(hosts_obj[6].id);
	//alert($("#"+hosts_obj[6].id).attr("title"));
	for(var i=0;i<hosts_obj.length;i++)
	{
		hosts_array[i]=hosts_obj[i].id;
	}
	$.ajax({
			type:"get",
			url:'update_service_table.py?hosts_list='+hosts_array,
			cache:false,
			success:function(result){
				//alert(result);
				result=eval("("+result+")");
				if(result.success==0)
				{
					img_array=result.html_str.toString().split(",");
					title_array=result.title_str.toString().split(",");
					id_array=result.id_array.toString().split(",");
					service_array=result.service_str.toString().split(",");
					host_id="#service_big_box_"+id_array[5]+"_"+service_array[5];
					//alert(host_id);
					//alert($(host_id).attr("title"));
					//alert(title_array[5]);
					for(var i=0;i<id_array.length;i++)
					{
						//id_array[i];
						host_id="#service_big_box_"+id_array[i]+"_"+service_array[i];
						//alert($(host_id).attr("title"));
						//alert(title_array[i]);
						$(host_id).attr("title",title_array[i]);
						
						$(host_id+"_img").attr("src","images/new/status-"+img_array[i]+".png");
						//alert($(host_id).attr("title"));
						/*$(host_id+"_img").removeClass("icon-0");
					        $(host_id+"_img").removeClass("icon-1");
					        $(host_id+"_img").removeClass("icon-2");
					        $(host_id+"_img").removeClass("icon-3");
					        $(host_id+"_img").addClass("icon-"+img_array[i]);*/
					}
				}
				
			}
		    });
		    
}
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
	//alert($("#service_big_box_"+host_id+"_SNMP_UPTIME").attr("title"));
	var flag_change=false;
	if(is_localhost==1)
	{
	$.prompt("Services of localhost are not editable.",{prefix:'jqismooth'});
	//return false;
	}
	else
	{
	//is_colorbox_open=true;
	clearTimeout(eventRecursion);
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
			$("#"+id).bind("multiselectclick", function(event, ui){
					id=$(this).attr("id");
					var sel=$("#"+id).val();
					if(sel!=ui.value)
					{
						service_hosts.push(host_id);
						service_time.push(ui.value);
						service_name.push(id);
						$("#apply_changes_services_button").removeAttr('disabled');
						if(ui.value==518400)
						{
							$("#service_box_"+host_id+"_"+id).html("Y");
						}
						else if(ui.value==43200)
						{
							$("#service_box_"+host_id+"_"+id).html("M");
						}
						else if(ui.value==1440)
						{
							$("#service_box_"+host_id+"_"+id).html("D");
						}
						else
						{
							$("#service_box_"+host_id+"_"+id).html(ui.value);
						}
						flag_change=true;
					}
				});
			}
			/*var service_names=$("#service_names").val().split(",");
			for(var i=0;i<service_names.length-1;i++)
			{
			id=service_names[i].replace(/ /g,'_');
			$("#"+id+i).multiselect({selectedList: 1,multiple:false,noneSelectedText: 'Select Time',minWidth:50});
			//if(service_names[i].toLowerCase().indexOf("uptime")!=-1)
			//{
			//	$("#"+id).multiselect("disable");
			//}
			//else
			//{
			//alert("#service_box_"+host_id+"_"+id);
			$("#"+id+i).bind("multiselectclick", function(event, ui){
					var sel=$("#"+id+i).val();
					alert(sel);
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
			//}*/
		
		},
		onClosed:function(){
			if(flag_change==true)
			{
				$().toastmessage('showWarningToast', "Please save changes by clicking on Apply Changes.");
				//is_colorbox_open=false;
				
			}
			else
			{
			AutoRefresh(refresh_interval);
			}
		},
		overlayClose:false
	});
	}
}
function performActionService(oLink,action, type, site, name1, name2) {
		    var oImg = $(oLink).find("img");
		    oImg.attr("src","images/icon_reloading.gif");
		    // Chrome and IE are not animating the gif during sync ajax request
		    // So better use the async request here
		    //get_url('nagios_action.py?action='+action+'&site='+site+'&host='+name1+'&service='+name2,actionResponseHandler, oImg);
		    //oImg = null;
		    
		    $.ajax({
			type:"get",
			url:'nagios_action.py',//actionResponseHandler, oImg,
			data:{"action":action,"site":site,"host":name1,"service":name2,"view_type":"UNMP"},
			cache:false,
			success:function(result){
					//oLink;
					result=result.substring(1,result.length-2);
					result=result.split("','");
					/*
					0 'OK', 1337773481, 0, 'SNMP RESPONSE : OK
					1 0
					2 33 min
					3 1 sec
					4 58 sec
					5 0.128615
					6 SNMP RESPONSE : OK ( Host Uptime - 0 Days, 0 Hours, 34 Mins, 30 Secs)'
					
					*/
					var recTableObj = $(oLink).parent().parent();
		                        var td0 = $(recTableObj).find("td:eq(0)");
		                        var span0=$(td0).find("span");
		                        if(result[1]!='undefined' && result[1]!="undefined" && result[1])
		                        {
				                $(span0).removeClass("icon-0");
				                $(span0).removeClass("icon-1");
				                $(span0).removeClass("icon-2");
				                $(span0).removeClass("icon-3");
				                $(span0).addClass("icon-"+result[1]);
				        }
				        else
				        {
				        	var td7 = $(recTableObj).find("td:eq(6)");
			                        $(td7).html("Service check is in progress. Please wait for atleast 120 seconds before scheduling the check again.");
				        }
		                        var td3 = $(recTableObj).find("td:eq(2)");
		                        $(td3).html(result[2]);
		                        var td4 = $(recTableObj).find("td:eq(3)");
		                        $(td4).html(result[3]);
		                        var td5 = $(recTableObj).find("td:eq(4)");
		                        $(td5).html(result[4]);
		                        var td6 = $(recTableObj).find("td:eq(5)");
		                        $(td6).html(result[5]);
		                        var td7 = $(recTableObj).find("td:eq(6)");
		                        $(td7).html(result[6]);
					oImg.attr("src","images/icon_reload.gif");
			}
		    });
		    
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
	AutoRefresh(refresh_interval);
}

function delService()
{
	$.prompt("Delete Service",{prefix:'jqismooth'});
}
