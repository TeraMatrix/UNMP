function deviceList() {
    device_type = "odu16,odu100";
    // this retreive the value of ipaddress textbox
    ip_address = $("input[id='filter_ip']").val();
    // this retreive the value of macaddress textbox
    mac_address = $("input[id='filter_mac']").val();
    // this retreive the value of selectdevicetype from select menu
    selected_device_type = $("select[id='device_type']").val();
    // this ajax return the call to function get_device_data_table which is in odu_view and pass the ipaddress,macaddress,devicetype with url
    $.ajax({
        type: "post",
        url: "get_device_list.py?&ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type,
        success: function (result) {
            if (result == 0 || result == "0") {
                $("#swt4_form_div").html("No profiling exist");
            }
            else if (result == 1 || result == "1") {
                parent.main.location = "odu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type;

            }
            else if (result == 2 || result == "2") {

                $("#swt4_form_div").html("Please Try Again");
            }
            else {
                $("#swt4_form_div").html(result);
                swt4_profiling();
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
    deviceList();

});

function selectlistFunction() {
    $("#swt_bandwidth_form").find("select[id='bandwidth_state_select_list_id']").change(function () {
        if (($("#swt_bandwidth_form").find("select[id='bandwidth_state_select_list_id']").val() == 0) || ($("#swt_bandwidth_form").find("select[id='bandwidth_state_select_list_id']").val() == "0")) {
            $("#swt_bandwidth_form").find("input[id='bandwidth_rate_id']").attr("disabled", "true");
        }
        else {
            $("#swt_bandwidth_form").find("input[id='bandwidth_rate_id']").removeAttr("disabled");
        }
    });
    $("#swt_storm_form").find("select[id='storm_state_id']").change(function () {

        if (($("#swt_storm_form").find("select[id='storm_state_id']").val() == 0) || ($("#swt_bandwidth_form").find("select[id='storm_state_id']").val() == "0")) {
            $("#swt_storm_form").find("select[id='storm_rate_id']").attr("disabled", "true");
            $("#swt_storm_form").find("select[id='storm_rate_id']").val("");
        }
        else {
            $("#swt_storm_form").find("select[id='storm_rate_id']").removeAttr("disabled");
        }
    });

    $("#swt_ip_config_form").find("select[id='swt_ip_mode_selection']").change(function () {

        if (($("#swt_ip_config_form").find("select[id='swt_ip_mode_selection']").val() == "dhcp")) {
            $("#swt_ip_config_form").find("input[id='swt4_ip_address']").attr("disabled", "true");
            $("#swt_ip_config_form").find("input[id='swt4_subnet_mask']").attr("disabled", "true");
            $("#swt_ip_config_form").find("input[id='swt4_gateway']").attr("disabled", "true");
        }
        else {
            $("#swt_ip_config_form").find("input[id='swt4_ip_address']").removeAttr("disabled");
            $("#swt_ip_config_form").find("input[id='swt4_subnet_mask']").removeAttr("disabled");
            $("#swt_ip_config_form").find("input[id='swt4_gateway']").removeAttr("disabled");
        }
    });

    $("#swt4_port_priority_form").find("select[id='port_base_priority_id']").change(function () {

        if (($("#swt4_port_priority_form").find("select[id='port_base_priority_id']").val() == 0) || ($("#swt4_port_priority_form").find("select[id='port_base_priority_id']").val() == "0")) {

            $("#swt4_port_priority_form").find("select[id='port_id']").attr("disabled", "true");
            $("#swt4_port_priority_form").find("select[id='priority_id']").attr("disabled", "true");
            $("#swt4_port_priority_form").find("input[id='id_swt_submit_save']").attr("disabled", "true");
        }
        else {
            $("#swt4_port_priority_form").find("select[id='port_id']").removeAttr("disabled");
            $("#swt4_port_priority_form").find("select[id='priority_id']").removeAttr("disabled");
            $("#swt4_port_priority_form").find("input").removeAttr("disabled");

        }
    });

    $("#swt4_dscp_priority_form").find("select[id='dscp_port_priority_id']").change(function () {
        if (($("#swt4_dscp_priority_form").find("select[id='dscp_port_priority_id']").val() == 0) || ($("#swt4_dscp_priority_form").find("select[id='dscp_port_priority_id']").val() == "0")) {
            $("#swt4_dscp_priority_form").find("select[id='dscp_id']").attr("disabled", "true");
            $("#swt4_dscp_priority_form").find("select[id='dscp_priority_id']").attr("disabled", "true");
            $("#swt4_dscp_priority_form").find("input[id='id_swt_submit_save']").attr("disabled", "true");
        }
        else {
            $("#swt4_dscp_priority_form").find("select[id='dscp_id']").removeAttr("disabled");
            $("#swt4_dscp_priority_form").find("select[id='dscp_priority_id']").removeAttr("disabled");
            $("#swt4_dscp_priority_form").find("input").removeAttr("disabled");

        }
    });

    $("#swt4_802_priority_form").find("select[id='802p_priority']").change(function () {
        if (($("#swt4_802_priority_form").find("select[id='802p_priority']").val() == 0) || ($("#swt4_802_priority_form").find("select[id='802p_priority']").val() == "0")) {
            $("#swt4_802_priority_form").find("select[id='802p_id']").attr("disabled", "true");
            $("#swt4_802_priority_form").find("select[id='802p_priority_id']").attr("disabled", "true");
            $("#swt4_802_priority_form").find("input[id='id_swt_submit_save']").attr("disabled", "true");
        }
        else {
            $("#swt4_802_priority_form").find("select[id='802p_id']").removeAttr("disabled");
            $("#swt4_802_priority_form").find("select[id='802p_priority_id']").removeAttr("disabled");
            $("#swt4_802_priority_form").find("input").removeAttr("disabled");

        }
    });


    $("#swt4_ip_base_priority_form").find("select[id='ip_priority']").change(function () {
        if (($("#swt4_ip_base_priority_form").find("select[id='ip_priority']").val() == 0) || ($("#swt4_ip_base_priority_form").find("select[id='ip_priority']").val() == "0")) {
            $("#swt4_ip_base_priority_form").find("select[id='ip_type_id']").attr("disabled", "true");
            $("#swt4_ip_base_priority_form").find("input[id='ip_priority_address']").attr("disabled", "true");
            $("#swt4_ip_base_priority_form").find("input[id='ip_priority_net_mask']").attr("disabled", "true");
            $("#swt4_ip_base_priority_form").find("select[id='ip_priority_id']").attr("disabled", "true");
            $("#swt4_ip_base_priority_form").find("input[id='id_swt_submit_save']").attr("disabled", "true");
        }
        else {
            $("#swt4_ip_base_priority_form").find("select[id='ip_type_id']").removeAttr("disabled");
            $("#swt4_ip_base_priority_form").find("input[id='ip_priority_address']").removeAttr("disabled");
            $("#swt4_ip_base_priority_form").find("input[id='ip_priority_net_mask']").removeAttr("disabled");
            $("#swt4_ip_base_priority_form").find("select[id='ip_priority_id']").removeAttr("disabled");
            $("#swt4_ip_base_priority_form").find("input").removeAttr("disabled");
        }
    });

}

function loadSelectlistFunction() {
    if (($("#swt_bandwidth_form").find("select[id='bandwidth_state_select_list_id']").val() == 0) || ($("#swt_bandwidth_form").find("select[id='bandwidth_state_select_list_id']").val() == "0")) {
        $("#swt_bandwidth_form").find("input[id='bandwidth_rate_id']").attr("disabled", "true");
    }
    else {
        $("#swt_bandwidth_form").find("input[id='bandwidth_rate_id']").removeAttr("disabled");
    }


    if (($("#swt_storm_form").find("select[id='storm_state_id']").val() == 0) || ($("#swt_storm_form").find("select[id='storm_state_id']").val() == "0")) {
        $("#swt_storm_form").find("select[id='storm_rate_id']").attr("disabled", "true");
        $("#swt_storm_form").find("select[id='storm_rate_id']").val("");
    }
    else {
        $("#swt_storm_form").find("select[id='storm_rate_id']").removeAttr("disabled");
    }

    if (($("#swt_ip_config_form").find("select[id='swt_ip_mode_selection']").val() == "dhcp")) {
        $("#swt_ip_config_form").find("input[id='swt4_ip_address']").attr("disabled", "true");
        $("#swt_ip_config_form").find("input[id='swt4_subnet_mask']").attr("disabled", "true");
        $("#swt_ip_config_form").find("input[id='swt4_gateway']").attr("disabled", "true");
    }
    else {
        $("#swt_ip_config_form").find("input[id='swt4_ip_address']").removeAttr("disabled");
        $("#swt_ip_config_form").find("input[id='swt4_subnet_mask']").removeAttr("disabled");
        $("#swt_ip_config_form").find("input[id='swt4_gateway']").removeAttr("disabled");
    }

    if (($("#swt4_port_priority_form").find("select[id='port_base_priority_id']").val() == 0) || ($("#swt4_port_priority_form").find("select[id='port_base_priority_id']").val() == "0")) {

        $("#swt4_port_priority_form").find("select[id='port_id']").attr("disabled", "true");
        $("#swt4_port_priority_form").find("select[id='priority_id']").attr("disabled", "true");
        $("#swt4_port_priority_form").find("input[id='id_swt_submit_save']").attr("disabled", "true");
    }
    else {
        $("#swt4_port_priority_form").find("select[id='port_id']").removeAttr("disabled");
        $("#swt4_port_priority_form").find("select[id='priority_id']").removeAttr("disabled");
        $("#swt4_port_priority_form").find("input").removeAttr("disabled");

    }

    if (($("#swt4_dscp_priority_form").find("select[id='dscp_port_priority_id']").val() == 0) || ($("#swt4_dscp_priority_form").find("select[id='dscp_port_priority_id']").val() == "0")) {
        $("#swt4_dscp_priority_form").find("select[id='dscp_id']").attr("disabled", "true");
        $("#swt4_dscp_priority_form").find("select[id='dscp_priority_id']").attr("disabled", "true");
        $("#swt4_dscp_priority_form").find("input[id='id_swt_submit_save']").attr("disabled", "true");
    }
    else {
        $("#swt4_dscp_priority_form").find("select[id='dscp_id']").removeAttr("disabled");
        $("#swt4_dscp_priority_form").find("select[id='dscp_priority_id']").removeAttr("disabled");
        $("#swt4_dscp_priority_form").find("input").removeAttr("disabled");

    }

    if (($("#swt4_802_priority_form").find("select[id='802p_priority']").val() == 0) || ($("#swt4_802_priority_form").find("select[id='802p_priority']").val() == "0")) {
        $("#swt4_802_priority_form").find("select[id='802p_id']").attr("disabled", "true");
        $("#swt4_802_priority_form").find("select[id='802p_priority_id']").attr("disabled", "true");
        $("#swt4_802_priority_form").find("input[id='id_swt_submit_save']").attr("disabled", "true");
    }
    else {
        $("#swt4_802_priority_form").find("select[id='802p_id']").removeAttr("disabled");
        $("#swt4_802_priority_form").find("select[id='802p_priority_id']").removeAttr("disabled");
        $("#swt4_802_priority_form").find("input").removeAttr("disabled");

    }

    if (($("#swt4_ip_base_priority_form").find("select[id='ip_priority']").val() == 0) || ($("#swt4_ip_base_priority_form").find("select[id='ip_priority']").val() == "0")) {
        $("#swt4_ip_base_priority_form").find("select[id='ip_type_id']").attr("disabled", "true");
        $("#swt4_ip_base_priority_form").find("input[id='ip_priority_address']").attr("disabled", "true");
        $("#swt4_ip_base_priority_form").find("input[id='ip_priority_net_mask']").attr("disabled", "true");
        $("#swt4_ip_base_priority_form").find("select[id='ip_priority_id']").attr("disabled", "true");
        $("#swt4_ip_base_priority_form").find("input[id='id_swt_submit_save']").attr("disabled", "true");
    }
    else {
        $("#swt4_ip_base_priority_form").find("select[id='ip_type_id']").removeAttr("disabled");
        $("#swt4_ip_base_priority_form").find("input[id='ip_priority_address']").removeAttr("disabled");
        $("#swt4_ip_base_priority_form").find("input[id='ip_priority_net_mask']").removeAttr("disabled");
        $("#swt4_ip_base_priority_form").find("select[id='ip_priority_id']").removeAttr("disabled");
        $("#swt4_ip_base_priority_form").find("input").removeAttr("disabled");
    }
}


function swt4CommonFormSubmit(formObj, btn) {

    btnName = $(btn).val();
    if ($("#" + formObj).valid()) {
        swtCommonAjaxRequest(formObj, btnName);
    }
    return false;
}


function commit_flash() {
    var host_id = $("input[id='host_id']").val();
    $.ajax({
        type: "post",
        url: "commit_flash.py?host_id=" + host_id,
        success: function (result) {
            $().toastmessage('showErrorToast', "Your Data is Going to Save Permanently on device");
        }
    });


}

function reboot() {

    var cb = $("#reboot_btn").colorbox(
        {
            href: "reboot.py",
            onComplete: function () {
                rebootFinal();
            },
            title: "Reboot Form",
            opacity: 0.4,
            maxWidth: "50%",
            width: "360px",
            height: "250px",
            top: 100


        });
    return false;
}

function rebootFinal() {
    var host_id = $("input[id='host_id']").val();

    $("#reboot_form").submit(function () {
        if (confirm("Do Yoy Want To Reboot The System?")) {
            var firmware = $("input[name='firmwarebtngroup']:checked").val();
            if ($("input[name='firmwarebtngroup']").attr("checked")) {
                $.ajax({
                    type: "post",
                    url: "reboot_final.py?host_id=" + host_id + "&firwmare=" + firmware,
                    success: function (result) {
                        result = eval("(" + result + ")");
                        $().toastmessage('showErrorToast', result.result);

                    }
                });
            }
            else {
                $().toastmessage('showErrorToast', "Please Select One Firmware");
            }
            return false;
        }
        else {
            return false;
        }

    });

}


function swtfilterAction() {
    $('.filterBtn').click(function () {
        var id = $(this).attr("id");
        if (id == 'configfiler') {

            $("#list li").hide();
            var target = $("#list li[class='Configuration']");
            target.show();
        }
        else if (id == 'qosFilter') {

            $("#list li").hide();
            var target = $("#list li[class='QoS']");
            target.show();
        }
        else {
            $("#list li").show();
        }
    });
}

function swt4_profiling() {
    $("a.tab-profile").click(function (e) {
        e.preventDefault();
        if ($(this).hasClass("tab-active") == false) {
            var anr = $(this).parent().find("a");
            anr.removeClass("tab-active");
            anr.addClass("tab-button");
            $(this).removeClass("tab-button");
            $(this).addClass("tab-active");
            var div = $(this).parent().next();
            div.find("div.form-div").hide();
            div.find($(this).attr("href")).show();
        }
    });
    swtfilterAction();
    selectlistFunction();
    loadSelectlistFunction();
    SwtIpConfigValidation();

    SwtPortSettingValidation();

    Swt4VlanSettingValidation();

    SwtBandwidthValidation();

    SwtStormValidation();

    swt4PortPriorityValidation();

    swt4DscpPriorityValidation();

    swt4802PriorityValidation();

    swt4IpPriority_Validation();

    swt4QueuePriorityValidation();

    swt4QueueWeightValidation();

    swt4QosAbstractionValidation();

    swt41pRemarkingValidation();

    $("input[id='commit_flash_btn']").click(function () {
        var mainLoading = $("div#main_loading");
        if (confirm("This is going to save all data permanently on device.Are You Sure You Want to do this?")) {
            mainLoading.show();

            commit_flash();
            setTimeout(function () {
                mainLoading.hide();
            }, 5000);
        }
        else {
            return false;
        }
    });
    reboot();

}


function swtCommonAjaxRequest(obj, btnValue) {

    var myForm = $("#" + obj);
    var loading = myForm.parent().parent().find("div.box-loading");
    var data = myForm.serialize() + "&swt_submit=" + btnValue;
    var loading = myForm.parent().parent().find("div.box-loading");
    var url = myForm.attr("action");
    var method = myForm.attr("method");
    var tab = myForm.attr("tab");
    var a_id = myForm.parent().parent().parent().find("a").eq(1).attr("id");

    if (tab == undefined) {
        tab = 0;
    }

    var divId = myForm.attr("div_id");
    var divAction = myForm.attr("div_action");
    if (btnValue == "Ok") {
        myForm.find("input").removeAttr("disabled");
        myForm.find("select").removeAttr("disabled");
        myForm.find("select").show();
        myForm.find("input.img-submit-button").remove();
        myForm.find("input.img-done-button").remove();
        myForm.find("input").show();
        myForm.find("input[id='id_swt_button_retry_all']").hide();
        myForm.find("input[id='id_swt_button_cancel']").hide();
        myForm.find("input[id='id_swt_button_ok']").hide();
        myForm.find("input[id='id_swt_submit_save']").show();
        selectlistFunction();
        loadSelectlistFunction();

    }
    else {
        loading.show();
        $.ajax({
            type: method,
            url: url,
            data: data,
            success: function (result) {

                try {

                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        if ((btnValue == "Save") || (btnValue == "Retry")) {

                            var json = result.result;
                            myForm.find("input.img-submit-button").remove();
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

                                }
                                else {
                                    imageCreate.attr({"type": "submit", "title": json[node],
                                        "class": "img-submit-button", "oid": node, "name": "odu100_submit"});
                                    inputTextboxName.attr({"disabled": false});
                                    selectListName.attr({"disabled": false});
                                    status = 1
                                }
                                imageCreate.val("");
                                $(imageCreate).insertAfter(inputTextboxName);
                                $(imageCreate).insertAfter(selectListName);

                            }
                            if (status == 1) {
                                myForm.find("#id_swt_button_ok").hide();
                                myForm.find("#id_swt_submit_save").hide();
                                myForm.find("#id_swt_button_retry_all").show();
                                myForm.find("#id_swt_button_cancel").show();
                                loading.hide();
                            }
                            else {
                                myForm.find("#id_swt_button_retry_all").hide();
                                myForm.find("#id_swt_button_cancel").hide();
                                myForm.find("#id_swt_submit_save").hide();
                                myForm.find("#id_swt_button_ok").show();
                                if (tab == 1 || tab == "1") {
                                    host_id = myForm.find("input[name='host_id']").val();
                                    $.ajax({
                                        type: "post",
                                        url: divAction + "?host_id=" + host_id,
                                        success: function (result) {
                                            $("div#" + divId).html(result);
                                        }

                                    });
                                    $("a#" + a_id).click();
                                }
                                loading.hide();
                            }
                        }
                        else if (btnValue == "Cancel") {
                            selectlistFunction();
                            loadSelectlistFunction();
                            var json = result.result;
                            loading.hide();
                            myForm.find("input").removeAttr("disabled");
                            myForm.find("select").removeAttr("disabled");
                            myForm.find("select").show();
                            myForm.find("input.img-submit-button").remove();
                            myForm.find("input.img-done-button").remove();
                            myForm.find("input").show();
                            myForm.find("input[id='id_swt_button_retry_all']").hide();
                            myForm.find("input[id='id_swt_button_cancel']").hide();
                            myForm.find("input[id='id_swt_button_ok']").hide();
                            myForm.find("input[id='id_swt_submit_save']").show();
                            for (var node in json) {

                                var inputTextboxName = $("input[id='" + json[node][0] + "']");
                                inputTextboxName.val(json[node][1]);
                                $("select[id ='" + json[node][0] + "'] option[value = '" + json[node][1] + "']").attr("selected", true);
                            }
                            $("#swt_bandwidth_form").find("select[id='bandwidth_state_select_list_id']").change();
                            $("#swt_storm_form").find("select[id='storm_state_id']").change();
                            $("#swt_ip_config_form").find("select[id='swt_ip_mode_selection']").change();


                        }

                    }
                    else {
                        loading.hide();
                        $().toastmessage('showErrorToast', result.result);
                    }

                }
                catch (err) {
                    loading.hide();
                    $().toastmessage('showErrorToast', err);

                }
            }
        });


    }

}


