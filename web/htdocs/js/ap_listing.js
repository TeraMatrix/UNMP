var timeSlot = 60000;
// spin loading object
var $spinLoading = $("div#spin_loading");		// create object that hold loading circle
var $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
var timecheck = 60000;	
$(function(){
	//we call the devicelist function 
	$("input[id='filter_ip']").ccplAutoComplete("common_ip_mac_search.py?device_type="+$("select[id='device_type']").val()+"&ip_mac_search="+1,{
                dataType: 'json',
                max: 30,
                selectedItem: "",
                callAfterSelect : function(obj){
                        ipSelectMacDeviceType(obj,1);
                }
        });
        
       $("input[id='filter_mac']").ccplAutoComplete("common_ip_mac_search.py?device_type="+$("select[id='device_type']").val()+"&ip_mac_search="+0,{
                dataType: 'json',
                max: 30,
                selectedItem: "",
                callAfterSelect : function(obj){
                        ipSelectMacDeviceType(obj,0);
                }
        });
	deviceList();
	$("#filterOptions").hide();
	$("#hide_search").show();
	$("#hide_search").toggle(function(){
		var $this = $(this);
		var $span = $this.find("span").eq(0);
		$span.removeClass("up");
		$span.addClass("dwn");
		$("#filterOptions").show();
		$this.css({
		        'background-color': "#F1F1F1",
                        'display': "block",
                        'height': '20px',
                        'position': 'static',
                        'overflow': 'hidden',
                        'width': "100%"
                     });
	},
	function(){
		var $this = $(this);
		var $span = $this.find("span").eq(0);
		$span.removeClass("dwn");
		$span.addClass("up");
		$("#filterOptions").hide();
		$this.css({
		        'background-color': "#F1F1F1",
                        'display': "block",
                        'height': '20px',
                        'overflow': 'hidden',
                        'position': 'static',
                        'right': 1,
                        'top': 1,
                        'width': "100%",
                        'z-index': 1000
                    });
		
	});
	//Here we call the click event of search button
	$("input[id='btnSearch']").click(function(){
	//call the device list function on click of search button
		deviceList();
	})
	$("#page_tip").colorbox(
	{
		href:"page_tip_ap_listing.py",
		title: "Page Tip",
		opacity: 0.4,
		maxWidth: "80%",
		width:"600px",
		height:"420px",
		onComplte:function(){}
	});
	$("body").click(function(){
	        $("#status_div").hide();
	        $(".listing-icon").removeClass("listing-icon-selected");
	
	});
	//spinStart($spinLoading,$spinMainLoading);
	//spinStop($spinLoading,$spinMainLoading);
});

function apFormwareUpdate(host_id,device_type,device_state)
{
	$.colorbox(
	{
		href:"ap_firmware_view.py?host_id=" + host_id + "&device_type=" + device_type + "&device_list_state=" + device_state,
		iframe:true,
		title: "Firmware Update",
		opacity: 0.4,
		maxWidth: "80%",
		width:"400px", 
		height:"200px", 
		onOpen:function(){spinStop($spinLoading,$spinMainLoading);},
		overlayClose:false
	});
}
//this the defination of device list function
//this function return the datatable   

