var timeSlot = 60000;
// spin loading object
var $spinLoading = null;		// create object that hold loading circle
var $spinMainLoading = null;	// create object that hold loading squire
var timecheck = 60000;	
var ap_mode = {0:'Standard',1:'Root AP',2:'Repeater',3:'Client',4:'Multi AP',5:'Multi VLAN',6:'Dynamic VLAN'}
$(function(){
	$spinLoading = $("div#spin_loading");		// create object that hold loading circle
	$spinMainLoading = $("div#main_loading");	// create object that hold loading squire	

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
	$("#up_down_search").toggle(function(){
		//var $span = $(this);
		//var $span = $this.find("span").eq(0);
		$("#up_down_search").removeClass("dwn");
		$("#up_down_search").addClass("up");
		$("#filterOptions").show();
		$("#hide_search").css({
		        'background-color': "#F1F1F1",
                        'display': "block",
                        'height': '20px',
                        'position': 'static',
                        'overflow': 'hidden',
                        'width': "100%"});
	},
	function(){
		//var $this = $(this);
		//var $span = $this.find("span").eq(0);
		$("#up_down_search").removeClass("up");
		$("#up_down_search").addClass("dwn");
		$("#filterOptions").hide();
		$("#hide_search").css({
		        'background-color': "#F1F1F1",
                        'display': "block",
                        'height': '20px',
                        'overflow': 'hidden',
                        'position': 'static',
                        'right': 1,
                        'top': 1,
                        'width': "100%",
                        'z-index': 1000});
		
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

function editClient(clientId)
{
        $.colorbox({
		href:"edit_ap_client.py?client_id=" + clientId,
		title: "Edit Client Details",
		opacity: 0.4,
		maxWidth: "80%",
		width:"600px", 
		height:"280px", 
		onComplete:function(){
		        $("#edit_client").validate({
		                rules:{
			                client_mac:{
				                required:true,
				                macAddress:true
			                },
			                client_name:{
				                required:true,
				                alphaNumeric:true
				                
			                },
			                client_ip:{
				                //required:true,
				                ipv4Address:true
			                }
		                },
		                messages:{
			                client_mac:{
				                required:"MAC Address is a required field",
				                macAddress:"Invalid MAC address"
			                },
			                client_name:{
				                required:"Client is a required field",
				                alphaNumeric:"Client Name should be alpha numeric"
			                },
			                client_ip:{
				                //required:"Client IP is a required field",
				                ipv4Address:"Invalid IP address"
			                }
		                }
	                });
	                $("#edit_client").submit(function(){
	                        
	                        var $formThis = $(this);
		                if($formThis.valid())
		                {
			                //spinStart($spinLoading,$spinMainLoading);
			                var action = $formThis.attr("action");
			                var method = $formThis.attr("method");
			                var data = $formThis.serialize();
			                $.ajax({
			                        type:method,
		                                url:action,
		                                data:data,
		                                cache:false,
		                                success:function(result){
		                                        if(result.success == 0)
		                                        {
		                                                $().toastmessage('showSuccessToast',String(result.result));
		                                                $.colorbox.close();
		                                                addClientListing();
		                                        }
		                                        else
		                                        {
		                                                $().toastmessage('showErrorToast',String(result.result));
		                                        }
		                                }
			                });
		                }
		                else
		                {
			                $().toastmessage('showErrorToast', "Invalid client details are entered, please recheck");
		                }
		                return false;
	                });
	                
		},
		overlayClose:false
	});
}

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
function apListing()
{
        $("#ap_device_div").show();
        $("#ap_client_div").hide();
        $("#ap_client").show();
        $("#ap_listing").hide();
        $("#filterOptions").hide();
        $("#hide_search").show();
}
function addClientListing()
{
        $("#ap_device_div").hide();
        $("#ap_client_div").show();
        $("#ap_client").hide();
        $("#ap_listing").show();
        $("#filterOptions").hide();
        $("#hide_search").hide();
        urlString = "get_client_data_table.py";
        spinStart($spinLoading,$spinMainLoading);
        var oTable = $('#client_data_table').dataTable({
                "bJQueryUI": true,
                "sPaginationType": "full_numbers",
                "bProcessing": true,
                "bServerSide": true,
                "aaSorting": [ [0,'desc'] ],
                "aoColumns": [ 
                      { "sWidth": "5%"},
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "5%" },
                      { "sWidth": "5%" },
                      { "sWidth": "5%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%","bSortable": false  }],
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
				spinStop($spinLoading,$spinMainLoading);
			});
			
		}
       	});
       	
        /*
        spinStart($spinLoading,$spinMainLoading);
        $.ajax({
		type:"post",
		url:urlString,
		cache:false,
		success:function(result){
		//alert(result);
			try
			{
				//result = eval("(" + result + ")");
				result = eval(result);
				
			}
			catch(err)
			{
				result = [];
				
			}
			//	create data table object
			var oTable = $('#client_data_table').dataTable({
                "bJQueryUI": true,
                "sPaginationType": "full_numbers",
                "bProcessing": true,
                "aaData": result,
                //"bServerSide": true,
               // "oSearch": {"sSearch": ip_address},
              "aoColumns": [ 
                      { "sWidth": "5%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%"},
                      { "sWidth": "10%"},
                      { "sWidth": "10%"},
                      { "sWidth": "10%"},
                      { "sWidth": "10%"},
                      { "sWidth": "10%"},
                      { "sWidth": "5%"}],
                "bDestroy": true
                //"sAjaxSource": urlString,
			});
		spinStop($spinLoading,$spinMainLoading);
		}

       	});
       	*/
       	
			/*$gridViewActiveHostDataTable = $gridViewActiveHostTableObj.dataTable({
				"bDestroy":true,
				"bJQueryUI": true,
				"bProcessing": true,
				"sPaginationType": "full_numbers",
				"bPaginate":true,
				"bStateSave": false,
				"aaData": result,
				"oLanguage":{
					"sInfo":"_START_ - _END_ of _TOTAL_",
					"sInfoEmpty":"0 - 0 of 0",
					"sInfoFiltered":"(of _MAX_)"
				},
				"aoColumns": [
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 0 ] },
					{ "bSearchable": false, "bVisible": false, "aTargets": [ 1 ] },
					{ "sTitle": "Host Name" , "sClass": "center", "sWidth": "18%"},
					{ "sTitle": "Host Alias" , "sClass": "center", "sWidth": "20%"},
					{ "sTitle": "IP Address", "sClass": "center", "sWidth": "18%" },
					{ "sTitle": "Device Type", "sClass": "center", "sWidth": "18%" },
					{ "sTitle": "MAC Address", "sClass": "center", "sWidth": "17%" },
					{ "sTitle": " ", "sWidth": "9%", "bVisible": false }
				]
			});
			$gridViewActiveHostDataTable.fnDraw();
			spinStop($spinLoading,$spinMainLoading);
		}
	});*/
	
	
	
	
	/*var oTable = $('#client_data_table').dataTable({
                "bJQueryUI": true,
                "sPaginationType": "full_numbers",
                "bProcessing": true,
                "bServerSide": true,
               // "oSearch": {"sSearch": ip_address},
                "aoColumns": [ 
                      { "sWidth": "5%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "5%" },
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
				/*fnCallback(json);
				$('.n-reconcile').tipsy({gravity: 'n'});
				//chkReconciliationRun();
	                        //oduListingTableClick();
	                        //chkDeviceStatus();
	                        //chkRadioStatus();
	                        //chkConnectedClients();
			});
		}
       	});
	//$('.n-reconcile').tipsy({gravity: 'n'}); // n | s | e | w
	
        //$("input[id='filter_ip']").val(ip_address);
         //$("input[id='filter_mac']").val(mac_address);
        //$("select[id='device_type']").val(device_type);
				
		//	}
		//});*/
		
}


