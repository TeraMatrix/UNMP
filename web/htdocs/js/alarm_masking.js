var $spinLoading = null;
var $spinMainLoading = null;
var deleteId=null;
$(function(){
	$spinLoading = $("div#spin_loading");		// create object that hold loading circle
	$spinMainLoading = $("div#main_loading");	// create object that hold loading squire
	dataTable();
	addAlarmForm();
	$.validator.addMethod('positiveNumber', function (value,element) { 
			return Number(value) > -1;
	}, ' Enter a positive number');

	$("#page_tip").colorbox(
	{
	href:"page_tip_alarm_masking.py",
	title: "Page Tip",
	opacity: 0.4,
	maxWidth: "80%",
	width:"450px",
	height:"350px",
	onComplte:function(){}
	});
	});
function addEditForm(masking_id,option)
{
		  spinStart($spinLoading,$spinMainLoading);
                    $.ajax({
                        type:"get",
                        url:"add_edit_masking_table_form.py?masking_id=" + masking_id + "&option=" + option,
			data:$(this).serialize(), // $(this).text?
			cache:false,
                        success:function(result){
				try
				{
					result=eval("("+result+")");
			   	}catch(err)
				{
					$().toastmessage('showErrorToast', 'Some unknown error occured,so please contact your Administrator');
					spinStop($spinLoading,$spinMainLoading);
					return;
				}
				if (result.success==1 || result.success=="1")
				{
					$().toastmessage('showErrorToast', 'Some system error occured, so please contact your Administrator');
					spinStop($spinLoading,$spinMainLoading);
					return	;
				}
				else if (result.success==2 || result.success=='2')
				{
					$().toastmessage('showErrorToast', 'Some database error occured,so please contact your Administrator');
					spinStop($spinLoading,$spinMainLoading);
					return;
				}

    				else
				{

					$("#demo_id").hide();
					$("#alarm_editable_div").html(result.html_form);
					$("#header").hide();
					$("#alarm_editable_div").show();
					spinStop($spinLoading,$spinMainLoading);
					if (option=="ADD")
					{			
					formSubmit(masking_id,option);
					}
					else
					{
					editFormSubmit(masking_id,option);
					}
					formCancel();
					maskingValidation();
				
			}	
                      },
                        error:function(req,status,err){   
                        }
                    });
        return false; //always remamber this	
}

function addAlarmForm()
{
	$("#add_masking").click(function(){
	addEditForm("","ADD");	
	
	});

}
function checkDeleteAlarm(event_uuid){
	deleteId=event_uuid;
	$.prompt('Are you sure want to delete this Alarm ?',{ buttons:{Ok:true,Cancel:false}, prefix:'jqismooth',callback:deleteAlarm});	
}


function deleteAlarm(v,m)
{
	if(v != undefined && v==true && deleteId)
	 {
	  spinStart($spinLoading,$spinMainLoading);
	    $.ajax({
                type:"get",
                url:"delete_masking_field.py?masking_id=" + deleteId,
		//data:$(this).serialize(), // $(this).text?
		cache:false,
                success:function(result){
		if (result != "")
		{	 
			try
			{
				result=eval("("+result+")");
		   	}catch(err)
			{
				$().toastmessage('showErrorToast', 'Some unknown error occured,so please contact your Administrator');
				spinStop($spinLoading,$spinMainLoading);
				return;
			}
				if (result.success==1 || result.success=="1")
				{
					$().toastmessage('showErrorToast', 'Some system error occured, so please contact your Administrator');
					spinStop($spinLoading,$spinMainLoading);
					return	;
				}
				else if (result.success==2 || result.success=="2")
				{
					$().toastmessage('showErrorToast', 'Some database error occured,so please contact your Administrator');
					spinStop($spinLoading,$spinMainLoading);
					return	;
				}

				else
				{

		 				$("#demo_id").show();
						$("#alarm_editable_div").hide();
						$("#demo_id").html("<table cellspacing=\"0\" cellpadding=\"0\" border=\"0\" id=\"example\" class=\"display\"></table>");
						spinStop($spinLoading,$spinMainLoading);
						dataTable();
				  }
		}
		else
		{
				$().toastmessage('showSuccessToast', "Event is successfully deleted.");
 				$("#demo_id").show();
				$("#alarm_editable_div").hide();
				$("#demo_id").html("<table cellspacing=\"0\" cellpadding=\"0\" border=\"0\" id=\"example\" class=\"display\"></table>");
				spinStop($spinLoading,$spinMainLoading);
				dataTable();

		}	
               },
                error:function(req,status,err){   
                }
            });
        return false; //always remamber this	
	}
	else
		{
		return false;
		}
}

