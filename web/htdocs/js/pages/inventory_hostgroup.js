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
var $manageGroupDiv = null;
var grpData=[];
var boxGrpArray = [];
var boxGrpNameArray = [];
var selectedHGName = "";
var grpNameArray = [];
var grpArray = [];

var messages = {
	"add":"Hostgroup is added successfully.",
	"edit":"Hostgroup details Updated successfully.",
	"del":"Selected Hostgroup(s) deleted successfully",
	"delConfirm":"Are You Sure want to delete Selected Hostgroup(s)?",
	"duplicateError":"Hostgroup name already exists, Please Enter different Hostgroup Name and Hostgroup Alias.",
	"noneSelectedError":"Please select atleast one Hostgroup.",
	"multiSelectedError":"Please select single Hostgroup.",
	"defaultDelError":"Deletion of Default Hostgroup is restricted.",
	"defaultEditError":"Updation of Default Hostgroup is restricted.",
	"validationError":"Invalid host details are entered,please recheck.",
	"dbError":"UNMP Database Server is busy at the moment,please try again later.",
	"noRecordError":"No such record found.",
	"sysError":"UNMP Server is busy at the moment, please try again later.",
	"unknownError":"UNMP Server is busy at the moment, please try again later.",
	"nagiosConfigError":"UNMP Server is busy at the moment, please try again later.",
	"licenseError":"To sucessfully complete this action, please upgrade your license."
};
var actionName = null;

$(function(){
	// spin loading object
	$spinLoading = $("div#spin_loading");		// create object that hold loading circle
	$spinMainLoading = $("div#main_loading");	// create object that hold loading squire

	/* create object of divs */
	$gridViewDiv = $("div#grid_view_div");
	$formDiv = $("div#form_div");	
	$manageGroupDiv = $("div#manage_group_div");
	
	/* show grid view only hide other */
	$gridViewDiv.show();
	$formDiv.hide();
	
	/* page tip [for page tip write this code on each page please dont forget to change "href" value because this link create your help tip page] */
	$("#page_tip").colorbox(
	{
		href:"help_inventory_hostgroup.py",
		title: "Page Tip",
		opacity: 0.4,
		maxWidth: "80%",
		width:"500px",
		height:"450px",
		onComplte:function(){}
	});
	
	/* create grid view */
	gridViewHostgroup();
	
	/* Click event handler for grid view */
	$('#grid_view tbody tr').live('click', function (event) {
		var id = this.id;
		if(event.target.nodeName.toLowerCase() != 'img')
		{
			var index = jQuery.inArray(id, aSelected);
		
			if ( index === -1 ) {
				aSelected.push( id );
			} else {
				aSelected.splice( index, 1 );
			}
		
			$(this).toggleClass('row_selected');
		}
	});
});


function advance_settings_colorbox()
{
	if($("#hostgroup_id").val()==undefined)
		$("#advanced_settings").hide();
	else
		window.location="edit_nagios_hostgroup_from_inventory.py?hostgroup_id="+$("#hostgroup_id").val();
}

function gridViewHostgroup()
{
	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"post",
		url:"grid_view_hostgroup.py",
		cache:false,
		success:function(result){
			try
			{
				result = eval(result);
			}
			catch(err)
			{
				result = [];
			}
			//	create data table object
			oTable = $('#grid_view').dataTable({
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true,
				"bStateSave": false,
				"aaData": result,
				"bLengthChange":true,
				"oLanguage":{
					"sInfo":"_START_ - _END_ of _TOTAL_",
					"sInfoEmpty":"0 - 0 of 0",
					"sInfoFiltered":"(of _MAX_)"
				},
				"fnRowCallback": function( nRow, aData, iDisplayIndex ) {
					if ( jQuery.inArray(aData.DT_RowId, aSelected) !== -1 ) {
						$(nRow).addClass('row_selected');
					}
					return nRow;
				},
				"aoColumns": [
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 0 ] },
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 1 ] },
					{ "sTitle": "S.No.", "bVisible": false, "aTargets": [ 2 ] },
					{ "sTitle": "Hostgroup Name" , "sClass": "center","sWidth": "150px"},
					{ "sTitle": "Hostgroup Alias" , "sClass": "center","sWidth": "150px"},
					{ "sTitle": "Assigned Groups" , "sClass": "center","sWidth": "auto"},
					{ "sTitle": "Number of Devices" , "sClass": "center","sWidth": "auto"},
					{ "sTitle": "Actions" , "sClass": "center","sWidth": "100px"}
				]
			});
			$("img.host_opr","#grid_view_group").tipsy({gravity: 'n'});
			manageHostgroupGroups($("img.img-link","#grid_view"));
			spinStop($spinLoading,$spinMainLoading);
		}
	});
}