/* ################################################################################### Validation Functions ##################################################################################### */

function SwtIpConfigValidation() {
    $("#swt_ip_config_form").validate({
        rules: {
            'swt_ip_mode_selection': {
                required: true

            },
            'swt4_ip_address': {
                required: true,
                ipv4Address: true
            },
            'swt4_subnet_mask': {
                required: true,
                ipv4Address: true
            },
            'swt4_gateway': {
                required: true,
                ipv4Address: true
            }
        },

        messages: {
            'swt_ip_mode_selection': {
                required: "*"

            },
            'swt4_ip_address': {
                required: "*",
                ipv4Address: "Invalid IP Address"
            },
            'swt4_subnet_mask': {
                required: "*",
                pv4Address: "Invalid IP Address"
            },
            'swt4_gateway': {
                required: "*",
                ipv4Address: "Invalid IP Address"
            }

        }
    });
}


function SwtPortSettingValidation() {
    $("#swt4_port_setting_form").validate({
        rules: {
            'swt_link_fault_selection': {
                required: true

            },
            'port_select_list_id': {
                required: true

            },
            'state_select_list_id': {
                required: true

            },
            'speed_duplex_list_id': {
                required: true

            },
            'flow_control_select_list': {
                required: true

            }
        },

        messages: {
            'swt_link_fault_selection': {
                required: "*"

            },
            'port_select_list_id': {
                required: "*"

            },
            'state_select_list_id': {
                required: "*"

            },
            'speed_duplex_list_id': {
                required: "*"

            },
            'flow_control_select_list': {
                required: "*"

            }
        }
    });
}