function editAlarm(masking_id)
{
	addEditForm(masking_id,"Edit");
	
}

function formCancel()
{
	$("#cancel_button").click(function() {
		$("#header").show();
		$("#alarm_editable_div").hide();
		$("#demo_id").show();
	});
}

function formSubmit(masking_id,option)
{
	$("#masking_form").submit(function (){
		if($(this).valid())
		{
		spinStart($spinLoading,$spinMainLoading);
                    $.ajax({
                        type:"get",
                        url:"add_form_entry2.py",
			data:$(this).serialize(), // $(this).text?
			cache:false,
                        success:function(result){
				try
				{
					result=eval("("+result+")");
			   	}catch(err)
				{
					$().toastmessage('showErrorToast', 'Some database error occured,so please contact your Administrator');
					spinStop($spinLoading,$spinMainLoading);
					return;
				}
					if (result.success==1 || result.success=="1")
					{
						$().toastmessage('showErrorToast', 'Some system error occured, so please contact your Administrator');
						spinStop($spinLoading,$spinMainLoading);
						return	;
					}
					else if (result.success==2 || result.success=='2')
					{
						$().toastmessage('showErrorToast', 'Some database error occured,so please contact your Administrator');
						spinStop($spinLoading,$spinMainLoading);
						return;
					}

					else if (result.success==3 || result.success=='3')
					{
						$().toastmessage('showErrorToast', 'This event field and event value already exists for this group.');
						spinStop($spinLoading,$spinMainLoading);
						return;
					}
					else
					{

					$().toastmessage('showSuccessToast', "Event is successfully Added.");
					$("#demo_id").show();
					$("#alarm_editable_div").hide();
					$("#demo_id").html("<table cellspacing=\"0\" cellpadding=\"0\" border=\"0\" id=\"example\" class=\"display\"></table>");
					spinStop($spinLoading,$spinMainLoading);
					dataTable();
					}
                            },
                        error:function(req,status,err){   
                        }
                     });
		  }
                   
        return false; //always remamber this                   

	});
}