function manageHostgroupGroups(imgObj)
{
	imgObj.tipsy({gravity: 'n'});
	imgObj.click(function(e){
		//e.stopPropagation();
		var $imgThis = $(this);
		showManageGroupDiv();
		$manageGroupDiv.html("");
		spinStart($spinLoading,$spinMainLoading);
		var id = $imgThis.attr("id");
		$.ajax({
			type:"get",
			url:"get_hostgroup_by_id.py?hostgroup_id=" + id,
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
					createHostgroupDetailsTable(result.result);
				}
				else
				{
					$().toastmessage('showErrorToast', messages[result.msg]);
					hideManageGroupDiv();
				}
				spinStop($spinLoading,$spinMainLoading);
			}
		});
	});
}
function createHostgroupDetailsTable(hostgroupDetails)
{
	var $table = $("<table/>");
	var $tr = $("<tr/>");
	var $th = $("<th/>");
	var $td = null;
	var $hidden = $("<input/>");
	var $img = $("<img/>");
	$img.attr({"class":"img-link","src":"images/new/close.png","title":"Close"});
	$img.click(function(){
		hideManageGroupDiv();
		gridViewHostgroup();
		
	});
	$img.css({"float":"right","margin-right":"10px"});
	$img.tipsy({gravity: 'n'});
	
	$table.attr({"class":"tt-table","cellspacing":"0","cellpadding":"0","width":"100%"})
	
	// store hostgroup id in hidden field.
	$hidden.attr({"type":"hidden","id":"hostgroup_id2","name":"hostgroup_id2"})
	$hidden.val(hostgroupDetails[0]);
	$hidden.appendTo($tr);
	
	$th.attr({"colspan":4,"class":"cell-title"});
	$th.html("Hostgroup Details");
	$img.appendTo($th);
	$th.appendTo($tr);
	$tr.appendTo($table);
	
	// creating new row
	$tr = $("<tr/>");
	
	// creating Hostgroup Name Label [column]
	$td = $("<td/>");
	$td.attr("class","cell-label");
	$td.html("Hostgroup Name");
	$td.appendTo($tr);
	
	// creating Hostgroup Name [column]
	$td = $("<td/>");
	$td.attr("class","cell-info");
	$td.html(hostgroupDetails[1]);
	selectedHGName = hostgroupDetails[1];
	$td.appendTo($tr);
	
	// creating Hostgroup Alias Label [column]
	$td = $("<td/>");
	$td.attr("class","cell-label");
	$td.html("Hostgroup Alias");
	$td.appendTo($tr);
	
	// creating Hostgroup Name [column]
	$td = $("<td/>");
	$td.attr("class","cell-info");
	$td.html(hostgroupDetails[2]);
	$td.appendTo($tr);
	
	// append row to table
	$tr.appendTo($table);
	
	
	// creating new row
	$tr = $("<tr/>");
	
	// creating Hostgroup Name Label [column]
	$td = $("<td/>");
	$td.attr("class","cell-label");
	$td.html("Created By");
	$td.appendTo($tr);
	
	// creating Hostgroup Name [column]
	$td = $("<td/>");
	$td.attr("class","cell-info");
	$td.html(hostgroupDetails[4]);
	$td.appendTo($tr);
	
	// creating Hostgroup Alias Label [column]
	$td = $("<td/>");
	$td.attr("class","cell-label");
	$td.html("Creation Time");
	$td.appendTo($tr);
	
	// creating Hostgroup Name [column]
	$td = $("<td/>");
	$td.attr("class","cell-info");
	$td.html(hostgroupDetails[5]);
	$td.appendTo($tr);
	
	// append row to table
	$tr.appendTo($table);
	
	// creating new row
	$tr = $("<tr/>");
	
	// creating Hostgroup Name Label [column]
	$td = $("<td/>");
	$td.attr("class","cell-label");
	$td.html("Updated By");
	$td.appendTo($tr);
	
	// creating Hostgroup Name [column]
	$td = $("<td/>");
	$td.attr("class","cell-info");
	$td.html(hostgroupDetails[6]);
	$td.appendTo($tr);
	
	// creating Hostgroup Alias Label [column]
	$td = $("<td/>");
	$td.attr("class","cell-label");
	$td.html("Update Time");
	$td.appendTo($tr);
	
	// creating Hostgroup Name [column]
	$td = $("<td/>");
	$td.attr("class","cell-info");
	$td.html(hostgroupDetails[3]);
	$td.appendTo($tr);
	
	// append row to table
	$tr.appendTo($table);
	
	$table.appendTo($manageGroupDiv);


	$table = $("<table/>");
	$table.attr({"class":"tt-table","cellspacing":"0","cellpadding":"0","width":"100%"});
	$table.css("margin-bottom","0px");
	
	$tr = $("<tr/>");
	$th = $("<th/>");
	$th.attr({"class":"cell-title"});
	$th.html("Assigned Group Details");
	
	$img = $("<img/>");
	$img.attr({"class":"img-link","src":"images/new/update.png","title":"Move Group"});
	$img.click(function(){
		moveGrpToHg();
	});
	$img.css({"float":"right","margin-right":"10px"});
	$img.tipsy({gravity: 'n'});
	$img.appendTo($th);
	
	$img = $("<img/>");
	$img.attr({"class":"img-link","src":"images/new/user-delete.png","title":"Delete Group"});
	$img.click(function(){
		delGrpFrmHg();
	});
	$img.css({"float":"right","margin-right":"10px"});
	$img.tipsy({gravity: 'n'});
	$img.appendTo($th);
	
	$img = $("<img/>");
	$img.attr({"class":"img-link","src":"images/new/user-add.png","title":"Add Group"});
	$img.css({"float":"right","margin-right":"10px"});
	$img.tipsy({gravity: 'n'});
	$img.colorbox(
	{
		href:"add_gpinhg_view.py",
		onComplete:function(){
			var selectAll = $("button#selectAll");
			showGrp(); searchEvent();
			selectAll.toggle(function(){
                    $('div#groups_in_hg').find('input:checkbox').attr('checked','checked');
                    $(this).find("span").text('uncheck all');
                },function(){
                    $('div#groups_in_hg').find('input:checkbox').removeAttr('checked');
                    $(this).find("span").text('check all');        
                });
		},
		title: "Assign/Add Groups To Hostgroup",
		opacity: 0.4,
		maxWidth: "80%",
		width:"550px",
		height:"450px"
	});
	$img.appendTo($th);
	
	$th.appendTo($tr);
	$tr.appendTo($table);
	
	$table.appendTo($manageGroupDiv);
	
	$table = $("<table/>");
	$table.attr({"cellpadding":"0", "cellspacing":"0", "border":"0", "class":"display", "id":"grid_view_group"});
	$table.appendTo($manageGroupDiv);
	user_get_log(hostgroupDetails[0]);
}
function showGrp(searchGrp)
{
	spinStart($spinLoading,$spinMainLoading);
	searchGrp = "";
	grpData = [];
	$.ajax({
		type:"get",
		url:"show_groups.py?hostgroup_id="+ $("input#hostgroup_id2").val() +"&all=0"+"&light_box="+1,
		cache:false,
		success:function(result1){
			try
			{
				grpData = eval(result1);
			}
			catch(err)
			{
				grpData = [];
			}
			 grpSearch();
			 spinStop($spinLoading,$spinMainLoading);
			//var searchGrp = $.trim($("div#hg_ingrp_head").find("input#search_hg")).val());
		}
	});
}
function searchEvent()
{
	$("input#search_grp").keyup(function(){
		 grpSearch($.trim($(this).val()));
	});	
}
function grpSearch(searchGrp)
{
	if (!searchGrp)
	{
		searchGrp = "";
	}
	var $grpTable = $("<table width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" class=\"tt-table\" />");
	var $grpTr = null;
	var j = 0;
    var flag_search = 0;
    var $div_btn = $('div#groups_in_hg').next().find('button');
	if (grpData.length < 1)
	{
		var $grpTr = $("<tr/>");
		var $grpTd = $("<td class=\"cell-info1\" > All UserGroups Assigned successfully to HostGroup </td>");
		$grpTd.appendTo($grpTr);
		$grpTr.appendTo($grpTable);
		$div_btn.attr('disabled',true).addClass("disabled");
		if ($("button#selectAll").find("span").text() == 'uncheck all')
		{   
    		$("button#selectAll").click();	
    	}	
		flag_search = 1
		
	}
	for (i in grpData)
	{	
		if (String(grpData[i][1]).indexOf(searchGrp) >= 0 )
		{
			flag_search = 2;
			if(j==0)
			{
				var $grpTr = $("<tr/>");
			}
			if (j < 3)
			{
				var $grpTd = $("<td class=\"cell-info1\" />");
				var $grpInput = $("<input type='checkbox' class='box-grp-check' name='group_check' value="+"'"+ String(grpData[i][0]) +"'" +" />");
				$grpInput.appendTo($grpTd);
				$grpTd.append("<span style=\"line-height:1.8em;\">" + (String(grpData[i][1])) + "</span>");
				$grpTd.appendTo($grpTr);
				j = j+1; 
				
			}
			if(j == 3)
			{
				$grpTr.appendTo($grpTable);
				j = 0;							
			}	
		}  
		
	} // end of outer for
	
	if (j != 0)
	{	j = 3 - j;
		while(j != 0)
		{
			var $grpTd = $("<td class=\"cell-info1\" />");
			$grpTd.appendTo($grpTr);
			j = j -1
		}
		$grpTr.appendTo($grpTable);	
	}
	
	if (flag_search == 0)
	{
		var $grpTr = $("<tr/>");
		var $grpTd = $("<td class=\"cell-info1\" > No matching records found</td>");
		$grpTd.appendTo($grpTr);
		$grpTr.appendTo($grpTable);	
		if ($("button#selectAll").find("span").text() == 'uncheck all')
		{   
    		$("button#selectAll").click();	
    	}
    	
    	$div_btn.attr('disabled',true).addClass("disabled");
	}
	if (flag_search == 2)
	{
	    if ($("button#selectAll").find("span").text() == 'uncheck all')
		    {   
        		$("button#selectAll").click();	
        	}
    	$div_btn.removeAttr('disabled').removeClass("disabled");
	}
	
	$("div#groups_in_hg").html($grpTable);
}
function boxAddGrp()
{
	boxGrpArray = [];
	boxGrpNameArray = [];
	$.each($("input[class='box-grp-check']:checked"), function(i,obj){
		boxGrpArray.push($(obj).val());
		boxGrpNameArray.push($(obj).parent().text());
	});
	//alert(String(boxGrpArray))
	if(boxGrpArray.length==0)
	{
		$.prompt("Select at least one Group(s)",{prefix:'jqismooth'});
	}
	else
	{
		$.prompt('Are you sure, you want to Add group(s) to this Hostgroup?',{ buttons:{Yes:true,No:false}, prefix:'jqismooth',callback:boxAddGrpCallback });	
	}
	
}

