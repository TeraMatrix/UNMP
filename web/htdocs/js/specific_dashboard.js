// new
var $spinLoading = null;
var $spinMainLoading = null;
var spIpAddress='';
var spMainObj=null;
var deviceTypeId='';
var graph_type=1;
var limitFlag=1;
var spRecursionVar=null;
var refresh_time=60000; // default time for refreshing the hidden datatime value.
var spE1MainObj=null;
var linkObj=null;
var spEndDate='';
var spEndTime='';
var totalSelectedGraph="";
$(function(){
	$spinLoading = $("div#spin_loading");		// create object that hold loading circle
	$spinMainLoading = $("div#main_loading");	// create object that hold loading squire

	$("input[id='current_rept_div']").attr("checked","checked");
	refresh_time=$("#sp_refresh_time").val();
	deviceTypeId=$("select[id='device_type']").val();
	$("#device_type").change(function(){
		$("#filter_ip").val("");
		$("#filter_mac").val("");		
			});
	$('#sp_start_date, #sp_start_time, #sp_end_date,  #sp_end_time').calendricalDateTimeRange({
		isoTime:true
	    });
	$("input[id='filter_ip']").keypress(function(){
		$("input[id='filter_mac']").val("");
		
	})
        $("input[id='btnSearch']").click(function(){
	//call the device list function on click of search button
		deviceList();
	})
        
	$("input[id='filter_ip']").ccplAutoComplete("common_ip_mac_search.py?device_type="+deviceTypeId+"&ip_mac_search="+1,{
            dataType: 'json',
            max: 30,
            selectedItem: $("input[id='filter_ip']").val(),
                callAfterSelect : function(obj){
                        ipSelectMacDeviceType(obj,1);
                }
        });
        
   $("input[id='filter_mac']").ccplAutoComplete("common_ip_mac_search.py?device_type="+deviceTypeId+"&ip_mac_search="+0,{
            dataType: 'json',
            max: 30,
            selectedItem: $("input[id='filter_mac']").val(),
            callAfterSelect : function(obj){
                    ipSelectMacDeviceType(obj,0);
            }
    });

	$("input[id='filter_ip']").val($("input[id='filter_ip']").val());	
	$("select[id='device_type']").val($("input[id='device_type']").val());
	$("select[id='device_type']").val(deviceTypeId);


        $("#hide_search").toggle(function(){
		var $this = $(this);
		var $span = $this.find("span").eq(0);
		$span.removeClass("up");
		$span.addClass("dwn");
		$("#filterOptions").hide();
		$this.css({
		        'background-color': "#F1F1F1",
                        'display': "block",
                        'height': '20px',
                        'position': 'static',
                        'overflow': 'hidden',
                        'width': "100%"});
	},
	function(){
		var $this = $(this);
		var $span = $this.find("span").eq(0);
		$span.removeClass("dwn");
		$span.addClass("up");
		$("#filterOptions").show();
		$this.css({
		        'background-color': "#F1F1F1",
                        'display': "block",
                        'height': '20px',
                        'overflow': 'hidden',
                        'position': 'relative',
			'border-bottom':'1px solid #AAA',
                        'right': 1,
                        'top': 1,
                        'width': "100%",
                        'z-index': 1000});
		
	});
//	$("#more_graph").toggle($('#more_graph_columns').attr('disabled',''),$('#more_graph_columns').attr('disabled',''));
	//deviceList();
	spIpAddress=$("input#filter_ip").val();
	//oduGraphButtonClick();
	//graphInitiator();   // calling the function for graph showing

	$("#page_tip").colorbox(
	{
	href:"page_tip_sp_monitor_dashboard.py",
	title: "Dashboard",
	opacity: 0.4,
	maxWidth: "80%",
	width:"650px",
	height:"500px",
	onComplte:function(){}
	})

	$('#sp_host_info_div').slideUp('fast');
	// Slide up and slide down functionality starthere  
 	$("#tab_yo").slideUp('fast');
	$("#sp_show_graph_list").toggle(
				function(){
				$('#tab_yo').slideDown('slow', function() {
				$("#sp_show_graph_list").val('Dashboard Configuration')
				  });
					},
			function(){
				$('#tab_yo').slideUp('slow', function() {
				$("#sp_show_graph_list").val('Dashboard Configuration')
				  });
				});
	$("#sp_ad_graph").click(function(){
		parent.main.location="get_ap_advanced_graph_value.py?ip_address='"+String(spIpAddress)+"'&device_type_id="+deviceTypeId;
	});

	// Slide up and slide down functionality end here
	// This function bring the all graph information
//	spUpdateDateTime();
	specificGenericGraphJson();
});


