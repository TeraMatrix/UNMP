var timeSlot = 60000;
var sysAdminState = 0;
var reconcileState = 0;
var timecheck = 60000;
var ipMacChange = 0;
var callB = null;
var chkPing = 0;
var anchorObj = null;
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
    else if (device_type == "ccu") {
        parent.main.location = "ccu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + selected_device_type;
    }
    else {
        // this ajax return the call to function get_device_data_table which is in odu_view and pass the ipaddress,macaddress,devicetype with url
        $.ajax({
            type: "get",
            url: "get_device_list_idu_profiling.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type,
            success: function (result) {
                if (result == 0 || result == "0") {
                    $().toastmessage('showWarningToast', "Searched Device Doesn't Exist");
                    parent.main.location = "idu_listing.py?ip_address=" + "" + "&mac_address=" + "" + "&selected_device_type=" + "";
                    //$("#idu_form_div").html("No profiling exist");
                }
                else if (result == 1 || result == "1") {
                    parent.main.location = "idu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type;

                }
                else if (result == 2 || result == "2") {

                    $("#idu_form_div").html("Please Try Again");
                }
                else {
                    $("#idu_form_div").html(result);
                    $("div.yo-tabs", "div#container_body").yoTabs();
                    $('.n-reconcile').tipsy({gravity: 'n'});
                    $("#filter_mac").val($("input[name='mac_address']").val());
                    $("#filter_ip").val($("input[name='ip_address']").val());
                    $("input[name='idu4_commit']").unbind().bind("click", function () {
                        if (reconcileState == 0 || reconcileState == null) {
                            if (sysAdminState == 0 || sysAdminState == null) {
                                commitFlashConfirm();
                            }
                            else {
                                $.prompt('Admin State is unlocked', { buttons: {Ok: true}, prefix: 'jqismooth'});
                            }
                        }
                        else {
                            $.prompt('Reconciliation is Running.Please Wait', { buttons: {Ok: true}, prefix: 'jqismooth'});
                        }
                    });
                    $("input[name='idu4_reboot']").unbind().bind("click", function () {
                        if (reconcileState == 0 || reconcileState == null) {
                            if (sysAdminState == 0 || sysAdminState == null) {
                                rebootconfirm();
                            }
                            else {
                                $.prompt('Admin State is unlocked', { buttons: {Ok: true}, prefix: 'jqismooth'});
                            }
                        }
                        else {
                            $.prompt('Reconciliation is Running.Please Wait', { buttons: {Ok: true}, prefix: 'jqismooth'});
                        }
                    });
                    $("input[name='idu4_reconcile']").unbind().bind("click", function () {
                        if (reconcileState == 0 || reconcileState == null) {
                            if (sysAdminState == 0 || sysAdminState == null) {
                                reconciliationConfirm();
                            }
                            else {
                                $.prompt('Admin State is unlocked', { buttons: {Ok: true}, prefix: 'jqismooth'});
                            }
                        }
                        else {
                            $.prompt('Reconciliation is Running.Please Wait', { buttons: {Ok: true}, prefix: 'jqismooth'});
                        }
                    });
                    $("input[name='idu4_adminState']").unbind().bind("click", function () {
                        if (reconcileState == 0 || reconcileState == null) {
                            if (sysAdminState == 0 || sysAdminState == null) {
                                adminStateConfirm();
                            }
                            else {
                                $.prompt('Admin State is unlocked', { buttons: {Ok: true}, prefix: 'jqismooth'});
                            }
                        }
                        else {
                            $.prompt('Reconciliation is Running.Please Wait', { buttons: {Ok: true}, prefix: 'jqismooth'});
                        }
                    });
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
    adminStatusCheck();
    $("#filterOptions").hide();
    $("#hide_search").show();
    $("#idu_form_div").css({'margin-top': '20px'});
    $("#hide_search").toggle(function () {
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
            $("#idu_form_div").css({'margin-top': '76px'});
        },
        function () {
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
            $("#idu_form_div").css({'margin-top': '20px'});

        });
    //$("div#container_body").css("padding-bottom","20px");
    // spin loading object
    //spinStart($spinLoading,$spinMainLoading);
    //spinStop($spinLoading,$spinMainLoading);
//	$("#page_tip").colorbox(
//	{
//		href:"page_tip_idu_profiling.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"650px",
//		height:"600px",
//		onComplte:function(){}
//	});

    $("#device_select_list").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Device Type', header: "Available Device Types"});

});


function alarmPortFormEdit(alarmPortId) {
    $.colorbox(
        {
            href: "alarmPortForm.py?alarmPortId=" + alarmPortId,
            title: "Alarm Port",
            opacity: 0.4,
            maxWidth: "80%",
            width: "550px",
            height: "450px",
            overlayClose: false
        });

}


function portConfigurationFormEdit(portConfigurationId, host_id, idName, className, selectedDevice) {
    $.colorbox(
        {
            href: "port_configuration_form.py?portConfigurationId=" + portConfigurationId + "&hostId=" + host_id + "&idName=" + idName + "&className=" + className + "&selected_device=" + selectedDevice,
            title: "Port Configuration",
            opacity: 0.4,
            maxWidth: "80%",
            width: "550px",
            height: "550px",
            overlayClose: false
        });
}

function portBandwidthFormEdit(portBandwidthId, host_id, idName, className, selectedDevice, index) {
    $.colorbox(
        {
            href: "port_bandwidth_form.py?portBandwidthId=" + portBandwidthId + "&hostId=" + host_id + "&idName=" + idName + "&className=" + className + "&selected_device=" + selectedDevice + "&index=" + index,
            title: "Port Bandwidth",
            opacity: 0.4,
            maxWidth: "80%",
            width: "550px",
            height: "500px",
            overlayClose: false
        });
}

function porte1FormEdit(e1PortId, host_id, idName, className, selectedDevice, index) {
    $.colorbox(
        {
            href: "e1_port.py?porte1Id=" + e1PortId + "&hostId=" + host_id + "&idName=" + idName + "&className=" + className + "&selected_device=" + selectedDevice + "&index=" + index,
            title: "Port E1 Configuration",
            opacity: 0.4,
            maxWidth: "80%",
            width: "550px",
            height: "500px",
            overlayClose: false
        });
}

function portQinQFormEdit(portQinQId, host_id, idName, className, selectedDevice, index) {
    $.colorbox(
        {
            href: "port_QinQ_form.py?portQinQId=" + portQinQId + "&hostId=" + host_id + "&idName=" + idName + "&className=" + className + "&selected_device=" + selectedDevice + "&index=" + index,
            title: "Port QinQ",
            opacity: 0.4,
            maxWidth: "80%",
            width: "550px",
            height: "500px",
            overlayClose: false
        });
}

function portVlanFormAddEdit(portVlanId, host_id, idName, className, selectedDevice, addEdit, vlanid) {
    $.colorbox(
        {
            href: "port_vlan_add_form.py?portVlanId=" + portVlanId + "&hostId=" + host_id + "&idName=" + idName + "&className=" + className + "&selected_device=" + selectedDevice + "&addEdit=" + addEdit + "&vlanId=" + vlanid,
            title: "Port VLAN",
            opacity: 0.4,
            maxWidth: "80%",
            width: "550px",
            height: "500px",
            overlayClose: false
        });

}

function portATUFormEdit(portATUId) {
    $.colorbox(
        {
            href: "port_ATU_form.py?portATUId=" + portATUId,
            title: "Port ATU",
            opacity: 0.4,
            maxWidth: "80%",
            width: "550px",
            height: "500px",
            overlayClose: false
        });
}

function portVlanFormDelete(id) {
    host_id = $("input[name='host_id']").val();
    selected_device = $("input[name='device_type_id']").val();
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "vlan_port_delete.py?vlanid=" + id + "&host_id=" + host_id,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                url = "update_vlan_port_form.py?host_id=" + host_id + "&selected_device=" + selected_device;
                method = "get";
                showdiv = "#content3_7";
                $.ajax({
                    type: method,
                    url: url,
                    success: function (result) {
                        $(showdiv).html(result);
                        spinStop($spinLoading, $spinMainLoading);
                    }
                });
            }
            else {
                $().toastmessage('showErrorToast', result.result);
                spinStop($spinLoading, $spinMainLoading);
            }
        }
    });

    return false;
}

