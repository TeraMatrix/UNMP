var drop_parent_check = false;
var $spinLoading = null;
var $spinMainLoading = null;
var click_check = 0;

$(document).ready(function () {

    // $('#area1').append('<div class="shoulddraggable" id="box1" style="width:100%;height:100px;top:0px;background-color:blue;" data-elementid="100"></div>');
    //$('#area1').append('<div class="dragDiv shoulddraggable"><h5 class="handler">Drag me</h5><div class="content">Yes, it is.</div></div>');

    // $('#area1').append('<div class="shoulddraggable" id="box2" style="width:100%;height:100px;top:100px;background-color:red;" data-elementid="100"></div>');
    $(".shoulddraggable").draggable({
        scroll: false,
        revert: "invalid",
        scope: "items",
        snap: true//,
    });
    /*.each(function(i, e) {
     $(e).data('origin', $(e).parent().attr('id'));
     });*/

    $('.hostgroup_class').droppable({
        scope: "items",
        activate: function (event, ui) {
            zindex = $("#" + ui.draggable.attr('id')).css("z-index");
            $("#" + ui.draggable.attr('id')).css("z-index", parseInt(zindex) + 5);
        },
        drop: function (event, ui) {
            // declare all id
            destination_box_id = $(this).attr('id');
            moving_host_id = ui.draggable.attr('id');
            old_parent_id = $("#" + moving_host_id).attr('parent_id');
            zindex = $("#" + ui.draggable.attr('id')).css("z-index");
            $("#" + ui.draggable.attr('id')).css("z-index", parseInt(zindex) - 5);
            //  set new parent
            click_check += 1;
            if (destination_box_id != old_parent_id) {


                drop_parent_check = true;
                $("#" + moving_host_id).attr('parent_id', destination_box_id);

                count_child_old_parent = $("div[parent_id=" + old_parent_id + "]").length;
                $("#" + old_parent_id).css("height", (count_child_old_parent) * 50); // set new height

                count_child = $("div[parent_id=" + destination_box_id + "]").length;
                $("#" + destination_box_id).css("height", (count_child) * 50); // set new height

                $("#" + destination_box_id).append($("#" + moving_host_id));
                $("#" + old_parent_id + ">#" + moving_host_id).remove();

                $("#" + moving_host_id).css("left", 0);
                $("#" + moving_host_id).css("top", 0);
                $("#" + moving_host_id).draggable('option', 'revert', 'invalid');

                //$("#"+moving_host_id).data('origin', $("#"+moving_host_id).parent().attr('id'));
                //alert("Element: "+ui.draggable.data("elementid")+" dragged into " + destination_box_id);
                //ui.draggable.text('From: ' + ui.draggable.data('origin'));
                //ui.draggable.data('origin', destination_box_id);
            }
            else {
                $("#" + moving_host_id).draggable('option', 'revert', true);
            }
        }
    })

//  $("#page_tip").colorbox(
//	{
//		href:"help_nagios_hostgroup.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"650px",
//		height:"450px"
//	});
});


function viewHostDetails(host_id) {
    click_check += 1;
    if (click_check % 2 != 0) {
        $.colorbox(
            {
                href: "nagios_host_details.py?host_id=" + host_id,
                //iframe:true,
                title: "Host details",
                opacity: 0.4,
                maxWidth: "90%",
                width: "1100px",
                height: "300px",
                overlayClose: false
            });
    }
    click_check = 0;
}


function apply_hostgroup_changes() {
    hostgroup_obj = $(".hostgroup_class");
    hostgroup_array = [];
    hostgroup_json = {};
    for (var i = 0; i < hostgroup_obj.length; i++) {

        child_hosts = $("div[parent_id=" + hostgroup_obj[i].id + "]");
        child_array = [];
        for (var j = 0; j < child_hosts.length; j++) {
            child_array[j] = child_hosts[j].id;
        }
        hostgroup_json[hostgroup_obj[i].id] = child_array;
    }
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire

    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "apply_hostgroup_host_changes.py?hostgroup_json=" + JSON.stringify(hostgroup_json),
        cache: false,
        success: function (result) {
            spinStop($spinLoading, $spinMainLoading);
            result = eval("(" + result + ")");
            if (result.success == 0 || result.success == '0') {
                $().toastmessage('showSuccessToast', "Hostgroups modified Successfully.");
            }
            else {
                $().toastmessage('showErrorToast', 'Hostgroups couldnt be modified currently.');
            }
        }
    });
}


