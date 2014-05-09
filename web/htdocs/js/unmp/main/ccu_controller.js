var timeSlot = 60000;
var sysAdminState = 0;
var reconcileState = 0;
var timecheck = 60000;
var ipMacChange = 0;
var callB = null;
function deviceList() {
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
    var device_type = "idu4";
    // this retreive the value of ipaddress textbox
    var ip_address = $("input[id='filter_ip']").val();
    // this retreive the value of macaddress textbox
    var mac_address = $("input[id='filter_mac']").val();
    // this retreive the value of selectdevicetype from select menu
    var selected_device_type = $("select[id='device_type']").val();
    spinStart($spinLoading, $spinMainLoading);
    if (selected_device_type == "ap25") {
        parent.main.location = "ap_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + selected_device_type;
    }
    else if (selected_device_type == "odu100" || selected_device_type == "odu16") {
        parent.main.location = "odu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + selected_device_type;
    }
    else if (selected_device_type == "idu4") {
        parent.main.location = "idu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + selected_device_type;
    }
    else {
        // this ajax return the call to function get_device_data_table which is in odu_view and pass the ipaddress,macaddress,devicetype with url
        $.ajax({
            type: "get",
            url: "get_device_list_ccu_profiling.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type,
            success: function (result) {
                if (result == 0 || result == "0") {
                    $().toastmessage('showWarningToast', "Searched Device Doesn't Exist");
                    parent.main.location = "ccu_listing.py?ip_address=" + "" + "&mac_address=" + "" + "&selected_device_type=" + "";
                    //$("#ccu_form_div").html("No profiling exist");
                }
                else if (result == 1 || result == "1") {
                    parent.main.location = "ccu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type;

                }
                else if (result == 2 || result == "2") {

                    $("#ccu_form_div").html("Please Try Again");
                }
                else {
                    $("#ccu_form_div").html(result);
                    $("div.yo-tabs", "div#container_body").yoTabs();
                    $('.n-reconcile').tipsy({gravity: 'n'});
                    $("#filter_mac").val($("input[name='mac_address']").val());
                    $("#filter_ip").val($("input[name='ip_address']").val());
                    ccu_reconciliation();

                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });

    }
}


function ccu_reconciliation() {
    $("input[name='ccu_reconcile']").unbind().bind("click", function () {
        if (reconcileState == 0 || reconcileState == null) {
            reconciliationConfirm();
        }
        else {
            $.prompt('Reconciliation is Running.Please Wait', { buttons: {Ok: true}, prefix: 'jqismooth'});
        }
    });
}


function reconciliationConfirm() {
    if (reconcileState == 0 || reconcileState == null) {
        $.prompt('Device Configuration data would be Synchronized with the UNMP server Database. \n Click Ok to confirm.', {
            buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: reconciliation});
    }
    else {
        $.prompt('Reconciliation is Running.Please Wait', { buttons: {Ok: true}, prefix: 'jqismooth'});
    }
}


function reconciliation(v, m) {
    if (v != undefined && v == true) {
        spinStart($spinLoading, $spinMainLoading);
        var host_id = $("input[name='host_id']").val();
        var device_type_id = $("input[name='device_type']").val();
        $.ajax({

            type: "post",
            url: "ccu_reconciliation.py?host_id=" + host_id + "&device_type_id=" + device_type_id,
            success: function (result) {
                if (parseInt(result.success) == 0) {
                    json = result.result
                    for (var node in json) {
                        if (parseInt(node) <= 35) {
                            $().toastmessage('showWarningToast', node + "% reconciliation done for device " + json[node][0] + "(" + json[node][1] + ")" + ".Please reconcile the device again");
                        }
                        else if (parseInt(node) <= 90) {
                            $().toastmessage('showWarningToast', node + "% reconciliation done for device " + json[node][0] + "(" + json[node][1] + ")" + ".Please reconcile the device again");
                        }
                        else {
                            $().toastmessage('showSuccessToast', "Reconciliation done successfully for device " + json[node][0] + "(" + json[node][1] + ")");
                        }
                        deviceList();
                        break;
                    }
                }
                else {
                    $().toastmessage('showErrorToast', result.result);
                }
                spinStop($spinLoading, $spinMainLoading);
            }

        });
    }
}

function ipSelectMacDeviceType(obj, ipMacVal) {

    selectedVal = $(obj).val();
    $.ajax({
        type: "get",
        url: "get_ip_mac_selected_device.py?selected_val=" + selectedVal + "&ip_mac_val=" + ipMacVal,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                if (ipMacVal == 1) {
                    $("input[id='filter_mac']").val(String(result.mac_address).toUpperCase());
                    $("select[id='device_type']").val(result.selected_device);
                }
                else {
                    $("input[id='filter_ip']").val(result.ip_address);
                    $("select[id='device_type']").val(result.selected_device);
                }
                deviceList();
            }
            else {
                $().toastmessage('showErrorToast', result.error);
            }
        }
    });
}