function portLinkFormEdit(portNum, bundleNum, tableName, tableId, tableIdValue, addEdit) {
    host_id = $("input[name='host_id']").val();
    selected_device = $("input[name='device_type_id']").val();
    $.colorbox(
        {
            href: "port_link_form.py?portnum=" + portNum + "&linknum=" + bundleNum + "&tablename=" + tableName + "&tableId=" + tableId + "&tableidvalue=" + tableIdValue + "&addEdit=" + addEdit + "&host_id=" + host_id +
                "&selected_device=" + selected_device,
            title: "Link Port Configuration",
            opacity: 0.4,
            width: "600px",
            height: "92%",
            overlayClose: false,
            onComplete: function () {
                $("#iduConfiguration_linkConfigurationTable_tsaAssign").multiselect({noneSelectedText: 'Select Timeslot', selectedList: 3, minWidth: 180}).multiselectfilter();
                $("#port_number").multiselect({noneSelectedText: 'Select Port', selectedList: 3, minWidth: 180, multiple: false}).multiselectfilter();
                $("#iduConfiguration_linkConfigurationTable_clockRecovery").multiselect({noneSelectedText: 'Select Clock Source', selectedList: 3, minWidth: 180, height: 70, multiple: false}).multiselectfilter();
                $("#vlan").multiselect({noneSelectedText: 'Select VLAN', selectedList: 3, minWidth: 180, height: 70, multiple: false}).multiselectfilter();
                $("#port_number").bind("multiselectclick", function (event, ui) {
                    var sel = $("select[name='port_number']").val();
                    if (sel != ui.value) {
                        var sel = $("select[name='port_number']").val();
                        $.ajax({
                            type: "get",
                            url: "get_selected_timeslot.py?portNum=" + ui.value + "&host_id=" + host_id + "&selected_device=" + selected_device,
                            success: function (result) {
                                $("#iduConfiguration_linkConfigurationTable_tsaAssign").html(result);
                                $("#iduConfiguration_linkConfigurationTable_tsaAssign").multiselect("refresh");
                            }
                        });
                    }
                });
            }
        });
}