function Swt4VlanSettingValidation() {
    $("#swt4_vlan_setting_form").validate({
        rules: {
            'vlan_ingress_filter_id': {
                required: true

            },
            'vlan_pass_all_id': {
                required: true

            },
            'vlan_port_id': {
                required: true

            },
            'pvid': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 1,
                max: 4094

            },
            'vlan_mode_id': {
                required: true

            }
        },

        messages: {
            'vlan_ingress_filter_id': {
                required: "*"

            },
            'vlan_pass_all_id': {
                required: "*"

            },
            'vlan_port_id': {
                required: "*"

            },
            'pvid': {
                required: "*",
                number: " It must be a number",
                positiveNumber: "It must be greater then zero",
                min: " It must be >= 1 and <= 4094",
                max: " It must be >= 1 and <= 4094"

            },
            'vlan_mode_id': {
                required: "*"

            }
        }
    });
}

function SwtBandwidthValidation() {
    $("#swt_bandwidth_form").validate({
        rules: {
            'bandwidth_cpu_protect_id': {
                required: true

            },
            'bandwidth_port_select_list_id': {
                required: true

            },
            'bandwidth_type_select_list_id': {
                required: true

            },
            'bandwidth_state_select_list_id': {
                required: true

            },
            'bandwidth_rate_id': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 64,
                max: 97664

            }
        },

        messages: {
            'bandwidth_cpu_protect_id': {
                required: "*"

            },
            'bandwidth_port_select_list_id': {
                required: "*"

            },
            'bandwidth_type_select_list_id': {
                required: "*"

            },
            'bandwidth_state_select_list_id': {
                required: "*"

            },
            'bandwidth_rate_id': {
                required: "*",
                number: " It must be a number",
                positiveNumber: "It must be greater then zero",
                min: " It must be >= 64 and <= 97664",
                max: " It must be >= 64 and <= 97664"

            }
        }
    });
}