function deviceList()
{
	// spin loading object
	// this retreive the value of ipaddress textbox
	var ip_address = $("input[id='filter_ip']").val();
	// this retreive the value of macaddress textbox
	var mac_address = $("input[id='filter_mac']").val();
	// this retreive the value of selectdevicetype from select menu
	var device_type = $("select[id='device_type']").val();
	urlString = ""
        if(device_type == "odu100" || device_type=="odu16")
        {       
                urlString = "get_device_data_table.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type ;
                parent.main.location = "odu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + device_type ;
        }
        else if(device_type == "idu4")
        {
               urlString = "idu_device_listing_table.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type
               parent.main.location = "idu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + device_type;
        }
        else
        {
                urlString = "ap_device_listing_table.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type
        }
	var oTable = $('#device_data_table').dataTable({
                "bJQueryUI": true,
                "sPaginationType": "full_numbers",
                "bProcessing": true,
                "bServerSide": true,
                "oSearch": {"sSearch": ip_address},
                "aoColumns": [ 
                      { "sWidth": "5%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%","bSortable": false  },
                      { "sWidth": "30%","bSortable": false  }],
                "bDestroy": true,
                "sAjaxSource": urlString,
               "fnServerData": function(sSource,aoData,fnCallback){
			$.getJSON( sSource, aoData, function (json) { 
				/**
				 * Insert an extra argument to the request: rm.
				 * It's the the name of the CGI form parameter that
				 * contains the run mode name. Its value is the
				 * runmode, that produces the json output for
				 * datatables.
				 **/
				fnCallback(json);
				$('.n-reconcile').tipsy({gravity: 'n'});
				chkReconciliationRun();
	                        oduListingTableClick();
	                        chkDeviceStatus();
	                        chkRadioStatus();
			});
		}
       	});
	//$('.n-reconcile').tipsy({gravity: 'n'}); // n | s | e | w
	
        $("input[id='filter_ip']").val(ip_address);
         $("input[id='filter_mac']").val(mac_address);
        $("select[id='device_type']").val(device_type);
				
		//	}
		//});
		
};

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

function wirelessStatus(event,obj,hostId,deviceTypeId)
{
        //event.stopPropagation();
        $(".listing-icon").removeClass("listing-icon-selected");
        $.ajax({
	                type: "get",
	                url : "show_wireless_status.py?host_id=" + hostId +"&device_type_id="+ deviceTypeId,
	                success:function(result){
	                        
	                        $(obj).parent().addClass("listing-icon-selected");
	                        $("#status_div").html(result);
                                $("#status_div").css({'top':event.pageY-90});
                                $("#status_div").css({'left':event.pageX-200-parseInt((($("#status_div").width())*2)/3)});
                                $("#status_div").show();
                                
	                }       
                });

}

/*function serviceStatus(event,obj,hostId,deviceTypeId)
{
        event.stopPropagation();
        $(".listing-icon").removeClass("listing-icon-selected");
        $.ajax({
	                type: "get",
	                url : "service_status.py?host_id=" + hostId +"&device_type_id="+ deviceTypeId,
	                success:function(result){
	                        
	                        $(obj).parent().addClass("listing-icon-selected");
	                        $("#status_div").html(result);
                                $("#status_div").css({'top':event.pageY-90});
                                $("#status_div").css({'left':event.pageX-parseInt((($("#status_div").width())*2)/3)});
                                $("#status_div").show();
                                
	                }       
                });

}

function systemInfo(event,obj,hostId,deviceTypeId)
{
        event.stopPropagation();
        $(".listing-icon").removeClass("listing-icon-selected");
        $.ajax({
	                type: "get",
	                url : "system_info.py?host_id=" + hostId +"&device_type_id="+ deviceTypeId,
	                success:function(result){
	                        
	                        $(obj).parent().addClass("listing-icon-selected");
	                        $("#status_div").html(result);
                                $("#status_div").css({'top':event.pageY-90});
                                $("#status_div").css({'left':event.pageX-parseInt((($("#status_div").width())*2)/3)});
                                $("#status_div").show();
                                
	                }       
                });

}


function apTrapStatus(event,obj,hostId,deviceTypeId,ipAddress)
{
        $(".listing-icon").removeClass("listing-icon-selected");
        event.stopPropagation();
        $.ajax({
	                type: "get",
	                url : "show_trap_alarms.py?host_id=" + hostId +"&device_type_id="+ deviceTypeId+"&ip_address="+ ipAddress,
	                success:function(result){
	                        $(obj).parent().addClass("listing-icon-selected");
	                        obj = $("#status_div");
	                        obj.html("");
	                        obj.html("<div class='sm-loading'></div><div class='sm-spin'></div>"+result);
                                obj.css({'top':event.pageY-90});
                                obj.css({'left':event.pageX-parseInt((($("#status_div").width())*3)/4)});
                                obj.show();
	                }       
                });

}

function show_radio_admin_state(event,obj,hostId,deviceTypeId)
{
        $(".listing-icon").removeClass("listing-icon-selected");
        event.stopPropagation();
        $.ajax({
	                type: "get",
	                url : "show_radio_admin.py?host_id=" + hostId +"&device_type_id="+ deviceTypeId,
	                success:function(result){
	                        $(obj).parent().addClass("listing-icon-selected");
	                        obj = $("#status_div");
	                        obj.html("");
	                        obj.html("<div class='sm-loading'></div><div class='sm-spin'></div>"+result);
                                obj.css({'top':event.pageY-90});
                                obj.css({'left':event.pageX-parseInt((($("#status_div").width())*2)/3)});
                                $("#status_div").find("img").tipsy({gravity: 'n'});
                                obj.show();
	                }       
                });


}*/