function hostInformation(){
	$('#sp_host_info_div').animate({
			    left: '+=50',
			    height: 'toggle'
			  }, 1000, function()
			  {
			  	var $hostInfo = $("#host_info");
				if ($hostInfo.attr('src')=="images/new_icons/round_plus.png")
				{
					$hostInfo.attr('src',"images/new_icons/round_minus.png");
					$hostInfo.attr('original-title','Hide Status')
//					$("#host_info").html("original-title='Hide Status'");
				}
				else
				{
					$hostInfo.attr('src',"images/new_icons/round_plus.png");
					$hostInfo.attr('original-title','Show Status')
				}
               }
             );
}

/*function toggle_options()
{
//		if(flag_more_options==false)
//		{
//		return;
//		}	
		if($("div#more_graph_columns").css("display")=="block")
		{
		 $("#more_graph_span").html("Expand");
		  
		}
		else
		{
		  $("#more_graph_span").html("Collapse");
		}
		
	  $("div#more_graph_columns").toggle();
}
*/




/*
// This function used for auto suggest search box.
function HostIPSearch(){
	var selected='';
	var selectedText='';
    $("#filter_ip").fcbkcomplete({
        isID:'fb_host',
        json_url: "show_ip_list.py",
        width:'150px',
        addontab: false,                   
        maxitems: 10,
	maxshownitems:10,
	input_min_size:1,
        height: 10,
        cache: true,
        newel: false,
        filter_selected:true
//        onselect: function(){
//				$("#host_search option:selected").each(function() {
				        //allHost.push($(this).val());
//				        selected=$(this).val();
//					selectedText=$(this).text();
//				     });
//					addSingleHost(selected,selectedText);
//				}

    });
}*/

function specificGenericGraphJson(){
	$.ajax({
		type:"post",
		url:"sp_generic_json.py?device_type_id="+deviceTypeId+"&ip_address="+spIpAddress,
		data:$(this).serialize(), // $(this).text?
		cache:false,
		success:function(result){
				var e1PortJsonDict={'graphs':[]};
				var linkJosnDict={'graphs':[]};
				
				if (result.success==0){
/*					var table_name='';
					for (node in result.graphs){
						table_name=String(result.graphs[node].ajax.data.table_name).split(",")[0];
						if (table_name=="idu_e1PortStatusTable")
						{
							var temp_dic=result.graphs[node];
							delete result.graphs[node];
							result.graphs.shift();
							e1PortJsonDict['graphs'][0]=temp_dic;
							//alert(JSON.stringify(e1PortJsonDict));
			               	e1PortJsonDict.graphColumn=2;       
							e1PortJsonDict.otherData=[{name:'start_date',value:function() { return $('input#sp_start_date').val();}},{name:'start_time',value:function() { return $('input#sp_start_time').val();}},{name:'end_date',value:function() { return $('input#sp_end_date').val();}},{name:'end_time',value:function() { return $('input#sp_end_time').val();}},{name:'flag',value:function() { return limitFlag; }},{name:'ip_address',value:function() { return spIpAddress; }},{name:'graph_type',value:function() { return graph_type; }}];
							spE1MainObj=$("#sp_e1_graph").yoAllGenericDashboard(e1PortJsonDict);
						}				
						else if(table_name=="idu_linkStatisticsTable")
						{
							var temp_dic=result.graphs[node];
							delete result.graphs[node];
							result.graphs.shift();
							linkJosnDict['graphs'][0]=temp_dic;
							//alert(JSON.stringify(e1PortJsonDict));
			               	linkJosnDict.graphColumn=2;       
							linkJosnDict.otherData=[{name:'start_date',value:function() { return $('input#sp_start_date').val();}},{name:'start_time',value:function() { return $('input#sp_start_time').val();}},{name:'end_date',value:function() { return $('input#sp_end_date').val();}},{name:'end_time',value:function() { return $('input#sp_end_time').val();}},{name:'flag',value:function() { return limitFlag; }},{name:'ip_address',value:function() { return spIpAddress; }},{name:'graph_type',value:function() { return graph_type; }}];
							linkObj=$("#sp_e1_graph").yoAllGenericDashboard(e1PortJsonDict);
						}
					}*/
				   result.otherData=[{name:'start_date',value:function() { return $('input#sp_start_date').val();}},{name:'start_time',value:function() { return $('input#sp_start_time').val();}},{name:'end_date',value:function() { return $('input#sp_end_date').val();}},{name:'end_time',value:function() { return $('input#sp_end_time').val();}},{name:'flag',value:function() { return limitFlag; }},{name:'ip_address',value:function() { return spIpAddress; }},{name:'graph_type',value:function() { return graph_type; }}];
					spAddDateTime();
	               	result.graphColumn=2;        
					spUpdateDateTime(); // update date time in text box
					$("#sp_main_graph").html("");
					spMainObj=$("#sp_main_graph").yoAllGenericDashboard(result);
					// $("#main_graph").html("");
//					apDeviceDetail();
//					updateDateTime();
					trapAlarmInformation('alarm');
				}
				else{
					$().toastmessage('showErrorToast',result.error_msg);
				}
		}
	});  
}