function maskingValidation()
{	
	$("#masking_form").validate({
	rules:{
		'trap_alarm_field':  { required:true
				     },
		'trap_alarm_value':  {
					required:true	},
		'actionid':	     {
					required:true    },
		'acknowledgeid':     {
					required:true	},
		'groupid':           {
					required:true	},
		'desc_id':           {
					required:true	},
		'schedule_time':     {
					positiveNumber: true
							}
		
		},
		messages:{
			
		'trap_alarm_field':{
					required: "please choose the any trap field."	},
		'trap_alarm_value':{
					required:"please enter the value according to trap field."},
		'actionid':{
					required: "please choose the action name."	},
		'acknowledgeid':{
					required: "please choose the acknowledge name."	},
		'groupid':{
					required: "please choose the group name."	},
		'desc_id':{
					required: "please give the description."	},

		'schedule_time':{
				
					positiveNumber:"It must be positive number"}

				}

		
	})
}
function dataTable()
{
	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"get",
		url:"alarm_masking_information.py",
		cache:false,
		success:function(result){
			$("#header").show();
				 try
				 {
				result=eval("("+result+")");
			   	}catch(err)
				{
					$().toastmessage('showErrorToast', 'Some database error occured,so please contact your Administrator');
					spinStop($spinLoading,$spinMainLoading);
					return;
				}
				if (result.success==1 || result.success=="1")
				{
					$().toastmessage('showErrorToast', 'Some system error occured, so please contact your Administrator');
					spinStop($spinLoading,$spinMainLoading);
					return	;
				}
				else if (result.success==2 || result.success=='2')
				{
					$().toastmessage('showErrorToast', 'Some database error occured,so please contact your Administrator');
					spinStop($spinLoading,$spinMainLoading);
					return;
				}
    				else
				{
					table_result=eval(result.event_table)

					$('#example').dataTable({
					        "bJQueryUI": true,
					        "bDestroy":true,
						"sPaginationType": "full_numbers",
						"aaData": table_result,
						"aoColumns": [
								{ "sTitle": "Event Fields","sClass": "center","sWidth": "10%" },
								{ "sTitle": "Event Value" , "sClass": "center","sWidth": "10%"},
								{ "sTitle": "Action Name","sClass": "center","sWidth": "10%" },
								{ "sTitle": "Group Name", "sClass": "center","sWidth": "10%" },
								{ "sTitle": "Scheduling (min)", "sClass": "center","sWidth": "10%" },
								{ "sTitle": "Is Repeated", "sClass": "center","sWidth": "10%" },
								{ "sTitle": "Acknowledge Status", "sClass": "center","sWidth": "15%" },
								{ "sTitle": " ", "sClass": "center","sWidth": "5%"  },
								{ "sTitle": " ","sWidth": "5%" ,
								"fnRender": function(obj) {
											var sReturn = obj.aData[ obj.iDataColumn ];
											if ( sReturn == "A" ) {
												sReturn = "<b>A</b>";
											}
											return sReturn;
									}

								}
							]
					});
					spinStop($spinLoading,$spinMainLoading);
				}
			},
		error:function(req,status,err){}
	  });
}

function editFormSubmit(masking_id,option)
{
	$("#masking_form").submit(function (){
		if($(this).valid())
		{
		spinStart($spinLoading,$spinMainLoading);
                    $.ajax({ 
                        type:"get",
                        url:"edit_masking_form_entry.py?" + $(this).serialize() +"&masking_id="+masking_id,
			cache:false,
                        success:function(result){
				 try
				 {
				result=eval("("+result+")");
			   	}catch(err)
				{
					$().toastmessage('showErrorToast', 'Some database error occured,so please contact your Administrator');
					spinStop($spinLoading,$spinMainLoading);
					return;
				}
				if (result.success==1 || result.success=="1")
				{
					$().toastmessage('showErrorToast', 'Some system error occured, so please contact your Administrator');
					spinStop($spinLoading,$spinMainLoading);
					return	;
				}
				else if (result.success==2 || result.success=='2')
				{
					$().toastmessage('showErrorToast', 'Some database error occured,so please contact your Administrator');
					spinStop($spinLoading,$spinMainLoading);
					return;
				}

				else if (result.success==3 || result.success=='3')
				{
					$().toastmessage('showErrorToast', 'This event field and event value Already exists for this group.');
					spinStop($spinLoading,$spinMainLoading);
					return;
				}
				else
				{
					$().toastmessage('showSuccessToast', "Event is successfully Edited.");
					$("#demo_id").show();
					$("#alarm_editable_div").hide();
					$("#demo_id").html("<table cellspacing=\"0\" cellpadding=\"0\" border=\"0\" id=\"example\" class=\"display\"></table>");
					spinStop($spinLoading,$spinMainLoading);
					dataTable();
					formCancel();
				}
                            },
                        error:function(req,status,err){   
                        }
                    });
		}                   
        return false; //always remamber this                   
	});

}


