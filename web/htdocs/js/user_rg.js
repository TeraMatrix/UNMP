/*
 * 
 * Author			:	RG
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


// Data Table Object
var oTable = null;

// Default Selected Link
var defaultSelectedLink = null;

// selected row 
var aSelected = [];

var $tooltip = null;

function userDataTable()
{
	aSelected = [];
	$.ajax({
		type:"get",
		url:"user_detail_table.py",
		success:function(result){
			
				oTable = $('#user_table').dataTable({
					"bDestroy":true,
					"bJQueryUI": true,
					"bProcessing": true,
					"sPaginationType": "full_numbers",
					"bStateSave": true,
					"aaData": eval(result),
					"fnRowCallback": function( nRow, aData, iDisplayIndex ) {
						if ( jQuery.inArray(aData.DT_RowId, aSelected) !== -1 ) {
							$(nRow).addClass('row_selected');
						}
						return nRow;
					},
					"aoColumns": [
						{ "bSearchable": false, "bVisible": false, "aTargets": [ 0 ] },
						{ "sTitle": "User Name", "sClass": "center","sWidth": "12%" },
						{ "sTitle": "First Name" , "sClass": "center","sWidth": "12%"},
						{ "sTitle": "Last Name", "sClass": "center","sWidth": "12%" },
						{ "sTitle": "Designation","sClass": "center","sWidth": "12%" },
						{ "sTitle": "Mobile No", "sClass": "center","sWidth": "12%"  },
						{ "sTitle": "E-Mail ID", "sClass": "center","sWidth": "30%"  }
					]
				});
				oTable.fnDraw();
			
			}
	});
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

$(document).ready(function() {
/* Click event handler */
	$('#user_table tbody tr').live('click', function () {
		var id = this.id;
		var index = jQuery.inArray(id, aSelected);
		
		if ( index === -1 ) {
			aSelected.push( id );
		} else {
			aSelected.splice( index, 1 );
		}
		
		$(this).toggleClass('row_selected');
	});
	userDataTable();
//	create data table object

	
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
		
	 
	 $("#close_add_user").click(function(){
	 	$("span#check_result").html(" ");
        if($tooltip)
	    	$tooltip.tooltip().hide();
		$("div#user_form").hide();
		$("div#edit_usr_form").hide();
		$("div#user_datatable").show();
	});
	// add tool tip
	 $tooltip = $("#add_user_form input[type='text'],#add_user_form input[type='password'],#add_user_form textarea,#add_user_form select").tooltip({
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
			user_name: {
				required: true,
				minlength: 5,
				maxlength: 15,
				noSpace: true
			},
			password: {
				required: true,
				minlength: 6
			},
			cpassword: {
				required: true,
				minlength: 6,
				equalTo: "#password"
			},
			groups : "required",
			
			first_name: {
				minlength: 1,
				alpha: true,
				maxlength: 25
			},
			last_name:{
				minlength: 1,
				maxlength: 25,
				alpha: true
			},
			mobile: {
				minlength: 10,
				maxlength: 10,
				positiveNumber: true,			
			},
			email_id: {
				email: true
			}
			
		},
		messages:{
			user_name: {
				required: "*",
				minlength: " at least 5 characters",
				maxlenght: " only 15 characters",
				noSpace: " No space Please"
			},
			
			password: {
				required: "*",
				minlength: " Your password must be at least 6 characters long"
			},
			
			cpassword: {
				required: "*",
				minlength: " Your password must be at least 6 characters long",
				equalTo: " Please enter the same password as above"
			},
			
			groups: {
				required: "*"	
			}
			
		}
	});
	$("#add_user_form").submit(function(){
		if($(this).valid())
		{
			
			var form = $(this);
			var method = form.attr("method");
			var action = form.attr("action");
		
			var data = form.serialize();
			//alert(data);
			$.ajax({
				type:method,
				url:action,
				data:data,
				success:function(result)
				{ 
					result = eval("("+ result +")");
					if(result.success == 0)
					{
						$().toastmessage('showSuccessToast', "User Added Successfully.");
						userDataTable();
						$("#close_add_user").click();
						
					}
					else if(result.success == 1)
					{
						
						$().toastmessage('showErrorToast', String(result["result"]));
					}
					else
					{
						var dt = result.result;
						for(key in dt)
						{
							resultStr+= key + ": " + dt[key]+"<br/>"
						}
						$().toastmessage('showErrorToast', "Some Fields are Missing or Incorrect.");
					}
					//result = {success:1,result:{"fname":"Filed Missing","lname":"Filed Wrong"}};
					/*resultStr = "";
					if(result.success == 1)
					{
						
						$.prompt(resultStr,{prefix:'jqismooth'});
					}
					else
					{
						$().toastmessage('showSuccessToast', "User Added Successfully.");
					}*/
					
					
				}
			});
		}
		else
		{
			$().toastmessage('showErrorToast', "Some Fields are Missing or Incorrect.");
		}
		return false;
	});
		
	
});

/*
 * I don't actually use this here, but it is provided as it might be useful and demonstrates
 * getting the TR nodes from DataTables
 */


function name_chk()
{
	if($("form").attr('id') == "add_user_form")
	{	
		val_ = $("input#user_name").val();
		type_ = "get";
		func_type = "user";	
	}
	else if($("form").attr('id') == "add_group_form")
	{
		val = $("input#group_name");
		type_ = "get";
		func_type = 0;	
	}
	if(val_.length > 4)
	{
		$.ajax({
				type:type_,
				url:"check_name.py?&name="+ val_ + "&type=" +func_type,
				success:function(result)
				{
					result = eval("("+ result +")");
					
					if(result.success == 0)
					{
						$("span#check_result").css("color","green");
						$("span#check_result").html("Name is Available ");
						
					}
					else
					{
						$("span#check_result").css("color","red");
						$("span#check_result").html("**Name is NOT Available ");
						
					}
					
				}
		});
	}
	else
	{
		$("span#check_result").html("");	
	}
}


