var timeslot = 30000;//this is used in settimeout function when device firmware is going to update until the firmware is update the function is called recursively after this timeout
var master_val = "";
var device_type = "";
function deviceList() {

    // spin loading object
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
    $("select[id='device_type']option[value='" + $("input[name='device_select']").val() + "']").attr("selected", true);
    device_type = "";
    // this retreive the value of ipaddress textbox
    ip_address = $("input[id='filter_ip']").val();
    // this retreive the value of macaddress textbox
    mac_address = $("input[id='filter_mac']").val();
    // this retreive the value of selectdevicetype from select menu
    selected_device_type = $("select[id='device_type']").val();
    spinStart($spinLoading, $spinMainLoading);
    // this ajax return the call to function get_device_data_table which is in odu_view and pass the ipaddress,macaddress,devicetype with url
    $.ajax({
        type: "post",
        url: "get_device_list_for_firmware.py?&ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type,
        cache: false,
        success: function (result) {
            //$("select[id='RU.RUConfTable.channelBandwidth'] option[value='"+ $("input[name='channelBandwidth']").val() +"']").attr("selected",true);

            if (parseInt(result) == 0 || result == "0") {

                if ($("#result-div").html() == "Firmware is in Progress") {
                    $("#firmware").attr("disabled", "true");
                    $("#result-div").html("Firmware is in Progress");
                    $("#result-div").show();
                    $("#odu16_form_div").html("No profiling exist");
                    $("#odu16_form_div").show();
                }
                else {
                    $("#result-div").html("No profiling exist");
                    $("#result-div").css("margin-left", "30px");
                    $("#odu16_form_div").hide();
                }
            }
            else if (result == 1 || result == "1") {
                parent.main.location = "odu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type;

            }
            else if (result == 2 || result == "2") {

                if ($("#result-div").html() == "Firmware is in Progress") {
                    $("#firmware").attr("disabled", "true");
                    $("#result-div").html("Firmware is in Progress");
                    $("#result-div").show();
                    $("#odu16_form_div").html("Please Try Again");
                    $("#odu16_form_div").show();
                }
                else {
                    $("#result-div").html("Please Try Again");
                    $("#result-div").css("margin-left", "30px");
                    $("#odu16_form_div").hide();
                }
            }
            else if (result == null || result == "") {

                if ($("#result-div").html() == "Firmware is in Progress") {
                    //$("#firmware").attr("disabled","true");
                    $("#result-div").html("Firmware is in Progress");
                    $("#result-div").show();
                    $("#odu16_form_div").html("No host Exist For This Device");
                    $("#odu16_form_div").show();

                }
                else {
                    $("#result-div").html("No host Exist For This Device");
                    $("#result-div").css("margin-left", "30px");
                    $("#odu16_form_div").hide();
                }
            }
            else {

                if ($("#result-div").html() == "Firmware is in Progress") {
                    $("#firmware").attr("disabled", "true");
                    $("#result-div").html("Firmware is in Progress");
                    $("#result-div").show();
                    $("#odu16_form_div").show();
                    $("#odu16_form_div").html(result);

                }
                else {
                    $("#odu16_form_div").show();
                    $("#result-div").html("");
                    $("#odu16_form_div").html(result);

                }
                $("input[name='select_master']").click(function () {
                    selectMaster(this);
                });
                if ($("#result_final").val() == 0 || $("#result_final").val() == "0") {

                    master_val = $("#tr_master").attr("master_value");
                    firmware_result();
                }

            }
            spinStop($spinLoading, $spinMainLoading);
        }

    });
}


function selectMaster(obj) {
    if ($("input[name='select_master']").attr("checked")) {

        var tableElement = $(obj).parent();
        var master = tableElement.next().attr("master_value");
        $("#master_value").val(master);
        tableElement = $(obj).parent().parent();
        var slave = tableElement.attr("slave_value");
        $("#slave_value").val(slave);
    }
    else {
        $("#result-div").html("Please Select One Master To upgrade");
    }
}