function portlinkformdelete(linkPortId, portNumber, bundleNumber) {
    host_id = $("input[name='host_id']").val();
    selected_device = $("input[name='device_type_id']").val();
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "link_port_delete.py?portid=" + linkPortId + "&portnumber=" + portNumber + "&bundleNumber=" + bundleNumber + "&host_id=" + host_id,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                url = "update_link_port_table.py?host_id=" + host_id + "&selected_device=" + selected_device;
                method = "get";
                showdiv = "#content1_3";
                $.ajax({
                    type: method,
                    url: url,
                    success: function (result) {
                        $(showdiv).html(result);
                        spinStop($spinLoading, $spinMainLoading);
                    }
                });
            }
            else {
                $().toastmessage('showErrorToast', result.result);
                spinStop($spinLoading, $spinMainLoading);
            }
        }
    });

    return false;

}
function commonFormSubmit(formObj, btn) {
    if (reconcileState == 0 || reconcileState == null) {
        if (sysAdminState == 0 || sysAdminState == null) {
            //if($("#"+formObj).valid())
            {
                spinStart($spinLoading, $spinMainLoading);
                CommonSetRequest(formObj, btn);
            }
        }
        else {
            $.prompt('Admin State is unlocked', { buttons: {Ok: true}, prefix: 'jqismooth'});
        }
    }
    else {
        $.prompt('Reconciliation is Running.Please Wait', { buttons: {Ok: true}, prefix: 'jqismooth'});
    }

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
    var host_id = myForm.find("input[name='host_id']").val();
    var index = myForm.find("input[name='index_id']").val();
    var selected_device = myForm.find("input[name='device_type']").val()
    if (formObj == "vlan_add_form") {
        number = 0
        $.each($('input[name="switch.vlanconfigTable.memberports"]:checked'), function () {
            number += parseInt($(this).val())
        });
        url += "?number=" + number;

    }
    if (btnValue == "Ok") {
        myForm.find("input").removeAttr("disabled");
        if (formObj != "link_form") {
            myForm.find("select").removeAttr("disabled");
            myForm.find("select").show();
            myForm.find("input").show();
        }
        else {
            myForm.find("input[name='vlan_tag']").attr("disabled", true);
            myForm.find("input[name='vlan_priority']").attr("disabled", true);
        }
        if (formObj == "") {

        }
        myForm.find("input[id='bw_id']").attr("disabled", true);
        myForm.find("input.img-submit-button").remove();
        myForm.find("input.img-done-button").remove();
        myForm.find("input[id='submit_retry']").hide();
        myForm.find("input[id='submit_cancel']").hide();
        myForm.find("input[id='submit_ok']").hide();
        myForm.find("input[id='submit_save']").show();
        spinStop($spinLoading, $spinMainLoading);
    }
    else {
        if (btnValue == "") {
            var oidValue = myForm.find("input[name='" + $(btn).attr("oid") + "']").val()
            if (oidValue == undefined) {
                oidValue = myForm.find("select[name='" + $(btn).attr("oid") + "']").val()
            }
            data = myForm.find("input[type='hidden'], :input:not(:hidden)").serialize() + "&host_id=" + myForm.find("input[name='host_id']").val() + "&device_type=" + myForm.find("input[name='device_type']").val() + "&" + $(btn).attr("oid") + "=" + oidValue + "&" + btnName + "=" + btnValue;
        }
        $.ajax({
            type: method,
            url: url,
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
                            var inputCheckButton = $("input[name='" + node + "']");
                            var parentDiv = inputCheckButton.parent();
                            if (json[node] == 0) {
                                var imageCreate = $("<input/>");
                                imageCreate.attr({"type": "button", "title": "Done", "class": "img-done-button", "oid": node});
                                if (formObj != "link_form") {
                                    selectListName.attr({"disabled": true});
                                    inputCheckButton.attr({"disabled": true});
                                    inputCheckButton.show();
                                    inputTextboxName.show();
                                    selectListName.show();
                                }
                                inputTextboxName.attr({"disabled": true});
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
                                inputCheckButton.attr({"disabled": false});
                                unSetStatus = 1
                                if (btnValue == "Save") {
                                    imgCount = imgCount + 1
                                }
                            }
                            imageCreate.insertAfter(inputTextboxName);
                            //imageCreate.insertAfter(selectListName);
                            selectListName.parent().append(imageCreate);
                            parentDiv.append(imageCreate);
                        }
                        if (imgCount >= 1) {
                            myForm.find("input[id='submit_ok']").hide();
                            myForm.find("input[id='submit_save']").hide();
                            myForm.find("input[id='submit_retry']").show();
                            myForm.find("input[id='submit_cancel']").show();
                        }
                        else {

                            myForm.find("input[id='submit_ok']").show();
                            myForm.find("input[id='submit_save']").hide();
                            myForm.find("input[id='submit_retry']").hide();
                            myForm.find("input[id='submit_cancel']").hide();
                            if (formObj == "swt_port_bandwidth_form") {
                                url = "update_bw_form.py?host_id=" + host_id + "&selected_device=" + selected_device;
                                method = "get";
                                showdiv = "#content3_2";
                                $.ajax({
                                    type: method,
                                    url: url,
                                    success: function (result) {
                                        result = $(result)
                                        result.find('.n-reconcile').tipsy({gravity: 'n'});
                                        $(showdiv).html(result);
                                    }
                                });

                            }
                            if (formObj == "qinq_form") {
                                url = "update_qinq_form.py?host_id=" + host_id + "&selected_device=" + selected_device;
                                method = "get";
                                showdiv = "#content3_3";
                                $.ajax({
                                    type: method,
                                    url: url,
                                    success: function (result) {
                                        result = $(result)
                                        result.find('.n-reconcile').tipsy({gravity: 'n'});
                                        $(showdiv).html(result);
                                    }
                                });
                            }
                            if (formObj == "swt_port_config_form") {
                                url = "update_swt_port_form.py?host_id=" + host_id + "&selected_device=" + selected_device;
                                method = "get";
                                showdiv = "#content3_1";
                                $.ajax({
                                    type: method,
                                    url: url,
                                    success: function (result) {
                                        result = $(result)
                                        result.find('.n-reconcile').tipsy({gravity: 'n'});
                                        $(showdiv).html(result);
                                    }
                                });
                            }
                            if (formObj == "vlan_add_form") {
                                url = "update_vlan_port_form.py?host_id=" + host_id + "&selected_device=" + selected_device;
                                method = "get";
                                showdiv = "#content3_7";
                                $.ajax({
                                    type: method,
                                    url: url,
                                    success: function (result) {
                                        result = $(result)
                                        result.find('.n-reconcile').tipsy({gravity: 'n'});
                                        $(showdiv).html(result);
                                    }
                                });
                            }
                            if (formObj == "link_form") {
                                url = "update_link_port_table.py?host_id=" + host_id + "&selected_device=" + selected_device;
                                method = "get";
                                showdiv = "#content1_3_1";
                                $.ajax({
                                    type: method,
                                    url: url,
                                    success: function (result) {
                                        result = $(result);
                                        result.find('.n-reconcile').tipsy({gravity: 'n'});
                                        $(showdiv).html(result);
                                    }
                                });
                            }
                            if (formObj == "e1_port_form") {
                                url = "update_e1_port_table.py?host_id=" + host_id + "&selected_device=" + selected_device;
                                method = "get";
                                showdiv = "#content1_2";
                                $.ajax({
                                    type: method,
                                    url: url,
                                    success: function (result) {
                                        result = $(result)
                                        result.find('.n-reconcile').tipsy({gravity: 'n'});
                                        $(showdiv).html(result);
                                    }
                                });
                            }

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
                            var inputCheckButton = $("input[name='" + node + "']");
                            var parentDiv = inputCheckButton.parent();
                            var imageCreate = $("<input/>");
                            if (json[node] == 0) {
                                imageCreate.attr({"type": "button", "title": "Done", "class": "img-done-button", "oid": node});
                                if (formObj != "link_form") {
                                    selectListName.attr({"disabled": true});
                                    inputCheckButton.attr({"disabled": true});
                                    inputCheckButton.show();
                                    inputTextboxName.show();
                                    selectListName.show();
                                }
                                else {
                                    myForm.find("input[name='vlan_tag']").attr("disabled", true);
                                    myForm.find("input[name='vlan_priority']").attr("disabled", true);
                                }
                                inputTextboxName.attr({"disabled": true});
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
                                inputCheckButton.attr({"disabled": false});
                            }

                            $(imageCreate).insertAfter(inputTextboxName);
                            //(imageCreate).insertAfter(selectListName);
                            selectListName.parent().append(imageCreate);
                            parentDiv.append(imageCreate);
                            myForm.find("input[id='ru.ra.raConfTable.guaranteedBroadcastBW']").attr({"disabled": true});
                        }
                        if (imgCount >= 1) {
                            myForm.find("input[id='submit_ok']").hide();
                            myForm.find("input[id='submit_save']").hide();
                            myForm.find("input[id='submit_retry']").show();
                            myForm.find("input[id='submit_cancel']").show();
                        }
                        else {
                            myForm.find("input[id='submit_ok']").show();
                            myForm.find("input[id='submit_save']").hide();
                            myForm.find("input[id='submit_retry']").hide();
                            myForm.find("input[id='submit_cancel']").hide();
                            if (formObj == "swt_port_bandwidth_form") {
                                url = "update_bw_form.py?host_id=" + host_id + "&selected_device=" + selected_device;
                                method = "get";
                                showdiv = "#content3_2";
                                $.ajax({
                                    type: method,
                                    url: url,
                                    success: function (result) {
                                        $(showdiv).html(result);
                                    }
                                });
                            }
                            if (formObj == "qinq_form") {
                                url = "update_qinq_form.py?host_id=" + host_id + "&selected_device=" + selected_device;
                                method = "get";
                                showdiv = "#content3_3";
                                $.ajax({
                                    type: method,
                                    url: url,
                                    success: function (result) {
                                        $(showdiv).html(result);
                                    }
                                });
                            }
                            if (formObj == "swt_port_config_form") {
                                url = "update_swt_port_form.py?host_id=" + host_id + "&selected_device=" + selected_device;
                                method = "get";
                                showdiv = "#content3_1";
                                $.ajax({
                                    type: method,
                                    url: url,
                                    success: function (result) {
                                        $(showdiv).html(result);
                                    }
                                });
                            }
                            if (formObj == "link_form") {
                                url = "update_link_port_table.py?host_id=" + host_id + "&selected_device=" + selected_device;
                                method = "get";
                                showdiv = "#content1_3_1";
                                $.ajax({
                                    type: method,
                                    url: url,
                                    success: function (result) {
                                        $(showdiv).html(result);
                                    }
                                });
                            }
                        }

                    }
                    else if (btnValue == "Cancel") {
                        if (formObj != "link_form") {
                            myForm.find("input").removeAttr("disabled");
                            myForm.find("input[id='bw_id']").attr("disabled", true);
                            myForm.find("select").removeAttr("disabled");
                            myForm.find("select").show();
                        }
                        else {
                            myForm.find("input[name='vlan_tag']").attr("disabled", true);
                            myForm.find("input[name='vlan_priority']").attr("disabled", true);
                        }
                        myForm.find("input.img-submit-button").remove();
                        myForm.find("input.img-done-button").remove();
                        myForm.find("input[id='submit_retry']").hide();
                        myForm.find("input[id='submit_cancel']").hide();
                        myForm.find("input[id='submit_ok']").hide();
                        myForm.find("input[id='submit_save']").show();
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
                    myForm.find("input[id='bw_id']").attr("disabled", true);
                }
                else {
                    $().toastmessage('showErrorToast', result.result);
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }

}

function commitFlashConfirm() {
    if (reconcileState == 0 || reconcileState == null) {
        if (sysAdminState == 0 || sysAdminState == null) {
            $.prompt('Do you want to store configuration data permanently on the device?\n Click Ok to confirm.', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: commitToFlash});
        }
        else {
            $.prompt('Admin State is unlocked', { buttons: {Ok: true}, prefix: 'jqismooth'});
        }
    }
    else {
        $.prompt('Reconciliation is Running. Please Wait', { buttons: {Ok: true}, prefix: 'jqismooth'});
    }
}