function disbaledReportButton()
{
	$("#sp_pdf_report").addClass("disabled");
	$("#sp_pdf_report").attr("disabled",true);
	$("#sp_excel_report").addClass("disabled");
	$("#sp_excel_report").attr("disabled",true);
	$("#sp_csv_report").addClass("disabled");
	$("#sp_csv_report").attr("disabled",true);
	$("#sp_ad_graph").addClass("disabled");
	$("#sp_ad_graph").attr("disabled",true);
	$("#sp_show_graph_list").addClass("disabled");
	$("#sp_show_graph_list").attr("disabled",true);
}

function enabledReportButton()
{
	$("#sp_pdf_report").removeClass("disabled");
	$("#sp_pdf_report").attr("disabled",false);
	$("#sp_excel_report").removeClass("disabled");
	$("#sp_excel_report").attr("disabled",false);
	$("#sp_csv_report").removeClass("disabled");
	$("#sp_csv_report").attr("disabled",false);
	$("#sp_ad_graph").removeClass("disabled");
	$("#sp_ad_graph").attr("disabled",false);
	$("#sp_show_graph_list").removeClass("disabled");
	$("#sp_show_graph_list").attr("disabled",false);
 	$("#tab_yo").slideUp('fast');

}


function deviceList()
{
	//var deviceTypeId = "ap25";
	// this retreive the value of ipaddress textbox
	var ip_address = $("input[id='filter_ip']").val();
	// this retreive the value of macaddress textbox
	var mac_address = $("input[id='filter_mac']").val();
	// this retreive the value of selectdevicetype from select menu
	var selected_device_type = $("select[id='device_type']").val();
	var selectListElem=$("#device_type option:selected").text();
	deviceTypeId=selected_device_type;

	if (selectListElem=="" || selectListElem==undefined)
		selectListElem=""
	// this ajax return the call to function get_device_data_table which is in odu_view and pass the ipaddress,macaddress,devicetype with url  
	if (selected_device_type=='odu16' || selected_device_type=='odu100')
		redirectPath='odu_listing.py';
	else if (selected_device_type=='ap25')
		redirectPath='ap_listing.py';
	else if (selected_device_type=='idu4')
		redirectPath='idu_listing.py';
	else
		redirectPath='odu_listing.py';
	apIpAddress=ip_address
	deviceTypeId=$("select[id='device_type']").val();
	//spinStop($spinLoading,$spinMainLoading);
		//	}
		//});
	

	$.ajax({
		type:"post",
		url:"get_device_list_ap_for_monitoring.py?&ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type,
		cache:false,
		success:function(result){
					$("#header3_text").html(selectListElem+" "+apIpAddress+" Dashboard");
					if (result == 0 || result == "0")
					{
						redirectOnListing(redirectPath);
                         //clearTimeout(tempObj);
//						 $("#sp_show_msg").html("No Data exist for this device.")
						 $("#adSrhap").hide(); // hide the button
						 $("#tab_yo").hide();
						 $("#event_table").hide();
						 $("#alarm_table").hide();
						 $("#main_host_info_div").hide();
						 $("#sp_main_graph").html("");
						disbaledReportButton();

					}
					else if (result==1 || result=="1")
					{
						parent.main.location = redirectPath+"?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type;
						
					}
					else if (result == 2 || result == "2")
					{
						redirectOnListing(redirectPath);
//						 $("#sp_show_msg").html("Please Try Again.")
						 $("#adSrhap").hide(); // hide the button
						 $("#tab_yo").hide();
						 $("#event_table").hide();
						 $("#alarm_table").hide();
						 //$("#ap_device_graph").hide();
						 $("#main_host_info_div").hide();
						 $("#sp_main_graph").html("");
						disbaledReportButton();


					}
					else 
				 	{	
						$("#sp_show_msg").html("")
					//	$("#adSrhap").show(); // show the button
						$("#tab_yo").show();
						$("input#filter_ip").val(result);
						spIpAddress=result;
						//$("#ap_device_graph").show();
						 $("#event_table").show();
						 $("#alarm_table").show();
						$("#main_host_info_div").show();
						$("#sp_main_graph").html("");
						spDeviceDetail();
						specificGenericGraphJson();
						enabledReportButton();						
					}
				}
		});
		
}