function boxAddGrpCallback(v,m)
{
	if(v != undefined && v==true)
	{
		spinStart($spinLoading,$spinMainLoading);
		$.ajax({
			type:"get",
			url:"add_group_tohostgroup.py?&hostgroup_id="+$("input#hostgroup_id2").val()+"&gp_ids="+String(boxGrpArray)+"&grp_names="+String(boxGrpNameArray)+"&hg_name="+selectedHGName,
			cache:false,
			success:function(result){
				result = eval("(" + result + ")");
				if(result.success == 0)
				{

					$().toastmessage('showSuccessToast', "Groups Added Successfully.");
					showGrp();
					user_get_log($("input#hostgroup_id2").val());
				}
				else
				{
					//alert(result.result);
					$().toastmessage('showWarningToast',String(result.result));
				}
				spinStop($spinLoading,$spinMainLoading);
			}
		});
	}

}

function delGrpFrmHg()
{	
	grpArray = [];
	grpNameArray  = [];
	$.each($("input[name='group_check']:checked"), function(i,obj){
		grpArray.push($(obj).val());
		grpNameArray.push($(obj).parent().text());
	});

	if(grpArray.length==0)
	{
		$.prompt("Select at least one Group",{prefix:'jqismooth'});
	}
	else
	{
		$.prompt('Are you sure, you want to delete Group(s) from this Hostgroup?',{ buttons:{Yes:true,No:false}, prefix:'jqismooth',callback:delGrpCallback });	
	}	
}

