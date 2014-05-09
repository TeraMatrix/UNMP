var reconcileHostId = null;
var reconcileDeviceTypeId = null;
var reconcileTablePrefix = null;
var reconcileInsertUpdate = null;
var imgReconcileBtnObj = null;
var $spinLoading = null;
var $spinMainLoading  = null;
var flagClick = false;
var timeSlot = 60000;
var lockUnlockEvent = null;
var lockUnlockObj = null;
var lockUnlockHostId = null;
var lockUnlockDeviceTypeId = null;
var lockUnlockAdminStateNames = null;
var lockUnlockState = null;
var singleEvent = null;
var singleObj = null;
var singleHostId = null;
var singleDeviceTypeId = null;
var singleAdminStateNames = null;
var singleState = null;
var loadingSpinCss={"left":"23px","top":"23px"};
var loadingSpinLines=12;
var loadingSpinLength=6;
var loadingSpinWidth=3;
var loadingSpinRadius=6;
var loadingSpinColor='#FFF';
var loadingSpinSpeed=1;
var loadingSpinTrail=30;
var loadingSpinShadow=true;
var timeCheck = 10000;
var callB = null;
var callC = null;
var opStatusDic = {0:'No operation', 1:'Firmware download', 2:'Firmware upgrade', 3:'Restore default config', 4:'Flash commit', 5:'Reboot', 6:'Site survey', 7:'Calculate BW', 8:'Uptime service', 9:'Statistics gathering', 10:'Reconciliation', 11:'Table reconciliation', 12:'Set operation', 13:'Live monitoring', 14:'Status capturing',15:'Refreshing Site Survey','16':'Refreshing RA Channel List'}
// This is the document ready function to call everytime when page is loaded 
$(function(){
	//we call the devicelist function 
	$("input[id='filter_ip']").ccplAutoComplete("common_ip_mac_search.py?device_type="+$("select[id='device_type']").val()+"&ip_mac_search="+1 ,{
                dataType: 'json',
                max: 30,
                cache:false,
                selectedItem: $("input[id='filter_ip']").val(),
                callAfterSelect : function(obj){
                        ipSelectMacDeviceType(obj,1);
                }
        });
        
       $("input[id='filter_mac']").ccplAutoComplete("common_ip_mac_search.py?device_type="+$("select[id='device_type']").val()+"&ip_mac_search="+0 + "&search_type=" ,{
                dataType: 'json',
                max: 30,
                cache:false,
                selectedItem: $("input[id='filter_mac']").val(),
                callAfterSelect : function(obj){
                        ipSelectMacDeviceType(obj,0);
                }
        });
        $("#filterOptions").hide();
	deviceList();
	
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
	//showIpSearch();
	//Here we call the click event of search button
	$("input[id='btnSearch']").click(function(){
	//call the device list function on click of search button
		deviceList();
	})
	$("#page_tip").colorbox(
	{
		href:"page_tip_odu_listing.py",
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
function sshTerminal(hostId,deviceType)
{
		$.colorbox(
		{
				href:"webssh.py?host_id="+hostId+"&device_type="+deviceType,
				//iframe : "true",
				title: "SSH Termial",
				transition: "none",
				overlayClose: false,
				escKey: false,
				opacity: 0.4,
				maxWidth: "80%",
				width:"800px",
				height:"600px",
				onLoad: function() {
                    //$('#cboxClose').remove();
                },
                onComplete: function(){
                            // Set termSelectCallback to noop (no operation) so we the user doesn't get a warning message in their JS console
                            GateOne.Terminal.termSelectCallback = GateOne.Utils.noop; // It's too early in the tutorial to worry about stuff like this =D
                            GateOne.restoreDefaults(); // Have to do this or the theme and font size will be overridden by the prefs stored by the browser \
                                                       //   (some prefs can always be overridden by the user)
                
                            var reauthenticate = function() {
                            
                                    // This will override the GateOne.Net.reauthenticate function so we can let users know that this \
                                    //    tutorial only works with anonymous auth
                                    alert('Your Gate One server is configured to authenticate users.\nThis part of the tutorial only works if authentication is disabled (aka anonymous auth).\n\nPlease configure your Gate One server for anonymous authentication: "./gateone.py --auth=None" or put "auth = None" in your server.conf).\n\nPress OK to reload this page.');
                                    window.location.reload();
                                }

                            var gourl = "http://172.22.0.91:4443";
                            var sshurl = $('input#ssh_url').val();

                            // Load Gate One with the settings we defined in the code example
                            GateOne.init({url: gourl, embedded: true, goDiv: '#gateone', prefix: 'go_', logLevel: 'DEBUG'});
                            GateOne.prefs.autoConnectURL = sshurl;
                            GateOne.prefs.fontSize = '140%';
                            //GateOne.prefs.style = {'background-color': 'rgba(0, 0, 0, 0.85)'};
                            GateOne.Net.reauthenticate = reauthenticate;
//style: {'background-color': 'rgba(0, 0, 0, 0.85)'}
                        var termClosed = function(termNum) {
                            // Gets attached to closeTermCallbacks to ensure that the tab gets removed/cleaned up when the terminal is closed
                            setTimeout(function () {
                                var firstTerminal = GateOne.Utils.getNode('.terminal'); // Returns the first terminal                                
                                if (!firstTerminal) {
                                    form = GateOne.Utils.getNode('#'+GateOne.prefs.prefix+'container');
                                    if (form)
                                    {
                                        createTerm();
                                        console.log('call ----- ');
                                        
                                    }
                                }
                                console.log('called');
                                //go.Input.queue(go.prefs.autoConnectURL+'\n');
                                //go.Net.sendChars();
                            }, 300);
                        }  
                            
                        var createTerm = function() {
                            // NOTE: We check for an existing 'container' below so we can append to it when a second terminal is added.  \
                            //   In your own code you can do something similar or just pass a different location to GateOne.Terminal.newTerminal() \
                            //  (as the 3rd argument).
                            //GateOne.prefs.autoConnectURL='ssh://cscape@172.22.0.94:22';
                            console.log("pass");
                            if (GateOne.initialized)
                            {
                                var existingContainer = GateOne.Utils.getNode('#'+GateOne.prefs.prefix+'container'), // In case the user clicks the button a second time
                                    container = GateOne.Utils.createElement('div', {'id': 'container', 'style': {'height': '100%', 'width': '100%'}}),
                                    gateone = GateOne.Utils.getNode('#gateone');
                                console.log("pass");
                                if (gateone){
                                console.log("pass");
                                }
                                if (!existingContainer) {
                                    gateone.appendChild(container); // Put our half-size terminal in the container
                                } else {
                                    container = existingContainer;
                                }

                                termNum = GateOne.Terminal.newTerminal(null, null, container); // Tell Gate One to use the new terminal
                                console.log("pass");
                                GateOne.Input.capture();
                                GateOne.Terminal.closeTermCallbacks.push(termClosed);
                            }
                            console.log("pass");
                            //GateOne.Terminal.updateTermCallbacks.push(callOnFirstUpdate);
                            return false;
                        }
                        setTimeout(function () {
                            createTerm();
                            //go.Input.queue(go.prefs.autoConnectURL+'\n');
                            //go.Net.sendChars();
                        }, 500);
                        

                    //alert("complete");
                },
                onCleanup: function(){
                        GateOne.Terminal.closeTermCallbacks = [];
                        //termDivClose = $("div#go_icon_closeterm");
                        //console.log(termDivClose);
                        //if (termDivClose)
                        //    termDivClose.onclick();
                        var firstTerminal = GateOne.Utils.getNode('.terminal'); // Returns the first terminal
                        var termClosed = function(termNum) {
                            // Gets attached to closeTermCallbacks to ensure that the tab gets removed/cleaned up when the terminal is closed
                            GateOne.Terminal.closeTerminal(termNum);
                            //GateOne.Utils.removeElement('#go_container');
                            
                            //GateOne.restoreDefaults();           
                        //    console.log('pass');
                            
                            console.log('END');
                        }
                        if (firstTerminal) {
                            var prevTermNum = firstTerminal.id.split('term')[1]; // Just want the number
                            termClosed(prevTermNum);
                        }

                },
                onClosed: function(){
                    console.log('Closing ');
                    $("#gateone_container").remove();
                    GateOne.restoreDefaults();           
                    //$.colorbox.remove();
                }
		});
}

function apFormwareUpdate(host_id,device_type,device_state)
{
	$.colorbox(
	{
		href:"odu_firmware_view.py?host_id=" + host_id + "&device_type=" + device_type + "&device_list_state=" + device_state,
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
//odu_listing.py?device_type=ODU16,odu100,ODU16S&device_list_state=enabled&selected_device_type=''")
	// spin loading object
	$spinLoading = $("div#spin_loading");		// create object that hold loading circle
	$spinMainLoading = $("div#main_loading");	// create object that hold loading squire	
	// this retreive the value of ipaddress textbox
	var ip_address = $("input[id='filter_ip']").val();

	// this retreive the value of macaddress textbox
	var mac_address = $("input[id='filter_mac']").val();
	// this retreive the value of selectdevicetype from select menu
	var device_type = $("select[id='device_type']").val();
        if(device_type == "ap25")
        {
               urlString = "ap_device_listing_table.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type;
               parent.main.location = "ap_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + device_type;
        }
        else if(device_type == "idu4")
        {
               urlString = "idu_device_listing_table.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type;
               parent.main.location = "idu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + device_type;
        }
        else if(device_type == "ccu")
        {
               urlString = "ccu_device_listing_table.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type
               parent.main.location = "ccu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + device_type;
        }
        else
        {       
                urlString = "get_device_data_table.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type ;
        }
				
	var oTable = $('#device_data_table').dataTable({
                "bJQueryUI": true,
                "sPaginationType": "full_numbers",
                "bProcessing": true,
                "bServerSide": true,
                "bDestroy": true,
                "oSearch": {"sSearch": ip_address},
                "aoColumns": [ 
                      { "sWidth": "1%"},
                      { "sWidth": "9%" },
                      { "sWidth": "9%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },
                      { "sWidth": "10%" },                                        
                      { "sWidth": "8%" },
                      { "sWidth": "10%"},
                      { "sWidth": "1%","bSortable": false },                      
                      { "sWidth": "18%","bSortable": false },
                      { "sWidth": "5%","bSortable": false }
                    ],
                "sAjaxSource": "get_device_data_table.py?&ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type,
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
				$('.w-reconcile').tipsy({gravity: 'w'});
				oduListingTableClick();
				chkReconciliationRun();
	                        //oduListingTableClick();
	                        chkDeviceStatus();
	                        globalAdminStatus();
			});
		}
       	});
	//$('.n-reconcile').tipsy({gravity: 'n'}); // n | s | e | w
	
	//spinStop($spinLoading,$spinMainLoading);
		//	}
		//});
	$("input[id='filter_ip']").val(ip_address);
	$("input[id='filter_mac']").val(mac_address);	
	$("select[id='device_type']").val(device_type);

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


function hideIPSearch()
{
	$("#filterOptions").hide();
}
function showIPSearch()
{
	$("#filterOptions").show();
}


// Configuration report generation 
function cnfigurationReportDownload(hostId){
        $.ajax({
                type: "get",
                url : "configuration_report_download.py?host_id=" + hostId,
                success:function(result){
                	try{
                		result = eval("(" + result + ")");
				if (result.success>=1 || result.success>="1")
				{
					$().toastmessage('showErrorToast', result.result);
				}
				else
				{
					$().toastmessage('showSuccessToast', 'Report Generated Successfully');
					window.location = "download/"+result.filename;
				}
                	}catch(err){
				$().toastmessage('showErrorToast',err);
                	}
			spinStop($spinLoading,$spinMainLoading);
                }
            });
}


/*function hwSwFrequencyStatus(event,obj,hostId,deviceTypeId)
{
        event.stopPropagation();
        $(".listing-icon").removeClass("listing-icon-selected");
        $.ajax({
	                type: "get",
	                url : "hw_sw_frequency_status.py?host_id=" + hostId +"&device_type_id="+ deviceTypeId,
	                success:function(result){
	                        
	                        $(obj).parent().addClass("listing-icon-selected");
	                        $("#status_div").html(result);
                                $("#status_div").css({'top':event.pageY-90});
                                $("#status_div").css({'left':event.pageX-parseInt((($("#status_div").width())*2)/3)});
                                $("#status_div").show();
                                
	                }       
                });

}

function peerStatus(event,obj,hostId,deviceTypeId)
{
        event.stopPropagation();
        $(".listing-icon").removeClass("listing-icon-selected");
        $.ajax({
	                type: "get",
	                url : "show_peer_status.py?host_id=" + hostId +"&device_type_id="+ deviceTypeId,
	                success:function(result){
	                        $(obj).parent().addClass("listing-icon-selected");
	                        $("#status_div").html(result);
                                $("#status_div").css({'top':event.pageY-90});
                                $("#status_div").css({'left':event.pageX-parseInt((($("#status_div").width())*2)/3)});
                                $("#status_div").show();
	                }       
                });

}



function trapStatus(event,obj,hostId,deviceTypeId,ipAddress)
{
        event.stopPropagation();
        $(".listing-icon").removeClass("listing-icon-selected");
        $.ajax({
	                type: "get",
	                url : "show_trap_alarms.py?host_id=" + hostId +"&device_type_id="+ deviceTypeId+"&ip_address="+ ipAddress,
	                success:function(result){
	                        $(obj).parent().addClass("listing-icon-selected");
	                        $("#status_div").html(result);
                                $("#status_div").css({'top':event.pageY-90});
                                $("#status_div").css({'left':event.pageX-parseInt((($("#status_div").width())*3)/4)});
                                $("#status_div").show();
	                }       
                });

}

function show_admin_state(event,obj,hostId,deviceTypeId)
{
        event.stopPropagation();
        $.ajax({
	                type: "get",
	                url : "admin_state_show.py?host_id=" + hostId +"&device_type_id="+ deviceTypeId,
	                success:function(result){
	                        $(obj).parent().addClass("listing-icon-selected");
	                        obj = $("#status_div");
	                        obj.html("");
	                        obj.html("<div class='sm-loading'></div><div class='sm-spin' style='top:22%;left:43%;height:45px;width:43px'></div>"+result);
                                obj.css({'top':event.pageY-90});
                                obj.css({'left':event.pageX-parseInt((($("#status_div").width())*2)/3)});
                                $("#status_div").find("img").tipsy({gravity: 'n'});
                                $("input[type='radio']").tipsy({gravity: 'n'});
                                $loading = obj.find("div.sm-loading");
                		$spin = obj.find("div.sm-spin");
                                obj.show();
	                }       
                });


}*/
function adminStateCheck(event,obj,hostId,deviceTypeId,adminStateName)
{
        //event.stopPropagation();
        //event.preventDefault();
        attrValue = $(obj).attr("state");
        if(parseInt(attrValue)==0)
        {
                attrValue=1;
        }
        else
        {
                attrValue=0;
                
        }
        singleEvent = event;
        singleObj = obj;
        singleHostId = hostId;
        singleDeviceTypeId = deviceTypeId;
        singleAdminStateName = adminStateName;
        
        var trObj = $(obj).parent().parent().parent().parent();
        if($(trObj).hasClass("unreachable"))
        {
                if(attrValue==1)
                {
                        if(adminStateName=="ru.ruConfTable.adminstate")
                        {
                                $.prompt('RU Admin State Unlock operation failed <br/>Device might be unreachable since '+String($(trObj).attr("timer")),{ buttons:{Ok:true}, prefix:'jqismooth'});
                        }
                        else if(adminStateName=="ru.ruConfTable.adminstate")
                        {
                                $.prompt('RA Admin State Unlock operation failed <br/>Device might be unreachable since '+String($(trObj).attr("timer")),{ buttons:{Ok:true}, prefix:'jqismooth'});
                        }
                        else
                        {
                                $.prompt('SYNC Admin State Unlock operation failed <br/>Device might be unreachable since '+String($(trObj).attr("timer")),{ buttons:{Ok:true}, prefix:'jqismooth'});
                        }
                }
                else
                        if(adminStateName=="ru.ruConfTable.adminstate")
                        {
                                $.prompt('RU Admin State Lock operation failed <br/>Device might be unreachable since '+String($(trObj).attr("timer")),{ buttons:{Ok:true}, prefix:'jqismooth'});
                        }
                        else if(adminStateName=="ru.ruConfTable.adminstate")
                        {
                                $.prompt('RA Admin State Lock operation failed <br/>Device might be unreachable since '+String($(trObj).attr("timer")),{ buttons:{Ok:true}, prefix:'jqismooth'});
                        }
                        else
                        {
                                $.prompt('SYNC Admin State Lock operation failed <br/>Device might be unreachable since '+String($(trObj).attr("timer")),{ buttons:{Ok:true}, prefix:'jqismooth'});
                        }
        }
        else
        {
                admin_state_change(true,null);
       }
}


function admin_state_change(v,m)
{
        if(v != undefined && v==true && singleEvent && singleObj && singleHostId && singleDeviceTypeId && singleAdminStateName)
	{
                attrValue = $(singleObj).attr("state");
                var recTableObj = $("#"+singleHostId).parent().parent().parent();
                var OPobj = $(recTableObj).find("td:eq(10)");
		OPobj.html("");
                OPobj.html('<center><div style="display:block;background:url(images/new/loading.gif) no-repeat scroll 0% 0% transparent; width: 16px; height: 16px;"><img id="operation_status" name="operation_status" src="images/host_status1.png" title="'+opStatusDic[12]+'" style=\"width:12px;height:12px;\"class=\"imgbutton n-reconcile\" original-title="'+opStatusDic[12]+'"/></div></center>');
                if(parseInt(attrValue)==0)
                {
                        attrValue=1;
                }
                else
                {
                        attrValue=0;
                        
                }
                $.ajax({
	                        type: "get",
	                        url : "change_admin_state.py?host_id=" + singleHostId +"&device_type_id="+ singleDeviceTypeId+"&admin_state_name="+ singleAdminStateName+"&state="+ attrValue,
	                        success:function(result){
	                                if(parseInt(result.success)==0)
	                                {
	                                        /*if(attrValue==1)
	                                        {
	                                                $(singleObj).attr({"class":"red"});
	                                                $(singleObj).attr({"state":1});
	                                                if(singleAdminStateName=="ru.ruConfTable.adminstate")
	                                                {
        	                                                $(singleObj).attr("original-title","RU State Unlocked");
	                                                }
	                                                else if(singleAdminStateName=="ru.ra.raConfTable.raAdminState")
	                                                {
	                                                     $(singleObj).attr("original-title","RA State Unlocked");   
	                                                }
	                                                else
	                                                {
	                                                        $(singleObj).attr("original-title","SYNC State Unlocked");
	                                                }
	                                                

	                                        }
	                                        else
	                                        {
	                                                $(singleObj).attr({"class":"red"});
	                                                $(singleObj).attr({"state":0});
	                                                if(singleAdminStateName=="ru.ruConfTable.adminstate")
	                                                {
        	                                                $(singleObj).attr("original-title","RU State Locked");
	                                                }
	                                                else if(singleAdminStateName=="ru.ra.raConfTable.raAdminState")
	                                                {
	                                                     $(singleObj).attr("original-title","RA State Locked");   
	                                                }
	                                                else
	                                                {
	                                                        $(singleObj).attr("original-title","SYNC State Locked");
	                                                }
	                                        }*/
	                                        clearTimeout(callC);
	                                        callC=null;
	                                        globalAdminStatus();
	                                        
	                                }
	                                else
	                                {
	                                        $().toastmessage('showErrorToast',result.result);
	                                }
	                                OPobj.html("");
                                        OPobj.html('<center><img id="operation_status" name="operation_status" src="images/host_status0.png" title="'+opStatusDic[0]+'" style=\"width:12px;height:12px;\"class=\"imgbutton n-reconcile\" original-title="'+opStatusDic[0]+'"/></center>');  
	                        }
	                        
	               });
	 }
}

/*function lock_unlock_check(event,obj,hostId,deviceTypeId,adminStateNames,state)
{
        event.stopPropagation();
        lockUnlockEvent = event;
        lockUnlockObj = obj;
        lockUnlockHostId = hostId;
        lockUnlockDeviceTypeId = deviceTypeId;
        lockUnlockAdminStateNames = adminStateNames;
        lockUnlockState = state;
        if(parseInt(state)==1)
        {
                $.prompt('Unlock admin state may cause reboot of the device',{ buttons:{Ok:true,Cancel:false}, prefix:'jqismooth',callback: lock_unlock_admin});
        }
        else
        {
                lock_unlock_admin(true,null);
        }
}

function lock_unlock_admin(v,m)
{
        if(v != undefined && v==true && lockUnlockEvent && lockUnlockObj && lockUnlockHostId && lockUnlockDeviceTypeId && lockUnlockAdminStateNames)
	{
	        spinStart($spin,$loading,loadingSpinCss,loadingSpinLines,loadingSpinLength,loadingSpinWidth,loadingSpinRadius,loadingSpinColor,loadingSpinSpeed,loadingSpinTrail,loadingSpinShadow);
                var tdObj = null;
                var radioObj = null;
                if(lockUnlockState==0)
                {
                        tdObj = $(lockUnlockObj).parent().next();
                        radioObj = $(tdObj).find("input[type='radio']");
                        $(radioObj).attr({"disabled":true});
                        
                }
                else
                {
                        tdObj = $(lockUnlockObj).parent().prev();
                        radioObj = $(tdObj).find("input[type='radio']");
                        $(radioObj).attr({"disabled":true});
                
                }
                $.ajax({
	                        type: "get",
	                        url : "all_lock_unlock.py?host_id=" + lockUnlockHostId +"&device_type="+ lockUnlockDeviceTypeId+"&admin_state_names="+ lockUnlockAdminStateNames+"&state="+ lockUnlockState,
	                        success:function(result){
	                                if(parseInt(result.success)==0)
	                                {
	                                        for(var node in result.result)
	                                        {
	                                                if(result.result[node]==0 || result.result[node]=='0')
	                                                {
	                                                        if(lockUnlockState==0)
	                                                        {
	                                                                $("img[name='"+node+"']").attr({"src":"images/temp/red_dot.png"});
	                                                                $("img[name='"+node+"']").attr({"state":lockUnlockState});
	                                                        }       
	                                                        else
	                                                        {
	                                                                $("img[name='"+node+"']").attr({"src":"images/temp/green_dot.png"});
	                                                                $("img[name='"+node+"']").attr({"state":lockUnlockState});
	                                                        }
	                                                        $("img[name='"+node+"']").attr({"original-title":"Set successfully"});
	                                                        
	                                                }
	                                                else
	                                                {
	                                                        $("img[name='"+node+"']").attr({"original-title":result.result[node]});
	                                                }
	                                                
	                                        }
	                                
	                                }
	                                else
	                                {
	                                        $().toastmessage('showErrorToast',result.result);
	                                
	                                }
	                                $(radioObj).attr({"disabled":false});
	                                spinStop($spin,$loading);
	                        }
	                });
        }
}

*/

function imgReconcile(obj,hostId,deviceTypeId,tablePrefix,insertUpdate)
{
	reconcileHostId = hostId;
	reconcileDeviceTypeId = deviceTypeId;
	reconcileTablePrefix = tablePrefix;
	reconcileInsertUpdate = insertUpdate;
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
		        $.prompt('Device Configuration data would be Synchronized with the UNMP server Database',{ buttons:{Ok:true,Cancel:false}, prefix:'jqismooth',callback: imgOdu16Reconcilation});
	        }
	}
}


function imgOdu16Reconcilation(v,m)
{
	if(v != undefined && v==true && reconcileHostId && reconcileDeviceTypeId && reconcileTablePrefix && reconcileInsertUpdate && imgReconcileBtnObj)
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
				$().toastmessage('showNoticeToast',"Reconciliation started successfully please wait for atleast 60 seconds.");
				flagClick = true;
				$.ajax({
					        type: "get",
					        url : "odu16_reconcilation.py?host_id=" + reconcileHostId +"&device_type_id="+ reconcileDeviceTypeId + "&table_prefix="+reconcileTablePrefix + 					      "&insert_update="+reconcileInsertUpdate,
					        success:function(result){
							                imgBtn.data("rec",0);
							                flagClick = false;
							                objTableDetail.removeClass("listing-color");
							                objTableDetail.addClass(objTableDetail.attr("listClass"));
							                objTableDetail.removeAttr("listClass");
							                flagClick = false;
							                //{'result': {0: ['RMMaster', '172.22.0.102']}, 'success': 0}
							                if(parseInt(result.success)==0)
							                {
                                                                                json = result.result
                                                                                for(var node in json)
                                                                                {
                                                                                        if(parseInt(node)<=35)
									                {
										                imgBtn.attr("src","images/new/r-red.png");
										                imgBtn.attr("original-title",node+"% Done");
										                $().toastmessage('showWarningToast',node+"% reconciliation done for device "+json[node][0]+"("+json[node][1]+")"+".Please reconcile the device again");
									                }
									                else if(parseInt(node)<=90)
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
						$.prompt('Reconciliation is Running.You have to Wait for 15 to 20 seconds',{prefix:'jqismooth'});
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
		url:"reconcilation_list.py",
		success:function(result){
						result =  eval("(" + result + ")");
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
									var imgRec = $(recTableObj).find("td:eq(9)").find("img:eq(4)");
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
										var imgRec = $(recTableObj).find("td:eq(9)").find("img:eq(4)");
										var imgBtn = $(imgRec);
								
										if(parseInt(json[node][1])<=35)
										{
											imgBtn.attr("src","images/new/r-red.png");
											imgBtn.attr("original-title",json[node][1]+"% Done");
											$().toastmessage('showWarningToast',json[node][1]+"% Done.Please Again Reconcile The Device");
										}
										else if(parseInt(json[node][1])<=90)
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
										objTable.removeClass("listing-color");
										objTable.addClass($(recTableObj).attr("listingClass"));
										objTable.removeAttr("listingClass");
									}
									
								}
							}
							callA = setTimeout(function()
							{
			
								chkReconciliationRun();

							},timeSlot);	
						}
				}
		});
	
}


function chkDeviceStatus()
{
        if(callB!=null)
        {
                clearTimeout(callB);
        }
	var host_id = $("input[name='host_id']").val();
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

					        },timeCheck);	
				        }
	        });
}

