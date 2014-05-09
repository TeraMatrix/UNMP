var calendar;
var nonRepeatedEvents = {};
var events = [];
var global_flag_click=false;
var firmware_check=false;
var device_select_list_html="";
function show_scheduling_status()
{
		$.ajax({
			type:"get",
			url:"show_scheduling_status.py",
			cache:false,
			success:function(result){
					//--- imp   //   $("div#notifi_sche_on").html(result);
					//$("div#notifi_sche_on").toggle();
					//$("#calendar").toggle();	
					//$("#back_scheduling_id").toggle();				
						result2 = eval("(" + result + ")");
						if(result2!="" && result2!=null)
						{
						    oTableLog = $('#scheduled_action_status_table').dataTable({
							"bDestroy":true,
							"bJQueryUI": true,
							"bProcessing": true,
							"bStateSave": false,
							"bLengthChange": false,
							"aaData": result2,
							"bPaginate":true,
							"iDisplayLength":25,
						        "bAutoWidth": true,
						         "bFilter": false,
					                "aaSorting": [[ 0, "desc" ]],
							"aoColumns": [
								{ "sTitle": "Time","sClass": "center","sWidth": "25%" },
								{ "sTitle": "Devices" , "sClass": "center","sWidth": "55%"},
								{ "sTitle": "Status" , "sClass": "center","sWidth": "20%"}
							]
						});
					     }
					     else
					     {
					     $('#scheduled_action_status_table').html("<tr></tr><tr><td style=\"text-align:center\">No scheduling records exist.</td></tr>");
					     }
				}
		});

}


function back_scheduling_status()
{
					$("div#notifi_sche_on").toggle();
					$("#calendar").toggle();	
					$("#back_scheduling_id").toggle();	
}



// Numeric only control handler
$.fn.ForceNumericOnly =
function()
{
    return this.each(function()
    {
        $(this).keydown(function(e)
        {
            var key = e.charCode || e.keyCode || 0;
            // allow backspace, tab, delete, arrows, numbers and keypad numbers ONLY
            return (
                key == 8 || 
                key == 9 ||
                key == 46 ||
                (key >= 37 && key <= 40) ||
                (key >= 48 && key <= 57) ||
                (key >= 96 && key <= 105));
        })
    })
};

// disable right click and enter time only
$.fn.TimeOnly =
function()
{
    return this.each(function()
    {
	$(this).bind("contextmenu", function(e) {
		e.preventDefault();
	});
        $(this).keydown(function(e){
		var key = e.charCode || e.keyCode || 0;
            // allow backspace, tab, delete, arrows, numbers, : and keypad numbers ONLY
            return (
                key == 8 || 
                key == 9 ||
                key == 46 ||
                key == 59 ||
                (key >= 37 && key <= 40) ||
                (key >= 48 && key <= 57) ||
                (key >= 96 && key <= 105));
        })
    })
};

function multiselect_device_func()
{
		device_select_list_html=$("#device_select_list").html();
		$("#device_select_list").multiselect({selectedList: 1,multiple:false,noneSelectedText: 'Select Device Type',header:"Available Device Types",minWidth:296});
		
		var sel2=$("#device_select_list").val();
		if(sel2!=null)
			{
				if(sel2=="idu4")
							{
								$("#radioDown_label").html("Admin State Down");
								$("#radioUp_label").html("Admin State Up");
							}
							else
							{
								$("#radioDown_label").html("Radio Down");
								$("#radioUp_label").html("Radio Up");
							}
				$.ajax({ 
				type:"get",
				url:"odu_scheduling_get_device_info.py"+'?device_type='+sel2,
				data:"",
				cache:false,
				success:function(result){ 
					try
					{
						//result=eval("("+result+")");
						$("#multi_select_list_inner_div").html(result);
						$("#multi_select_list_inner_div").css("display","block");
						multiSelectAccessPoint("odu");
					}	
					catch(err)
					{
						//alert(err);
						result = [];
					}
				 }
				});
			}
		$("#device_select_list").bind("multiselectclick", function(event, ui){
			var sel=$("#device_select_list").val();
					if(ui.value=="idu4")
							{
								$("#radioDown_label").html("Admin State Down");
								$("#radioUp_label").html("Admin State Up");
							}
							else
							{
								$("#radioDown_label").html("Radio Down");
								$("#radioUp_label").html("Radio Up");
							}
			if(sel!=null && sel!=ui.value)
			{
				$.ajax({ 
				type:"get",
				url:"odu_scheduling_get_device_info.py"+'?device_type='+ui.value,
				data:"",
				cache:false,
				success:function(result){ 
					try
					{
						//result=eval("("+result+")");
						$("#multi_select_list_inner_div").html(result);
						$("#multi_select_list_inner_div").css("display","block");
						multiSelectAccessPoint("odu");
					}	
					catch(err)
					{
						//alert(err);
						result = [];
					}
				 }
				});
			}
		});


		/*$("#device_select_list").bind("multiselectclose", function(event, ui){
			var sel=$("#device_select_list").val();
			if(sel!=null)
			{
				$.ajax({ 
				type:"get",
				url:"odu_scheduling_get_device_info.py"+'?device_type='+sel,
				data:"",
				cache:false,
				success:function(result){ 
					try
					{
						//result=eval("("+result+")");
						$("#multi_select_list_inner_div").html(result);
						$("#multi_select_list_inner_div").css("display","block");
						multiSelectAccessPoint("odu");
					}	
					catch(err)
					{
						//alert(err);
						result = [];
					}
				 }
				});

			}	
			});*/
			
}

