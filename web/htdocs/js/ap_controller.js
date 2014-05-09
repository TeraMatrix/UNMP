var timeSlot = 60000;
var reconcileState = 0;
var reconcile_chk_status_btn = 0;
var selectVap = [];
var selectVapChange = []
var selectVapVap = []
/* Data Table Object */
var $gridViewAPMacTableObj = null;
var $gridViewAPMacDataTable = null;
var $gridViewAPMacFetched = 0;
var $gridViewAPMacSelectedTr = [];		/* Datatable selected rows Array */
var isRepeater = false;
var timecheck = 60000;
var radioStatechk = null;
var ipMacChange = null;
function getRepaeaterValue()
{
	
	if(parseInt($("input[name='radioSetup.radioAPmode']:checked").val())==2)
	{
		isRepeater = true;
	}	
	else
	{
		isRepeater = false;
	}

}
function deviceList()
{
	$spinLoading = $("div#spin_loading");		// create object that hold loading circle
	$spinMainLoading = $("div#main_loading");	// create object that hold loading squire
	var device_type = "ap25";
	// this retreive the value of ipaddress textbox
	var ip_address = $("input[id='filter_ip']").val();
	// this retreive the value of macaddress textbox
	var mac_address = $("input[id='filter_mac']").val();
	// this retreive the value of selectdevicetype from select menu
	var selected_device_type = $("select[id='device_type']").val();
	spinStart($spinLoading,$spinMainLoading);
	if(selected_device_type=="idu4")
	{
	        parent.main.location = "idu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + selected_device_type;
	}
	else if(selected_device_type=="odu100" || selected_device_type=="odu16")
	{
	        parent.main.location = "odu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + selected_device_type;
	}
	else
	{
	// this ajax return the call to function get_device_data_table which is in odu_view and pass the ipaddress,macaddress,devicetype with url  
	        $.ajax({
		        type:"get",
		        url:"get_device_list_ap_profiling.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type,
		        success:function(result){
					        if (result == 0 || result == "0")
					        {
					                $().toastmessage('showWarningToast',"Searched Device Doesn't Exist");
						        parent.main.location = "ap_listing.py?ip_address=" + "" + "&mac_address=" + "" + "&selected_device_type=" + "";
						        // $("#ap_form_div").html("No profiling exist");
					        }
					        else if (result==1 || result=="1")
					        {
						        parent.main.location = "ap_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type;
						
					        }
					        else if (result == 2 || result == "2")
					        {
					
						        $("#ap_form_div").html("Please Try Again");
					        }
					        else 
				         	{
						        $("#ap_form_div").html(result);
						        var host_id = $("input[name='host_id']").val();
                        		var device_type_id = $("input[name='device_type']").val();
                        		radioEnableDisable();
                        		radioStartUpMode();
                        		manageVlan();
                        		gatinIndex();
                        		agreegation();
                        		channelWidth();
                        		txChainMask();
                        	        rxChainMask();
                        	        upnpServer();
                                	sysLog();
                        	        aclState();
                        	        aclMode();
                        	        vapAclSelection(); 
                        	        Toggleradio();
                        	        selectedVap();
                        	        getRepaeaterValue();               	    
				        Thresholdchange();
				        Securitymode();
				        WPAevents();
				        Services();
				        ACL();
				        Macadd();
				        vapVapSelection();
				        vapModeHideShow();
				        vlanHideShow();
				        chk_reconcile_status(host_id);
				        $("select#rts_mode").change(function(){
					        Thresholdchange();
				        });
				        $("select#frag_mode").change(function(){
					        Thresholdchange();
				        });
				        $gridViewAPMacDataTable = $("table#showmac").dataTable({
				                "bDestroy":true,
				                "bJQueryUI": true,
				                "bProcessing": true,
				                "sPaginationType": "full_numbers",
				                "aLengthMenu": [[20, 40, 60, -1],[20, 40, 60, "All"]],
				                "iDisplayLength":20,
				                "aaSorting": []
			                });
						
			                $("div#config_tabs","div#container_body").yoTabs();
			                $("#filter_mac").val($("input[name='mac_address']").val());
                                        $("#filter_ip").val($("input[name='ip_address']").val());
			                $("input[name='ap25_commit']").unbind().bind("click",function(){
				                if(reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null)
				                {
					                commitFlashConfirm();
				                }	
				                else
				                {
					                $.prompt('Reconciliation is Running.Please Wait',{ buttons:{Ok:true}, prefix:'jqismooth'});
				                }
		                   	});
			                $("input[name='ap25_reboot']").unbind().bind("click",function(){
				                if(reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null)
				                {
					                rebootConfirm();
				                }	
				                else
				                {
					                $.prompt('Reconciliation is Running.Please Wait',{ buttons:{Ok:true}, prefix:'jqismooth'});
				                }
		                   	});
			                $("input[name='ap25_reconcile']").unbind().bind("click",function(){
				                if(reconcileState == 0 || reconcileState == null)
				                {
					                reconciliation_chk();
				                }	
				                else
				                {
					                $.prompt('Reconciliation is Running.Please Wait',{ buttons:{Ok:true}, prefix:'jqismooth'});
				                }
		                   	});
				        $("#ap_acl_form").find('select[id="vapSelection.selectVap"]').change(function()
                                        {
                                            changeVapAclSelect();   
                                        })
                                        $("#ap_vap_form").find('select[id="vapselectionid"]').change(function()
                                        {
                                            vapVapSelection();   
                                        })
		                       }
				
		                        if(isRepeater==true)
                           		 {
	                            		$("#wepradio").hide();
	                            		$("div#wepdiv").hide();
	                            	}
	                                 else
	                                {    
                	                    	$("#wepradio").show();
                                    		if($("#sec_wep").attr("checked"))
                                    		{
                                    		        $("div#wepdiv").show();
                                    		}
                                    		else
                                    		{
                                    		       $("div#wepdiv").hide();
                                    		}
	                            	   
	                               }
	                               $("#ap_radio_form").find('input[name="radioSetup.radioAggregation"]').click(function()
	                               {
	                                                if ($(this).attr("checked"))
	                                                {
                                                               if(parseInt($(this).val())==0)
                                                               {
                                                                
                                                                        $("#ap_radio_form").find("input[name='radioSetup.radioAggFrames']").attr({"disabled":true});
                                                                        $("#ap_radio_form").find("input[name='radioSetup.radioAggSize']").attr({"disabled":true});
                                                                        $("#ap_radio_form").find("input[name='radioSetup.radioAggMinSize']").attr({"disabled":true});
                                                               }
                                                               else
                                                               {
                                                                
                                                                        $("#ap_radio_form").find("input[name='radioSetup.radioAggFrames']").attr({"disabled":false});
                                                                        $("#ap_radio_form").find("input[name='radioSetup.radioAggSize']").attr({"disabled":false});
                                                                        $("#ap_radio_form").find("input[name='radioSetup.radioAggMinSize']").attr({"disabled":false});
                                                               }
                                                      }
	                               });
	                              $("#ap_radio_form").find('input[name="radioSetup.radioAggregation"]:checked').click();
	                        if(ipMacChange==1)
				{
				        $("#header3_text").text(ip_address +" "+ "AP"+" Configuration");
				        chkRadioStatus();
				        ipMacChange = 0;
				}      
			        spinStop($spinLoading,$spinMainLoading);
                        }
	        });
	        
        }
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
	                                ipMacChange=1;  
	                                deviceList();
	                        }
	                        else
	                        {
	                             $().toastmessage('showErrorToast',result.error);   
	                        }
	                }
	       });
}


function selectedVap()
{
	
    var vapselected = $('select[name="radioSetup.numberofVAPs"]').val();
    for(i=1;i<=8;i++)
	{
	    var vapVap = $("select[id='vapSelection.selectVap'] option[value='" + i + "']");
	    var vapAcl = $("select[name='vapselectionid'] option[value='" + i + "']");
	    if(i>parseInt(vapselected))
	    {
	        vapVap.hide();
	        vapAcl.hide();
	        vapVap.attr("disabled",true);
	        vapAcl.attr("disabled",true);
	    }
	    else
	    {
	        vapVap.show();
	        vapAcl.show();
	        vapVap.attr("disabled",false);
	        vapAcl.attr("disabled",false);

	    }
	}
	$('#ap_acl_form select[id="vapSelection.selectVap"]').attr("selected",true);
	
}