function delGrpCallback(v,m)
{
	if(v != undefined && v==true)
	{
		spinStart($spinLoading,$spinMainLoading);
		var action = "del_group_fromhostgroup.py";
		var data = "gp_ids=" + String(grpArray)+"&hostgroup_id=" + String($("input#hostgroup_id2").val())+"&grp_names="+String(grpNameArray)+"&hg_name="+selectedHGName;
		var method = "get";
		$.ajax({
			url:action,
			type:method,
			data:data,
			cache:false,
			success:function(result){
				result = eval("(" + result + ")");
				if(result.success == 0)
				{
					$().toastmessage('showSuccessToast', "Hostgroup(s) Deleted Successfully.");
					user_get_log($("input#hostgroup_id2").val());
				}
				else
				{
					$().toastmessage('showWarningToast',String(result.result));
				}
				spinStop($spinLoading,$spinMainLoading);
			}
		});
	}

}

function moveGrpToHg()
{
	grpArray = [];
	grpNameArray = [];
	$.each($("input[name='group_check']:checked"), function(i,obj){
		grpArray.push($(obj).val());
		grpNameArray.push($(obj).parent().text());
	});
	if(grpArray.length==0)
	{
		$.prompt("Select at least one Group",{prefix:'jqismooth'});
	}
	else
	{
		boxHGroupId = "";
		var move_box = $.colorbox(
		{
			href:"move_gptohg_view.py?hg_id="+$("input#hostgroup_id2").val(),
			onComplete:function(){
				$('select#groups').change(function() 
				{		boxHGroupId = "";
						var $this = $(this);
						boxHGroupId = $this.val();
					});
					
				},
			title: "Move User Group to Another Hostgroup",
			opacity: 0.4,
			maxWidth: "80%",
			width:"400px",
			height:"150px"
		});	
	}
		
}