function SwtStormValidation() {
    $("#swt_storm_form").validate({
        rules: {
            'storm_type_id': {
                required: true

            },
            'storm_state_id': {
                required: true

            },
            'storm_rate_id': {
                required: true

            }

        },

        messages: {
            'storm_type_id': {
                required: "*"

            },
            'storm_state_id': {
                required: "*"

            },
            'storm_rate_id': {
                required: "*"

            }

        }
    });
}

function swt4PortPriorityValidation() {
    $("#swt4_port_priority_form").validate({
        rules: {
            'port_base_priority_id': {
                required: true

            },
            'port_id': {
                required: true

            },
            'priority_id': {
                required: true

            }

        },

        messages: {
            'port_base_priority_id': {
                required: "*"

            },
            'port_id': {
                required: "*"

            },
            'priority_id': {
                required: "*"

            }

        }
    });
}


function swt4DscpPriorityValidation() {
    $("#swt4_dscp_priority_form").validate({
        rules: {
            'dscp_port_priority_id': {
                required: true

            },
            'dscp_id': {
                required: true

            },
            'dscp_priority_id': {
                required: true

            }

        },

        messages: {
            'dscp_port_priority_id': {
                required: "*"

            },
            'dscp_id': {
                required: "*"

            },
            'dscp_priority_id': {
                required: "*"

            }

        }
    });
}