function changeVapAclSelect()
{
        for(var i in selectVap)
        {
            if(parseInt($("#ap_acl_form").find('select[id="vapSelection.selectVap"]').val())==i)
            {
                if(parseInt(selectVap[i][0])==0)
                {        
                    $('input[name="basicACLconfigTable.aclState"]').filter("[value='0']").attr('checked', true);
                }
                else
                {
                    $('input[name="basicACLconfigTable.aclState"]').filter("[value='1']").attr('checked', true);
                }
                if(parseInt(selectVap[i][1])==0)
                {
                   $('input[name="basicACLconfigTable.aclMode"]').filter("[value='0']").attr('checked', true);
                }
                else
                {
                    $('input[name="basicACLconfigTable.aclMode"]').filter("[value='1']").attr('checked', true);
                }
                $('input[name="vap_selection_id"]').val(selectVap[i][2]);
                $.ajax({
                        type:"post",
                        url:"select_vap_acl.py?vap_select_id="+selectVap[i][2],
                        success:function(result)
                        {
                            $("#macdiv").html(result);
                            $gridViewAPMacDataTable = $("table#showmac").dataTable({
						        "bDestroy":true,
						        "bJQueryUI": true,
						        "bProcessing": true,
						        "sPaginationType": "full_numbers",
						        "aLengthMenu": [[20, 40, 60, -1],[20, 40, 60, "All"]],
						        "iDisplayLength":20,
						        "aaSorting": []
					        });
                        }
                   });
                break;    
            }
            else
            {
                continue;
            }
            
        }
	     ACL();

}



function vapAclSelection()
{
    var host_id = $("input[name='host_id']").val();
    var device_type = $("input[name='device_type']").val(); 
    
    $.ajax({
            type:"post",
            url:"selectVap.py?host_id=" + host_id +"&device_type="+device_type,
            success:function(result)
            {
                result = eval(result);
                selectVap = [0];
                for(var i in result)
                {
                     selectVap[selectVap.length] = result[i] ;
                }
            }
        });
}

function vapVapForm()
{

    for(i in selectVapVap)
    {
          if(parseInt($("#ap_vap_form").find('select[id="vapselectionid"]').val())==i)  
          {

            $('input[name="selectionvap_id"]').val(selectVapVap[i][0]);
            $("input[name='basicVAPconfigTable.vapESSID']").val(selectVapVap[i][1]);
            if(parseInt(selectVapVap[i][2])==1)
            {
                $("input[name='basicVAPsetup.vapHiddenESSIDstate']").attr("checked", "checked");
            }
            else
            {
                $("input[name='basicVAPsetup.vapHiddenESSIDstate']").removeAttr("checked");
            }
            $("input[name='basicVAPconfigTable.vapRTSthresholdValue']").val(selectVapVap[i][3]);
            $("input[name='basicVAPconfigTable.vapFragmentationThresholdValue']").val(selectVapVap[i][4]);
            $("input[name='basicVAPconfigTable.vapBeaconInterval']").val(selectVapVap[i][5]);
            if(parseInt(selectVapVap[i][6])==0)
            {
                $('input[name="vapWEPsecurityConfigTable.vapWEPmode"]').filter("[value='0']").attr('checked', true);
            }
            else if(parseInt(selectVapVap[i][6])==1)
            {
                $('input[name="vapWEPsecurityConfigTable.vapWEPmode"]').filter("[value='1']").attr('checked', true);
            }
            else
            {
                $('input[name="vapWEPsecurityConfigTable.vapWEPmode"]').filter("[value='2']").attr('checked', true);
            }
            if(parseInt(selectVapVap[i][7])==1)
            {
                $('input[name="vapWEPsecurityConfigTable.vapWEPprimaryKey"]').filter("[value='1']").attr('checked', true);
            }
            else if(parseInt(selectVapVap[i][7])==2)
            {
                $('input[name="vapWEPsecurityConfigTable.vapWEPprimaryKey"]').filter("[value='2']").attr('checked', true);
            }
            else if(parseInt(selectVapVap[i][7])==3)
            {
                $('input[name="vapWEPsecurityConfigTable.vapWEPprimaryKey"]').filter("[value='3']").attr('checked', true);
            }
            else
            {
                $('input[name="vapWEPsecurityConfigTable.vapWEPprimaryKey"]').filter("[value='4']").attr('checked', true);
            }
             $("input[name='vapWEPsecurityConfigTable.vapWEPkey1']").val(selectVapVap[i][8]);
             $("input[name='vapWEPsecurityConfigTable.vapWEPkey2']").val(selectVapVap[i][9]);
             $("input[name='vapWEPsecurityConfigTable.vapWEPkey3']").val(selectVapVap[i][10]);
             $("input[name='vapWEPsecurityConfigTable.vapWEPkey4']").val(selectVapVap[i][11]);

            if(parseInt(selectVapVap[i][12])==0)
            {
                $('input[name="vapWPAsecurityConfigTable.vapWPAmode"]').filter("[value='0']").attr('checked', true);
            }
            else if(parseInt(selectVapVap[i][12])==1)
            {
                $('input[name="vapWPAsecurityConfigTable.vapWPAmode"]').filter("[value='1']").attr('checked', true);
            }
            else if(parseInt(selectVapVap[i][12])==2)
            {
                $('input[name="vapWPAsecurityConfigTable.vapWPAmode"]').filter("[value='2']").attr('checked', true);
            }
            else
            {
                $('input[name="vapWPAsecurityConfigTable.vapWPAmode"]').filter("[value='3']").attr('checked', true);
            }  
            if(parseInt(selectVapVap[i][13])==0)
            {
                $('input[name="vapWPAsecurityConfigTable.vapWPAcypher"]').filter("[value='0']").attr('checked', true);
            }
            $("input[name='vapWPAsecurityConfigTable.vapWPArekeyInterval']").val(selectVapVap[i][14]);
            $("input[name='vapWPAsecurityConfigTable.vapWPAmasterReKey']").val(selectVapVap[i][15]);
            $("input[name='vapWPAsecurityConfigTable.vapWEPrekeyInt']").val(selectVapVap[i][16]);     
            
            if(parseInt(selectVapVap[i][17])==0)
            {
                $('input[name="vapWPAsecurityConfigTable.vapWPAkeyMode"]').filter("[value='0']").attr('checked', true);
            }
            else
            {
                $('input[name="vapWPAsecurityConfigTable.vapWPAkeyMode"]').filter("[value='1']").attr('checked', true);
            } 
            $('input[name="vapWPAsecurityConfigTable.vapWPAconfigPSKPassPhrase"]').val(selectVapVap[i][18]);
            if(parseInt(selectVapVap[i][19])==0)
            {
                $('input[name="vapWPAsecurityConfigTable.vapWPArsnPreAuth"]').filter("[value='0']").attr('checked', true);
            }
            else
            {
                $('input[name="vapWPAsecurityConfigTable.vapWPArsnPreAuth"]').filter("[value='1']").attr('checked', true);
            }       
            $("input[name='vapWPAsecurityConfigTable.vapWPArsnPreAuthInterface']").val(selectVapVap[i][20]);
            $("input[name='vapWPAsecurityConfigTable.vapWPAeapReAuthPeriod']").val(selectVapVap[i][21]);
            $("input[name='vapWPAsecurityConfigTable.vapWPAserverIP']").val(selectVapVap[i][22]);
            $("input[name='vapWPAsecurityConfigTable.vapWPAserverPort']").val(selectVapVap[i][23]);
            $("input[name='vapWPAsecurityConfigTable.vapWPAsharedSecret']").val(selectVapVap[i][24]);
            if(i==1)
            {
                $('input[name="basicVAPconfigTable.vapSecurityMode"]').filter("[value='"+selectVapVap[i][25]+"']").attr('checked', true);
                if(parseInt(selectVapVap[i][26])==0)
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='0']").attr('checked', true);
                }
                else
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='1']").attr('checked', true);
                }
                $("input[name='basicVAPconfigTable.vlanId']").val(selectVapVap[i][27]);
                $("input[name='basicVAPconfigTable.vlanPriority']").val(selectVapVap[i][28]); 
            }
            else if(i==2)
            {
                $('input[name="basicVAPconfigTable.vapSecurityMode"]').filter("[value='"+selectVapVap[i][29]+"']").attr('checked', true);
                if(parseInt(selectVapVap[i][30])==0)
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='0']").attr('checked', true);
                }
                else
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='1']").attr('checked', true);
                }
                $("input[name='basicVAPconfigTable.vlanId']").val(selectVapVap[i][31]);
                $("input[name='basicVAPconfigTable.vlanPriority']").val(selectVapVap[i][32]);
            }
            else if(i==3)
            {
                $('input[name="basicVAPconfigTable.vapSecurityMode"]').filter("[value='"+selectVapVap[i][33]+"']").attr('checked', true);
                if(parseInt(selectVapVap[i][34])==0)
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='0']").attr('checked', true);
                }
                else
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='1']").attr('checked', true);
                }
                $("input[name='basicVAPconfigTable.vlanId']").val(selectVapVap[i][35]);
                $("input[name='basicVAPconfigTable.vlanPriority']").val(selectVapVap[i][36]);
            }
            else if(i==4)
            {
                $('input[name="basicVAPconfigTable.vapSecurityMode"]').filter("[value='"+selectVapVap[i][37]+']').attr('checked', true);
                if(parseInt(selectVapVap[i][38])==0)
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='0']").attr('checked', true);
                }
                else
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='1']").attr('checked', true);
                }
                $("input[name='basicVAPconfigTable.vlanId']").val(selectVapVap[i][39]);
                $("input[name='basicVAPconfigTable.vlanPriority']").val(selectVapVap[i][40]);
                
            }
            else if(i==5)
            {
                $('input[name="basicVAPconfigTable.vapSecurityMode"]').filter("[value='"+selectVapVap[i][41]+"']").attr('checked', true);
                if(parseInt(selectVapVap[i][42])==0)
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='0']").attr('checked', true);
                }
                else
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='1']").attr('checked', true);
                }
                $("input[name='basicVAPconfigTable.vlanId']").val(selectVapVap[i][43]);
                $("input[name='basicVAPconfigTable.vlanPriority']").val(selectVapVap[i][44]);
                
            }
            else if(i==6)
            {
                $('input[name="basicVAPconfigTable.vapSecurityMode"]').filter("[value='"+selectVapVap[i][45]+']').attr('checked', true);
                if(parseInt(selectVapVap[i][46])==0)
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='0']").attr('checked', true);
                }
                else
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='1']").attr('checked', true);
                }
                $("input[name='basicVAPconfigTable.vlanId']").val(selectVapVap[i][47]);
                $("input[name='basicVAPconfigTable.vlanPriority']").val(selectVapVap[i][48]);
                
            }
            else if(i==7)
            {
                $('input[name="basicVAPconfigTable.vapSecurityMode"]').filter("[value='"+selectVapVap[i][49]+"']").attr('checked', true);
                if(parseInt(selectVapVap[i][50])==0)
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='0']").attr('checked', true);
                }
                else
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='1']").attr('checked', true);
                }
                $("input[name='basicVAPconfigTable.vlanId']").val(selectVapVap[i][51]);
                $("input[name='basicVAPconfigTable.vlanPriority']").val(selectVapVap[i][52]);
                
            }
            else if(i==8)
            {
                $('input[name="basicVAPconfigTable.vapSecurityMode"]').filter("[value='"+selectVapVap[i][53]+"']").attr('checked', true);
                if(parseInt(selectVapVap[i][54])==0)
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='0']").attr('checked', true);
                }
                else
                {
                    $('input[name="basicVAPconfigTable.vapMode"]').filter("[value='1']").attr('checked', true);
                }
                $("input[name='basicVAPconfigTable.vlanId']").val(selectVapVap[i][55]);
                $("input[name='basicVAPconfigTable.vlanPriority']").val(selectVapVap[i][56]);
                
            }
            
            if(isRepeater==true)
            {
            	if(i==1)
            	{
            		$("#wepradio").hide();
            		$("#wepdiv").hide();
            		
            	}
            	else
            	{
            		$("#wepradio").show();
            		if($("input[name='sec_wep']").attr("checked"))
            		{
            		        $("div#wepdiv").show();
            		}
            		else
            		{
            		       $("div#wepdiv").hide();
            		}
            	}
            
            }
            else
            {
            	if(i==1)
            	{
            		$("#wepradio").show();
            		if($("input[name='sec_wep']").attr("checked"))
            		{
            		        $("div#wepdiv").show();
            		}
            		else
            		{
            		       $("div#wepdiv").hide();
            		}
            	}
            	else
            	{
            		$("#wepradio").hide();
            		$("div#wepdiv").hide();
            	}
            }
            
            break; 
          }
          else
          {
            continue;
          }
    }
    gatinIndex();
    agreegation();
    txChainMask();
    rxChainMask();
    Thresholdchange();
    Securitymode();
    WPAevents();
}

