/*
 * 
 * Author			:	Mahipal Choudhary
 * Version			:	0.1
 * Modify Date			:	12-September-2011
 * Purpose			:	Define All Required Javascript Functions
 * Require Library		:	jquery 1.4 or higher version and jquery.validate
 * Browser			:	Mozila FireFox [3.x or higher] and Chrome [all versions]
 * 
 * Copyright (c) 2011 Codescape Consultant Private Limited
 * 
 */

$(document).ready(function() {
	$("div.yo-tabs").yoTabs();
	// page tip [for page tip write this code on each page please dont forget to change "href" value because this link create your help tip page]
	/*$("#page_tip").colorbox(
	{
		href:"#",
		title: "Page Tip",
		opacity: 0.4,
		maxWidth: "80%",
		width:"350px",
		height:"250px"
	});*/
	
	// spin loading object [write this code on each page]
	var spinLoading = $("div#spin_loading");		// create object that hold loading circle
	var spinMainLoading = $("div#main_loading");	// create object that hold loading squire
	$("#edit_user_form").show();
	$("#edit_password_form").hide();

	$("a#personal_information_tab").click(function(e){
		e.preventDefault();
		currentTab = "active";
		$("#edit_user_form").show();
	    $("#edit_password_form").hide();
	});
	
	/* Disable Host Tab*/
	$("a#change_password_tab").click(function(e){
		e.preventDefault();
		currentTab = "active";
		$("#edit_user_form").hide();
	    $("#edit_password_form").show();
	});
	
	
	
	$("#edit_user_form").validate({
		rules:{
			first_name: {
				alpha: true,
				maxlength: 25
			},
			last_name:{
				maxlength: 25,
				alpha: true
			},
			mobile: {
				minlength: 10,
				maxlength: 10,
				positiveNumber: true		
			},
			email_id: {
				email: true
			}
			
		},
		
		messages:{
			
		}
	});
		$("#edit_password_form").validate({
		rules:{
			password: {
				required: true,
				equalTo: "#true_password"
				
			},
			confirm_password_1: {
				required: true,
				minlength: 3
			},
			confirm_password_2: {
				required: true,
				minlength: 3,
				equalTo: "#confirm_password_1"
			}
		},
		messages:{
			password: {
				required: "*",
				minlength: " Your password must be at least 6 characters long",
				equalTo: " Please enter the correct old password"
			},
			
			confirm_password_1: {
				required: "*",
				minlength: " Your password must be at least 6 characters long"
			},
			confirm_password_2: {
				required: "*",
				minlength: " Your password must be at least 6 characters long",
				equalTo: " Please enter the same password as above"
			}
			
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
				cache:false,
				success:function(result)
				{ 
					if(result == 0)
					{
						$().toastmessage('showSuccessToast', "User Details Saved Successfully.");
						//$("#close_edit_user").click();
						
					}
					else if(result.success == 1)
					{
						
						$().toastmessage('showErrorToast', String(result));
					}
				}
			});
		}
		else
		{
			$().toastmessage('showErrorToast', "Some Fileds are Missing or Incorrect.");
		}
		return false;
	});
	
	
	$("#edit_password_form").submit(function(){
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
				cache:false,
				success:function(result)
				{ 
					if(result == 0)
					{
						$().toastmessage('showSuccessToast', "Password Saved Successfully.");
						//$("#close_edit_password").click();
						
					}
					else if(result.success == 1)
					{
						
						$().toastmessage('showErrorToast', "Password couldn't be saved");
					}
				}
			});
		}
		else
		{
			$().toastmessage('showErrorToast', "Some Fileds are Missing or Incorrect.");
		}
		return false;
	});

	$("#close_edit_user").click(function(){
		window.history.go(-1);
	});
	
				
	$("#close_edit_password").click(function(){
		window.history.go(-1);
	});
	// add tool tip
	$tooltipEditPassword = $("form#edit_password_form input[type='password']").tooltip({
		// place tooltip on the right edge
		position: "center right",
		// a little tweaking of the position
		offset: [-2, 10],
		// use the built-in fadeIn/fadeOut effect
		effect: "fade",
		// custom opacity setting
		opacity: 0.7
	});				
	// add tool tip
	$tooltipEditUserDetails = $("form#edit_user_form input[type='text'],form#edit_user_form textarea").tooltip({
		// place tooltip on the right edge
		position: "center right",
		// a little tweaking of the position
		offset: [-2, 10],
		// use the built-in fadeIn/fadeOut effect
		effect: "fade",
		// custom opacity setting
		opacity: 0.7
	});				
});