function ipSelectMacDeviceType(obj,ipMacVal)
{
    selectedVal = $(obj).val();
    $.ajax({
        type:"get",
        url:"get_ip_mac_selected_device.py?selected_val="+selectedVal+"&ip_mac_val="+ipMacVal,
        success:function(result){
            if(parseInt(result.success)==0)
            {
                    if(ipMacVal==1)
                    {
                            $("input[id='filter_mac']").val(String(result.mac_address).toUpperCase());
                            $("select[id='device_type']").val(result.selected_device);
                    }
                    else
                    {
                            $("input[id='filter_ip']").val(result.ip_address);
                            $("select[id='device_type']").val(result.selected_device);
                    }
		    deviceList();
            }
            else
            {
                 $().toastmessage('showErrorToast',result.error);   
            }
        }
   });
}


function redirectOnListing(redirctPath){
		 $().toastmessage('showWarningToast',"Searched Device Doesn't Exist");
		setTimeout(function(){
		parent.main.location = redirectPath+"?ip_address=" + "" + "&mac_address=" + "" + "&selected_device_type=" + "";							
		},1500);
}


function spDeviceDetail()
{
	spinStart($spinLoading,$spinMainLoading);
	$.ajax({
		type:"post",
		url:"sp_device_details.py?ip_address="+spIpAddress+"&device_type_id="+deviceTypeId,
		data:$(this).serialize(),
		cache:false,
		success:function(result){
					if (result.success>=1 || result.success>="1")
					{
						$().toastmessage('showErrorToast',result.error_msg);
					}
					else
					{
						$("#sp_host_info_div").html(result.device_table);	
					}
			},		
		error:function(req,status,err){
		}
	});
	spinStop($spinLoading,$spinMainLoading);
}


// Update the date time in text Box
function advancedUpdateDateTime(){
    $.ajax({
        type:"post",
        url:"advanced_update_date_time.py?device_type_id="+deviceTypeId,
		data:$(this).serialize(), // $(this).text?
		cache:false,
	    success:function(result){
			if (result.success==1 || result.success=="1")
			{
				$().toastmessage('showWarningToast', "Date time not receving in proper format.");
				return	;
			}
			else
			{
				$("#sp_end_date").val(result.end_date);
				$("#sp_end_time'").val(result.end_time);
			}
        }
	});
   return false;	
}