function vapVapSelection()
{
    var host_id = $("input[name='host_id']").val();
    var device_type = $("input[name='device_type']").val(); 
    
    $.ajax({
            type:"post",
            url:"vap_vap_select.py?host_id=" + host_id +"&device_type="+device_type,
            success:function(result)
            {
                result = eval(result);
                selectVapVap = [0];
                for(var i in result)
                {
                     selectVapVap[selectVapVap.length] = result[i] ;
                }
                 vapVapForm();
            }
        });

}



function radioEnableDisable()
{
    if(parseInt($("input[name='radioState']").val())==1)
    {
        $('input[name="radioSetup.radioState"]').filter("[value='1']").attr('checked', true);
    }
    else if(parseInt($("input[name='radioState']").val())==0)
    {
        $('input[name="radioSetup.radioState"]').filter("[value='0']").attr('checked', true);
    }
    else
    {
         $('input[name="radioSetup.radioState"]').filter("[value='1']").attr('checked', true);
    }

}

function radioStartUpMode()
{
    if(parseInt($("input[name='startupmode']").val())==0)
    {
        $('input[name="radioSetup.radioAPmode"]').filter("[value='0']").attr('checked', true);
    }
    else if(parseInt($("input[name='startupmode']").val())==1)
    {
        $('input[name="radioSetup.radioAPmode"]').filter("[value='1']").attr('checked', true);
    }
    else if(parseInt($("input[name='startupmode']").val())==2)
    {
        $('input[name="radioSetup.radioAPmode"]').filter("[value='2']").attr('checked', true);
    }
    else if(parseInt($("input[name='startupmode']").val())==3)
    {
        $('input[name="radioSetup.radioAPmode"]').filter("[value='3']").attr('checked', true);
    }    
    else if(parseInt($("input[name='startupmode']").val())==4)
    {
        $('input[name="radioSetup.radioAPmode"]').filter("[value='4']").attr('checked', true);
    }        
    else if(parseInt($("input[name='startupmode']").val())==5)
    {
        $('input[name="radioSetup.radioAPmode"]').filter("[value='5']").attr('checked', true);
    }            
    else
    {
         $('input[name="radioSetup.radioAPmode"]').filter("[value='1']").attr('checked', true);
    }
}

function manageVlan()
{
    if(parseInt($("input[name='managevlan']").val())==0)
    {
        $('input[name="radioSetup.radioManagementVLANstate"]').filter("[value='0']").attr('checked', true);
    }
    else if(parseInt($("input[name='managevlan']").val())==1)
    {
        $('input[name="radioSetup.radioManagementVLANstate"]').filter("[value='1']").attr('checked', true);
    }
    else
    {
        $('input[name="radioSetup.radioManagementVLANstate"]').filter("[value='1']").attr('checked', true);
    }
}


function gatinIndex()
{
    if(parseInt($("input[name='gatingindex']").val())==0)
    {
        $('input[name="radioSetup.radioGatingIndex"]').filter("[value='0']").attr('checked', true);
    }
    else if(parseInt($("input[name='gatingindex']").val())==1)
    {
        $('input[name="radioSetup.radioGatingIndex"]').filter("[value='1']").attr('checked', true);
    }
    else
    {
        $('input[name="radioSetup.radioGatingIndex"]').filter("[value='1']").attr('checked', true);
    }
}

function agreegation()
{
    if(parseInt($("input[name='aggregation']").val())==0)
    {
        $('input[name="radioSetup.radioAggregation"]').filter("[value='0']").attr('checked', true);
    }
    else if(parseInt($("input[name='aggregation']").val())==1)
    {
        $('input[name="radioSetup.radioAggregation"]').filter("[value='1']").attr('checked', true);
    }
    else
    {
        $('input[name="radioSetup.radioAggregation"]').filter("[value='1']").attr('checked', true);
    }
}

function channelWidth()
{
    if(parseInt($("input[name='channelwidth']").val())==0)
    {
        $('input[name="radioSetup.radioChannelWidth"]').filter("[value='0']").attr('checked', true);
    }
    else if(parseInt($("input[name='channelwidth']").val())==1)
    {
        $('input[name="radioSetup.radioChannelWidth"]').filter("[value='1']").attr('checked', true);
    }
    else
    {
        $('input[name="radioSetup.radioChannelWidth"]').filter("[value='1']").attr('checked', true);
    }
}

function txChainMask()
{
    if(parseInt($("input[name='txchainmask']").val())==0)
    {
        $('input[name="radioSetup.radioTXChainMask"]').filter("[value='0']").attr('checked', true);
    }
    else if(parseInt($("input[name='txchainmask']").val())==1)
    {
        $('input[name="radioSetup.radioTXChainMask"]').filter("[value='1']").attr('checked', true);
    }
    else if(parseInt($("input[name='txchainmask']").val())==2)
    {
        $('input[name="radioSetup.radioTXChainMask"]').filter("[value='2']").attr('checked', true);
    }
    else
    {
        $('input[name="radioSetup.radioTXChainMask"]').filter("[value='2']").attr('checked', true);
    }
}

