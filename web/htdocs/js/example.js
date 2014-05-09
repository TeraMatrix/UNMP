/*
 * 
 * Author			:	Yogesh Kumar
 * Project			:	UNMP
 * Version			:	0.1
 * File Name		:	example.js
 * Creation Date	:	12-September-2011
 * Modify Date		:	12-September-2011
 * Purpose			:	Define All Required Javascript Functions
 * Require Library	:	jquery 1.4 or higher version and jquery.validate
 * Browser			:	Mozila FireFox [3.x or higher] and Chrome [all versions]
 * 
 * Copyright (c) 2011 Codescape Consultant Private Limited
 * 
 */

// Data Table Row's 
var tableData = [
	[11 ,1, "Yogesh", "Kumar", "Ajmer", "CCPL"],
	[23 ,2, "Yogesh", "Kumar", "Gurgaon", "Google"],
	[55 ,3, "Yogesh", "Kumar", "Jaipur", "Microsoft"],
	[56 ,4, "Yogesh", "Kumar", "Ajmer", "Google"],
	[67 ,5, "Yogesh", "Kumar", "Ajmer", "IBM"],
	[78 ,6, "Yogesh", "Kumar", "Jaipur", "TCS"],
	[85 ,7, "Yogesh", "Kumar", "Ajmer", "Accenture"],
	[88 ,8, "Yogesh", "Kumar", "Gurgaon", "Wipro"],
	[96 ,9, "Yogesh", "Kumar", "Ajmer", "Microsoft"],
	[97, 10, "Yogesh", "Kumar", "Jaipur", "Google"],
	[98, 11, "Yogesh", "Kumar", "Ajmer", "IBM"],
	[99, 12, "Yogesh", "Kumar", "Ajmer", "TCS"],
	[100, 13, "Yogesh", "Kumar", "Gurgaon", "Infosys"],
	[101, 14, "Yogesh", "Kumar", "Ajmer", "CCPL"],
	[102, 15, "Yogesh", "Kumar", "Ajmer", "Infosys"],
	[103, 16, "Yogesh", "Kumar", "Gurgaon", "CCPL"],
	[104, 17, "Yogesh", "Kumar", "Ajmer", "CCPL"],
	[105, 18, "Yogesh", "Kumar", "Jaipur", "Infosys"],
	[106, 19, "Yogesh", "Kumar", "Ajmer", "Infosys"],
	[107, 20, "Yogesh", "Kumar", "Gurgaon", "CCPL"],
	[108, 21, "Yogesh", "Kumar", "Ajmer", "CCPL"],
	[109, 22, "Yogesh", "Kumar", "Ajmer", "CCPL"],
	[110, 23, "Yogesh", "Kumar", "Gurgaon", "IBM"],
	[111, 24, "Yogesh", "Kumar", "Ajmer", "CCPL"],
	[113, 25, "Yogesh", "Kumar", "Ajmer", "CCPL"],
	[178, 26, "Yogesh", "Kumar", "Ajmer", "IBM"]
];


// Data Table Object
var oTable = null;

// Default Selected Link
var defaultSelectedLink = null;
 
