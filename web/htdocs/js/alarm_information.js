 var alarm_status="current"
$(function(){
	text_event();
	current_click();

	check_select();
});


function check_select()
{
	$("#main_chk_box").change(function()
	{	
		if($("#main_chk_box").is(":checked"))
		{
			$(".event_chk").attr('checked', true);
		}
		else
		{
			$(".event_chk").attr('checked', false);
		}
	});
}
function current_click()
{
	var firstTr = "";
	$(".filCmd").click(function() {
		 $(this).parent().children().removeClass("selected");
		 alarm_status = $(this).addClass("selected").attr("id");
		//remove the selected
		//$(this).addClass("selected");
		//alarm_status = alarm_status.split("_");
		//alarm_status = alarm_status[0];
		//console.log("rajendra");
                    $.ajax({
                        type:"POST",
                        url:'alarm_datail_function.py?alarm_status='+alarm_status,
			data:$(this).serialize(), // $(this).text?
                        success:function(result){
                                //console.log(result);
				firstTr = $("#event_body tr:eq(0)").clone();
				$("#event_body").html(result)
				firstTr.prependTo("#event_body");
				check_select();
                            },
                        error:function(req,status,err){   
                        }
                    });
                   
        return false; //always remamber this
                

			
	});
}



function text_event()
{
  document.onkeypress = function(e)
{  

    var e=window.event || e;
    if(e.target.type !='textarea')
     {

//	var alarm_status = $(this).addClass("selected").attr("id");

        var evtKeyCode = e ? e.which : event.keyCode;
 
        if(evtKeyCode == 13)
        {

	var event_id= $("#event_id").val()
	var up_time= $("#up_tym").val()
	var trap_rcv= $("#trap_rcv").val()
	var event_type= $("#eve_typ").val()
	
	var object_type= $("#obj_typ").val()
	var event_dscr= $("#eve_dscr").val()


//		alert(String(e))
//				alert($("form#alarm_info_form").serialize());
	                    $.ajax({
	                        type:"post",
	                       	url:"alarm_datail_function.py?event_id="+event_id+"&up_tym="+up_time+"&trap_rcv="+trap_rcv+"&eve_typ="+event_type+"&obj_typ="+object_type+"&event_dscr="+event_dscr+"&alarm_status="+alarm_status, 
				data:$(this).serialize(), // $(this).text?
	                        success:function(result){
                               //alert(result);
 				firstTr = $("#event_body tr:eq(0)").clone();
				$("#event_body").html(result)
				firstTr.prependTo("#event_body");
                         	check_select();
                            },
                        error:function(req,status,err){   
                        }
                    });
                   
        return false; //always remamber this                   

        }
     }
}

}