function rxChainMask()
{
    if(parseInt($("input[name='rxchainmask']").val())==0)
    {
        $('input[name="radioSetup.radioRXChainMask"]').filter("[value='0']").attr('checked', true);
    }
    else if(parseInt($("input[name='rxchainmask']").val())==1)
    {
        $('input[name="radioSetup.radioRXChainMask"]').filter("[value='1']").attr('checked', true);
    }
    else if(parseInt($("input[name='rxchainmask']").val())==2)
    {
        $('input[name="radioSetup.radioRXChainMask"]').filter("[value='2']").attr('checked', true);
    }
    else
    {
        $('input[name="radioSetup.radioRXChainMask"]').filter("[value='2']").attr('checked', true);
    }
}

function upnpServer()
{
    if(parseInt($("input[name='upnpserver']").val())==0)
    {
        $('input[name="services.upnpServerStatus"]').filter("[value='0']").attr('checked', true);
    }
    else if(parseInt($("input[name='upnpserver']").val())==1)
    {
        $('input[name="services.upnpServerStatus"]').filter("[value='1']").attr('checked', true);
    }
    else
    {
        $('input[name="services.upnpServerStatus"]').filter("[value='1']").attr('checked', true);
    }
}

function sysLog()
{
    if(parseInt($("input[name='systemlog']").val())==0)
    {
        $('input[name="services.systemLogStatus"]').filter("[value='0']").attr('checked', true);
    }
    else if(parseInt($("input[name='systemlog']").val())==1)
    {
        $('input[name="services.systemLogStatus"]').filter("[value='1']").attr('checked', true);
    }
    else
    {
        $('input[name="services.systemLogStatus"]').filter("[value='1']").attr('checked', true);
    }
}

function aclState()
{
    if(parseInt($("input[name='aclState']").val())==0)
    {
        $('input[name="basicACLconfigTable.aclState"]').filter("[value='0']").attr('checked', true);
    }
    else if(parseInt($("input[name='aclState']").val())==1)
    {
        $('input[name="basicACLconfigTable.aclState"]').filter("[value='1']").attr('checked', true);
    }
    else
    {
        $('input[name="basicACLconfigTable.aclState"]').filter("[value='0']").attr('checked', true);
    }
}

function aclMode()
{
    if(parseInt($("input[name='aclMode']").val())==0)
    {
        $('input[name="basicACLconfigTable.aclMode"]').filter("[value='0']").attr('checked', true);
    }
    else if(parseInt($("input[name='aclMode']").val())==1)
    {
        $('input[name="basicACLconfigTable.aclMode"]').filter("[value='1']").attr('checked', true);
    }
    else
    {
        $('input[name="basicACLconfigTable.aclMode"]').filter("[value='0']").attr('checked', true);
    }
}




var callA = null;
function chk_reconcile_status(host_id)
{
	var host_id = $("input[name='host_id']").val();
    if(callA)
    {
        clearTimeout(callA);
    }
    $.ajax({
        type:"post",
        url:"chk_reconciliation_status.py?host_id=" + host_id,
        success:function(result)
		        {
			        if(result.success == 0)
			        {
				        var json = result.result
				        if(json[0]==1)
				        {
				            reconcile_chk_status_btn = 1;
				        }
				        else if(json[0]==0)
				        {
				                reconcile_chk_status_btn = 0;
					        $("input[id='ap25_reconcile']").removeAttr("disabled");
				        }
				        else if(json[0]==2)
				        {
				            
					        if(json[1]<=35)
					        {
						        $().toastmessage('showWarningToast',json[1]+"% Done.Please Again Reconcile The Device");
					        }
					        else if(json[1]<=90)
					        {
						        $().toastmessage('showWarningToast',json[1]+"% Done.Please Again Reconcile The Device");
					        }
					        else
					        {
						        $().toastmessage('showSuccessToast','Reconcilation Done SuccessFully');
					        }
					        deviceList();
					        $("input[id='odu16_reconcile']").removeAttr("disabled");
				        }
			        }
			        else
			        {
			                $().toastmessage('showErrorToast',result.result);
			        }
		        callA = setTimeout(function()
		        {
			        chk_reconcile_status(host_id);

		        },timeSlot);
		     }
         });
}

function reconciliation_chk()
{
    
    var host_id = $("input[name='host_id']").val();
    if(reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null)
    {
        spinStart($spinLoading,$spinMainLoading);
        $.ajax({
	        type:"post",
	        url:"chk_reconciliation_status.py?host_id=" + host_id,
	        success:function(result)
		        {	
			        
			        if(result.success == 0)	
			        {
				        var json = result.result
				        if(json[0]==0)
				        {
					        reconcile_chk_status_btn = 0;
					        chk_common_rec(host_id);
					        spinStop($spinLoading,$spinMainLoading);
				        }
				        else if(json[0]==1)
				        {
					        spinStop($spinLoading,$spinMainLoading);
					        reconcile_chk_status_btn = 1;
					        $.prompt('Reconciliation is already Running.Please Wait',{ buttons:{Ok:true}, prefix:'jqismooth'});
				        }
				        else if(json[0]==2)
				        {
					
					        if(json[1]<=35)
					        {
						        $().toastmessage('showWarningToast',json[1]+"% Done.Please Again Reconcile The Device");
					        }
					        else if(json[1]<=90)
					        {
						        $().toastmessage('showWarningToast',json[1]+"% Done.Please Again Reconcile The Device");
					        }
					        else
					        {
						        $().toastmessage('showSuccessToast','Reconcilation Done SuccessFully');
					        }
					        reconcile_chk_status_btn = 0;
					        deviceList();	
					        spinStop($spinLoading,$spinMainLoading);
				        }
				        else
				        {
					        $.prompt('No Hosts Exist',{ buttons:{Ok:true}, prefix:'jqismooth'});
				        }
			        }
		        }
	        });
        }
        else
        {
	        $.prompt('Reconciliation is Running.Please Wait',{ buttons:{Ok:true}, prefix:'jqismooth'});	
        }
        return false;
}


function chk_common_rec(host_id)
{
        $.ajax({
                type: "get",
                url : "chk_common_reconcile.py?host_id="+host_id,
                success:function(result){
                        if(parseInt(result.success)==0)
                        {
                                common_rec()
                        }  
                        else
                        {
                                $().toastmessage('showWarningToast',result.result);
                        }      
                }
               });
            return false;
}
function common_rec()
{        
        text_name = $("a.active").text();
        var text_val = text_name.replace(/\s/g,"%20");
        $.colorbox(
	{
		href:"local_reconciliation.py?textname="+text_val,
		title: "Form Reconciliation",
		opacity: 0.4,
		maxWidth: "80%",
		width:"500px",
		height:"250px"
	});
}

function reconcileForm(obj,formid)
{
        formObj = $(obj);
        formId = $("#"+formid);
        $.prompt('Device Configuration data would be Synchronized with the UNMP server Database',{ buttons:{Ok:true,Cancel:false}, prefix:'jqismooth',callback: AP25reconciliation});
        return false;
}

function AP25reconciliation(v,m)
{
	if(v != undefined && v==true)
	{
		spinStart($spinLoading,$spinMainLoading);
		var host_id = $("input[name='host_id']").val();
		var device_type_id = $("input[name='device_type']").val();
		data = $(formId).serialize();
	        form_rec = $("input[name='form_rec']:checked").val();
	        var divId = $("a.active").attr("href");
	        //var divId = attrText.replace("#","");
	        formName = $(divId).find("input[name='common_rec']").attr("form_name");
	        tableName = $(divId).find("input[name='common_rec']").attr("tablename");
                if(parseInt(form_rec)==0)
                {
                        $.ajax({
			                type: "get",
			                url : "common_reconcile.py?host_id="+host_id+"&device_type="+device_type_id+"&tableName="+tableName,
			                data:data,
			                success:function(result)
			                {
			                                if(parseInt(result.success)==0)
			                                {
		                                                $.ajax({
		                                                        type: "get",
		                                                        url : "ap_form_reconcile.py?formName="+formName+"&host_id="+host_id+"&device_type="+device_type_id,
		                                                        success:function(htmlResult)
		                                                        {
		                                                                $(divId).html();
		                                                                $(divId).html(htmlResult);
		                                                                functionsCall();
		                                                                clearTimeout(callA);
		                                                                callA=null;
		                                                                chkRadioStatus();
		                                                                
		                                                        }
		                                                      });
                                                                $().toastmessage('showSuccessToast', text_name+" Reconciliation done successfully");
                                                        }
                                                        else
			                                {
			                                        $().toastmessage('showErrorToast',result.result);
			                                }
			                                $.colorbox.close();
			                                spinStop($spinLoading,$spinMainLoading);
                                        }
                                     });
                }
                else if(form_rec==undefined)
                {
                        $().toastmessage('showErrorToast',"Please select the reconciliation mode");
                        spinStop($spinLoading,$spinMainLoading);
                }
                else
                {
		        $.ajax({
		            type: "post",
		            url : "ap25_reconcilation.py?host_id=" + host_id +"&device_type_id="+device_type_id,
		            success:function(result){
	                           if(result.success == 0)
						        {
							        var json = result.result
							        for(var node in json)
							        {
								        if(node<=35)
								        {
									        $().toastmessage('showWarningToast',node+"% reconciliation done for device "+json[node][0]+"("+json[node][1]+")"+".Please reconcile the device again");
								        }
								        else if(node<=90)
								        {
									        $().toastmessage('showWarningToast',node+"% reconciliation done for device "+json[node][0]+"("+json[node][1]+")"+".Please reconcile the device again");
								        }
								        else
								        {
									        $().toastmessage('showSuccessToast',"Reconciliation done successfully for device "+json[node][0]+"("+json[node][1]+")");
								        }
								        
								        deviceList();
								        break;
							        }
						        }
						        else
						        {
							        $().toastmessage('showErrorToast',result.result);
						        }
						        $.colorbox.close();
						        spinStop($spinLoading,$spinMainLoading);
					        }
			        });
		     }
	}

}