// This function update date and time
function spAddDateTime(){
    $.ajax({
        type:"post",
        url:"sp_add_date_time_on_slide.py?device_type_id="+deviceTypeId+"&ip_address="+spIpAddress,
		cache:false,
	    success:function(result){
			if (result.success==1 || result.success=="1")
			{
				$().toastmessage('showWarningToast', "Date time not receving in proper format.");
			}
			else
			{
				$("#more_graph_columns").html(result.show_graph_table);
				totalSelectedGraph=$("#sp").val();
				$("#sp_start_date").val(result.start_date);
				$("#sp_end_date").val(result.end_date);
				$("#sp_start_time").val(result.start_time);
				$("#sp_end_time").val(result.end_time);
				multiSelectColumns();				
			}
    	}
	});
   return false; //always remamber this	
}




function spUpdateDateTime(){
	if(spRecursionVar!=null)
	{	
		clearInterval(spRecursionVar);
	}
	spDeviceDetail();
	spAddDateTime();
	trapAlarmInformation();
	spRecursionVar=setInterval(function (){spAddDateTime();},refresh_time*60000);
}



function trapAlarmInformation()
		{
		//console.log(divObj);
		$.ajax({
			type:"post",
			url:"sp_event_alarm_information.py?ip_address="+spIpAddress,
			data:$(this).serialize(),
			cache:false,
			success:function(result){
					if (result.success>=1 || result.success>="1")
					{
						$().toastmessage('showErrorToast',result.error_msg);
					}
					else
					{
						//$("#alarm_dashboard").html(result.alarm_table);
						$("#event_dashboard").html(result.event_table);
						

					}
				},
				error:function(req,status,err){
			}
		});
}


// This is function create the Excel Report
function spExcelReportGeneration(){
	spCommonReportCreating('sp_excel_report_genrating.py','UBR_excel.xls');
}
// This is create the PDF Report.
function spPDFReportGeneration(){
	spCommonReportCreating('sp_pdf_report_genrating.py','UBR_PDF_Report.pdf');
}

// This is create the CSV Report.
function spCSVReportGeneration(){
	spCommonReportCreating('sp_csv_report_genrating.py','UBR_CSV_Report.csv');
}