function swt4802PriorityValidation() {
    $("#swt4_802_priority_form").validate({
        rules: {
            '802p_priority': {
                required: true

            },
            '802p_id': {
                required: true

            },
            '802p_priority_id': {
                required: true

            }

        },

        messages: {
            '802p_priority': {
                required: "*"

            },
            '802p_id': {
                required: "*"

            },
            '802p_priority_id': {
                required: "*"

            }

        }
    });
}

function swt4IpPriority_Validation() {
    $("#swt4_ip_base_priority_form").validate({
        rules: {
            'ip_priority': {
                required: true

            },
            'ip_type_id': {
                required: true

            },
            'ip_priority_address': {
                required: true,
                ipv4Address: true
            },
            'ip_priority_net_mask': {
                required: true,
                ipv4Address: true
            },
            'ip_priority_id': {
                required: true

            }
        },

        messages: {
            'ip_priority': {
                required: "*"

            },
            'ip_type_id': {
                required: "*"

            },
            'ip_priority_address': {
                required: "*",
                pv4Address: "Invalid IP Address"
            },
            'ip_priority_net_mask': {
                required: "*",
                ipv4Address: "Invalid IP Address"
            },
            'ip_priority_id': {
                required: "*"

            }

        }
    });
}


function swt4QueuePriorityValidation() {
    $("#swt4_queue_priority_form").validate({
        rules: {
            'qid_map_id': {
                required: true

            },
            'qid_map_priority_id': {
                required: true

            }
        },

        messages: {
            'qid_map_id': {
                required: "*"

            },
            'qid_map_priority_id': {
                required: "*"

            }

        }
    });
}


function swt4QueueWeightValidation() {
    $("#swt4_queue_weight_form").validate({
        rules: {
            'queue_id': {
                required: true

            },
            'qid_weight_id': {
                required: true

            }
        },

        messages: {
            'queue_id': {
                required: "*"

            },
            'qid_weight_id': {
                required: "*"

            }

        }
    });
}


function swt4QosAbstractionValidation() {
    $("#swt4_qos_abstraction_form").validate({
        rules: {
            'qos_priority_id': {
                required: true

            },
            'qos_level_id': {
                required: true

            }
        },

        messages: {
            'qos_priority_id': {
                required: "*"

            },
            'qos_level_id': {
                required: "*"

            }

        }
    });
}


function swt41pRemarkingValidation() {
    $("#swt4_1p_remarking_form").validate({
        rules: {
            '1p_remarking_id': {
                required: true

            },
            '1p_remarking_priority': {
                required: true

            }
        },

        messages: {
            '1p_remarking_id': {
                required: "*"

            },
            '1p_remarking_priority': {
                required: "*"

            }

        }
    });
}