function functionsCall()
{
        radioEnableDisable();
	radioStartUpMode();
	manageVlan();
	gatinIndex();
	agreegation();
	channelWidth();
	txChainMask();
        rxChainMask();
        upnpServer();
	sysLog();
        aclState();
        aclMode();
        vapAclSelection(); 
        Toggleradio();
        selectedVap();
        getRepaeaterValue();               	    
        Thresholdchange();
        Securitymode();
        WPAevents();
        Services();
        ACL();
        Macadd();
        vapVapSelection();
        vapModeHideShow();
        vlanHideShow();        
        $("select#rts_mode").change(function(){
	        Thresholdchange();
        });
        $("select#frag_mode").change(function(){
	        Thresholdchange();
        });
        $gridViewAPMacDataTable = $("table#showmac").dataTable({
                "bDestroy":true,
                "bJQueryUI": true,
                "bProcessing": true,
                "sPaginationType": "full_numbers",
                "aLengthMenu": [[20, 40, 60, -1],[20, 40, 60, "All"]],
                "iDisplayLength":20,
                "aaSorting": []
        });
	$gridViewAPMacDataTable.css("width","100%");
        $("#ap_acl_form").find('select[id="vapSelection.selectVap"]').change(function()
        {
            changeVapAclSelect();   
        })
        $("#ap_vap_form").find('select[id="vapselectionid"]').change(function()
        {
            vapVapSelection();   
        })

        if(isRepeater==true)
	 {
    		$("#wepradio").hide();
    		$("div#wepdiv").hide();
    	}
         else
        {    
            	$("#wepradio").show();
    		if($("#sec_wep").attr("checked"))
    		{
    		        $("div#wepdiv").show();
    		}
    		else
    		{
    		       $("div#wepdiv").hide();
    		}
    	   
       }
       $("#ap_radio_form").find('input[name="radioSetup.radioAggregation"]').click(function()
       {
                        if ($(this).attr("checked"))
                        {
                               if(parseInt($(this).val())==0)
                               {
                                
                                        $("#ap_radio_form").find("input[name='radioSetup.radioAggFrames']").attr({"disabled":true});
                                        $("#ap_radio_form").find("input[name='radioSetup.radioAggSize']").attr({"disabled":true});
                                        $("#ap_radio_form").find("input[name='radioSetup.radioAggMinSize']").attr({"disabled":true});
                               }
                               else
                               {
                                
                                        $("#ap_radio_form").find("input[name='radioSetup.radioAggFrames']").attr({"disabled":false});
                                        $("#ap_radio_form").find("input[name='radioSetup.radioAggSize']").attr({"disabled":false});
                                        $("#ap_radio_form").find("input[name='radioSetup.radioAggMinSize']").attr({"disabled":false});
                               }
                      }
       });
        $("#ap_radio_form").find('input[name="radioSetup.radioAggregation"]:checked').click();
}

function commitFlashConfirm()
{
	$.prompt('Do you want to store this configuration permanently on the device?\n Click Ok to confirm.',{ buttons:{Ok:true,Cancel:false}, prefix:'jqismooth',callback:commitToFlash});
}

function commitToFlash(v,m)
{
	if(v != undefined && v==true)
	{
		spinStart($spinLoading,$spinMainLoading);
		var host_id = $("input[id='host_id']").val();	
		$.ajax({
				type:"post",
				url:"commit_to_flash.py?host_id=" + host_id,
				success:function(result)
				{
					if(result.success==0)
					{
							$().toastmessage('showSuccessToast',result.result);
					}
					else
					{
						$().toastmessage('showErrorToast',result.result);						
					}
					spinStop($spinLoading,$spinMainLoading);
				}
		});
		return false
	}

}

function rebootConfirm()
{
    $.prompt('This will cause device to reboot.It may take several minutes.\nAre you sure you want to do this?',{ buttons:{Ok:true,Cancel:false}, prefix:'jqismooth',callback:reboot});
}

function reboot(v,m)
{
	if(v != undefined && v==true)
	{
		spinStart($spinLoading,$spinMainLoading);
		var host_id = $("input[id='host_id']").val();	
		$.ajax({
				type:"post",
				url:"ap25_reboot.py?host_id=" + host_id,
				success:function(result)
				{
					if(result.success==0)
					{
						$().toastmessage('showSuccessToast',result.result);
					}
					else
					{
						$().toastmessage('showErrorToast',result.result);						
					}
					spinStop($spinLoading,$spinMainLoading);
				}
		});
		return false
	}

}

function apScan()
{
	var host_id = $("input[id='host_id']").val();
            $.colorbox(
            {
                    href:"ap_scan.py?host_id=" + host_id,
                    title : "AP Scan",
                    opacity: 0.4,
                    maxWidth: "80%",
                    width:"700px",
                    height:"400px",
                    overlayClose:false
            });
}

function Toggleradio()
{
	if ($("input#startup_standard").attr("checked") || $("input#startup_rootap").attr("checked") || $("input#startup_client").attr("checked"))
	{
		$('select[id="radioSetup.numberofVAPs"] option[value="1"]').attr("selected",true);
		$('select[id="radioSetup.numberofVAPs"]').attr("disabled",true);
	}
	else if ($("input#startup_repeater").attr("checked"))
	{
		$('select[id="radioSetup.numberofVAPs"] option[value="2"]').attr("selected",true);
		$('select[id="radioSetup.numberofVAPs"]').attr("disabled",true);
	}
	if($("#startup_multi").attr("checked") || $("input#startup_multivlan").attr("checked"))
	{
	    var selectVapValue= $('select[name="radioSetup.numberofVAPs"]').val();
		$("select[id='radioSetup.numberofVAPs'] option[value='"+selectVapValue+"']").attr("selected",true);
		$('select[id="radioSetup.numberofVAPs"]').attr("disabled",false);
	}
	if($("input#startup_multivlan").attr("checked"))
	{
		$("#manage_vlan_div").show();
	}
	else
	{
		$("#manage_vlan_div").hide();
	}
	if($("input#startup_repeater").attr("checked") || $("input#startup_client").attr("checked"))
	{
	    $('select[name="radioSetup.radioChannel"]').attr("disabled",true);
	}
	else
	{
		$('select[name="radioSetup.radioChannel"]').attr("disabled",false);
	}

}

function vapModeHideShow()
{
    if(parseInt($("input[name='radioSetup.radioAPmode']:checked").val())==4)
    {
        $("#vap_mode").show();
        $("#vap_mode").find("input").removeAttr("disabled");
    }
    else
    {
        $("#vap_mode").hide();
        $("#vap_mode").find("input").attr({'disabled':true});
    }
    
}

function vlanHideShow()
{
    if(parseInt($("input[name='radioSetup.radioAPmode']:checked").val())==5)
    {
        $("#vlan_id").show();
        $("#vlan_id").find("input").removeAttr('disabled');
        $("#vlan_priority").show();
        $("#vlan_priority").find("input").removeAttr('disabled');

    }
    else
    {
        $("#vlan_id").hide();
        $("#vlan_id").find("input").attr({'disabled':true});
        $("#vlan_priority").hide();
        $("#vlan_priority").find("input").attr({'disabled':true});
    }
    
}


function Thresholdchange()
{
	if($("#rts_mode").val()=="1")
	{
		$("input[id='basicVAPconfigTable.vapRTSthresholdValue']").show();
	}
	else
	{
		$("input[id='basicVAPconfigTable.vapRTSthresholdValue']").hide();
	}
	if($("#frag_mode").val()=="1")
	{
		$("input[id='basicVAPconfigTable.vapFragmentationThresholdValue']").show();
	}
	else
	{
		$("input[id='basicVAPconfigTable.vapFragmentationThresholdValue']").hide();
	}
}