// disable all keys and right click
$.fn.DisableKeyAndRightClick =
function()
{
    return this.each(function()
    {
	$(this).bind("contextmenu", function(e) {
		e.preventDefault();
	});
        $(this).keydown(function(e){
		return false;
        })
    })
};

function MyEvents(start,end, callback) {
  events = [];
  $.each(nonRepeatedEvents.events,function(i,ev)
  {
	events.push(ev);
  });
  $.ajax({
 	type:"post",
	url:"load_repeative_events_odu.py",
	success:function(result){
		result = eval("(" + result + ")");
		//alert(result);
		$.each(result.daily,function(i,rs){
			stime = String(rs.start).split(":");
			etime = String(rs.end).split(":");
  			// Setup the event
			var startEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						stime[0],stime[1],stime[2]);
			var endEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						etime[0],etime[1],etime[2]);
			while (startEvent <= end) {
			    events.push({
			      id: rs.id,
			      title: rs.title,
			      start: new Date(startEvent.valueOf()),
			      end: new Date(endEvent.valueOf()),
			      allDay: false
			    });
			    // increase by one Day
			    startEvent.setDate(startEvent.getDate() + 1);
			    endEvent.setDate(endEvent.getDate() + 1);
			}

		});
		$.each(result.weekly,function(i,rs){
			stime = String(rs.start).split(":");
			etime = String(rs.end).split(":");
  			// Setup the event
			var startEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						stime[0],stime[1],stime[2]);
			var endEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						etime[0],etime[1],etime[2]);
			if(rs.sun == 1)
			{
				startEvent.setDate((startEvent.getDate() - startEvent.getDay()) + 0);
				endEvent.setDate((endEvent.getDate() - endEvent.getDay()) + 0);
				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setDate(startEvent.getDate() + 7);
				    endEvent.setDate(endEvent.getDate() + 7);
				}
			}
  			// Setup the event
			startEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						stime[0],stime[1],stime[2]);
			endEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						etime[0],etime[1],etime[2]);
			if(rs.mon == 1)
			{
				startEvent.setDate((startEvent.getDate() - startEvent.getDay()) + 1);
				endEvent.setDate((endEvent.getDate() - endEvent.getDay()) + 1);
				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setDate(startEvent.getDate() + 7);
				    endEvent.setDate(endEvent.getDate() + 7);
				}
			}
			// Setup the event
			startEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						stime[0],stime[1],stime[2]);
			endEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						etime[0],etime[1],etime[2]);
			if(rs.tue == 1)
			{
				startEvent.setDate((startEvent.getDate() - startEvent.getDay()) + 2);
				endEvent.setDate((endEvent.getDate() - endEvent.getDay()) + 2);
				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setDate(startEvent.getDate() + 7);
				    endEvent.setDate(endEvent.getDate() + 7);
				}
			}
			// Setup the event
			startEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						stime[0],stime[1],stime[2]);
			endEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						etime[0],etime[1],etime[2]);
			if(rs.wed == 1)
			{
				startEvent.setDate((startEvent.getDate() - startEvent.getDay()) + 3);
				endEvent.setDate((endEvent.getDate() - endEvent.getDay()) + 3);
				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setDate(startEvent.getDate() + 7);
				    endEvent.setDate(endEvent.getDate() + 7);
				}
			}
			// Setup the event
			startEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						stime[0],stime[1],stime[2]);
			endEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						etime[0],etime[1],etime[2]);
			if(rs.thu == 1)
			{
				startEvent.setDate((startEvent.getDate() - startEvent.getDay()) + 4);
				endEvent.setDate((endEvent.getDate() - endEvent.getDay()) + 4);
				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setDate(startEvent.getDate() + 7);
				    endEvent.setDate(endEvent.getDate() + 7);
				}
			}
			// Setup the event
			startEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						stime[0],stime[1],stime[2]);
			endEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						etime[0],etime[1],etime[2]);
			if(rs.fri == 1)
			{
				startEvent.setDate((startEvent.getDate() - startEvent.getDay()) + 5);
				endEvent.setDate((endEvent.getDate() - endEvent.getDay()) + 5);
				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setDate(startEvent.getDate() + 7);
				    endEvent.setDate(endEvent.getDate() + 7);
				}
			}
			// Setup the event
			startEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						stime[0],stime[1],stime[2]);
			endEvent = new Date(start.getFullYear(),
						start.getMonth(),
						start.getDate(),
						etime[0],etime[1],etime[2]);
			if(rs.sat == 1)
			{
				startEvent.setDate((startEvent.getDate() - startEvent.getDay()) + 6);
				endEvent.setDate((endEvent.getDate() - endEvent.getDay()) + 6);
				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setDate(startEvent.getDate() + 7);
				    endEvent.setDate(endEvent.getDate() + 7);
				}
			}
		});
		$.each(result.monthly,function(i,rs){
			stime = String(rs.start).split(":");
			etime = String(rs.end).split(":");
  			// Setup the event
			if(rs.jan == 1)
			{
				var startEvent = new Date(start.getFullYear(),
							0,
							rs.date,
							stime[0],stime[1],stime[2]);
				var endEvent = new Date(start.getFullYear(),
							0,
							rs.date,
							etime[0],etime[1],etime[2]);

				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setMonth(startEvent.getMonth() + 12);
				    endEvent.setMonth(endEvent.getMonth() + 12);
				}
			}
			if(rs.feb == 1)
			{
				var startEvent = new Date(start.getFullYear(),
							1,
							rs.date,
							stime[0],stime[1],stime[2]);
				var endEvent = new Date(start.getFullYear(),
							1,
							rs.date,
							etime[0],etime[1],etime[2]);

				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setMonth(startEvent.getMonth() + 12);
				    endEvent.setMonth(endEvent.getMonth() + 12);
				}
			}
			if(rs.mar == 1)
			{
				var startEvent = new Date(start.getFullYear(),
							2,
							rs.date,
							stime[0],stime[1],stime[2]);
				var endEvent = new Date(start.getFullYear(),
							2,
							rs.date,
							etime[0],etime[1],etime[2]);

				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setMonth(startEvent.getMonth() + 12);
				    endEvent.setMonth(endEvent.getMonth() + 12);
				}
			}
			if(rs.apr == 1)
			{
				var startEvent = new Date(start.getFullYear(),
							3,
							rs.date,
							stime[0],stime[1],stime[2]);
				var endEvent = new Date(start.getFullYear(),
							3,
							rs.date,
							etime[0],etime[1],etime[2]);

				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setMonth(startEvent.getMonth() + 12);
				    endEvent.setMonth(endEvent.getMonth() + 12);
				}
			}
			if(rs.may == 1)
			{
				var startEvent = new Date(start.getFullYear(),
							4,
							rs.date,
							stime[0],stime[1],stime[2]);
				var endEvent = new Date(start.getFullYear(),
							4,
							rs.date,
							etime[0],etime[1],etime[2]);

				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setMonth(startEvent.getMonth() + 12);
				    endEvent.setMonth(endEvent.getMonth() + 12);
				}
			}
			if(rs.jun == 1)
			{
				var startEvent = new Date(start.getFullYear(),
							5,
							rs.date,
							stime[0],stime[1],stime[2]);
				var endEvent = new Date(start.getFullYear(),
							5,
							rs.date,
							etime[0],etime[1],etime[2]);

				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setMonth(startEvent.getMonth() + 12);
				    endEvent.setMonth(endEvent.getMonth() + 12);
				}
			}
			if(rs.jul == 1)
			{
				var startEvent = new Date(start.getFullYear(),
							6,
							rs.date,
							stime[0],stime[1],stime[2]);
				var endEvent = new Date(start.getFullYear(),
							6,
							rs.date,
							etime[0],etime[1],etime[2]);

				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setMonth(startEvent.getMonth() + 12);
				    endEvent.setMonth(endEvent.getMonth() + 12);
				}
			}
			if(rs.aug == 1)
			{
				var startEvent = new Date(start.getFullYear(),
							7,
							rs.date,
							stime[0],stime[1],stime[2]);
				var endEvent = new Date(start.getFullYear(),
							7,
							rs.date,
							etime[0],etime[1],etime[2]);

				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setMonth(startEvent.getMonth() + 12);
				    endEvent.setMonth(endEvent.getMonth() + 12);
				}
			}
			if(rs.sep == 1)
			{
				var startEvent = new Date(start.getFullYear(),
							8,
							rs.date,
							stime[0],stime[1],stime[2]);
				var endEvent = new Date(start.getFullYear(),
							8,
							rs.date,
							etime[0],etime[1],etime[2]);

				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setMonth(startEvent.getMonth() + 12);
				    endEvent.setMonth(endEvent.getMonth() + 12);
				}
			}
			if(rs.oct == 1)
			{
				var startEvent = new Date(start.getFullYear(),
							9,
							rs.date,
							stime[0],stime[1],stime[2]);
				var endEvent = new Date(start.getFullYear(),
							9,
							rs.date,
							etime[0],etime[1],etime[2]);

				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setMonth(startEvent.getMonth() + 12);
				    endEvent.setMonth(endEvent.getMonth() + 12);
				}
			}
			if(rs.nov == 1)
			{
				var startEvent = new Date(start.getFullYear(),
							10,
							rs.date,
							stime[0],stime[1],stime[2]);
				var endEvent = new Date(start.getFullYear(),
							10,
							rs.date,
							etime[0],etime[1],etime[2]);

				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setMonth(startEvent.getMonth() + 12);
				    endEvent.setMonth(endEvent.getMonth() + 12);
				}
			}
			if(rs.dec == 1)
			{
				var startEvent = new Date(start.getFullYear(),
							11,
							rs.date,
							stime[0],stime[1],stime[2]);
				var endEvent = new Date(start.getFullYear(),
							11,
							rs.date,
							etime[0],etime[1],etime[2]);

				while (startEvent <= end) {
				    events.push({
				      id: rs.id,
				      title: rs.title,
				      start: new Date(startEvent.valueOf()),
				      end: new Date(endEvent.valueOf()),
				      allDay: false
				    });
				    // increase by one week
				    startEvent.setMonth(startEvent.getMonth() + 12);
				    endEvent.setMonth(endEvent.getMonth() + 12);
				}
			}
		});
	  callback(events);
	}
   });
}
function MyCalendar()
{
$.ajax({
		type:"post",
		url:"load_non_repeative_events_odu.py",
		success:function(result){
			nonRepeatedEvents = eval("(" + result + ")");
			events = nonRepeatedEvents.events;
			$('#calendar').html("");
			calendar = $('#calendar').fullCalendar({
				header: {
					left: 'prev,next today',
					center: 'title',
					right: 'month,agendaWeek,agendaDay'
				},
				selectable: true,
				selectHelper: true,
				select: function(start, end, allDay, jsEvent, view) {
					$(".day, .month").attr("checked",false);
					$("#repeatType option:eq(0)").attr("selected",true);
					$("div[id='multiSelectListodu']").find("div.selected").find("img").click();

					if(allDay == true)
					{
						end.setDate(end.getDate() + 1);
					}
					//Weekly
					if(start.getDay() == 0)
						$("#daysun").attr("checked",true);
					if(start.getDay() == 1)
						$("#daymon").attr("checked",true);
					if(start.getDay() == 2)
						$("#daytue").attr("checked",true);
					if(start.getDay() == 3)
						$("#daywed").attr("checked",true);
					if(start.getDay() == 4)
						$("#daythu").attr("checked",true);
					if(start.getDay() == 5)
						$("#dayfri").attr("checked",true);
					if(start.getDay() == 6)
						$("#daysat").attr("checked",true);

					// Monthly
					if(start.getMonth() == 0)
						$("#monthjan").attr("checked",true);
					if(start.getMonth() == 1)
						$("#monthfeb").attr("checked",true);
					if(start.getMonth() == 2)
						$("#monthmar").attr("checked",true);
					if(start.getMonth() == 3)
						$("#monthapr").attr("checked",true);
					if(start.getMonth() == 4)
						$("#monthmay").attr("checked",true);
					if(start.getMonth() == 5)
						$("#monthjun").attr("checked",true);
					if(start.getMonth() == 6)
						$("#monthjul").attr("checked",true);
					if(start.getMonth() == 7)
						$("#monthaug").attr("checked",true);
					if(start.getMonth() == 8)
						$("#monthsep").attr("checked",true);
					if(start.getMonth() == 9)
						$("#monthoct").attr("checked",true);
					if(start.getMonth() == 10)
						$("#monthnov").attr("checked",true);
					if(start.getMonth() == 11)
						$("#monthdec").attr("checked",true);

					$("#dates").val(start.getDate());
					$("#cEvent").show().css("top",(jsEvent.pageY-150)).css("left",jsEvent.pageX);
					$("#dEvent").hide();
					$("#startDate").val((start.getDate()<10?("0" + start.getDate()):start.getDate()) + "/" + ((start.getMonth()<9)?("0" + (start.getMonth() + 1)):(start.getMonth() + 1)) + "/" + start.getFullYear());
					$("#endDate").val((end.getDate()<10?("0" + end.getDate()):end.getDate()) + "/" + ((end.getMonth()<9)?("0" + (end.getMonth() + 1)):(end.getMonth() + 1)) + "/" + end.getFullYear());
					$("#startTime").val((start.getHours()<10?("0" + start.getHours()):start.getHours()) + ":" + (start.getMinutes()<10?("0" + start.getMinutes()):(start.getMinutes())));
					$("#endTime").val((end.getHours()<10?("0" + end.getHours()):end.getHours()) + ":" + (end.getMinutes()<10?("0" + end.getMinutes()):(end.getMinutes())));

					$("input[name='repeat']").attr("checked",false);
					$("#trRepeatType, #trDay, #trDate, #trMonth").hide();
					$("#startDate, #endDate").show();
					//calendar.fullCalendar('unselect');
				},
				editable: true,
				events: MyEvents,
				dayClick: function(date, allDay, jsEvent, view) {
					
				    },
				eventClick: function(calEvent, jsEvent, view) {
					$("input[name='scheduleId']").val(calEvent.id);
					//alert('Coordinates: ' + jsEvent.pageX + ',' + jsEvent.pageY);
					//alert('View: ' + view.name);
					// change the border color just for fun
					jsEvent.stopPropagation()
					$("#dEvent").show().css("top",(jsEvent.pageY-150)).css("left",jsEvent.pageX);
					$("#cEvent").hide();
					//$(this).css('border-color', 'red');
				    },
				unselect: function(view, jsEvent){
					$("#cEvent").hide();
					$("#dEvent").hide();
					},
				unselectCancel: ".calender-pop-up",
				allDaySlot:false,
				height:1100,
				defaultView:"agendaWeek",
				eventResize: function(event,dayDelta,minuteDelta,revertFunc) {
					$.ajax({
						type:"post",
						url:"event_resize_odu.py?id=" + event.id + "&day=" + dayDelta + "&minute=" + minuteDelta,
						success:function(result){//alert(result);
							if(result != "0")
							{
								revertFunc();
								//alert("Some Error Occur, Please Try Again.");
								$().toastmessage('showErrorToast', "some error occured");
							}
						}
					});
				    },
				eventDrop: function(event,dayDelta,minuteDelta,allDay,revertFunc) {
					$.ajax({
						type:"post",
						url:"event_drop_odu.py?id=" + event.id + "&day=" + dayDelta + "&minute=" + minuteDelta,
						success:function(result){//alert(result);
							if(result != "0")
							{
								revertFunc();
								//alert("Some Error Occur, Please Try Again.");
								$().toastmessage('showErrorToast', "You Can't Schedule before the current time");
							}
						}
					});
				    }
			});
		}
	});
}
$(document).ready(function() {
	MyCalendar();
	multiselect_device_func();
	multiSelectAccessPoint("odu");
	show_scheduling_status();

	$("input[name='repeat']").click(function(){
		if(this.checked)
		{
			$("#startDate").hide();
			$("#endDate").hide();
			$("#trRepeatType").show();
			$("#repeatType").change();
		}
		else
		{
			$("#trRepeatType, #trDay, #trDate, #trMonth").hide();
			$("#startDate, #endDate").show();
		}
	});
	$("input[name='radio']").click(function(){
		check_count();
	});
	$("#repeatType").change(function(){
		if($("#repeatType").val() == "Daily")
		{
			$("#trDay, #trDate, #trMonth").hide();
		}
		else if($("#repeatType").val() == "Weekly")
		{
			$("#trDate, #trMonth").hide();
			$("#trDay").show();
		}
		else if($("#repeatType").val() == "Monthly")
		{
			$("#trDate, #trMonth").show();
			$("#trDay").hide();
		}
	});
	$('a[rel*=facebox]').facebox({
		loadingImage : 'facebox/loading.gif',
		closeImage   : 'facebox/closelabel.png'
	});
	$("#showAP").click(function(){
		$.facebox({ ajax: "view_access_point_list_odu.py?scheduleId=" + $("input[name='scheduleId']").val() });
		$("#dEvent").hide();
	});
	$(document).click(function(){
		$("#dEvent").hide();
	});
	$('#startDate, #startTime, #endDate,  #endTime').calendricalDateTimeRange({
		isoTime:true
	});
	$('#startDate,  #endDate').DisableKeyAndRightClick();
	$('#startTime,  #endTime').TimeOnly();
	
	
	$("#page_tip").colorbox(  			//page tip
	    {
		href:"view_page_tip_scheduling.py",
		title: "Page Tip",
		opacity: 0.4,
		maxWidth: "80%",
		width:"600px",
		height:"400px"
	    });
	    
	$("#select_file").toggle(function () {
                selectFirmwareTable();
        },function(){ 
                $("#firmware_table_div").slideUp(); 
        });
        $("input[name='upload_new_file']").click(function(){
                //uploadFile();
                FirmwareUpdate();
        });    

});
function optionSelected(obj)
{
        var $obj = $(obj);
        if($obj.attr("checked"))
        {
                $("#selected_firmware").val($obj.attr("id"));
        }
}