$(function () {
    $("input[id='btnSearch']").click(function () {
        //call the device list function on click of search button
        deviceList();
    });
    $("input[id='filter_ip']").keypress(function () {
        $("input[id='filter_mac']").val("");
    })
    $("input[id='filter_mac']").keypress(function () {
        $("input[id='filter_ip']").val("");
    })
    $("input[id='filter_ip']").ccplAutoComplete("common_ip_mac_search.py?device_type=" + $("select[id='device_type']").val() + "&ip_mac_search=" + 1, {
        dataType: 'json',
        max: 30,
        selectedItem: $("input[id='filter_ip']").val(),
        callAfterSelect: function (obj) {
            ipSelectMacDeviceType(obj, 1);
        }
    });

    $("input[id='filter_mac']").ccplAutoComplete("common_ip_mac_search.py?device_type=" + $("select[id='device_type']").val() + "&ip_mac_search=" + 0, {
        dataType: 'json',
        max: 30,
        selectedItem: $("input[id='filter_mac']").val(),
        callAfterSelect: function (obj) {
            ipSelectMacDeviceType(obj, 0);
        }
    });
    deviceList();
    //adminStatusCheck();
    $("#filterOptions").hide();
    $("#hide_search").show();
    $("#ccu_form_div").css({'margin-top': '20px'});
    $("#hide_search").toggle(function () {
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
            $("#ccu_form_div").css({'margin-top': '76px'});
        },
        function () {
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
            $("#ccu_form_div").css({'margin-top': '20px'});

        });
    //$("div#container_body").css("padding-bottom","20px");
    // spin loading object
    //spinStart($spinLoading,$spinMainLoading);
    //spinStop($spinLoading,$spinMainLoading);
    /*	$("#page_tip").colorbox(
     {
     href:"page_tip_odu_profiling.py",
     title: "Page Tip",
     opacity: 0.4,
     maxWidth: "80%",
     width:"650px",
     height:"600px",
     onComplte:function(){}
     });*/

    $("#device_select_list").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Device Type', header: "Available Device Types"});

});


function commonFormSubmit(formObj, btn) {
    spinStart($spinLoading, $spinMainLoading);
    CommonSetRequest(formObj, btn);
    return false;
}