function Securitymode()
{
	if($("#sec_open").attr("checked"))
	{
		$("#opendiv").show();
	}
	else
	{
		$("#opendiv").hide();
	}
	
	if($("#sec_wep").attr("checked"))
	{
	        if($("select[id='vapselectionid']").val()==1)
	        {
		        $("#wepdiv").show();
		}
		else
		{
		       $("#wepdiv").hide();
		}
		if(isRepeater==true)
		{
		        if($("select[id='vapselectionid']").val()==2)
	                {
		                $("#wepdiv").show();
		        }
		        else
		        {
		               $("#wepdiv").hide();
		        }        
		}
	}
	else
	{
		$("div#wepdiv").hide();
	}

	if($("#sec_wpa").attr("checked"))
	{
		$("#wpadiv").show();
	}
	else
	{
		$("#wpadiv").hide();
	}
}


function WPAevents()
{
	if($("#chk_PersonalKey").attr("checked"))
	{
		$("#personalShared").find("input").attr("disabled",false);
	}
	else
	{
		$("#personalShared").find("input").attr("disabled",true);
	}
	if($("#chk_EnterpriseKey").attr("checked"))
	{
		$("#enterprise").find("input").attr("disabled",false);
		$("#personalShared").find("input").attr("disabled",true);
	}
	else
	{
		$("#enterprise").find("input").attr("disabled",true);
		$("#enterprise").find("input").attr("checked",false);
	}
	if($("#sec_802").attr("checked"))
	{
		$("#chk_PersonalKey").attr("disabled",true);
		$("#chk_PersonalKey").attr("checked",false);
		$("#personalShared").find("input").attr("disabled",true);
		$("#enterprise").find("input").attr("disabled",false);
		$("#chk_EnterpriseKey").attr("checked",true);
		
	}
	else
	{
		$("#chk_PersonalKey").attr("disabled",false);
		$("#personalShared").find("input").attr("disabled",false);
	}

}

function ACL()
{
	if($("#acl_enabled").attr("checked"))
	{
		$("#acl_mac_type").show();
		$("#acl_mac_div").show();
	}
	if($("#acl_disabled").attr("checked"))
	{
		$("#acl_mac_type").hide();
		$("#acl_mac_div").hide();
	}
	
}

function Services()
{
	if($("#Syslog_enable").attr("checked"))
	{
		$('input[id="services.systemLogIP"]').attr("disabled",false);
		$('input[id="services.systemLogPort"]').attr("disabled",false);
	}
	else
	{
		$('input[id="services.systemLogIP"]').attr("disabled",true);
		$('input[id="services.systemLogPort"]').attr("disabled",true);
	}
}

function Macaddform()
{
	$.colorbox(
	{
		href:"acl_add_form.py",
		title : "ACL ADD",
		opacity: 0.4,
		maxWidth: "80%",
		width:"500px",
		height:"350px",
		overlayClose:false,
		onComplete:function() {
			Macadd();
		}
	});
}

function Macadd()
{
	
	if($("#single_add").attr("checked"))
	{
		$("#single_add_div").show();
		$("#multiple_add_div").find("textarea[name='mac_text']").attr({"disabled":true});
	}
	else
	{
	    $("#multiple_add_div").find("textarea[name='mac_text']").removeAttr("disabled");
		$("#single_add_div").hide();
	}
	if($("#multiple_add").attr("checked"))
	{
	    $("#single_add_div").find("input[name='mac_text']").attr({"disabled":true});
		$("#multiple_add_div").show();
	}
	else
	{
	    $("#single_add_div").find("input[name='mac_text']").removeAttr("disabled");
		$("#multiple_add_div").hide();
	}
	
}

function Uploadmacform()
{
	$.colorbox(
	{
		href:"acl_upload_form.py",
		title : "ACL Upload",
		opacity: 0.4,
		maxWidth: "80%",
		overlayClose:false
	});
	
}

function commonFormSubmit(formObj,btn)
{
	if(reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null)
	{
		//if($("#"+formObj).valid())
		if(formObj == 'acl_add_form')
		{   
		    spinStart($spinLoading,$spinMainLoading);
		    aclAddMac(formObj,btn);
		}
		else
		{
			spinStart($spinLoading,$spinMainLoading);
			CommonSetRequest(formObj,btn);
		}
	}
	else
	{
		$.prompt('Reconciliation is Running.Please Wait',{ buttons:{Ok:true}, prefix:'jqismooth'});
	}
	return false;
}