function spCommonReportCreating(redirectPath,file_name){
	/*if (totalSelectedGraph==""){
		$().toastmessage('showWarningToast', "Please select atleast one graph from dashboard configuration.");
		return false;
	}*/
	graph_json={};
	var field=[];
	var cal_type=null;
	var graph=null;
	var tab_option=null;
	var totalGraph = 0;
	var graphQuerySrting = "";
	var ajaxData={};
	var start_date=$("#sp_start_date").val();
	var start_time=$("#sp_start_time").val();
	var end_date=$("#sp_end_date").val();
	var end_time=$("#sp_end_time").val();
	//var subObj=spMainObj.options.db;
	
	for (node in spMainObj.options.db)
	{
		totalGraph+=1;
		field=[];
		//alert(spMainObj.options.db[node]["options"].calType[0].name);
		var tempFileds = spMainObj.options.db[node]["options"].fields;
		for (var i=0;i<tempFileds.length;i++ )
			{
				if (tempFileds[i].isChecked==1)
				{
					field[field.length]=tempFileds[i].name;
				}
			}

		calculationType= spMainObj.options.db[node]["options"].calType;
		for (var j=0;j<calculationType.length;j++ )
			{
				if (calculationType[j].isChecked==1)
				{
					cal_type=calculationType[j].name;
				}
			}
		graphType= spMainObj.options.db[node]["options"].type;
		for (var j=0;j<graphType.length;j++ )
			{
				if (graphType[j].isChecked==1)
				{
					graph=graphType[j].value;
				}
			}

		tab_option = spMainObj.options.db[node]["options"].tabList.selected;
		ajaxData=spMainObj.options.db[node]["options"].ajax.data['table_name'];
		
		graphQuerySrting+= "&start"+String(totalGraph)+"="+spMainObj.options.db[node]["options"].startFrom;
		graphQuerySrting+= "&limit"+String(totalGraph)+"="+spMainObj.options.db[node]["options"].itemLimit;

		graphQuerySrting+= "&table_name" + String(totalGraph) + "=" + ajaxData;
		graphQuerySrting+= "&type"+String(totalGraph)+"="+graph;
		
		graphQuerySrting+= "&field"+String(totalGraph)+"="+field;
		graphQuerySrting+= "&cal"+String(totalGraph)+"="+cal_type;
		graphQuerySrting+= "&tab"+String(totalGraph)+"="+tab_option;
		graphQuerySrting+= "&graph_name"+String(totalGraph)+"="+spMainObj.options.db[node]["options"].displayName;
	}
	graphQuerySrting+= "&total_graph=" + String(totalGraph)
	var select_option=$("input[name='option']:checked").val();
		if (select_option==0){
//				endDateStr=spEndDate.split("/");
//				endTimeStr=spEndTime.split(":");
//				var cdate = new Date(endDateStr[2],parseInt(endDateStr[1])-1, endDateStr[0],endTimeStr[0],endTimeStr[1]); 

/*			var cur_date=new Date();
			var d=cur_date.getDate();
			var y=cur_date.getFullYear();
			var m=cur_date.getMonth();
			var h = cur_date.getHours();
			var mi = cur_date.getMinutes();
			var cdate=new Date(y,m,d,h,mi);
*/
/*				var str1  = $("#sp_start_date").val();
				var str2  = $("#sp_end_date").val();
				var str3  = $("#sp_start_time").val();
				var str4  = $("#sp_end_time").val();
				str1=str1.split("/");
				str2=str2.split("/");
				str3=str3.split(":");
				str4=str4.split(":");
*/
//				alert(String(cdate));
//				alert(String(date1));
//				alert(String(date2));

/*				var date1 = new Date(str1[2],parseInt(str1[1])-1, str1[0],str3[0],str3[1]); 
				var date2 = new Date(str2[2],parseInt(str2[1])-1, str2[0],str4[0],str4[1]);
				if(date2 < date1)
				{
					 $().toastmessage('showWarningToast', "End Date can't be greater than Start Date");
				}
				else if(cdate<date1 || cdate<date2)
					{

					 	$().toastmessage('showWarningToast', "Dates can't be greater than current Date");
					}
				else 
					{*/
				    spinStart($spinLoading,$spinMainLoading);
				    $.ajax({
					type:"post",
					url:"advanced_update_date_time.py?device_type_id="+deviceTypeId,
						data:$(this).serialize(), // $(this).text?
						cache:false,
					    	success:function(result){
							if (result.success==1 || result.success=="1")
							{
								$().toastmessage('showWarningToast', "Date time not receving in proper format.");
								return	;
							}
							else
							{
								$.ajax({
									type:"post",
									url:redirectPath+"?ip_address="+spIpAddress+"&start_date="+start_date+"&start_time="+start_time+"&end_date="+result.end_date+"&end_time="+result.end_time+"&device_type_id="+deviceTypeId+"&select_option="+select_option+"&limitFlag="+limitFlag+graphQuerySrting,
									data:$(this).serialize(),
									cache:false,
									success:function(result){
											if (result.success>=1 || result.success>="1")
											{
												$().toastmessage('showErrorToast', result.error_msg);
											}
											else
											{
												$().toastmessage('showSuccessToast', 'Report Generated Successfully');
												window.location = "download/"+result.file_name;

											}
												spinStop($spinLoading,$spinMainLoading);

										}
								});  
								}
							}
							});
			}
			else
			{
					spinStart($spinLoading,$spinMainLoading);
					$.ajax({
						type:"post",
						url:redirectPath+"?ip_address="+spIpAddress+"&start_date="+start_date+"&start_time="+start_time+"&end_date="+end_date+"&end_time="+end_time+"&device_type_id="+deviceTypeId+"&select_option="+select_option+"&limitFlag="+limitFlag+graphQuerySrting,
						data:$(this).serialize(),
						cache:false,
						success:function(result){
								if (result.success>=1 || result.success>="1")
								{
									$().toastmessage('showErrorToast', result.error_msg);
								}
								else
								{
									$().toastmessage('showSuccessToast', 'Report Generated Successfully');
									window.location = "download/"+result.file_name;

								}
									spinStop($spinLoading,$spinMainLoading);
							}
					});  
	}
}