function addUser()
{
	$("div#user_datatable").hide();
	$("div#edit_usr_form").hide();
	$("div#user_form").show();
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
		
		
		$.ajax({
			type:"get",
			url:"edit_user_view.py?&user_id="+id,
			success:function(result)
			{
                if (result.indexOf("NOUSERAVAILABLEWITHTHISID") >= 0)
                {
					$().toastmessage('showErrorToast', 'User Not Avaliabe for Edit \n May be User is Deleted');
					userDataTable();
					
                }
                else if (result.indexOf("SOMEERROROCCURMAYBEDBERROR") >= 0)
                {
                	$().toastmessage('showErrorToast', ' Some Error is Occur Please Try Again /n May be DB not started /n OR Contact Your Admin');
					userDataTable();	
                }
                else
				{
					$("div#edit_usr_form").html(result) ;
					$("div#user_datatable").hide();
					$("div#user_form").hide();
					$("div#edit_usr_form").show();
				
					$("#close_edit_user").click(function(){
						//if($tooltip)
				       		//	$tooltip.tooltip().hide();
						$("div#user_form").hide();
						$("div#edit_usr_form").hide();
						$("div#user_datatable").show();
                
					});
				
					$tooltip = $("#edit_usr_form input[type='text'],#edit_usr_form  textarea,#edit_usr_form  select").tooltip({
						// place tooltip on the right edge
						position: "center right",
						// a little tweaking of the position
						offset: [-2, 10],
						// use the built-in fadeIn/fadeOut effect
						effect: "fade",
						// custom opacity setting
						opacity: 0.7
					});
							
						
					$("#edit_user_form").validate({
						rules:{
							groups : "required",
							first_name: {
								minlength: 4,
								maxlength: 25,
								alpha: true
							},
							last_name:{
								minlength: 4,
								maxlength: 25,
								alpha: true
							},
							mobile: {
								minlength: 10,
								maxlength: 10,
								positiveNumber: true,			
							},
							email_id: {
								email: true
							}
						},
						messages:{
							groups: "*"
						}
					});
					
					$("#edit_user_form").submit(function(){
						if($(this).valid())
						{
							
							var form = $(this);
							var method = form.attr("method");
							var action = form.attr("action");
							var data = form.serialize();
							//alert(data);
							$.ajax({
								type:method,
								url:action,
								data:data,
								success:function(result)
								{
									//alert(result); 
									result = eval("("+ result +")");
									if(result.success == 0)
									{
										$().toastmessage('showSuccessToast', "User Updated Successfully.");
										userDataTable();
										$("#close_edit_user").click();
									}
									else if(result.success == 1)
									{
										
										$().toastmessage('showErrorToast', String(result["result"]));
									}
									else
									{
										var dt = result.result;
										for(key in dt)
										{
											resultStr+= key + ": " + dt[key]+"<br/>"
										}
										$().toastmessage('showErrorToast', "Some Fields are Missing or Incorrect.");
									}
									//result = {success:1,result:{"fname":"Filed Missing","lname":"Filed Wrong"}};
									/*resultStr = "";
									if(result.success == 1)
									{
										
										$.prompt(resultStr,{prefix:'jqismooth'});
									}
									else
									{
										$().toastmessage('showSuccessToast', "User Added Successfully.");
									}*/
									
									
								}
							});
							return false;
						}
						else
						{
							$().toastmessage('showErrorToast', "Some Fields are Missing or Incorrect.");
						}
						
					});	
					return false;
				
				}
			}
		});
		return false;
		//$.prompt(String(id),{prefix:'jqismooth'});
		//$().toastmessage('showWarningToast', "Edit User Module in progress .");
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
		//spinStart(spinLoading,spinMainLoading);
		var selectedRow= fnGetSelected(oTable);
		var rLength = selectedRow.length;
		var idStr = "";
		var selectedDeletedRowArray = [];
		for(var i = 0;i<selectedRow.length;i++)
		{
			var iRow = oTable.fnGetPosition(selectedRow[i]);
			var aData = oTable.fnGetData(iRow);
			if(i>0)
			{
				idStr+=",";
			}
			idStr += String(aData[0]);
			selectedDeletedRowArray.push(iRow);
			// if delete successfully then call this function
			
		}
		var action = "del_user.py";
		var data = "user_ids=" + idStr;
		var method = "get";
		$.ajax({
			url:action,
			type:method,
			data:data,
			success:function(result){
				result = eval("(" + result + ")");
				if(result.success == 0)
				{
					for(var j=0;j<selectedDeletedRowArray.length;j++)
						oTable.fnDeleteRow(selectedDeletedRowArray[j]);
					//alert("Deleted Successfully");
					$().toastmessage('showSuccessToast', "User(s) Deleted Successfully.");
					userDataTable();
				}
				else
				{
					alert(result.result);
				}
			}
		});
//		return false;
//		setTimeout(function(){
//			$().toastmessage('showSuccessToast', "Group Deleted Successfully.");
//			spinStop(spinLoading,spinMainLoading);
//		},4000);

	}
	else
	{
		$().toastmessage('showNoticeToast', "Remain Unchanged.");
	}
}


function delUserCall(v,m)
{
	
	
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