$(document).ready(function() {
	var aSelected = [];

//	create data table object
	oTable = $('#example').dataTable({
		"bDestory":true,
		"bJQueryUI": true,
		"bProcessing": true,
		"sPaginationType": "full_numbers",
		"bPaginate":true,
		"bStateSave": false,
		"aaData": tableData,
		"aLengthMenu": [[20, 40, 60, -1],[20, 40, 60, "All"]],
		"bLengthChange":true,
		"sScrollY":String($("div#container_body").height()-115),
		"iDisplayLength":20,
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
			{ "sTitle": "S.No.","sWidth": "5%" },
			{ "sTitle": "First Name" , "sClass": "center","sWidth": "20%"},
			{ "sTitle": "Last Name", "sClass": "center","sWidth": "20%" },
			{ "sTitle": "Address","sClass": "center","sWidth": "25%" },
			{ "sTitle": "Company", "sClass": "center","sWidth": "30%"  }
		]
	});
	oTable.fnDraw();
	/* Click event handler */
	$('#example tbody tr').live('click', function () {
		var id = this.id;
		var index = jQuery.inArray(id, aSelected);
		
		if ( index === -1 ) {
			aSelected.push( id );
		} else {
			aSelected.splice( index, 1 );
		}
		
		$(this).toggleClass('row_selected');
	});
	//$(".dataTables_filter").css({"width":"95%"});
	//$('#example tr').click( function() {
	//	if ($(this).hasClass('row_selected'))
	//		$(this).removeClass('row_selected');
	//	else
	//		$(this).addClass('row_selected');
	//});
	
	// page tip [for page tip write this code on each page please dont forget to change "href" value because this link create your help tip page]
	$("#page_tip").colorbox(
	{
		href:"help_format.py",
		title: "Page Tip",
		opacity: 0.4,
		maxWidth: "80%",
		width:"350px",
		height:"250px"
	});
	
	// spin loading object [write this code on each page]
	var spinLoading = $("div#spin_loading");		// create object that hold loading circle
	var spinMainLoading = $("div#main_loading");	// create object that hold loading squire
	
	 // add tool tip
	 $("#add_user_form input,textarea,select").tooltip({
		// place tooltip on the right edge
		position: "center right",
		// a little tweaking of the position
		offset: [-2, 10],
		// use the built-in fadeIn/fadeOut effect
		effect: "fade",
		// custom opacity setting
		opacity: 0.7
	});
	$("#add_user_form").validate({
		rules:{
			first_name:{
				required:true
			},
			last_name:{
				required:true
			},
			sex:{
				required:true
			},
			address:{
				required:true
			},
			city:{
				required:true
			}
		},
		messages:{
			first_name:{
				required:"First Name is Required Field"
			},
			last_name:{
				required:"Last Name is Required Field"
			},
			sex:{
				required:"Sex is Required Field"
			},
			address:{
				required:"Address is Required Field"
			},
			city:{
				required:"City is Required Field"
			}
		}
	});
	$("#add_user_form").submit(function(){
		if($(this).valid())
		{
			$().toastmessage('showSuccessToast', "User Added Successfully.");
		}
		else
		{
			$().toastmessage('showErrorToast', "Some Fileds are Missing or Incorrect.");
		}
		return false;
	});
	$("#close_add_user").click(function(){
		$("div#user_datatable").show();
		$("div#user_form").hide();
	});
});

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
function addUser()
{
	$("div#user_datatable").hide();
	$("div#user_form").show();
	$().toastmessage('showWarningToast', "Add User Module incomplete module.");
}
function editUser()
{
	var selectedRow= fnGetSelected(oTable);
	var rLength = selectedRow.length; 
	if(rLength==0)
	{
		$.prompt("Please Select Atleast one user",{prefix:'jqismooth'});
	}
	else if (rLength == 1)
	{
		var iRow = oTable.fnGetPosition(selectedRow[0]);
		var aData = oTable.fnGetData(iRow);
		var id = aData[0];
		$.prompt(String(id),{prefix:'jqismooth'});
		$().toastmessage('showErrorToast', "You could not edit user details.");
	}
	else
	{
		$.prompt("Please Select Only Single user",{prefix:'jqismooth'});
	}		
}

function deleteUserCallback(v,m){
	if(v != undefined && v==true)
	{
		// spin loading object
		var spinLoading = $("div#spin_loading");		// create object that hold loading circle
		var spinMainLoading = $("div#main_loading");	// create object that hold loading squire
		spinStart(spinLoading,spinMainLoading);
		var selectedRow= fnGetSelected(oTable);
		var rLength = selectedRow.length;
		for(var i = 0;i<selectedRow.length;i++)
		{
			var iRow = oTable.fnGetPosition(selectedRow[i]);
			var aData = oTable.fnGetData(iRow);
			var id = aData[0];
			// if delete successfully then call this function
			oTable.fnDeleteRow(iRow);
		}
		setTimeout(function(){
			$().toastmessage('showSuccessToast', "User(s) Deleted Successfully.");
			spinStop(spinLoading,spinMainLoading);
		},4000);
	}
	else
	{
		$().toastmessage('showNoticeToast', "Remain Unchanged.");
	}
}

function delUser()
{
	var selectedRow= fnGetSelected(oTable);
	var rLength = selectedRow.length; 
	if(rLength==0)
	{
		$.prompt("Select Atleast one user",{prefix:'jqismooth'});
	}
	else
	{
		$.prompt('Are you sure, you want to delete this user?',{ buttons:{Ok:true,Cancel:false}, prefix:'jqismooth',callback:deleteUserCallback });
	}	
}
