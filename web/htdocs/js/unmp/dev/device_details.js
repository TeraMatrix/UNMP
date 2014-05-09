/*
 * 
 * Author			:	Yogesh Kumar
 * Project			:	UNMP
 * Version			:	0.1
 * File Name		:	example.js
 * Creation Date	:	12-September-2011
 * Modify Date		:	12-September-2011
 * Purpose			:	Define All Required Javascript Functions
 * Require Library	:	jquery 1.4 or higher version and jquery.validate
 * Browser			:	Mozila FireFox [3.x or higher] and Chrome [all versions]
 * 
 * Copyright (c) 2011 Codescape Consultant Private Limited
 * 
 */

function performActionService(oLink, action, type, site, name1, name2) {
    var oImg = $(oLink).find("img");
    oImg.attr("src", "images/icon_reloading.gif");
    // Chrome and IE are not animating the gif during sync ajax request
    // So better use the async request here
    //get_url('nagios_action.py?action='+action+'&site='+site+'&host='+name1+'&service='+name2,actionResponseHandler, oImg);
    //oImg = null;

    $.ajax({
        type: "get",
        url: 'nagios_action.py',//actionResponseHandler, oImg,
        data: {"action": action, "site": site, "host": name1, "service": name2},
        cache: false,
        success: function (result) {
            //alert(result);
            //oLink;
            result = result.substring(1, result.length - 2);
            result = result.split("','");
            /*
             0 'OK', 1337773481, 0, 'SNMP RESPONSE : OK
             1 0
             2 33 min
             3 1 sec
             4 58 sec
             5 0.128615
             6 SNMP RESPONSE : OK ( Host Uptime - 0 Days, 0 Hours, 34 Mins, 30 Secs)'

             */
            var recTableObj = $(oLink).parent().parent();
            var td0 = $(recTableObj).find("td:eq(0)");
            var span0 = $(td0).find("span");
            $(span0).addClass("icon-" + result[1]);
            var td3 = $(recTableObj).find("td:eq(2)");
            $(td3).html(result[2]);
            var td4 = $(recTableObj).find("td:eq(3)");
            $(td4).html(result[3]);
            var td5 = $(recTableObj).find("td:eq(4)");
            $(td5).html(result[4]);
            var td6 = $(recTableObj).find("td:eq(5)");
            $(td6).html(result[5]);
            var td7 = $(recTableObj).find("td:eq(6)");
            $(td7).html(result[6]);
            oImg.attr("src", "images/icon_reload.gif");
        }
    });

}

$(function () {

    //spinStart($("#dashboard1").find("div.sm-spin"),$("#dashboard1").find("div.sm-loading"),{"left":"30px","top":"30px"},12,8,3,7,'#FFF',1,30,true);
    $("div.yo-tabs").yoTabs();

    $("#host_more_detail_button").toggle(function () {
            $("#more_details_div").show();
            $(this).find("span").html("Hide");
        },
        function () {
            $("#more_details_div").hide();
            $(this).find("span").html("More");
        });
//	$("#page_tip").colorbox(
//	{
//		href:"page_tip_device_detail.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"450px",
//		height:"350px",
//		onComplte:function(){}
//	});

});