function CommonSetRequest(formObj,btn)
{
	var btnName = $(btn).attr("name");
	var btnValue = $(btn).val();
	var myForm = $("#"+formObj);
	var data = myForm.serialize()+ "&" + btnName + "=" + btnValue;
	var url = myForm.attr("action");
	var method = myForm.attr("method");
	var imgCount = myForm.find(".img-submit-button").length;
	var host_id = $("input[name='host_id']").val();
	var selected_device = $("input[name='device_type']").val();
	var essid = 0
	
    if(myForm.find("input[name='basicVAPconfigTable.vapHiddenESSIDstate']").attr("checked"))
    {
        essid = 1
    }
    else
    {
        essid = 0
    }
	if(btnValue == "Ok")
	{
	        
		myForm.find("input").removeAttr("disabled");
		myForm.find("select").removeAttr("disabled");
		myForm.find("input[id='bw_id']").attr("disabled",true);
		myForm.find("select").show();
		myForm.find("input").show();
		myForm.find("input.img-submit-button").remove();
		myForm.find("input.img-done-button").remove();
		myForm.find("input[id='id_retry']").hide();
		myForm.find("input[id='id_cancel']").hide();
		myForm.find("input[id='id_ok']").hide();
		myForm.find("input[id='id_save']").show();	
		//myForm.find('select[name="radioSetup.radioCountryCode"]').attr("disabled",true);
		spinStop($spinLoading,$spinMainLoading);	
		Services();
		Toggleradio();
		Thresholdchange();
		if(parseInt($("input[name='radioSetup.radioAggregation']:checked").val())==0)
                {                        
                        $("input[name='radioSetup.radioAggFrames']").attr({"disabled":true});
                        $("input[name='radioSetup.radioAggMinSize']").attr({"disabled":true});
                        $("input[name='radioSetup.radioAggSize']").attr({"disabled":true});
                }
                else
                {
                        $("input[name='radioSetup.radioAggFrames']").removeAttr("disabled");
                        $("input[name='radioSetup.radioAggMinSize']").removeAttr("disabled");
                        $("input[name='radioSetup.radioAggSize']").removeAttr("disabled");                                                
                }
                if(parseInt($("input[name='vapWPAsecurityConfigTable\.vapWPAkeyMode']:checked").val())==0)
                {
                        $("#personalShared").find("input").removeAttr("disabled");
                        $("#enterprise").find("input").attr({"disabled":true});
                }
                else
                {
                        $("#personalShared").find("input").attr({"disabled":true});
                        $("#enterprise").find("input").removeAttr("disabled");
                }
	}
	else if(btnValue=="Cancel")
	{
		myForm.find("input").removeAttr("disabled");
		myForm.find("input[id='bw_id']").attr("disabled",true);
		myForm.find("select").removeAttr("disabled");
		myForm.find("select").show();
		myForm.find("input.img-submit-button").remove();
		myForm.find("input.img-done-button").remove();
		myForm.find("input[id='id_retry']").hide();
		myForm.find("input[id='id_cancel']").hide();
		myForm.find("input[id='id_ok']").hide();
		myForm.find("input[id='id_save']").show();
		spinStop($spinLoading,$spinMainLoading);
        }
	else
	{
		if(btnValue == "")
		{
			var oidValue = myForm.find("input[name='" + $(btn).attr("oid") + "']").val()
			if(oidValue==undefined)
			{
				oidValue = myForm.find("select[name='" + $(btn).attr("oid") + "']").val()	
			}
			if(formObj=="ap_vap_form")
		        {
		                vap_selection_id = $("#selectionvap_id").val();
		                vap_id = $("select[id='vapselectionid']").val();
			        data = $(btn).attr("oid") +"="+ oidValue + "&" + btnName + "=" + btnValue + "&selectionvap_id=" + vap_selection_id + "&vapselectionid=" + vap_id;
			        
	                }
	                else if(formObj=="ap_acl_form")
		        {
		                vap_selection_id = $("#vap_selection_id").val();
		                vap_id = $("select[id='vapSelection.selectVap']").val();
			        data = $(btn).attr("oid") +"="+ oidValue + "&" + btnName + "=" + btnValue + "&vap_selection_id=" + vap_selection_id + "&vapSelection.selectVap=" + vap_id;
	                }
	                else
	                {
			        data = $(btn).attr("oid") +"="+ oidValue + "&" + btnName + "=" + btnValue;
                        }
		}
		$.ajax({
				type:method,
				url:url+"?host_id="+host_id+"&device_type="+selected_device+"&essid="+essid,
				data:data,
				success:function(result)
				{
				    
					if(result.success==0 || result.success=="0")
					{
						if((btnValue == "Save") || (btnValue == "Retry"))
						{
							var json = result.result;
							myForm.find("input.img-submit-button").remove();
							myForm.find("submit.img-submit-button").remove();
							for(var node in json)
							{
							    
								var selectListName = $("select[id='"+node+"']");
								var inputTextboxName = $("input[id='"+node+"']");
								var inputradiobutton = $("input[name='"+node+"']");
								var parentDiv = inputradiobutton.parent();
								if (json[node] == 0) 
								{	
								    
									var imageCreate = $("<input/>");
									imageCreate.attr({"type":"button","title":"Done","class":"img-done-button","oid":node});
									if(node=="radioSetup.numberofVAPs")
									{
									     selectedVap();
									}
									if(formObj=="ap_radio_form")
									{
									        Toggleradio();
									}
									if(node=="radioSetup.radioAPmode")
									{
									     vapModeHideShow();
									     vlanHideShow();
									} 
									inputTextboxName.attr({"disabled":true});
									selectListName.attr({"disabled":true});
									inputradiobutton.attr({"disabled":true});
									inputTextboxName.show();
									selectListName.show();
									inputradiobutton.show();
									if(node == "radioSetup.radioAPmode")
									{
										getRepaeaterValue();
									}
									setStatus = 0
									if(btnValue == "Retry")
									{
										imgCount = imgCount-1
									}
								}
								else
								{
									var imageCreate = $("<input/>");
									imageCreate.attr({"type":"button","title":json[node],
									"class":"img-submit-button","oid":node,"name":"ap_common_submit"});
									imageCreate.click(function(){
									        commonFormSubmit(formObj,this);
									});
									imageCreate.val("");
									inputTextboxName.attr({"disabled":false});
									selectListName.attr({"disabled":false});
									inputradiobutton.attr({"disabled":false});
									unSetStatus = 1
									if(btnValue=="Save")
									{
										imgCount = imgCount+1
									}
								}
								imageCreate.insertAfter(inputTextboxName);
								imageCreate.insertAfter(selectListName);
								parentDiv.append(imageCreate);
							 }
							if (imgCount >= 1)
							{
								myForm.find("input[id='id_ok']").hide();
								myForm.find("input[id='id_save']").hide();
								myForm.find("input[id='id_retry']").show();
								myForm.find("input[id='id_cancel']").show();
							}
							else
							{
								
								myForm.find("input[id='id_ok']").show();
								myForm.find("input[id='id_save']").hide();
								myForm.find("input[id='id_retry']").hide();
								myForm.find("input[id='id_cancel']").hide();
							}
						}
						else if(btnValue == "")
						{
							var json = result.result;
							var inputObj = myForm.find("input[id='"+$(btn).attr("oid")+"']");
							var imageFind = inputObj.next();
							if(inputObj.val()==undefined)
							{
								imageFind = myForm.find("select[id='"+$(btn).attr("oid")+"']").next();
							}
							imageFind.remove();
							for(var node in json)
							{	
								var selectListName = $("select[id='"+node+"']");
								var inputTextboxName = $("input[id='"+node+"']");
								var inputradiobutton = $("input[name='"+node+"']");
								var imageCreate = $("<input/>");
								if (json[node] == 0) 
								{
									imageCreate.attr({"type":"button","title":"Done","class":"img-done-button","oid":node});
									inputTextboxName.attr({"disabled":true});
									selectListName.attr({"disabled":true});
									inputradiobutton.attr({"disabled":true});
									inputTextboxName.show();
									selectListName.show();
									inputradiobutton.show();
									imgCount = imgCount-1;
								}
								else
								{
									imageCreate.attr({"type":"button","title":json[node],
									"class":"img-submit-button","oid":node,"name":"ap_common_submit"});
									imageCreate.click(function(){
									        commonFormSubmit(formObj,this);
									});
									imageCreate.val("");
									selectListName.attr({"disabled":false});
									inputTextboxName.attr({"disabled":false});
									selectListName.attr({"disabled":false});
									inputradiobutton.attr({"disabled":false});
								}
							
								$(imageCreate).insertAfter(inputTextboxName);
								$(imageCreate).insertAfter(selectListName);
								$(imageCreate).insertAfter(inputradiobutton);
								//myForm.find("input[id='ru.ra.raConfTable.guaranteedBroadcastBW']").attr({"disabled":true});
							}
							if (imgCount >= 1)
							{
								myForm.find("input[id='id_ok']").hide();
								myForm.find("input[id='id_save']").hide();
								myForm.find("input[id='id_retry']").show();
								myForm.find("input[id='id_cancel']").show();
							}
							else
							{
								myForm.find("input[id='id_ok']").show();
								myForm.find("input[id='id_save']").hide();
								myForm.find("input[id='id_retry']").hide();
								myForm.find("input[id='id_cancel']").hide();
							}
							
						}
						else if(btnValue=="Cancel")
						{
							myForm.find("input").removeAttr("disabled");
							myForm.find("input[id='bw_id']").attr("disabled",true);
							myForm.find("select").removeAttr("disabled");
							myForm.find("select").show();
							myForm.find("input.img-submit-button").remove();
							myForm.find("input.img-done-button").remove();
							myForm.find("input[id='id_retry']").hide();
							myForm.find("input[id='id_cancel']").hide();
							myForm.find("input[id='id_ok']").hide();
							myForm.find("input[id='id_save']").show();
							/*for(var node in result)
							{
								if(node=="success")
								{
									continue;
								}
								else
								{
									var inputTextboxName = $("input[id='"+node+"']");
									inputTextboxName.val(result[node]);
									$("select[id='"+node+"'] option[value='" +result[node]+"']").attr("selected",true);
								}
							}*/

						}
					}
					else
					{
						$().toastmessage('showErrorToast',result.result);
					}
					
					//myForm.find('select[name="radioSetup.radioCountryCode"]').attr("disabled",true);
					Services();
					//Toggleradio();
					selectedVap();
					Thresholdchange();
					spinStop($spinLoading,$spinMainLoading);
				}
			});
	}

}

function aclSingleDelete()
{
        var rowCount = $('#showmac').find('tr').eq(1).text();
        if (rowCount!="No data available in table")
        {
            var selected_vap = $("#ap_acl_form").find('select[id="vapSelection.selectVap"]').val();
	        var vap_selection_id = $('input[name="vap_selection_id"]').val();
	        var host_id = $("input[name='host_id']").val();
	        var selected_device = $("input[name='device_type']").val();
	        var macValues = [];
            $('#mac_chk:checked').each(function() 
            {
                macValues.push($(this).val());
            });
            if((macValues.length)>0)
            {
                spinStart($spinLoading,$spinMainLoading);
                $.ajax({
		            type: "get",
		            url : "delete_single_mac.py?host_id="+host_id+"&device_type="+selected_device+"&selected_vap="+selected_vap+"&vap_selection_id="+vap_selection_id+"&mac_text="+String(macValues),
		            success:function(result){
		                    if(result.success==0)
	                            {
	                                $().toastmessage('showSuccessToast',result.result);
	                                $.ajax({
		                                type:"post",
                                        url:"select_vap_acl.py?vap_select_id="+vap_selection_id,
                                        success:function(result)
                                        {
                                            $("#macdiv").html(result);
                                            $gridViewAPMacDataTable = $("table#showmac").dataTable({
					                            "bDestroy":true,
					                            "bJQueryUI": true,
					                            "bProcessing": true,
					                            "sPaginationType": "full_numbers",
					                            "aLengthMenu": [[20, 40, 60, -1],[20, 40, 60, "All"]],
					                            "iDisplayLength":20,
					                            "aaSorting": []
				                            });
				                        }
				                     });
	                            }
	                            else
	                            {
	                                $().toastmessage('showErrorToast',result.result);
	                            }
	                           spinStop($spinLoading,$spinMainLoading);
	                       }
	                });
            }
            else
            {
                $.prompt('Please select MAC for delete',{ buttons:{Ok:true}, prefix:'jqismooth'});
            }
        }
        else
        {
            $().toastmessage('showWarningToast',"There is no MAC to delete");
        }
}