function selectFirmwareTable()
{
    //var device_type = $("input[name='selected_device']").val();
    var device_type = $("#device_select_list").val();
    /*$.ajax({
		type:"get",
		url:"select_firmware_table.py?device_type=" + device_type,
		success:function(result){
		       $("#firmware_table_div").html(result); 
		       $("#firmware_table_div").slideDown();    
		       $("input[name='firmware_file']").click(function(){
	                        optionSelected(this);
	                });    
		}    
        });
        */
        
        $.colorbox(
	{
		href:"select_firmware_table.py?device_type=" + device_type,
		//iframe:true,
		title : "Select File",
		opacity: 0.4,
		maxWidth: "80%",
		width:"400px",
		height:"350px",
		onComplete:function(){  
					$("input[name='firmware_file']").click(function(){
			                optionSelected(this);
		                  	});
		                  },
		overlayClose:false
	});
}


function uploadFile()
{
        //var device_type = $("input[name='selected_device']").val();
        var device_type = $("#device_select_list").val();
        //var host_id = $("input[name='host_id']").val();
        var host_id=$("input[id='hdodu']").val();
	$.colorbox(
	{
		href:"update_firmware_view.py?host_id="+host_id+"&device_type="+device_type,
		iframe:true,
		title : "Upload File",
		opacity: 0.4,
		maxWidth: "80%",
		width:"400px",
		height:"250px",
		onClosed:function(){var device_type = $("input[name='selected_device']").val();
                                    $.ajax({
		                                type:"get",
		                                url:"select_firmware_table.py?device_type=" + device_type,
		                                success:function(result){
		                                       $("#firmware_table_div").html(result);   
		                                }    
                                        });
		                  },
		overlayClose:false
	});
}