function commitToFlash(v, m) {
    if (v != undefined && v == true) {
        spinStart($spinLoading, $spinMainLoading);
        var host_id = $("input[id='host_id']").val();
        var device_type_id = $("input[id='device_type_id']").val();
        $.ajax({
            type: "post",
            url: "commit_to_flash.py?host_id=" + host_id + "&device_type_id=" + device_type_id,
            success: function (result) {
                if (result.success == 0) {
                    json = result.result
                    for (var node in json) {
                        if (json[node] == 0) {
                            $().toastmessage('showSuccessToast', 'Configuration data stored permanently in the device');
                        }

                    }
                }
                else {
                    $().toastmessage('showErrorToast', result.result);
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
        return false
    }

}

function rebootconfirm() {
    if (reconcileState == 0 || reconcileState == null) {
        if (sysAdminState == 0 || sysAdminState == null) {
            $.prompt('Are you sure you want to reboot this device? \n Click Ok to confirm',
                { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: reboot});
        }
        else {
            $.prompt('Admin State is unlocked', { buttons: {Ok: true}, prefix: 'jqismooth'});
        }
    }
    else {
        $.prompt('Reconciliation is Running.Please Wait', { buttons: {Ok: true}, prefix: 'jqismooth'});
    }
}

function reboot(v, m) {
    if (v != undefined && v == true) {
        spinStart($spinLoading, $spinMainLoading);
        var host_id = $("input[id='host_id']").val();
        var device_type_id = $("input[id='device_type_id']").val();
        $.ajax({
            type: "post",
            url: "reboot.py?host_id=" + host_id,
            success: function (result) {
                if (result.success == 0) {
                    json = result.result
                    for (var node in json) {
                        //console.log(json);
                        //console.log(json[node]);
                        if (json[node] == 0 || parseInt(node) == 53) {
                            chkPing = 0;
                            pingCheck();
                        }
                        else {
                            $().toastmessage('showErrorToast', result.result);
                            spinStop($spinLoading, $spinMainLoading);
                        }
                    }
                }
                else {
                    $().toastmessage('showWarningToast', result.result);
                    spinStop($spinLoading, $spinMainLoading);
                }
            }
        });
        return false
    }
}

//var callA = null;
//var timeInterval = 1000
function pingCheck() {
    chkPing = chkPing + 1
    var host_id = $("input[id='host_id']").val();
    $.ajax({
        type: "post",
        url: "ping_check.py?host_id=" + host_id,
        success: function (result) {
            if (result == 0) {
                $().toastmessage('showSuccessToast', 'Device Rebooted SuccesFully');
                spinStop($spinLoading, $spinMainLoading);
            }
            else if (result == 2) {
                $().toastmessage('showErrorToast', 'Host does not Exist');
                spinStop($spinLoading, $spinMainLoading);
            }
            else {
                if (chkPing < 30) {
                    pingCheck();
                }
                else {
                    $().toastmessage('showErrorToast', 'Device Not Responding');
                    spinStop($spinLoading, $spinMainLoading);
                }
            }
        }
    });
    return false;
}


function reconciliationConfirm() {
    var host_id = $("input[id='host_id']").val();
    if (reconcileState == 0 || reconcileState == null) {
        if (sysAdminState == 0 || sysAdminState == null) {
            chk_common_rec(host_id);
        }
        else {
            $.prompt('Admin State is unlocked', { buttons: {Ok: true}, prefix: 'jqismooth'});
        }
    }
    else {
        $.prompt('Reconciliation is Running.Please Wait', { buttons: {Ok: true}, prefix: 'jqismooth'});
    }

}

function chk_common_rec(host_id) {
    $.ajax({
        type: "get",
        url: "chk_common_reconcile.py?host_id=" + host_id,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                common_rec()
            }
            else {
                $().toastmessage('showWarningToast', result.result);
            }
        }
    });
    return false;
}
function common_rec() {
    hrefAttr = $("a.active").attr("href");
    anchorObj = $(hrefAttr).find("a.active");
    text_name = $(anchorObj).text();
    var text_val = text_name.replace(/\s/g, "%20");
    $.colorbox(
        {
            href: "local_reconciliation.py?textname=" + text_val,
            title: "Form Reconciliation",
            opacity: 0.4,
            maxWidth: "80%",
            width: "500px",
            height: "250px"
        });
}

function reconcileForm(obj, formid) {
    formObj = $(obj);
    formId = $("#" + formid);
    $.prompt('Device Configuration data would be Synchronized with the UNMP server Database', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: reconciliation});
    return false;
}


function reconciliation(v, m) {
    if (v != undefined && v == true) {
        spinStart($spinLoading, $spinMainLoading);
        var host_id = $("input[id='host_id']").val();
        var device_type_id = $("input[id='device_type_id']").val();
        data = $(formId).serialize();
        form_rec = $("input[name='form_rec']:checked").val();
        var divId = $(anchorObj).attr("href");
        //var divId = attrText.replace("#","");
        formName = $(divId).find("input[name='common_rec']").attr("form_name");
        tableName = $(divId).find("input[name='common_rec']").attr("tablename");
        var table_prefix = "idu_";
        if (parseInt(form_rec) == 0) {
            $.ajax({
                type: "get",
                url: "common_reconcile.py?host_id=" + host_id + "&device_type=" + device_type_id + "&tableName=" + tableName,
                data: data,
                success: function (result) {
                    if (parseInt(result.success) == 0) {
                        $.ajax({
                            type: "get",
                            url: "idu_form_reconcile.py?formName=" + formName + "&host_id=" + host_id + "&device_type=" + device_type_id,
                            success: function (htmlResult) {
                                $(divId).html();
                                $(divId).html(htmlResult);
                                getAdminStateIdu(host_id, device_type_id);
                            }
                        });
                        $().toastmessage('showSuccessToast', text_name + " Reconciliation done successfully");
                    }
                    else {
                        $().toastmessage('showErrorToast', result.result);
                    }
                    $.colorbox.close();
                    spinStop($spinLoading, $spinMainLoading);
                }
            });
        }
        else if (form_rec == undefined) {
            $().toastmessage('showErrorToast', "Please select the reconciliation mode");
            spinStop($spinLoading, $spinMainLoading);
        }
        else {
            $.ajax({
                type: "post",
                url: "device_update_reconciliation.py?host_id=" + host_id + "&device_type_id=" + device_type_id + "&table_prefix=" + table_prefix,
                success: function (result) {
                    if (result.success == 0) {
                        var json = result.result
                        for (var node in json) {
                            if (node <= 35) {
                                $().toastmessage('showWarningToast', node + "% reconciliation done. \n Please reconcile the device again");
                            }
                            else if (node <= 90) {

                                $().toastmessage('showWarningToast', node + "% reconciliation done. \n Please reconcile the device again");
                            }
                            else {

                                $().toastmessage('showSuccessToast', "Reconciliation done successfully");
                            }
                            break;
                        }
                        getAdminStateIdu(host_id, device_type_id);
                        $.colorbox.close();
                        deviceList();
                    }
                    else {
                        $().toastmessage('showErrorToast', result.result);
                    }
                    spinStop($spinLoading, $spinMainLoading);
                }
            });
            return false;
        }
        $.colorbox.close();
    }
}

function getAdminStateIdu(hostId, deviceType) {

    $.ajax({
        type: "get",
        url: "global_admin.py?host_id=" + hostId,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                json = result.result;
                for (var node in json) {
                    var adminDivObj = $("#admin_div");
                    var objTable = $(adminDivObj);
                    for (var item in json[node][0]) {
                        var imgRec = $(adminDivObj).find("a:eq(" + item + ")");
                        var imgbtn = $(imgRec);
                        var port = parseInt(item) + 1;
                        tdObj = $("#content1_2").find("table").find("tr:eq(" + port + ")").find("td:eq(3)");
                        if (parseInt(json[node][0][item]) == 1 && parseInt(json[node][2][item]) == 1) {
                            imgbtn.attr({"class": "green"});
                            imgbtn.html("E1" + " " + "Port" + (parseInt(item) + 1) + " " + "Unlocked");
                            tdObj.html("Unlocked");
                        }
                        else if (parseInt(json[node][0][item]) == 1 && parseInt(json[node][2][item]) == 0) {
                            imgbtn.attr({"class": "red"});
                            imgbtn.html("E1" + " " + "Port" + (parseInt(item) + 1) + " " + "Unlocked");
                            tdObj.html("Unlocked");
                        }
                        else {
                            imgbtn.attr({"class": "red"});
                            imgbtn.html("E1" + " " + "Port" + (parseInt(item) + 1) + " " + "Locked");
                            tdObj.html("Locked");
                        }
                    }

                    var imgRec = $(adminDivObj).find("a:eq(4)");
                    var imgbtn = $(imgRec);
                    if (parseInt(json[node][1]) == 1) {
                        imgbtn.html("IDU Admin Unlocked");
                        imgbtn.attr({"class": "green"});
                    }
                    else {
                        imgbtn.attr({"class": "red"});
                        imgbtn.html("IDU Admin Locked");
                    }
                    for (var item in json[node][2]) {
                        var port = parseInt(item) + 1;
                        tdObj = $("#content1_3").find("table").find("tr:eq(" + port + ")").find("td:eq(9)");
                        imgbtn = $(tdObj).find("a");
                        if (parseInt(json[node][2][item]) == 1) {
                            imgbtn.attr({"class": "green"});
                            imgbtn.html("Unlocked");
                        }
                        else {
                            imgbtn.attr({"class": "red"});
                            imgbtn.html("Locked");
                        }
                    }

                }
            }
        }
    });
}