function deviceList()
{
         $("#ap_device_div").show();
        $("#ap_client_div").hide();
	// spin loading object
	// this retreive the value of ipaddress textbox
	var ip_address = $("input[id='filter_ip']").val();
	// this retreive the value of macaddress textbox
	var mac_address = $("input[id='filter_mac']").val();
	// this retreive the value of selectdevicetype from select menu
	var device_type = $("select[id='device_type']").val();
	spinStart($spinLoading,$spinMainLoading);
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
                      { "sWidth": "5%" },
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
	                        chkConnectedClients();
        			spinStop($spinLoading,$spinMainLoading);
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
                           spinStop($spinLoading,$spinMainLoading);     
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
						                var imgRec = $(recTableObj).find("td:eq(7)").find("a:eq(0)"); 
						                var apMode = $(recTableObj).find("td:eq(6)");
						                var objModeAP = $(apMode);
						                var imgbtn = $(imgRec);
						                if(parseInt(json[node][0]) == 1)
								{
							                imgbtn.attr({"class":"green"});
							                imgbtn.attr({"state":1});
							                imgbtn.attr({"original-title":"Radio Enabled"});
							        }
							        else
							        {
                                                                        imgbtn.attr({"class":"red"});
							                imgbtn.attr({"state":0});
							                imgbtn.attr({"original-title":"Radio Disabled"});							        
							        }
							        objModeAP.html(ap_mode[parseInt(json[node][1])]);
						        }
						}
						callC = setTimeout(function()
						{
		
							chkRadioStatus();

						},timecheck);	
					}
                });
}

var callD=null;
function chkConnectedClients()
{
        host_id = $("input[name='host_id']").val();
        if(callD!=null)
        {
                clearTimeout(callD);
        }
	$.ajax({
		type:"get",
		url:"connected_clients.py?host_id="+host_id,
		success:function(result){
						if(parseInt(result.success)==0)
						{
						        json = result.result;
					                var recTableObj = $("#"+json[1]).parent().parent().parent();
					                var objTable = $(recTableObj); 					               
					                var tdData = $(recTableObj).find("td:eq(5)");
        				                $(tdData).html(json[0]);
	        				        
						}
						callD = setTimeout(function()
						{
		
							chkConnectedClients();

						},timecheck);	
					}
                });
}