function aclChkAllDelete()
{

    if(reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null)
    {
        var rowCount = $('#showmac').find('tr').eq(1).text();
        if (rowCount!="No data available in table")
        {
            $.prompt('This will delete all the MAC for this seleceted vap.\nAre you sure you want to do this',{ buttons:{Ok:true,Cancel:false}, prefix:'jqismooth',callback: aclAllDelete});
        }
        else
        {
            $().toastmessage('showWarningToast',"There is no MAC to delete");
        }
    }
    else
    {
        $.prompt('Reconciliation is Running.Please Wait',{ buttons:{Ok:true}, prefix:'jqismooth'});
    }
    
}

function aclAllDelete(v,m)
{
    if(v != undefined && v==true)
    {
        spinStart($spinLoading,$spinMainLoading);
        var selected_vap = $("#ap_acl_form").find('select[id="vapSelection.selectVap"]').val();
        var vap_selection_id = $('input[name="vap_selection_id"]').val();
        var host_id = $("input[name='host_id']").val();
        var selected_device = $("input[name='device_type']").val();
        $.ajax({
                type: "get",
                url : "delete_all_mac.py?host_id="+host_id+"&device_type="+selected_device+"&selected_vap="+selected_vap+"&vap_selection_id="+vap_selection_id,
                success:function(result){
                    if(result.success==0)
                    {
                        $().toastmessage('showSuccessToast',result.result);
                        $.ajax({
                            type:"post",
                        url:"select_vap_acl.py?vap_select_id="+vap_selection_id,
                        success:function(result)
                        {
                            $("#macdiv").html(result);
                            $gridViewAPMacDataTable = $("table#showmac").dataTable({
	                                "bDestroy":true,
	                                "bJQueryUI": true,
	                                "bProcessing": true,
	                                "sPaginationType": "full_numbers",
	                                "aLengthMenu": [[20, 40, 60, -1],[20, 40, 60, "All"]],
	                                "iDisplayLength":20,
	                                "aaSorting": []
                                });
                            }
                         });
                    }
                    else
                    {
                        $().toastmessage('showErrorToast',result.result);
                    }
                    spinStop($spinLoading,$spinMainLoading);
                }
             });
    }		     
}

function aclAddMac(formObj,btn)
{        
    if(reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null)
    {
	    spinStart($spinLoading,$spinMainLoading);
	    var myForm = $("#"+formObj);
	    var btnName = $(btn).attr("name");
	    var btnValue = $(btn).val();
	    var selected_vap = $("#ap_acl_form").find('select[id="vapSelection.selectVap"]').val();
	    var vap_selection_id = $('input[name="vap_selection_id"]').val();
	    var host_id = $("input[name='host_id']").val();
        var selected_device = $("input[name='device_type']").val()
		var url=myForm.attr("action");
		var method=myForm.attr("method");	
		var data = myForm.serialize()+ "&" + btnName + "=" + btnValue;	
	    $.ajax({
		    type: method,
		    url : url+"?host_id="+host_id+"&device_type="+selected_device+"&selected_vap="+selected_vap+"&vap_selection_id="+vap_selection_id,
		    data: data,
		    success:function(result){
		            if(result.success==0)
		            {
		                $("#mac_text").val("");
		                $("#multiple_add_div").find("textarea[name='mac_text']").val("");
		                $().toastmessage('showSuccessToast',result.result);
		                $.ajax({
		                    type:"post",
                            url:"select_vap_acl.py?vap_select_id="+vap_selection_id,
                            success:function(result)
                            {
                                $("#macdiv").html(result);
                                $gridViewAPMacDataTable = $("table#showmac").dataTable({
					                "bDestroy":true,
					                "bJQueryUI": true,
					                "bProcessing": true,
					                "sPaginationType": "full_numbers",
					                "aLengthMenu": [[20, 40, 60, -1],[20, 40, 60, "All"]],
					                "iDisplayLength":20,
					                "aaSorting": []
				                });
				            }
				         });
		            }
		            else
		            {
		                $().toastmessage('showErrorToast',result.result);
		            }
		        }
	    });
	    spinStop($spinLoading,$spinMainLoading);
    }
    else
    {
	    $.prompt('Reconciliation is Running.Please Wait',{ buttons:{Ok:true}, prefix:'jqismooth'});
    }
}

function radio_enable_disable(event,obj,hostId,adminStateName)
{
        spinStart($spinLoading,$spinMainLoading);
        attrValue = $(obj).attr("state");
        if(parseInt(attrValue)==0)
        {
                attrValue=1;
        }
        else
        {
                attrValue=0;
                
        }
       // event.stopPropagation();
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
	                                        $(obj).html("Radio Enabled");
	                                        radioStateChk = 1;
	                                }
	                                else
	                                {
	                                        $(obj).attr({"class":"red"});
	                                        $(obj).attr({"state":0});
	                                        $(obj).attr({"original-title":"Radio Disabled"});
	                                        $(obj).html("Radio Disabled");	 
	                                        radioStateChk = 0;                                       
	                                }
	                                        if(radioStateChk!=null)
                                                {
                                                        if(radioStateChk == 1)
                                                        {
                                                                $('input[name="radioSetup.radioState"]').filter("[value='1']").attr('checked', true);
                                                        }
                                                        else
                                                        {
                                                                $('input[name="radioSetup.radioState"]').filter("[value='0']").attr('checked', true);
                                                        }
                                                }
	                        }
	                        else
	                        {
	                                $().toastmessage('showErrorToast',result.result);
	                        }
	                 spinStop($spinLoading,$spinMainLoading);       
	                }
	                
	       });

}


$(function(){
	$("input[id='btnSearch']").click(function(){
	//call the device list function on click of search button
		deviceList();
		
	});
	$("input[id='filter_ip']").keypress(function(){
		$("input[id='filter_mac']").val("");
	})
	$("input[id='filter_mac']").keypress(function(){
	        $("input[id='filter_ip']").val("");
	})
	$("input[id='filter_ip']").ccplAutoComplete("common_ip_mac_search.py?device_type="+$("select[id='device_type']").val()+"&ip_mac_search="+1,{
                        dataType: 'json',
                        max: 30,
                        selectedItem: $("input[id='filter_ip']").val(),
                        callAfterSelect : function(obj){
                                ipSelectMacDeviceType(obj,1);
                        }
                });
                
       $("input[id='filter_mac']").ccplAutoComplete("common_ip_mac_search.py?device_type="+$("select[id='device_type']").val()+"&ip_mac_search="+0,{
                dataType: 'json',
                max: 30,
                selectedItem: $("input[id='filter_mac']").val(),
                callAfterSelect : function(obj){
                        ipSelectMacDeviceType(obj,0);
                }
        });
	deviceList();
	
	$("#filterOptions").hide();
	$("#hide_search").show();
	$("#ap_form_div").css({'margin-top':'20px'});
	$("#hide_search").toggle(function(){
		var $this = $(this);
		var $span = $this.find("span").eq(0);
		$span.removeClass("dwn");
		$span.addClass("up");
		$("#filterOptions").show();
		$this.css({
		        'background-color': "#F1F1F1",
                        'display': "block",
                        'height': '20px',
                        'position': 'static',
                        'overflow': 'hidden',
                        'width': "100%"});
                $("#ap_form_div").css({'margin-top':'76px'});
	},
	function(){
		var $this = $(this);
		var $span = $this.find("span").eq(0);
		$span.removeClass("up");
		$span.addClass("dwn");
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
                        'z-index': 1000});
                $("#ap_form_div").css({'margin-top':'20px'});
		
	});
	//$("div#container_body").css("padding-bottom","20px");
	// spin loading object
	//spinStart($spinLoading,$spinMainLoading);
	//spinStop($spinLoading,$spinMainLoading);
	/*$("#page_tip").colorbox(
	{
		href:"page_tip_odu_profiling.py",
		title: "Page Tip",
		opacity: 0.4,
		maxWidth: "80%",
		width:"650px",
		height:"600px",
		onComplte:function(){}
	});*/
	
});

var callA=null;
function chkRadioStatus()
{
        if(ipMacChange==1)
	{
	         clearTimeout(callA);
	}
        var host_id = $("input[name='host_id']").val();
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
							                radioStateChk = 1;
							        }
							        else
							        {
                                                                        imgbtn.attr({"class":"red"});
							                imgbtn.attr({"state":0});
							                imgbtn.attr({"original-title":"Radio Disabled"});							        
							                radioStateChk = 0;
							       }
						        }
						        if(radioStateChk!=null)
                                                        {
                                                                if(radioStateChk == 1)
                                                                {
                                                                        $('input[name="radioSetup.radioState"]').filter("[value='1']").attr('checked', true);
                                                                }
                                                                else
                                                                {
                                                                        $('input[name="radioSetup.radioState"]').filter("[value='0']").attr('checked', true);
                                                                }
                                                        }
						}
						callA = setTimeout(function()
						{
		
							chkRadioStatus();

						},timecheck);	
					}
                });
}