function adminStateConfirm() {

    if (reconcileState == 0 || reconcileState == null) {
        if (sysAdminState == 0 || sysAdminState == null) {

            $.prompt('Are you sure you want to lock this device? \n Click Ok to confirm.', {
                buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: reconciliation});
        }
        else {
            $.prompt('Admin State is unlocked', { buttons: {Ok: true}, prefix: 'jqismooth'});
        }
    }
    else {
        $.prompt('Reconciliation is Running.Please Wait', { buttons: {Ok: true}, prefix: 'jqismooth'});
    }

}

function main_admin_state_change(event, obj, hostId, adminStateName) {
    attrValue = $(obj).attr("state");
    if (parseInt(attrValue) == 0) {
        attrValue = 1;
    }
    else {
        attrValue = 0;

    }
    //event.preventDefault();
    $.ajax({
        type: "get",
        url: "main_admin_parameters.py?host_id=" + hostId + "&admin_state_name=" + adminStateName + "&state=" + attrValue,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                if (attrValue == 1) {
                    //  $(obj).attr({"class":"green"});
                    $(obj).attr({"state": 1});
                }
                else {
                    //$(obj).attr({"class":"red"});
                    $(obj).attr({"state": 0});
                }
                clearTimeout(callA);
                callA = null;
                adminStatusCheck();
            }
            else {
                $().toastmessage('showErrorToast', result.result);
            }
        }

    });

}