function radio_enable_disable(event,obj,hostId,adminStateName)
{
        attrValue = $(obj).attr("state");
        if(parseInt(attrValue)==0)
        {
                attrValue=1;
        }
        else
        {
                attrValue=0;
                
        }
        var trObj = $(obj).parent().parent().parent().parent();
        if($(trObj).hasClass("unreachable"))
        {
                if(attrValue==1)
                {
                       $.prompt('Radio Enable operation failed <br/>Device might be unreachable since '+String($(trObj).attr("timer")),{ buttons:{Ok:true}, prefix:'jqismooth'});
                 }
                 else
                 {
                        $.prompt('Radio Disbale operation failed <br/>Device might be unreachable since '+String($(trObj).attr("timer")),{ buttons:{Ok:true}, prefix:'jqismooth'});
                 }
        }
        else
        {
                $.ajax({
	                        type: "get",
	                        url : "disable_enable_radio.py?host_id=" + hostId +"&admin_state_name="+ adminStateName+"&state="+ attrValue,
	                        success:function(result){
	                                if(parseInt(result.success)==0)
	                                {
	                                        if(attrValue==1)
	                                        {
	                                                $(obj).attr({"class":"green"});
	                                                $(obj).attr({"state":1});
	                                                $(obj).attr({"original-title":"Radio Enabled"});
	                                        }
	                                        else
	                                        {
	                                                $(obj).attr({"class":"red"});
	                                                $(obj).attr({"state":0});
	                                                $(obj).attr({"original-title":"Radio Disabled"});	                                        
	                                        }
	                                }
	                                else
	                                {
	                                        $().toastmessage('showErrorToast',result.result);
	                                }
	                        }
	                        
	               });
        }
}


function imgReconcile(obj,hostId,deviceTypeId)
{
	reconcileHostId = hostId;
	reconcileDeviceTypeId = deviceTypeId;
	imgReconcileBtnObj = $(obj);
	var imgBtn = imgReconcileBtnObj;
	var recTableObj = imgBtn.parent().parent();
	var tableObj = $(recTableObj);
	if(tableObj.hasClass("listing-color"))
	{
			
	}
	else
	{
	        if(imgBtn.data("rec")==1) 
	        {
			        //$.prompt('Reconciliation is already Running.Please Wait',{ buttons:{Ok:true}, prefix:'jqismooth'});	
			        spinStop($spinLoading,$spinMainLoading);
	        }
	        else
	        {
		        $.prompt('Device Configuration data would be Synchronized with the UNMP server Database. \n',{ buttons:{Ok:true,Cancel:false}, prefix:'jqismooth',callback: imgOdu16Reconcilation});
	        }
        }
}