//{'result': {'80': [1, 1, 1], '43': [1, 0, 0], '79': [1, 1, 1]}, 'success': 0}

function globalAdminStatus()
{
	var host_id = $("input[name='host_id']").val();
	if(callC!=null)
	{
	        clearTimeout(callC);
	}
        $.ajax({
	        type:"get",
	        url:"global_admin_status.py?host_id="+host_id,
	        success:function(result){
					        if(parseInt(result.success)==0)
					        {
					                json = result.result;
					                for(var node in json)
						        {  
						                var recTableObj = $("#"+node).parent().parent().parent();
						                var objTable = $(recTableObj);
						                if(parseInt(json[node][0]) == 1 && parseInt(json[node][6]) == 0)
							        {
							                var imgRec = $(recTableObj).find("td:eq(8)").find("a:eq(0)"); 
               						                var imgbtn = $(imgRec);
							                imgbtn.attr({"original-title":"RU State Unlocked"});
						                        imgbtn.attr({"class":"red"});
						                        imgbtn.attr({"state":1});
						                }
						                else if(parseInt(json[node][0]) == 1 && parseInt(json[node][6]) == 1)
							        {
							                var imgRec = $(recTableObj).find("td:eq(8)").find("a:eq(0)"); 
               						                var imgbtn = $(imgRec);
							                imgbtn.attr({"original-title":"RU State Unlocked"});
						                        imgbtn.attr({"class":"green"});
						                        imgbtn.attr({"state":1});
						                }
						                else
						                {
							                var imgRec = $(recTableObj).find("td:eq(8)").find("a:eq(0)"); 
               						                var imgbtn = $(imgRec);
						                        imgbtn.attr({"class":"red"});
						                        imgbtn.attr({"original-title":"RU State Locked"});
						                        imgbtn.attr({"state":0});
						                } 
						                
					                        if(parseInt(json[node][1]) == 1 && parseInt(json[node][7]) == 0)
						                {
						                        var imgRec = $(recTableObj).find("td:eq(8)").find("a:eq(1)"); 
               						                var imgbtn = $(imgRec);
					                                imgbtn.attr({"class":"red"});
					                                imgbtn.attr({"original-title":"SYNC State Unlocked"});
					                                imgbtn.attr({"state":1});
					                        }
					                        else if(parseInt(json[node][1]) == 1 && parseInt(json[node][7]) == 1)
						                {
						                        var imgRec = $(recTableObj).find("td:eq(8)").find("a:eq(1)"); 
               						                var imgbtn = $(imgRec);
					                                imgbtn.attr({"class":"green"});
					                                imgbtn.attr({"original-title":"SYNC State Unlocked"});
					                                imgbtn.attr({"state":1});
					                        }
					                        else
						                {
						                        var imgRec = $(recTableObj).find("td:eq(8)").find("a:eq(1)"); 
               						                var imgbtn = $(imgRec);
					                                imgbtn.attr({"class":"red"});
					                                imgbtn.attr({"original-title":"SYNC State Locked"});
					                                imgbtn.attr({"state":0});
					                        }
					                        if(parseInt(json[node][2]) == 1 && parseInt(json[node][8]) == 0)
							        {
							                var imgRec = $(recTableObj).find("td:eq(8)").find("a:eq(2)"); 
               						                var imgbtn = $(imgRec);
							                imgbtn.attr({"original-title":"RA State Unlocked"});
						                        imgbtn.attr({"class":"red"});
						                        imgbtn.attr({"state":1});
						                }
						                else if(parseInt(json[node][2]) == 1 && parseInt(json[node][8]) == 1)
							        {
							                var imgRec = $(recTableObj).find("td:eq(8)").find("a:eq(2)"); 
               						                var imgbtn = $(imgRec);
							                imgbtn.attr({"original-title":"RA State Unlocked"});
						                        imgbtn.attr({"class":"green"});
						                        imgbtn.attr({"state":1});
						                }
						                else
						                {
							                var imgRec = $(recTableObj).find("td:eq(8)").find("a:eq(2)"); 
               						                var imgbtn = $(imgRec);
						                        imgbtn.attr({"class":"red"});
						                        imgbtn.attr({"original-title":"RA State Locked"});
						                        imgbtn.attr({"state":0});
						                }
                                                                
						                var imgRec = $(recTableObj).find("td:eq(7)");
						                var imgbtn = $(imgRec);
						                if(json[node][3]!="")
						                {
						                        imgbtn.html(json[node][3]);
						                }
						                var OPobj = $(recTableObj).find("td:eq(10)");
					                		OPobj.html("");
					                        OPobj.html('<center><img id="operation_status" name="operation_status" src="'+json[node][4]+'" title="'+opStatusDic[json[node][5]]+'" style=\"width:12px;height:12px;\"class=\"imgbutton n-reconcile\" original-title="'+opStatusDic[json[node][5]]+'"/></center>');
					                        
					                        
					                        
					                        //console.log(imgOP.attr("original-title"));
					                        //console.log(json[node][5]);
					                        //console.log(opStatusDic[json[node][5]]);
					                        //"<center><img id=\"operation_status\" name=\"operation_status\" src=\"%s\" title=\"%s\" style=\"width:12px;height:12px;\"class=\"imgbutton n-reconcile\" original-title=\"%s\"/></center>
//					                        imgOP.removeAttr("original-title");
//					                        imgOP.attr("original-title",opStatusDic[json[node][5]]);
					                        //console.log(imgOP.attr("original-title"));
						        }
					        }
					
					        callC = setTimeout(function()
					        {
	
						        globalAdminStatus();

					        },timeCheck);	
				        }
	        });
}



