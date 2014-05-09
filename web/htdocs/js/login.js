
$(function(){
	// Loading - Spin Object
	var spinLoading = $("div#spin_loading");		// create object that hold loading circle
	var spinMainLoading = $("div#main_loading");	// create object that hold loading squire
	var loginBox = $("#login_box");
	var doc = $(document);
	var pageHeight = doc.height();
	var pageWidth = doc.width();
	var loginBoxHeight = loginBox.height();
	var loginBoxWidth = loginBox.width();
	var loginBoxPositionTop = String(((pageHeight/2) - (loginBoxHeight/2))*100/pageHeight) + "%";
	var loginBoxPositionLeft = String(((pageWidth/2) - (loginBoxWidth/2))*100/pageWidth) + "%";
	// spin loading object
	//loginBox.css({"top":loginBoxPositionTop,"left":loginBoxPositionLeft});
	$("input[name='username']").focus();
	$('body').addClass('login_body');
	$("#login_form").submit(function(){
		var formObj = $(this);
		if($(this).valid())
		{
			spinStart(spinLoading,spinMainLoading);
				$.ajax({
					type:formObj.attr("method"),
					url:formObj.attr("action"),
					data:formObj.serialize(),
					cache:false,
					success:function(result){
						try
						{
							jsonResult = eval("(" + result + ")");
							if(jsonResult.success == 0)
							{
								spinStop(spinLoading,spinMainLoading);
								//parent.side.location = jsonResult.result[0];
								window.location.reload();
							}
							else 
								if(jsonResult.success == 2)
								{
									spinStop(spinLoading,spinMainLoading);
									$.prompt('This account seems to be logged in from some other location too.You will be logged out from all the other sessions.',{ buttons:{Ok:true}, prefix:'jqismooth',callback:sessionUser });
								}
								else
								{	spinStop(spinLoading,spinMainLoading);
									$().toastmessage('showErrorToast', jsonResult.result);
									//spinStop(spinLoading,spinMainLoading);
								}
							}
						catch(error)
						{
							spinStop(spinLoading,spinMainLoading);
							$().toastmessage('showErrorToast', "Please Enter Valid Username and Password ");
							//$().toastmessage('showErrorToast', result);
							//spinStop(spinLoading,spinMainLoading);
						}	
					}
				});
			}

		else
		{
			$().toastmessage('showErrorToast', "Please Enter Username and Password.");
		}
		return false;		
	});
	$("#login_form").validate({
		rules:{
			username:{
				required:true
			},
			password:{
				required:true
			}
		},
		messages:{
			username:{
				required:" "
			},
			password:{
				required:" "
			}
		}//,	window.location.reload()
		//errorElement:"div"
	});
	// add tool tip
	 /*$("#login_form input[type='text'],input[type='password']").tooltip({
		// place tooltip on the right edge
		position: "center right",
		// a little tweaking of the position
		offset: [-2, 10],
		// use the built-in fadeIn/fadeOut effect
		effect: "fade",
		// custom opacity setting
		opacity: 0.7
	});*/
	setTimeout(function()
	{
		if(tactical_call != null)
		{
			clearTimeout(tactical_call);
		}
	},25000);
});

function sessionUser(v,m)
{

	$().toastmessage('showSuccessToast', "Successfully logged in!!");
	//$("#login_form").submit();
	window.location.reload();

}