// Selectded list function start here 
function multiSelectColumns()
{       
	$(".plus").click(function(){
		plusHostParentOption(this);
	})
	$(".minus").click(function(){
		minusHostParentOption(this);
	})
	var hostParentArray = [];
	var tempHostParent=$("input[name='spTemp']").val();
	if(tempHostParent!=undefined)
	{
	   hostParentArray=tempHostParent.split(",");
	}
	for(k=0;k<hostParentArray.length; k++)
	{
		$("div[id='multiSelectList']").find("img[id='" + $.trim(hostParentArray[k])+"']").click();
	}
	$("#rm").click(function(e){
		e.preventDefault();
		$("div[id='multiSelectList']").find("div.selected").find("img").click();
	})
	$("#add").click(function(e){
		e.preventDefault();
		$("div[id='multiSelectList']").find("div.nonSelected").find("img").click();
	})
}
function minusHostParentOption(Obj)
{
	liObj = $("<li/>");
	imgObj = $("<img/>");
	liObj.append($(Obj).attr("name"));
	imgObj.attr("src","images/add16.png").attr("class","plus plus").attr("alt","+").attr("id",$(Obj).attr("id")).attr("name",$(Obj).attr("name")).click(function(){
		plusHostParentOption(this)
	})
	liObj.append(imgObj);
	$(Obj).parent().parent().parent().parent().find("div.nonSelected").find("ul").append(liObj);
	$(Obj).parent().parent().parent().parent().find("input[name='sp']").val("");
	j = 0
	for(i=0;i<$(Obj).parent().parent().find("li").size();i++)
	{
		var addedHostParent = $(Obj).parent().parent().find("li").eq(i).find("img").attr("id");
		if( addedHostParent != $(Obj).attr("id"))
		{
			if(j == 0)
			{
				$(Obj).parent().parent().parent().parent().find("input[name='sp']").val($.trim(addedHostParent));
			}
			else
			{
				$(Obj).parent().parent().parent().parent().find("input[name='sp']").val($(Obj).parent().parent().parent().parent().find("input[name='sp']").val() + "," + $.trim(addedHostParent));
			}
			j++;
		}
	}
	$(Obj).parent().parent().parent().parent().find("span#count").html(j)
	$(Obj).parent().remove();
}

function plusHostParentOption(Obj)
{
	var countParent = 0;
	liObj = $("<li/>");
	imgObj = $("<img/>");
	liObj.append($(Obj).attr("name"));
	imgObj.attr("src","images/minus16.png").attr("class","minus").attr("alt","-").attr("id",$(Obj).attr("id")).attr("name",$(Obj).attr("name")).click(function(){
		minusHostParentOption(this)
	})
	liObj.append(imgObj);
	$(Obj).parent().parent().parent().parent().find("div.selected").find("ul").append(liObj);
        hdval = $(Obj).parent().parent().parent().parent().find("input[name='sp']").val()
	if($.trim(hdval) == "")
	{
		$(Obj).parent().parent().parent().parent().find("input[name='sp']").val($(Obj).attr("id"))
	}
	else
	{
		$(Obj).parent().parent().parent().parent().find("input[name='sp']").val(hdval + "," +$(Obj).attr("id"))
	}
	countParent = $(Obj).parent().parent().parent().parent().find("span#count").html();
	$(Obj).parent().parent().parent().parent().find("span#count").html(parseInt(countParent) + 1);
	$(Obj).parent().remove();
}


function show_graph_click(){
	totalSelectedGraph=$("#sp").val();
	if (totalSelectedGraph==""){
		$().toastmessage('showWarningToast', "Please select atleast one graph from dashboard configuration.");
		return false;
	}
	$.ajax({
		type:"post",
		url:"update_show_graph.py?device_type_id="+deviceTypeId+"&selected_graph="+$("#sp").val(),
//		data:$(this).serisalize(), // $(this).text?
		cache:false,
		success:function(result){
			    try
			    {
					result=eval("("+result+")");
			   	}catch(err)
				{
					$().toastmessage('showWarningToast', "UNMP Server has encountered an error. Please retry after some time.");
					return;
				}
				if (result.success==1 || result.success=="1")
				{
					$().toastmessage('showWarningToast',messages[result.msg]);
					return	;
				}
				else
				{
					specificGenericGraphJson();
				}
			}
		});
}
