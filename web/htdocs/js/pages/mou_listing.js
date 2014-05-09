var $gridViewDiv = null;
var $configDiv = null;
var $iframeDiv = null;
var $topBar = null;
$(function(){
	$("#page_tip").hide();
	$gridViewDiv = $("#grid_view,#hide_search");
	$configDiv = $("#iframe_configuration");
	$iframeDiv = $("#edit_configuration");
	$topBar = $("#filterOptions");
	
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
                        'width': "100%"});
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
                        'z-index': 1000});
		
	});
        $("input[id='btnSearch']").click(function(){
	//call the device list function on click of search button
		deviceList();
	})
});

function backToListing()
{
	$gridViewDiv.show();
	$configDiv.hide();
	$topBar.hide();
}

function editConfiguration(thisObj)
{
	$gridViewDiv.hide();
	$topBar.hide();
	$configDiv.show();
	var $iframe = $("<iframe/>").attr({"id":"iframe_edit_configuration","src":thisObj.attr("href")}).css({"display":"block","height":"100%","width":"100%","border":"0px none"});
	$iframeDiv.html("");
	$iframe.appendTo($iframeDiv);
}

function deviceList()
{
	// spin loading object
	// this retreive the value of ipaddress textbox
	var ip_address = $("input[id='filter_ip']").val();
	// this retreive the value of macaddress textbox
	var mac_address = $("input[id='filter_mac']").val();
	// this retreive the value of selectdevicetype from select menu
	var device_type = $("select[id='device_type']").val();
	$.ajax({ 
			type:"get",
			url:"get_mou_details.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type ,
			cache:false,
			success:function(result){
			        oTableLog = $('#device_data_table').dataTable({
			                        "bDestroy":true,
			                        "bJQueryUI": true,
			                        "bProcessing": true,
			                        "sPaginationType": "full_numbers",
			                        "bPaginate":true,
			                        "bStateSave": false,
			                        "aaData": result.result,
			                        "aoColumns": [
					                { "sTitle": "Host Alias","sWidth": "15%" },
					                { "sTitle": "Host Group" , "sClass": "center","sWidth": "15%"},
					                { "sTitle": "IP Address", "sClass": "center","sWidth": "15%" },
					                { "sTitle": "MAC Address", "sClass": "center","sWidth": "15%" },
					                { "sTitle": "Device Type", "sClass": "center","sWidth": "15%" },
					                { "sTitle": "Actions", "sClass": "center","sWidth": "15%" }
				                ]
		                        });
				backToListing();
				$("a.iframe").click(function(e){
					e.preventDefault();
					editConfiguration($(this));
				});
				$('.n-reconcile').tipsy({gravity: 'n'});
			}
        });
}