function idu_admin_state_change(event, obj, hostId, primaryId, portNum, adminStateName, adminType) {
    attrValue = $(obj).attr("state");
    if (parseInt(attrValue) == 0) {
        attrValue = 1;
    }
    else {
        attrValue = 0;

    }
    //event.preventDefault();
    if (parseInt(adminType) == 0) {
        urlString = "e1_admin_parameters.py?host_id=" + hostId + "&primary_id=" + primaryId + "&port_num=" + portNum + "&admin_state_name=" + adminStateName + "&state=" + attrValue
    }
    else {
        bundleNum = $(obj).attr("bundle_num");
        urlString = "link_admin_parameters.py?host_id=" + hostId + "&primary_id=" + primaryId + "&port_num=" + portNum + "&bundle_num=" + bundleNum + "&admin_state_name=" + adminStateName + "&state=" + attrValue
    }

    $.ajax({
        type: "get",
        url: urlString,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                if (attrValue == 1) {
                    $(obj).attr({"state": 1});

                }
                else {
                    $(obj).attr({"state": 0});

                }
                clearTimeout(callA);
                callA = null;
                adminStatusCheck();
            }
            else {
                $().toastmessage('showErrorToast', result.result);
            }
        }

    });


}

var callA = null;
function adminStatusCheck() {
    var host_id = $("input[name='host_id']").val();
    $.ajax({
        type: "get",
        url: "global_admin.py?host_id=" + host_id,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                json = result.result;
                for (var node in json) {
                    var adminDivObj = $("#admin_div");
                    var objTable = $(adminDivObj);
                    for (var item in json[node][0]) {
                        var imgRec = $(adminDivObj).find("a:eq(" + item + ")");
                        var imgbtn = $(imgRec);
                        var port = parseInt(item) + 1;
                        tdObj = $("#content1_2").find("table").find("tr:eq(" + port + ")").find("td:eq(3)");
                        if (parseInt(json[node][0][item]) == 1 && parseInt(json[node][2][item]) == 1) {
                            imgbtn.attr({"class": "green"});
                            imgbtn.html("E1" + " " + "Port" + (parseInt(item) + 1) + " " + "Unlocked");
                            tdObj.html("Unlocked");
                        }
                        else if (parseInt(json[node][0][item]) == 1 && parseInt(json[node][2][item]) == 0) {
                            imgbtn.attr({"class": "red"});
                            imgbtn.html("E1" + " " + "Port" + (parseInt(item) + 1) + " " + "Unlocked");
                            tdObj.html("Unlocked");
                        }
                        else {
                            imgbtn.attr({"class": "red"});
                            imgbtn.html("E1" + " " + "Port" + (parseInt(item) + 1) + " " + "Locked");
                            tdObj.html("Locked");
                        }
                    }

                    var imgRec = $(adminDivObj).find("a:eq(4)");
                    var imgbtn = $(imgRec);
                    if (parseInt(json[node][1]) == 1) {
                        imgbtn.html("IDU Admin Unlocked");
                        imgbtn.attr({"class": "green"});
                    }
                    else {
                        imgbtn.attr({"class": "red"});
                        imgbtn.html("IDU Admin Locked");
                    }
                    for (var item in json[node][2]) {
                        var port = parseInt(item) + 1;
                        tdObj = $("#content1_3").find("table").find("tr:eq(" + port + ")").find("td:eq(9)");
                        imgbtn = $(tdObj).find("a");
                        if (parseInt(json[node][2][item]) == 1) {
                            imgbtn.attr({"class": "green"});
                            imgbtn.html("Unlocked");
                        }
                        else {
                            imgbtn.attr({"class": "red"});
                            imgbtn.html("Locked");
                        }
                    }

                }
            }

            callA = setTimeout(function () {

                adminStatusCheck();

            }, timecheck);
        }
    });

}