function boxMoveGrp()
{
	if(boxHGroupId == "" || boxHGroupId == null)
	{
			$.prompt("Select at least one HostGroup",{prefix:'jqismooth'});		
	}
	else if(grpArray.length==0)
	{
		$.prompt("Select at least one Group",{prefix:'jqismooth'});
	}
	else
	{

		$.prompt('Are you sure, you want to Move Group(s) from this Hostgroup?',{ buttons:{Yes:true,No:false}, prefix:'jqismooth',callback:boxMoveGrpCallback });	
	}
	
}

function boxMoveGrpCallback(v,m)
{
	if(v != undefined && v==true)
	{
		spinStart($spinLoading,$spinMainLoading);
		var hostgroup_name = "";
		hostgroup_name = $("div#selectGroupDiv").find("select#groups option:selected").text();
		$.ajax({
			type:"get",
			url:"move_group_tohostgroup.py?&hostgroup_id="+boxHGroupId+"&gp_ids="+String(grpArray)+"&old_hostgroup_id="+$("input#hostgroup_id2").val()+"&sel_hg="+selectedHGName+"&grp_names="+String(grpNameArray)+"&hg_name="+hostgroup_name,
			cache:false,
			success:function(result){
				result = eval("(" + result + ")");
				if(result.success == 0)
				{

					$().toastmessage('showSuccessToast', "Group(s) Moved Successfully.");
					boxHGroupId = "";
					//user_get_log();//$("button[id='" + selectedHGroupId + "']").click();
					user_get_log($("input#hostgroup_id2").val());
					$("div#cboxClose").click();
				}
				else
				{
					//alert(result.result);
					$().toastmessage('showWarningToast',String(result.result));
				}
				spinStop($spinLoading,$spinMainLoading);
			}
		});
	}

}