function FirmwareUpdate()
{
       firmware_check=true;
	$.colorbox(
	{
		href:"device_firmware_view.py",
		iframe:true,
		title: "Select Firmware Image",
		opacity: 0.4,
		maxWidth: "80%",
		width:"400px", 
		height:"350px", 
		//onClosed:function(){alert($("#mahipal").html());},
		overlayClose:false
	});

	//alert([host_id,device_type,device_state]);
}
function createEvent()
{
	$("#scheduling_button_div").hide();
	$("#dateError").hide();
	$("#eventForm").show();
	$("#calendar").hide();
	$("#cEvent").hide();
	$("#dEvent").hide();
	$("#device_select_list").html(device_select_list_html);
	$("#device_select_list").multiselect("refresh");
	$("#device_select_list").multiselect("enable");
	$("#multi_select_list_inner_div").css("display","block");
	multiselect_device_func();
}
function eventSubmit()
{
	startDate = $("#startDate").val().split("/");
	startTime = $("#startTime").val().split(":");
	endDate = $("#endDate").val().split("/");
	endTime = $("#endTime").val().split(":");
	var sDateObj;
	var eDateObj;

	if (startDate.length == 3 && endDate.length == 3 && startTime.length == 2 && endTime.length == 2)
	{	
		now = new Date();
		sDateObj = new Date(startDate[2],parseInt(startDate[1])-1,startDate[0],startTime[0],startTime[1],0);
		eDateObj = new Date(endDate[2],parseInt(endDate[1])-1,endDate[0],endTime[0],endTime[1],0);
		if((sDateObj.getTime() < now.getTime() || eDateObj.getTime() < now.getTime()) && ( sDateObj.getDate()<now.getDate() || eDateObj.getDate()<now.getDate()))
		{
			//alert("");
				$().toastmessage('showErrorToast', "Date Should be Today or Greater then Today");
		}
		else if(sDateObj.getTime()< eDateObj.getTime())
		{
			$("#dateError").hide();
			// start
			if($("input[id='hdodu']").val() == "")
			{
				//alert("Please select at least one UBR ");
				$().toastmessage('showErrorToast', "Please select at least one Device");
			}
			else if(($("#selected_firmware").val() == "") && $('input[name="radio"]').filter("[value='Firmware']").attr('checked'))
			{
				$().toastmessage('showErrorToast', "Please select the image file for firmware");
			}
			else
			{
				if($("input[name='repeat']").attr("checked"))
				{
					if($("#repeatType").val() == "Weekly")
					{
						if($("#trDay").find("input:checked").size() == 0)
						{
							//alert("Please Select at least one day");
							$().toastmessage('showErrorToast', "Please select at least one day");
						}
						else
						{
							addSchedule();
						}
					}
					else if($("#repeatType").val() == "Monthly")
					{
						if($("#trMonth").find("input:checked").size() == 0)
						{
							//alert("Please Select at least one month");
							$().toastmessage('showErrorToast', "Please select at least one month");
						}
						else
						{
							addSchedule();
						}
					}
					else if($("#repeatType").val() == "Daily")
					{
						addSchedule();
					}
				}
				else
				{
					addSchedule();
				}
			}
			// end
		}
		else
		{
			$("#dateError").show();
		}
	}
	else
	{
		$("#dateError").show();
	}
}
function addSchedule()
{
	$.ajax({
		type:"post",
		url:"add_odu_scheduler.py?" +$("#schedulingForm").serialize(),
		async:false,
		success:function(result){
			//alert(result);
			if(result != "-1")
			{
				$("#eventForm").hide();
				$("#calendar").show();
				$("#scheduling_button_div").show();
				if(!$("input[name='repeat']").attr("checked"))
				{
					var sDate = $("#startDate").val().split("/");
					var eDate = $("#endDate").val().split("/");
					var sTime = $("#startTime").val().split(":");
					var eTime = $("#endTime").val().split(":");
					var start = new Date(sDate[2],(parseInt(sDate[1]) - 1),sDate[0],sTime[0],sTime[1]);
					var end = new Date(eDate[2],(parseInt(eDate[1]) - 1),eDate[0],eTime[0],eTime[1]);
					calendar.fullCalendar('renderEvent',
						{
							id: result,
							title: $("input[name='radio']:checked").val(),
							start: start,
							end: end,
							allDay:false
						},
						true // make the event "stick"
					);
				}
				else
				{
					MyCalendar();
				}
			}
			else
			{
				//alert("");
				$().toastmessage('showErrorToast', "MycalSome Error occured, Please Try Again.");
			}
		}
	});
}
function eventCancel()
{
	$("#eventForm").hide();
	$("#calendar").show();
	$("#scheduling_button_div").show();
	$("input[id='submitEve']").show();
	$("input[id='updateEve']").hide();
	$("#show_scheduling_id").show();
	$("#device_select_list").multiselect("refresh");
}
function deleteSchedule()
{
	$.ajax({
		type:"post",
		url:"delete_odu_scheduler.py?scheduleId=" + $("input[name='scheduleId']").val(),
		success:function(result){
			if(result == "0")
			{
				MyCalendar();
			}
			else
			{
				//alert("");
				$().toastmessage('showErrorToast', "Schedule Does not Deleted. Please try again");
			}
			$("#dEvent").hide();
		}
	});
}
function editSchedule()
{
	$("#dateError").hide();
	$.ajax({
		type:"post",
		url:"get_odu_schedule_details.py?scheduleId=" + $("input[name='scheduleId']").val(),
		success:function(result){
				result = eval("(" + result + ")");
				$("#multi_select_list_inner_div").html(result.html_list);	
				$("#multi_select_list_inner_div").css("display","block");
				multiSelectAccessPoint("odu");
				if(result.aplist == undefined)
					$("input[name='hdTempodu']").val("")
				else
					$("input[name='hdTempodu']").val(result.aplist)
				$("#device_select_list").html('<option selected value="'+result.device_type_id+'">'+result.device_type_name+"</option>");
				//alert($("#device_select_list").html());
				$("#device_select_list").multiselect("refresh");
				$("#device_select_list").multiselect("disable");
				// Weekly
				// sunday
				if(result.sun == 1)
					$("#daysun").attr("checked",true);
				else
					$("#daysun").attr("checked",false);
				// monday
				if(result.mon == 1)
					$("#daymon").attr("checked",true);
				else
					$("#daymon").attr("checked",false);
				// tuesday
				if(result.tue == 1)
					$("#daytue").attr("checked",true);
				else
					$("#daytue").attr("checked",false);
				// wednusday
				if(result.wed == 1)
					$("#daywed").attr("checked",true);
				else
					$("#daywed").attr("checked",false);
				// thursday
				if(result.thu == 1)
					$("#daythu").attr("checked",true);
				else
					$("#daythu").attr("checked",false);
				// friday
				if(result.fri == 1)
					$("#dayfri").attr("checked",true);
				else
					$("#dayfri").attr("checked",false);
				// saturday
				if(result.sat == 1)
					$("#daysat").attr("checked",true);
				else
					$("#daysat").attr("checked",false);

				// Monthly
				if(result.jan == 1)
					$("#monthjan").attr("checked",true);
				else
					$("#monthjan").attr("checked",false);
				if(result.feb == 1)
					$("#monthfeb").attr("checked",true);
				else
					$("#monthfeb").attr("checked",false);
				if(result.mar == 1)
					$("#monthmar").attr("checked",true);
				else
					$("#monthmar").attr("checked",false);
				if(result.apr == 1)
					$("#monthapr").attr("checked",true);
				else
					$("#monthapr").attr("checked",false);
				if(result.may == 1)
					$("#monthmay").attr("checked",true);
				else
					$("#monthmay").attr("checked",false);
				if(result.jun == 1)
					$("#monthjun").attr("checked",true);
				else
					$("#monthjun").attr("checked",false);
				if(result.jul == 1)
					$("#monthjul").attr("checked",true);
				else
					$("#monthjul").attr("checked",false);
				if(result.aug == 1)
					$("#monthaug").attr("checked",true);
				else
					$("#monthaug").attr("checked",false);
				if(result.sep == 1)
					$("#monthsep").attr("checked",true);
				else
					$("#monthsep").attr("checked",false);
				if(result.oct == 1)
					$("#monthoct").attr("checked",true);
				else
					$("#monthoct").attr("checked",false);
				if(result.nov == 1)
					$("#monthnov").attr("checked",true);
				else
					$("#monthnov").attr("checked",false);
				if(result.dece == 1)
					$("#monthdec").attr("checked",true);
				else
					$("#monthdec").attr("checked",false);

				$("#dates").val(result.dates);
				$("#repeatType option[value='" + result.repeattype + "']").attr("selected",true).change();

				if(result.isrepeat == 1)
				{
					$("#repeat").attr("checked",true);
					$("#startDate").hide();
					$("#endDate").hide();
					$("#trRepeatType").show();
					$("#repeatType").change();
				}
				else
				{
					$("#trRepeatType, #trDay, #trDate, #trMonth").hide();
					$("#startDate, #endDate").show();
					$("#repeat").attr("checked",false);
				}

				$("#endTime").val(result.endtime.substring(0,result.endtime.lastIndexOf(":")));
				$("#startTime").val(result.starttime.substring(0,result.starttime.lastIndexOf(":")));
				endDateTemp = String(result.enddate).split("-");
				$("#endDate").val(endDateTemp[2]+"/"+endDateTemp[1]+"/"+endDateTemp[0]);
				startDateTemp = String(result.startdate).split("-");
				$("#startDate").val(startDateTemp[2]+"/"+startDateTemp[1]+"/"+startDateTemp[0]);
				if(result.event == "Up")
					$("#radioUp").attr("checked",true);
				else 
				    if(result.event == "Down")
					$("#radioDown").attr("checked",true);
				    else
				         $("#radioFirmware").attr("checked",true);
				         $("#selected_firmware").val(result.firmware_file);

				$("#scheduleId").val(result.scheduleid);
				$("#dEvent").hide();
				$("#eventForm").show();
				$("#calendar").hide();
				$("#scheduling_button_div").hide();
				$("#show_scheduling_id").hide();
				$("input[id='submitEve']").hide();
				$("input[id='updateEve']").show();
				$("div[id='multiSelectListodu']").find("div.selected").find("img").click();
				var accessPointArray = $("input[name='hdTempodu']").val().split(",");
				for(k=0;k<accessPointArray.length; k++)
				{
					$("div[id='multiSelectListodu']").find("img[id='" + $.trim(accessPointArray[k])+"']").click();
				}
		}
	});
}