function CommonSetRequest(formObj, btn) {
    var btnName = $(btn).attr("name");
    var btnValue = $(btn).val();
    var myForm = $("#" + formObj);
    var data = myForm.serialize() + "&" + btnName + "=" + btnValue;
    var url = myForm.attr("action");
    var method = myForm.attr("method");
    var imgCount = myForm.find(".img-submit-button").length;
    var host_id = $("input[name='host_id']").val();
    var selected_device = $("input[name='device_select']").val();
    if (btnValue == "Ok") {
        myForm.find("input").removeAttr("disabled");
        myForm.find("select").removeAttr("disabled");
        myForm.find("select").show();
        myForm.find("input").show();
        myForm.find("input.img-submit-button").remove();
        myForm.find("input.img-done-button").remove();
        myForm.find("input[id='ccu_retry']").hide();
        myForm.find("input[id='ccu_cancel']").hide();
        myForm.find("input[id='ccu_ok']").hide();
        myForm.find("input[class='ui-disabled']").attr({"disabled": true});
        myForm.find("input[id='ccu_save']").show();
        spinStop($spinLoading, $spinMainLoading);
    }
    else {
        if (btnValue == "") {
            var oidValue = myForm.find("input[name='" + $(btn).attr("oid") + "']").val()
            if (oidValue == undefined) {
                oidValue = myForm.find("select[name='" + $(btn).attr("oid") + "']").val()
            }
            data = "host_id=" + myForm.find("input[name='host_id']").val() + "&device_type=" + myForm.find("input[name='device_type']").val() + "&" + $(btn).attr("oid") + "=" + oidValue + "&" + btnName + "=" + btnValue;
        }
        $.ajax({
            type: method,
            url: url + "?host_id=" + host_id + "&device_type=" + selected_device,
            data: data,
            success: function (result) {
                if (result.success == 0 || result.success == "0") {
                    if ((btnValue == "Save") || (btnValue == "Retry")) {
                        var json = result.result;
                        myForm.find("input.img-submit-button").remove();
                        myForm.find("submit.img-submit-button").remove();
                        for (var node in json) {

                            var selectListName = $("select[id='" + node + "']");
                            var inputTextboxName = $("input[id='" + node + "']");
                            if (json[node] == 0) {
                                var imageCreate = $("<input/>");
                                imageCreate.attr({"type": "button", "title": "Done", "class": "img-done-button", "oid": node});
                                inputTextboxName.attr({"disabled": true});
                                selectListName.attr({"disabled": true});
                                inputTextboxName.show();
                                selectListName.show();
                                setStatus = 0
                                if (btnValue == "Retry") {
                                    imgCount = imgCount - 1
                                }
                            }
                            else {
                                var imageCreate = $("<input/>");
                                imageCreate.attr({"type": "button", "title": json[node],
                                    "class": "img-submit-button", "oid": node, "name": "common_submit"});
                                imageCreate.click(function () {
                                    commonFormSubmit(formObj, this);
                                });
                                imageCreate.val("");
                                inputTextboxName.attr({"disabled": false});
                                selectListName.attr({"disabled": false});
                                //	inputradiobutton.attr({"disabled":false});
                                unSetStatus = 1;
                                if (btnValue == "Save") {
                                    imgCount = imgCount + 1;
                                }
                            }
                            imageCreate.insertAfter(inputTextboxName);
                            imageCreate.insertAfter(selectListName);
                        }
                        if (imgCount >= 1) {
                            myForm.find("input[id='ccu_ok']").hide();
                            myForm.find("input[id='ccu_save']").hide();
                            myForm.find("input[id='ccu_retry']").show();
                            myForm.find("input[id='ccu_cancel']").show();
                        }
                        else {
                            myForm.find("input[id='ccu_ok']").show();
                            myForm.find("input[id='ccu_save']").hide();
                            myForm.find("input[id='ccu_retry']").hide();
                            myForm.find("input[id='ccu_cancel']").hide();
                        }
                    }
                    else if (btnValue == "") {
                        var json = result.result;
                        var inputObj = myForm.find("input[id='" + $(btn).attr("oid") + "']");
                        var imageFind = inputObj.next();
                        if (inputObj.val() == undefined) {
                            imageFind = myForm.find("select[id='" + $(btn).attr("oid") + "']").next();
                        }
                        imageFind.remove();
                        for (var node in json) {
                            var selectListName = $("select[id='" + node + "']");
                            var inputTextboxName = $("input[id='" + node + "']");
                            var imageCreate = $("<input/>");
                            if (json[node] == 0) {
                                imageCreate.attr({"type": "button", "title": "Done", "class": "img-done-button", "oid": node});
                                inputTextboxName.attr({"disabled": true});
                                selectListName.attr({"disabled": true});
                                inputTextboxName.show();
                                selectListName.show();
                                imgCount = imgCount - 1;
                            }
                            else {
                                imageCreate.attr({"type": "button", "title": json[node],
                                    "class": "img-submit-button", "oid": node, "name": "common_submit"});
                                imageCreate.click(function () {
                                    commonFormSubmit(formObj, this);
                                });
                                imageCreate.val("");
                                selectListName.attr({"disabled": false});
                                inputTextboxName.attr({"disabled": false});
                            }

                            $(imageCreate).insertAfter(inputTextboxName);
                            $(imageCreate).insertAfter(selectListName);
                        }
                        if (imgCount >= 1) {
                            myForm.find("input[id='ccu_ok']").hide();
                            myForm.find("input[id='ccu_save']").hide();
                            myForm.find("input[id='ccu_retry']").show();
                            myForm.find("input[id='ccu_cancel']").show();
                        }
                        else {
                            myForm.find("input[id='ccu_ok']").show();
                            myForm.find("input[id='ccu_save']").hide();
                            myForm.find("input[id='ccu_retry']").hide();
                            myForm.find("input[id='ccu_cancel']").hide();
                        }

                    }
                    else if (btnValue == "Cancel") {
                        myForm.find("input").removeAttr("disabled");
                        myForm.find("input[id='bw_id']").attr("disabled", true);
                        myForm.find("select").removeAttr("disabled");
                        myForm.find("select").show();
                        myForm.find("input.img-submit-button").remove();
                        myForm.find("input.img-done-button").remove();
                        myForm.find("input[id='ccu_retry']").hide();
                        myForm.find("input[id='ccu_cancel']").hide();
                        myForm.find("input[id='ccu_ok']").hide();
                        myForm.find("input[id='ccu_save']").show();
                        for (var node in result) {
                            if (node == "success") {
                                continue;
                            }
                            else {
                                var inputTextboxName = $("input[id='" + node + "']");
                                inputTextboxName.val(result[node]);
                                $("select[id='" + node + "'] option[value='" + result[node] + "']").attr("selected", true);
                            }
                        }

                    }
                }
                else {
                    $().toastmessage('showErrorToast', result.result);
                }

                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }

}


