var errorMessages = {
                        'noHost':'No Host Exist',
                        'missingDeviceType':'Please shut down the UNMP and reconcile the device',
                        'missingNodeType' : 'Node Type missing.Please reconcile the device',
                        'masterSlave' : 'Master not exist For this Device',
                        'networkUnreachable' : 'Netwrok is Unreachable.Please Try after some time.',
                        'exception' : 'System Error Occured.Contact Your Administrator.',
                        'noProfile' :"No Profiling Exist",
                        'noSite' : 'There is no site for this device',
                        'notPingMaster': 'The device is not responsive'
};

var json = {};
var link_tunnel_status = 0
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
	// this ajax return the call to function get_device_data_table which is in odu_view and pass the ipaddress,macaddress,devicetype with url  
	$.ajax({
		type:"get",
		url:"firmware_master_slave_list.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type,
		success:function(result){
					        if (result.success == 0)
					        {
					                if(result.msg == 'noProfile')
					                {
						                $("#firmware_div").html("No Host Exist");
						        }
						        else if(result.msg == 'moreProfile')
					                {
						                parent.main.location = "odu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + 
						                                "&selected_device_type=" + selected_device_type;
						        }
						        else
						        {
						                $("#firmware_div").html("");
						                var htmlText = ""
						                json = result.site
						                for(var i=0; i<json.length;i++)
						                {
						                        htmlText+="<p>" + String(json[i]["node_type"]) + ":" + String(json[i]["ip_address"]) + "</p>";
						                        if(json[i]["link_status"]!=2 || json[i]["tunnel_status"]!=1)
						                        {
						                                link_tunnel_status = link_tunnel_status + 1
						                        }
                                                                        
						                }
						                
						                $("#firmware_div").append(htmlText);
						                $("#firmware_table_div").hide();
						                if(result.msg!=1)
						                {
        						                $().toastmessage('showErrorToast',errorMessages[result.msg]);
        						        }
						                $("#select_file").toggle(function () {
						                        selectFirmwareTable();
						                },function(){ 
						                        $("#firmware_table_div").slideUp(); 
						                });
						                $("input[name='upload_new_file']").click(function(){
						                        uploadFile();
						                });
						        }       
					        }
					      spinStop($spinLoading,$spinMainLoading);  
					  }
		});
}				



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
    var device_type = $("input[name='selected_device']").val();
    $.ajax({
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
}


function uploadFile()
{
        var device_type = $("input[name='selected_device']").val();
        var host_id = $("input[name='host_id']").val();
	$.colorbox(
	{
		href:"update_firmware_view.py?host_id="+host_id+"&device_type="+device_type,
		iframe:true,
		title : "Upload File",
		opacity: 0.4,
		maxWidth: "80%",
		width:"700px",
		height:"700px",
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

$(function(){
	$("input[id='btnSearch']").click(function(){
	//call the device list function on click of search button
		deviceList();
	});
	$("input[id='filter_ip']").keypress(function(){
		$("input[id='filter_mac']").val("");
	})
	deviceList();
	
});					