function user_data(user_tabledata)
{
	oTableUser = $('#grid_view_group').dataTable({
		"bDestroy":true,
		"bJQueryUI": true,
		"bProcessing": true,
		"sPaginationType": "full_numbers",
		"bPaginate":true,
		"bStateSave": false,
		"aaData": user_tabledata,
		"aaSorting" : [],
		"oLanguage":{
			"sInfo":"_START_ - _END_ of _TOTAL_",
			"sInfoEmpty":"0 - 0 of 0",
			"sInfoFiltered":"(of _MAX_)"
		},
/*		"fnRowCallback": function( nRow, aData, iDisplayIndex ) {
			if ( jQuery.inArray(aData.DT_RowId, aSelectedLog) !== -1 ) {
				$(nRow).addClass('row_selected');
			}
			return nRow;
		},*/
		"aoColumns": [
			{ "sTitle": "SELECT","sClass": "center","sWidth": "5%" },
			{ "sTitle": "GROUP NAME","sClass": "center","sWidth": "10%" },
			{ "sTitle": "USERS IN THIS GROUP" , "sClass": "center","sWidth": "60%"},
			{ "sTitle": "DETAILS" , "sClass": "center","sWidth": "10%"}
		]
	});
	$("img.img-link","#grid_view_group").tipsy({gravity: 'n'});
};
function viewGroupDetails(gid)
{
	$.colorbox(
	{
		href:"viewGroupDetails.py?group_id="+gid,
		onComplete:function(){
		},
		title: "Details of Users Present in this Group",
		opacity: 0.4,
		maxWidth: "80%",
		width:"550px",
		height:"450px"
	});
	
}
function user_get_log(hgId)
{
	spinStart($spinLoading,$spinMainLoading);
	$.ajax({ 
		type:"get",
		url:"show_groups_user.py?hostgroup_id="+ hgId,
		cache:false,
		success:function(result){ 
			try
			{
				result = eval("(" + result + ")");
			}
			catch(err)
			{
				result=[];
				//$().toastmessage('showErrorToast', err);
			}
			user_data(result);
			spinStop($spinLoading,$spinMainLoading);
		}
	});
}