function firmwareUpdateButton(obj) {


    var imageCreate = $("<input/>");
    $('table#firmware_table tr').each(function () {
        if ($(this).find("input[name='select_master']").attr("checked")) {

            if ($(this).find("td").hasClass("loadingimage")) {

                imageCreate.attr({"title": "loading", "class": "img-loader"});
                imageCreate.css("float", "right");
                $(this).find("td.loadingimage").append(imageCreate);
                $(this).css("background-color", "#EEE");
                $("#result-div").html("Firmware is in Progress");
                $("#result-div").css("margin-left", "30px");
                $("#result-div").show();

            }
        }
    });


    var master = $("div#odu16_form_div").find("input[id='master_value']").val();


    var slave = $("div#odu16_form_div").find("input[id='slave_value']").val();
    $("div#odu16_form_div").find("input[id='device_type']").val($("select[id='device_type']").val());
    device_type = $("div#odu16_form_div").find("input[id='device_type']").val();

    filename = $("input[id='firmware_file']").val();
    if (master == undefined || slave == undefined || device_type == undefined) {
        $(obj).removeAttr("disabled");
        if ($("div#odu16_form_div").html() != "") {
            $("#result-div").html($("div#odu16_form_div").html());
            $("#result-div").css("margin-left", "30px");
            $("div#odu16_form_div").html("");
        }

    }
    else {
        $.ajax({
            type: "get",
            url: "firmware_update_set.py?&master=" + master + "&slave=" + slave + "&device_type=" + device_type + "&filename=" + filename,
            cache: false,
            success: function (result) {

                try {
                    finalresult = eval("(" + result + ")");
                    $("#firmware_table").find("input.img-done-button").remove();
                    $("#firmware_table").find("input.img-submit-button").remove();

                    if (finalresult.success == 0) {

                        var json = finalresult.result;
                        var imageCreate = $("<input/>");
                        for (var node in json) {
                            var td_element = $("#" + node);
                            if (json[node] == 0) {

                                imageCreate.attr({"type": "button", "title": "Done", "class": "img-done-button", "name": node});
                                var input_img_loader = td_element.find("input.img-loader")
                                input_img_loader.css("display", "None");
                                imageCreate.css("float", "right");
                                td_element.append(imageCreate);
                                $(obj).removeAttr("disabled");
                                $("#result-div").html(json[node]);
                                $("#result-div").css("margin-left", "30px");
                            }
                            else {

                                /*imageCreate.attr({"type":"submit","title":json[node],
                                 "class":"img-submit-button","oid":node,"name":"odu100_submit","value":""});
                                 var input_img_loader = td_element.find("input.img-loader")
                                 //input_img_loader.css("display","None");
                                 imageCreate.css("float","right");
                                 td_element.append(imageCreate);*/

                                $(obj).removeAttr("disabled");
                                $("#result-div").html(json[node]);
                                $("#result-div").css("margin-left", "30px");

                            }
                            $(obj).removeAttr("disabled");
                            $("#firmware_table").find("input.img-loader").remove();
                            $("#firmware_table").find("tr").css("background-color", "#FFF");
                        }
                    }
                    else {

                        $("#result-div").html("Device is not connected");
                        $(obj).removeAttr("disabled");
                        $("#firmware_table").find("input.img-done-button").remove();
                        $("#firmware_table").find("input.img-submit-button").remove();
                        $("#firmware_table").find("input.img-loader").remove();
                        $("#firmware_table").find("tr").css("background-color", "#FFF");
                    }
                }
                catch (err) {
                    $(obj).removeAttr("disabled");
                    if (result == "False" || result == false) {
                        $("#result-div").html(" Please Select Device Type For Upgrade");
                    }
                    else {
                        $("#result-div").html("Select Device For Upgrade");
                    }

                }
            }

        });

        return false;
    }

}
var callA = null;
function firmware_result() {


    if (master_val == undefined) {
        $("#result-div").html($("#odu16_form_div").html());
        $("#odu16_form_div").html("");
        $("#result-div").show();
        $("#result-div").css("margin-left", "30px");
    }
    else {
        $.ajax({
            type: "get",
            url: "update_firmware_result.py?master=" + master_val,
            cache: false,
            success: function (result) {
                result = eval("(" + result + ")");

                for (var r in result) {
                    if (r == 0 || r == "0") {

                        $("input[name='select_master']").attr("checked", "true");
                        $("input[name='select_master']").attr("disabled", "true");
                        $("#firmware").attr("disabled", "true");
                        $("#result-div").html("Firmware is in Progress");
                        $("#result-div").show();
                        $("#result-div").css("margin-left", "30px");
                        callA = setTimeout(function () {

                            firmware_result();

                        }, timeslot);
                    }
                    else {

                        $().toastmessage('showErrorToast', result[1]);
                        $("#result-div").html("");
                        $("input[name='select_master']").attr("checked", "false");
                        $("#result-div").css("margin-left", "30px");
                        $("#result-div").show();
                        $("#firmware_table").find("input.img-loader").remove();
                        $("#firmware_table").find("tr").css("background-color", "#FFF");
                        $("#firmware").removeAttr("disabled");
                        $("input[name='select_master']").removeAttr("disabled");
                    }
                }
            }

        });
    }
}
$(function () {

    deviceList();
    //$("#firmware").attr("disabled","true");

    $("input[id='btnSearch']").click(function () {

        //call the device list function on click of search button
        if ($("#result-div").html() == "Firmware is in Progress") {
            $("#firmware").attr("disabled", "true");
            $("#result-div").html("Firmware is in Progress");
            $("#result-div").show();
            deviceList();

        }
        else {
            deviceList();
            $("div#firmware-update").find("#firmware-update-child-div").find("input[id='firmware']").removeAttr("disabled");
        }


    });
    $("input[id='firmware']").click(function () {
        $("#firmware").attr("disabled", "true");
        firmwareUpdateButton(this);
    });
//	$("#page_tip").colorbox(
//	{
//		href:"page_tip_firmware_update.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"450px",
//		height:"350px",
//		onComplte:function(){}
//	});
});