function eventUpdate()
{
	startDate = $("#startDate").val().split("/");
	startTime = $("#startTime").val().split(":");
	endDate = $("#endDate").val().split("/");
	endTime = $("#endTime").val().split(":");
	var sDateObj;
	var eDateObj;

	if (startDate.length == 3 && endDate.length == 3 && startTime.length == 2 && endTime.length == 2)
	{
		now = new Date();
		sDateObj = new Date(startDate[2],parseInt(startDate[1])-1,startDate[0],startTime[0],startTime[1],0);
		eDateObj = new Date(endDate[2],parseInt(endDate[1])-1,endDate[0],endTime[0],endTime[1],0);
		if(sDateObj.getTime() < now.getTime() || eDateObj.getTime() < now.getTime())
		{
		
			//alert("");
			$().toastmessage('showErrorToast', "Date Should be Today or Greater then Today");
		}
		else if(sDateObj.getTime()< eDateObj.getTime())
		{
			$("#dateError").hide();
			// start
			if($("input[id='hdodu']").val() == "")
			{
				//alert("");
				$().toastmessage('showErrorToast', "Please select at least one Device");
			}
			else
			{
				if($("input[name='repeat']").attr("checked"))
				{
					if($("#repeatType").val() == "Weekly")
					{
						if($("#trDay").find("input:checked").size() == 0)
						{
							//alert("");
							$().toastmessage('showErrorToast', "Please Select at least one day");
						}
						else
						{
							updateSchedule();
						}
					}
					else if($("#repeatType").val() == "Monthly")
					{
						if($("#trMonth").find("input:checked").size() == 0)
						{
							alert("Please Select at least one month");
						}
						else
						{
							updateSchedule();
						}
					}
					else if($("#repeatType").val() == "Daily")
					{
						updateSchedule();
					}
				}
				else
				{
					updateSchedule();
				}
			}
			// end
		}
		else
		{
			$("#dateError").show();
		}
	}
	else
	{
		$("#dateError").show();
	}
}
function updateSchedule()
{
	$.ajax({
		type:"post",
		url:"update_odu_scheduler.py?" +$("#schedulingForm").serialize(),
		success:function(result){
			//alert(result);
			if(result != "-1")
			{
				MyCalendar();
			}
			else
			{
				//alert("");
				$().toastmessage('showErrorToast', "UpdSome Error occured, Please Try Again.");
			}
		}
	});
	eventCancel()
}
/*============================= Multiple Selecter For Host Parent =========================*/
function multiSelectAccessPoint(accessPoint)
{
	$(".plus"+accessPoint).click(function(){
		plusHostParentOption(accessPoint,this);
	})
	$(".minus"+accessPoint).click(function(){
		minusHostParentOption(accessPoint,this);
	})
	var hostParentArray = [];
	var tempHostParent=$("input[name='hdTemp" + accessPoint + "']").val();
	if(tempHostParent!=undefined)
	{
	   hostParentArray=tempHostParent.split(",");
	}
	for(k=0;k<hostParentArray.length; k++)
	{
		$("div[id='multiSelectList" + accessPoint + "']").find("img[id='" + $.trim(hostParentArray[k])+"']").click();
	}
	$("#rm"+accessPoint).click(function(e){
		e.preventDefault();
		$("div[id='multiSelectList" + accessPoint + "']").find("div.selected").find("img").click();
	})
	$("#add"+accessPoint).click(function(e){
		e.preventDefault();
		$("div[id='multiSelectList" + accessPoint + "']").find("div.nonSelected").find("img").click();
	})
}
function minusHostParentOption(accessPoint, Obj)
{
	liObj = $("<li/>");
	imgObj = $("<img/>");
	liObj.append($(Obj).attr("name"));
	imgObj.attr("src","images/add16.png").attr("class","plus plus" + accessPoint + "").attr("alt","+").attr("id",$(Obj).attr("id")).attr("name",$(Obj).attr("name")).click(function(){
		plusHostParentOption(accessPoint,this)
	})
	liObj.append(imgObj);
	$(Obj).parent().parent().parent().parent().find("div.nonSelected").find("ul").append(liObj);
	$(Obj).parent().parent().parent().parent().find("input[name='hd" + accessPoint + "']").val("");
	j = 0
	for(i=0;i<$(Obj).parent().parent().find("li").size();i++)
	{
		var addedHostParent = $(Obj).parent().parent().find("li").eq(i).find("img").attr("id");
		if( addedHostParent != $(Obj).attr("id"))
		{
			if(j == 0)
			{
				$(Obj).parent().parent().parent().parent().find("input[name='hd" + accessPoint + "']").val($.trim(addedHostParent));
			}
			else
			{
				$(Obj).parent().parent().parent().parent().find("input[name='hd" + accessPoint + "']").val($(Obj).parent().parent().parent().parent().find("input[name='hd" + accessPoint + "']").val() + "," + $.trim(addedHostParent));
			}
			j++;
		}
	}
	$(Obj).parent().parent().parent().parent().find("span#count").html(j)
	$(Obj).parent().remove();
	check_count();
}
function plusHostParentOption(accessPoint, Obj)
{
	var countParent = 0;
	liObj = $("<li/>");
	imgObj = $("<img/>");
	liObj.append($(Obj).attr("name"));
	imgObj.attr("src","images/minus16.png").attr("class","minus minus" + accessPoint).attr("alt","-").attr("id",$(Obj).attr("id")).attr("name",$(Obj).attr("name")).click(function(){
		minusHostParentOption(accessPoint,this)
	})
	liObj.append(imgObj);
	$(Obj).parent().parent().parent().parent().find("div.selected").find("ul").append(liObj);
        hdval = $(Obj).parent().parent().parent().parent().find("input[name='hd" + accessPoint + "']").val()
	if($.trim(hdval) == "")
	{
		$(Obj).parent().parent().parent().parent().find("input[name='hd" + accessPoint + "']").val($(Obj).attr("id"))
	}
	else
	{
		$(Obj).parent().parent().parent().parent().find("input[name='hd" + accessPoint + "']").val(hdval + "," +$(Obj).attr("id"))
	}
	countParent = $(Obj).parent().parent().parent().parent().find("span#count").html();
	$(Obj).parent().parent().parent().parent().find("span#count").html(parseInt(countParent) + 1);
	$(Obj).parent().remove();
	check_count();
}

function check_count()
{
	var host_id=$("input[id='hdodu']").val();
	var event_type=$("input[name='radio']:checked").val();
	if(host_id!="" && event_type=="Firmware")
		{
			$("#firmware_update_div_label").show();
			$("#firmware_update_div_value").show();
			$("#firmware_div_complete").show();
		}
		else
		{
			$("#firmware_update_div_label").hide();
		    	$("#firmware_update_div_value").hide();
		    	$("#firmware_div_complete").hide();
		}
}
/*============================= End Multiple Selecter For Access point =========================*/