function edit_hostgroup_service(hostgroup_id, hostgroup_alias) {
    child_hosts = $("div[parent_id=hostgroup" + hostgroup_id + "]");
    child_array = [];
    for (var i = 0; i < child_hosts.length; i++) {
        child_array[i] = child_hosts[i].id;
    }
    //$("#apply_changes_host_services").click(function(){ applyChanges(); });
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire

    $.colorbox(
        {
            href: "edit_hostgroup_service_details.py?hostgroup_id=" + hostgroup_id + "&child_hosts=" + child_array + "&hostgroup_alias=" + hostgroup_alias,
            title: hostgroup_alias,
            opacity: 0.4,
            maxWidth: "90%",
            width: "500px",
            height: "300px",
            overlayClose: false,
            onComplete: function () {
                $("#snmp_uptime_service_time").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Time', minWidth: 50});
                $("#snmp_uptime_hosts_list").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select Hosts', minWidth: 50}).multiselectfilter();
                $("#snmp_uptime_hosts_list").multiselect("checkAll");

                $("#statistics_service_time").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Time', minWidth: 50});
                $("#statistics_service_hosts_list").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select Hosts', minWidth: 50}).multiselectfilter();
                $("#statistics_service_hosts_list").multiselect("checkAll");


                function applyChanges() {
                    if (($("#statistics_service_hosts_list").val() != "None" && $("#statistics_service_hosts_list").val() != null) || ($("#snmp_uptime_hosts_list").val() != "None" && $("#snmp_uptime_hosts_list").val() != null)) {

                        hosts_snmp_uptime_array = $("#snmp_uptime_hosts_list").val();
                        selected_snmp_uptime_time = $("#snmp_uptime_service_time").val();

                        hosts_service_hosts_array = $("#statistics_service_hosts_list").val();
                        selected_service_hosts_time = $("#statistics_service_time").val();
                        spinStart($spinLoading, $spinMainLoading);
                        $.ajax({
                            type: "get",
                            url: "apply_nagios_hostgroup_changes.py?hostgroup_id=" + hostgroup_id + "&hosts_snmp_uptime_array=" + hosts_snmp_uptime_array + "&selected_snmp_uptime_time=" + selected_snmp_uptime_time + "&hosts_service_hosts_array=" + hosts_service_hosts_array + "&selected_service_hosts_time=" + selected_service_hosts_time,
                            cache: false,
                            success: function (result) {
                                result = eval("(" + result + ")");
                                if (result.success == 0 || result.success == '0') {
                                    spinStop($spinLoading, $spinMainLoading);
                                    $().toastmessage('showSuccessToast', "Servcies modified Successfully.");
                                    if (hosts_service_hosts_array != null) {
                                        for (var i = 0; i < hosts_service_hosts_array.length; i++) {
                                            //if($("#service_box_"+hosts_service_hosts_array[i]+"_statistics").html()!="-")
                                            //{
                                            if (selected_service_hosts_time == 518400) {
                                                $("#service_box_" + hosts_service_hosts_array[i] + "_statistics").html("Y");
                                            }
                                            else if (selected_service_hosts_time == 43200) {
                                                $("#service_box_" + hosts_service_hosts_array[i] + "_statistics").html("M");
                                            }
                                            else if (selected_service_hosts_time == 1440) {
                                                $("#service_box_" + hosts_service_hosts_array[i] + "_statistics").html("D");
                                            }
                                            else {
                                                $("#service_box_" + hosts_service_hosts_array[i] + "_statistics").html(selected_service_hosts_time);
                                            }
                                            //$("#service_box_"+hosts_service_hosts_array[i]+"_statistics").html(selected_service_hosts_time);
                                            //}
                                        }
                                    }
                                    if (hosts_snmp_uptime_array) {
                                        for (var i = 0; i < hosts_snmp_uptime_array.length; i++) {
                                            //if($("#service_box_"+hosts_snmp_uptime_array[i]+"_uptime").html()!="-")
                                            //{
                                            //$("#service_box_"+hosts_snmp_uptime_array[i]+"_uptime").html(selected_snmp_uptime_time);
                                            if (selected_snmp_uptime_time == 518400) {
                                                $("#service_box_" + hosts_snmp_uptime_array[i] + "_uptime").html("Y");
                                            }
                                            else if (selected_snmp_uptime_time == 43200) {
                                                $("#service_box_" + hosts_snmp_uptime_array[i] + "_uptime").html("M");
                                            }
                                            else if (selected_snmp_uptime_time == 1440) {
                                                $("#service_box_" + hosts_snmp_uptime_array[i] + "_uptime").html("D");
                                            }
                                            else {
                                                $("#service_box_" + hosts_snmp_uptime_array[i] + "_uptime").html(selected_snmp_uptime_time);
                                            }
                                            //}
                                        }
                                    }
                                    $.colorbox.close();
                                }
                                else {
                                    spinStop($spinLoading, $spinMainLoading);
                                    $().toastmessage('showErrorToast', 'Services couldnt be modified currently.');
                                }
                            }
                        });
                    }
                    else {
                        $().toastmessage('showWarningToast', "Please select at least one host.");
                    }
                }

                $("#apply_changes_host_services").click(function () {
                    applyChanges();
                });
            }
        });
}

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
        data: {"action": action, "site": site, "host": name1, "service": name2, "view_type": "UNMP"},
        cache: false,
        success: function (result) {
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
            if (result[1] != 'undefined' && result[1] != "undefined" && result[1]) {
                $(span0).removeClass("icon-0");
                $(span0).removeClass("icon-1");
                $(span0).removeClass("icon-2");
                $(span0).removeClass("icon-3");
                $(span0).addClass("icon-" + result[1]);
            }
            else {
                var td7 = $(recTableObj).find("td:eq(6)");
                $(td7).html("Service check is in progress. Please wait for atleast 120 seconds before scheduling the check again.");
            }
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