function imgOdu16Reconcilation(v,m)
{
	if(v != undefined && v==true && reconcileHostId && reconcileDeviceTypeId)
	{
		spinStop($spinLoading,$spinMainLoading);
		var imgBtn = imgReconcileBtnObj;
		var tableObj = imgBtn.parent().parent();
		var objTableDetail = $(tableObj);
		if(objTableDetail.hasClass("listing-color"))
		{
			$.prompt('Reconciliation is already Running.Please Wait',{ buttons:{Ok:true}, prefix:'jqismooth'});	
		}	
		else
		{
			if(imgBtn.data("rec")==undefined)
			{
				imgBtn.data("rec",0);
			}		
			if(imgBtn.data("rec")==0) 
			{
				imgBtn.data("rec",1);
				var classAttr = objTableDetail.attr("class");
				objTableDetail.attr("listClass",classAttr);
				objTableDetail.removeClass(classAttr);
				objTableDetail.addClass("listing-color");
				flagClick = true;
				$.ajax({
					type: "get",
					url : "update_reconciliation.py?host_id=" + reconcileHostId +"&device_type_id="+ reconcileDeviceTypeId ,
					success:function(result){
									imgBtn.data("rec",0);
									flagClick = false;
									objTableDetail.removeClass("listing-color");
									objTableDetail.addClass(objTableDetail.attr("listClass"));
									objTableDetail.removeAttr("listClass");
									flagClick = false;
									try
									{
										if(result.success == 0)
										{
											var json = result.result
											for(var node in json)
											{
												if(node<=35)
												{
													imgBtn.attr("src","images/new/r-red.png");
													imgBtn.attr("original-title",node+"% Done");
													$().toastmessage('showWarningToast',node+"% reconciliation done for device "+json[node][0]+"("+json[node][1]+")"+".Please reconcile the device again");
												}
												else if(node<=90)
												{
													imgBtn.attr("src","images/new/r-black.png");
													imgBtn.attr("original-title",node+"% Done");
													$().toastmessage('showWarningToast',node+"% reconciliation done for device "+json[node][0]+"("+json[node][1]+")"+".Please reconcile the device again");
												}
												else
												{
													imgBtn.attr("src","images/new/r-green.png");
													imgBtn.attr("original-title","Reconciliation "+node+" % Done");
													$().toastmessage('showSuccessToast',"Reconciliation done successfully for device "+json[node][0]+"("+json[node][1]+")");
												}
												break;
											}
										}
										else
										{
											$().toastmessage('showErrorToast',result.result);
										}
									}
									catch(err)
									{
								
									}
								}
					});
				return false;
			}
		}
	}
	else
	{
		spinStop($spinLoading,$spinMainLoading);
	}
	
}

function oduListingTableClick()
{
	var tableObj = $("table#device_data_table tr");
	
	tableObj.click(function(event){
				var elementClick = $(event.target);
				if($(this).hasClass("listing-color") || $(this).hasClass(""))//check this type of condition because when more than one reconciliation performs the class has been 												      empty due to confliction of objects
				{
					if($(elementClick).hasClass("imgEditodu16"))
					{
						$.prompt('Reconciliation is Running. Please wait.',{prefix:'jqismooth'});
						return false;	
					}	
				}
				else
				{
					if(elementClick.is("img"))
					{
						spinStart($spinLoading,$spinMainLoading);
					}
				}
				
			});
}
var callA=null;
function chkReconciliationRun()
{
        if(callA!=null)
        {
                clearTimeout(callA);
        }
	$.ajax({
		type:"get",
		url:"reconciliation_status.py",
		success:function(result){
						if(result.success == 0)
						{
							var json = result.result;
							var oldClassAttr = null;
							for(var node in json)
							{
								var recTableObj = $("#"+node).parent().parent().parent();
								var objTable = $(recTableObj);
								if(parseInt(json[node][0]) == 1)
								{
									if(objTable.hasClass("listing-color"))
									{
									} 
									else
									{
										var classAttr = objTable.attr("class");
										objTable.attr("listingClass",classAttr);
										objTable.removeClass(classAttr);
										objTable.addClass("listing-color");
									}
								}
								else if(parseInt(json[node][0])==2)
								{
									var imgRec = $(recTableObj).find("td:eq(4)").find("img:eq(4)");
									var imgBtn = $(imgRec);
									if(json[node][1]<=35)
									{
										imgBtn.attr("src","images/new/r-red.png");
										imgBtn.attr("original-title",json[node][1]+"% Done");
										$().toastmessage('showWarningToast',json[node][1]+"% Done.Please Again Reconcile The Device");
									}
									else if(json[node][1]<=90)
									{
										imgBtn.attr("src","images/new/r-black.png");
										imgBtn.attr("original-title",json[node][1]+"% Done");
										$().toastmessage('showWarningToast',json[node][1]+"% Done.Please Again Reconcile The Device");
									}
									else
									{
										imgBtn.attr("src","images/new/r-green.png");
										imgBtn.attr("original-title",json[node][1]+"% Done");
										$().toastmessage('showSuccessToast','Reconcilation Done SuccessFully');
									}
								}
								else
								{
									if(objTable.hasClass("listing-color"))
									{
										var imgRec = $(recTableObj).find("td:eq(4)").find("img:eq(4)");
										var imgBtn = $(imgRec);
								
										if(parseInt(json[node][1])<=35)
										{
											imgBtn.attr("src","images/new/r-red.png");
											imgBtn.attr("original-title",json[node][1]+"% Done");
										}
										else if(parseInt(json[node][1])<=90)
										{
											imgBtn.attr("src","images/new/r-black.png");
											imgBtn.attr("original-title",json[node][1]+"% Done");
										}
										else
										{
											imgBtn.attr("src","images/new/r-green.png");
											imgBtn.attr("original-title",json[node][1]+"% Done");
										}
										objTable.removeClass("listing-color");
										objTable.addClass($(recTableObj).attr("listingClass"));
										objTable.removeAttr("listingClass");
									}
									
								}
							}
						}
					callA = setTimeout(function()
					{
	
						chkReconciliationRun();

					},timeSlot);	
				}
		});
	
}