function createForm(act,id)
{
	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"post",
		url:"form_hostgroup.py",
		cache:false,
		success:function(result){
			$formDiv.html(result);
			addFormToolTip();
			cancelForm();
			$form = $("form#form_hostgroup");
			$formTitle = $("form#form_hostgroup th#form_title");
			$formInput = $("form#form_hostgroup input[type='text']");
			$formAddButton = $("form#form_hostgroup button[id='add_hostgroup']");
			$formEditButton = $("form#form_hostgroup button[id='edit_hostgroup']");
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
		}
	});
	if($("#hostgroup_id").val()==undefined || $("#hostgroup_id").val()=="")
		$("#advanced_settings").hide();
}
function addFormToolTip()
{
	// add tool tip
	$tooltip = $("form#form_hostgroup input[type='text']").tooltip({
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
function cancelForm()
{
	$("button#cancel_hostgroup").click(function(){
		hideForm();
	});
}
function hideForm()
{
	$gridViewDiv.show();
	$formDiv.hide();
	$manageGroupDiv.hide();
	/* this is bcoz when validation unsuccess and you click on cancel button then tooltip visible so this code will hide that. */
	if($tooltip)
		$tooltip.tooltip().hide();
}
function showForm()
{
	$gridViewDiv.hide();
	$formDiv.show();
	$manageGroupDiv.hide();
	
}
function showManageGroupDiv()
{
	$gridViewDiv.hide();
	$formDiv.hide();
	$manageGroupDiv.show();
}
function hideManageGroupDiv()
{

	$gridViewDiv.show();
	$formDiv.hide();
	$manageGroupDiv.hide();
	
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
						gridViewHostgroup();
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
			hostgroup_name:{
				required:true,
				alphaNumeric: true,
				noSpace: true
			},
			hostgroup_alias:{
				required:true,
				alphaNumeric: true
			}
		},
		messages:{
			hostgroup_name:{
				required:"Hostgroup Name is Required Field",
				alphaNumeric: "Name should be alpha numeric",
				noSpace: "Space Not Allowed"
			},
			hostgroup_alias:{
				required:"Hostgroup Alias is Required Field",
				alphaNumeric: "Alias should be alpha numeric"
			}
		}
	});
}
function addForm()
{
	$("#advanced_settings").hide();
	$formTitle.html("Add Hostgroup");
	$form.attr("action","add_hostgroup.py");
	$formInput.val("");
	$formAddButton.css({"display":"inline-block"});
	$formEditButton.hide();	
	showForm();	
	if($("#hostgroup_id").val()==undefined || $("#hostgroup_id").val()=="")
		$("#advanced_settings").hide();
}
function editForm(id)
{
	$formTitle.html("Edit Hostgroup");
	$form.attr("action","edit_hostgroup.py");
	$formEditButton.css({"display":"inline-block"});
	$formAddButton.hide();
	$.ajax({
		type:"get",
		url:"get_hostgroup_by_id.py?hostgroup_id=" + id,
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
				$form.find("input#hostgroup_id").val(result.result[0]);
				$formInput.eq(0).val(result.result[1]);
				$formInput.eq(1).val(result.result[2]);
				showForm();
			}
			else
			{
				$().toastmessage('showErrorToast', messages[result.msg]);
			}
		}
	});
}
function addHostgroup()
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

function editHostgroup(id,isDefault)
{
	if(isDefault == 0)
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
		$.prompt(messages["defaultEditError"],{prefix:'jqismooth'});
	}
}

function delHostgroup()
{
	actionName = "delConfirm";
	hideForm();
	var selectedRow= fnGetSelected(oTable);
	var rLength = selectedRow.length; 
	if(rLength==0)
	{
		$.prompt(messages["noneSelectedError"],{prefix:'jqismooth'});
	}
	else
	{
		$.prompt(messages[actionName],{ buttons:{Ok:true,Cancel:false}, prefix:'jqismooth',callback:delHostgroupCallback });
	}	
}

function delHostgroupCallback(v,m){
	actionName = "del"
	if(v != undefined && v==true)
	{
		var action = "del_hostgroup.py";
		var method = "get";
		spinStart($spinLoading,$spinMainLoading);
		var selectedRow= fnGetSelected(oTable);
		var rLength = selectedRow.length;
		var hostgroupId = [];
		var isDefault = false;
		for(var i = 0;i<selectedRow.length;i++)
		{
			var iRow = oTable.fnGetPosition(selectedRow[i]);
			var aData = oTable.fnGetData(iRow);
			if(aData[1] == 0)
			{
				hostgroupId.push(aData[0]);
			}
			else
			{
				isDefault = true;
				break;
			}
		}
		if(isDefault)
		{
			$.prompt(messages["defaultDelError"],{prefix:'jqismooth'});
			spinStop($spinLoading,$spinMainLoading);
		}
		else
		{
			$.ajax({
				type:method,
				url:action + "?hostgroup_ids=" + String(hostgroupId),
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
							var iRow = oTable.fnGetPosition(selectedRow[i]);
							oTable.fnDeleteRow(iRow);
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