var callB=null;
function chkDeviceStatus()
{
	host_id = $("input[name='host_id']").val();
	if(callB!=null)
	{
	        clearTimeout(callB);
	}
	$.ajax({
		type:"get",
		url:"device_status.py?host_id="+host_id,
		success:function(result){
						if(parseInt(result.success)==0)
						{
						        json = result.result;
						        for(var node in json)
							{  
							        var recTableObj = $("#"+node).parent().parent().parent();
					                        var objTable = $(recTableObj); 
					                        var tdObj = $(recTableObj).find("td:eq(0)");
					                        var trObj = $(tdObj).parent();
					                        var imgRec = $(tdObj).find("img:eq(0)"); 
					                        var imgbtn = $(imgRec);
						                if(parseInt(json[node][0]) == 1)
							        {
						                        imgbtn.attr({"src":"images/temp/red_dot.png"});
                                                                        imgbtn.attr({"original-title":"Device Unreachable since "+String(json[node][1])});
                                                                        $(trObj).addClass("unreachable");
                                                                        $(trObj).attr({"timer":String(json[node][1])});
						                }
						                else
						                {
						                        imgbtn.attr({"src":"images/temp/green_dot.png"});
						                        imgbtn.attr({"original-title":"Device Reachable"});
						                        $(trObj).removeClass("unreachable");
						                        $(trObj).removeAttr("timer");
						                }
							}
						}
						
						callB = setTimeout(function()
						{
		
							chkDeviceStatus();

						},timecheck);	
					}
		});
	
}
//{'result': {'70': '0'}, 'success': 0}
var callC=null;
function chkRadioStatus()
{
        host_id = $("input[name='host_id']").val();
        if(callC!=null)
        {
                clearTimeout(callC);
        }
	$.ajax({
		type:"get",
		url:"chk_radio_state.py?host_id="+host_id,
		success:function(result){
						if(parseInt(result.success)==0)
						{
						        json = result.result;
						        for(var node in json)
						        {
						                var recTableObj = $("#"+node).parent().parent().parent();
						                var objTable = $(recTableObj); 
						                var imgRec = $(recTableObj).find("td:eq(6)").find("a:eq(0)"); 
						                var imgbtn = $(imgRec);
						                if(parseInt(json[node]) == 1)
								{
							                imgbtn.attr({"class":"green"});
							                imgbtn.attr({"state":1});
							                imgbtn.attr({"original-title":"Radio Enabled"});
							        }
							        else
							        {
                                                                        imgbtn.attr({"class":"red"});
							                imgbtn.attr({"state":0});
							                imgbtn.attr({"original-title":"Radio Disabled"});							        }
						        }
						}
						callC = setTimeout(function()
						{
		
							chkRadioStatus();

						},timecheck);	
					}
                });
}

