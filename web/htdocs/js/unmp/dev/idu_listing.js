var timeSlot = 60000;
var loadingSpinCss = {"left": "28px", "top": "29px"};
var loadingSpinLines = 12;
var loadingSpinLength = 6;
var loadingSpinWidth = 3;
var loadingSpinRadius = 6;
var loadingSpinColor = '#FFF';
var loadingSpinSpeed = 1;
var loadingSpinTrail = 30;
var loadingSpinShadow = true;
var timecheck = 60000;
var errorMsg = "Some server problem occurred, Please try again later."
var globalLinkObj = null;
var unreachable = null;
var timer = null;
$(function () {
    //we call the devicelist function
    $("input[id='filter_ip']").ccplAutoComplete("common_ip_mac_search.py?device_type=" + $("select[id='device_type']").val() + "&ip_mac_search=" + 1, {
        dataType: 'json',
        max: 30,
        cache: false,
        selectedItem: $("input[id='filter_ip']").val(),
        callAfterSelect: function (obj) {
            ipSelectMacDeviceType(obj, 1);
        }
    });

    $("input[id='filter_mac']").ccplAutoComplete("common_ip_mac_search.py?device_type=" + $("select[id='device_type']").val() + "&ip_mac_search=" + 0 + "&search_type=", {
        dataType: 'json',
        max: 30,
        cache: false,
        selectedItem: $("input[id='filter_mac']").val(),
        callAfterSelect: function (obj) {
            ipSelectMacDeviceType(obj, 0);
        }
    });
    deviceList();
    $("#filterOptions").hide();
    $("#hide_search").show();
    $("#up_down_search").toggle(function () {
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
        function () {
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
    //Here we call the click event of search button
    $("input[id='btnSearch']").click(function () {
        //call the device list function on click of search button
        deviceList();
    })
//	$("#page_tip").colorbox(
//	{
//		href:"page_tip_idu_listing.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"600px",
//		height:"420px",
//		onComplte:function(){}
//	});
    $("body").click(function () {
        $("#status_div").hide();
        $(".listing-icon").removeClass("listing-icon-selected");
    });
    //spinStart($spinLoading,$spinMainLoading);
    //spinStop($spinLoading,$spinMainLoading);
});
function iduFirmwareUpdate(host_id, device_type, device_state) {
    spinStop($spinLoading, $spinMainLoading);
    $.colorbox(
        {
            href: "idu_firmware_view.py?host_id=" + host_id + "&device_type=" + device_type + "&device_list_state=" + device_state,
            iframe: true,
            title: "Firmware Update",
            opacity: 0.4,
            maxWidth: "80%",
            width: "400px",
            height: "300px",
            overlayClose: false
        });
}

function deviceList() {
    // spin loading object
    // this retreive the value of ipaddress textbox
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
    var ip_address = $("input[id='filter_ip']").val();
    // this retreive the value of macaddress textbox
    var mac_address = $("input[id='filter_mac']").val();
    // this retreive the value of selectdevicetype from select menu
    var device_type = $("select[id='device_type']").val();
    if (device_type == "odu100" || device_type == "odu16") {
        urlString = "get_device_data_table.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type;
        parent.main.location = "odu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + device_type;
    }
    else if (device_type == "ap25") {
        urlString = "ap_device_listing_table.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type;
        parent.main.location = "ap_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + device_type;
    }
    else if (device_type == "ccu") {
        urlString = "ccu_device_listing_table.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type
        parent.main.location = "ccu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + device_type;
    }
    else {
        urlString = "idu_device_listing_table.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type
    }
    var oTable = $('#device_data_table').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "bServerSide": true,
        "oSearch": {"sSearch": ip_address},
        "aoColumns": [
            { "sWidth": "2%"},
            { "sWidth": "10%"},
            { "sWidth": "10%" },
            { "sWidth": "10%" },
            { "sWidth": "11%" },
            { "sWidth": "15%" },
            { "sWidth": "10%" },
            { "sWidth": "10%", "bSortable": false },
            { "sWidth": "20%", "bSortable": false }
        ],
        "bDestroy": true,
        "sAjaxSource": "idu_device_listing_table.py?&ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type,
        "fnServerData": function (sSource, aoData, fnCallback) {
            $.getJSON(sSource, aoData, function (json) {
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
                chkReconciliationRun();
                oduListingTableClick();
                chkDeviceStatus();
                adminStatusCheck();
            });
        }
    });


    //	}
    //});
    $("input[id='filter_ip']").val(ip_address);
    $("input[id='filter_mac']").val(mac_address);
    $("select[id='device_type']").val(device_type);
};


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


function imgReconcile(obj, hostId, deviceTypeId, tablePrefix, insertUpdate) {
    reconcileHostId = hostId;
    reconcileDeviceTypeId = deviceTypeId;
    reconcileTablePrefix = tablePrefix;
    reconcileInsertUpdate = insertUpdate;
    imgReconcileBtnObj = $(obj);
    var imgBtn = imgReconcileBtnObj;
    var recTableObj = imgBtn.parent().parent();
    var tableObj = $(recTableObj);
    if (tableObj.hasClass("listing-color")) {

    }
    else {
        if (imgBtn.data("rec") == 1) {
            //$.prompt('Reconciliation is already Running.Please Wait',{ buttons:{Ok:true}, prefix:'jqismooth'});
            spinStop($spinLoading, $spinMainLoading);
        }
        else {
            $.prompt('Device Configuration data would be Synchronized with the UNMP server Database. \n', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: imgOdu16Reconcilation});
        }
    }
}


function imgOdu16Reconcilation(v, m) {
    if (v != undefined && v == true && reconcileHostId && reconcileDeviceTypeId && reconcileTablePrefix && reconcileInsertUpdate && imgReconcileBtnObj) {
        spinStop($spinLoading, $spinMainLoading);
        var imgBtn = imgReconcileBtnObj;
        var tableObj = imgBtn.parent().parent();
        var objTableDetail = $(tableObj);
        if (objTableDetail.hasClass("listing-color")) {
            $.prompt('Reconciliation is already Running.Please Wait', { buttons: {Ok: true}, prefix: 'jqismooth'});
        }
        else {
            if (imgBtn.data("rec") == undefined) {
                imgBtn.data("rec", 0);
            }
            if (imgBtn.data("rec") == 0) {
                imgBtn.data("rec", 1);
                var classAttr = objTableDetail.attr("class");
                objTableDetail.attr("listClass", classAttr);
                objTableDetail.removeClass(classAttr);
                objTableDetail.addClass("listing-color");
                flagClick = true;
                $.ajax({
                    type: "get",
                    url: "device_update_reconciliation.py?host_id=" + reconcileHostId + "&device_type_id=" + reconcileDeviceTypeId + "&table_prefix=" + reconcileTablePrefix + "&insert_update=" + reconcileInsertUpdate,
                    success: function (result) {
                        imgBtn.data("rec", 0);
                        flagClick = false;
                        objTableDetail.removeClass("listing-color");
                        objTableDetail.addClass(objTableDetail.attr("listClass"));
                        objTableDetail.removeAttr("listClass");
                        flagClick = false;
                        try {
                            if (result.success == 0) {
                                var json = result.result
                                for (var node in json) {
                                    if (parseInt(node) <= 35) {
                                        imgBtn.attr("src", "images/new/r-red.png");
                                        imgBtn.attr("original-title", node + "% Done");
                                        $().toastmessage('showWarningToast', node + "% reconciliation done for device " + json[node][0] + "(" + json[node][1] + ")" + ".Please reconcile the device again");
                                    }
                                    else if (parseInt(node) <= 90) {
                                        imgBtn.attr("src", "images/new/r-black.png");
                                        imgBtn.attr("original-title", node + "% Done");
                                        $().toastmessage('showWarningToast', node + "% reconciliation done for device " + json[node][0] + "(" + json[node][1] + ")" + ".Please reconcile the device again");
                                    }
                                    else {
                                        imgBtn.attr("src", "images/new/r-green.png");
                                        imgBtn.attr("original-title", "Reconciliation " + node + " % Done");
                                        $().toastmessage('showSuccessToast', "Reconciliation done successfully for device " + json[node][0] + "(" + json[node][1] + ")");
                                    }
                                    break;
                                }
                            }
                            else {
                                $().toastmessage('showErrorToast', result.result);
                            }
                        }
                        catch (err) {

                        }
                    }
                });
                return false;
            }
        }
    }
    else {
        spinStop($spinLoading, $spinMainLoading);
    }

}

function show_link_admin_state(event, obj, hostId, deviceTypeId) {
    $(".listing-icon").removeClass("listing-icon-selected");
    globalLinkObj = $(obj);
    $.ajax({
        type: "get",
        url: "link_admin_state_show.py?host_id=" + hostId + "&device_type_id=" + deviceTypeId,
        success: function (result) {
            $(obj).parent().addClass("listing-icon-selected");
            obj = $("#status_div");
            obj.html("");
            obj.html("<div class='sm-loading'></div><div class='sm-spin' style='top:32%;left:31%'></div>" + result);
            obj.css({'top': event.pageY - 90});
            obj.css({'left': event.pageX - 200 - parseInt((($("#status_div").width()) * 2) / 3)});
            $("#status_div").find("a").tipsy({gravity: 'n'});
            if (unreachable == true) {
                $("#status_div").addClass("unreachable");
            }
            else {
                $("#status_div").removeClass("unreachable");
            }
            $("input[type='radio']").tipsy({gravity: 'n'});
            $loading = obj.find("div.sm-loading");
            $spin = obj.find("div.sm-spin");
            obj.show();

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
    var trObj = $(obj).parent().parent().parent().parent();
    var divStatus = $("#table_status").parent();
    if ($(trObj).hasClass("unreachable") || $(divStatus).hasClass("unreachable")) {
        if (attrValue == 1) {
            if (parseInt(adminType) == 0) {
                $.prompt('E1 Port' + portNum + ' Unlock operation failed <br/>Device might be unreachable since ' + String($(trObj).attr("timer")), { buttons: {Ok: true}, prefix: 'jqismooth'});
            }
            else {
                $.prompt('Link Port' + portNum + ' Unlock operation failed <br/>Device might be unreachable since ' + timer, { buttons: {Ok: true}, prefix: 'jqismooth'});
            }
        }
        else {
            if (parseInt(adminType) == 0) {
                $.prompt('E1 Port' + portNum + ' Lock operation failed <br/>Device might be unreachable since ' + String($(trObj).attr("timer")), { buttons: {Ok: true}, prefix: 'jqismooth'});
            }
            else {
                $.prompt('Link Port' + portNum + ' Lock operation failed <br/>Device might be unreachable since ' + timer, { buttons: {Ok: true}, prefix: 'jqismooth'});
            }
        }
    }
    else {
        // event.preventDefault();
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
                        $(obj).attr({"class": "green"});
                        $(obj).attr({"state": 1});
                        if (parseInt(adminType) == 0) {
                            $(obj).attr({"original-title": "E1 Port" + portNum + " " + "Unlocked"});
                        }
                        else {
                            $(obj).attr({"original-title": "Link" + portNum + " " + "Unlocked"});
                        }
                    }
                    else {
                        $(obj).attr({"class": "red"});
                        $(obj).attr({"state": 0});
                        if (parseInt(adminType) == 0) {
                            $(obj).attr({"original-title": "E1 Port" + portNum + " " + "Locked"});
                        }
                        else {
                            $(obj).attr({"original-title": "Link" + portNum + " " + "Locked"});
                        }

                    }
                    if (parseInt(adminType) != 0) {
                        $.ajax({
                            type: "get",
                            url: "link_status_count.py?host_id=" + hostId,
                            success: function (result) {
                                if (parseInt(result.success) == 0) {
                                    if (parseInt(result.result) <= 35) {
                                        globalLinkObj.attr({"class": "red"});
                                    }
                                    else if (parseInt(result.result) <= 90) {
                                        globalLinkObj.attr({"class": "yellow"});
                                    }
                                    else {
                                        globalLinkObj.attr({"class": "green"});
                                    }
                                    globalLinkObj.attr({"original-title": result.result + "% Links Unlocked"});

                                }
                                else {
                                    globalLinkObj.attr({"class": "red"});
                                    globalLinkObj.attr({"original-title": "No Link Exists"});
                                }
                            }
                        });
                    }
                }
                else {
                    $().toastmessage('showErrorToast', result.result);
                }
            }

        });
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
    var trObj = $(obj).parent().parent().parent().parent();
    if ($(trObj).hasClass("unreachable")) {
        if (attrValue == 1) {
            $.prompt('Admin State Unlock operation failed <br/>Device might be unreachable since ' + String($(trObj).attr("timer")), { buttons: {Ok: true}, prefix: 'jqismooth'});
        }
        else {
            $.prompt('Admin State Lock operation failed <br/>Device might be unreachable since ' + String($(trObj).attr("timer")), { buttons: {Ok: true}, prefix: 'jqismooth'});
        }
    }
    else {
        // event.preventDefault();
        $.ajax({
            type: "get",
            url: "main_admin_parameters.py?host_id=" + hostId + "&admin_state_name=" + adminStateName + "&state=" + attrValue,
            success: function (result) {
                if (parseInt(result.success) == 0) {
                    if (attrValue == 1) {
                        $(obj).attr({"class": "green"});
                        $(obj).attr({"state": 1});
                    }
                    else {
                        $(obj).attr({"class": "red"});
                        $(obj).attr({"state": 0});
                    }
                }
                else {
                    $().toastmessage('showErrorToast', result.result);
                }
            }

        });

    }

}

function link_lock_unlock_admin(event, obj, hostId, adminStateName, state) {
    spinStart($spin, $loading, loadingSpinCss, loadingSpinLines, loadingSpinLength, loadingSpinWidth, loadingSpinRadius, loadingSpinColor, loadingSpinSpeed, loadingSpinTrail, loadingSpinShadow);
    var tdObj = null;
    var radioObj = null;
    // event.stopPropagation();
    var divStatus = $("#table_status").parent();
    if (unreachable == true) {
        if (state == 0) {
            $.prompt('Lock all Link operation failed <br/>Device might be unreachable since ' + timer, { buttons: {Ok: true}, prefix: 'jqismooth'});
        }
        else {
            $.prompt('Unlock all Link operation failed <br/>Device might be unreachable since ' + timer, { buttons: {Ok: true}, prefix: 'jqismooth'});
        }
    }
    else {
        tableObj = $(obj).parent().parent();
        if (state == 0) {
            tdObj = $(obj).parent().next();
            radioObj = $(tdObj).find("input[type='radio']");
            $(radioObj).attr({"disabled": true});

        }
        else {
            tdObj = $(obj).parent().prev();
            radioObj = $(tdObj).find("input[type='radio']");
            $(radioObj).attr({"disabled": true});

        }
        $.ajax({
            type: "get",
            url: "link_all_locked_unlocked.py?host_id=" + hostId + "&admin_state_name=" + adminStateName + "&state=" + state,
            success: function (result) {
                if (parseInt(result.success) == 0) {
                    i = 1
                    for (var node in result.result) {
                        if (result.result[node] == 0 || result.result[node] == '0') {

                            if (state == 0) {
                                $("#" + node).attr({"class": "red"});
                                $("#" + node).attr({"state": state});

                            }
                            else {
                                $("#" + node).attr({"src": "green"});
                                $("#" + node).attr({"state": state});
                            }
                            $("#" + node).attr({"original-title": "Link " + String(i) + "Unlocked"});

                        }
                        else {
                            $("#" + node).attr({"original-title": "Link " + String(i) + "Locked"});
                        }
                        i = i + 1

                    }
                    $.ajax({
                        type: "get",
                        url: "link_status_count.py?host_id=" + hostId,
                        success: function (result) {
                            if (parseInt(result.success) == 0) {
                                if (parseInt(result.result) <= 35) {
                                    globalLinkObj.attr({"class": "red"});
                                }
                                else if (parseInt(result.result) <= 90) {
                                    globalLinkObj.attr({"class": "yellow"});
                                }
                                else {
                                    globalLinkObj.attr({"class": "green"});
                                }
                                globalLinkObj.attr({"original-title": result.result + "% Links Unlocked"});

                            }
                            else {
                                globalLinkObj.attr({"class": "red"});
                                globalLinkObj.attr({"original-title": "No Link Exists"});
                            }
                        }
                    });

                }
                else {
                    $().toastmessage('showErrorToast', result.result);

                }
                $(radioObj).attr({"disabled": false});
                spinStop($spin, $loading);
            }
        });
    }

}


function oduListingTableClick() {
    var tableObj = $("table#device_data_table tr");
    tableObj.click(function (event) {
        var elementClick = $(event.target);
        if ($(this).hasClass("listing-color") || $(this).hasClass(""))//check this type of condition because when more than one reconciliation performs the class has been 												      empty due to confliction of objects
        {
            if ($(elementClick).hasClass("imgEditodu16")) {
                $.prompt('Reconciliation is Running. Please wait.', {prefix: 'jqismooth'});
                return false;
            }
        }

    });
}
var callA = null;
function chkReconciliationRun() {
    if (callA != null) {
        clearTimeout(callA);
    }
    $.ajax({
        type: "get",
        url: "reconciliation_status_idu.py",
        success: function (result) {
            if (result.success == 0) {
                var json = result.result;
                var oldClassAttr = null;
                for (var node in json) {
                    var recTableObj = $("#" + node).parent().parent().parent();
                    var objTable = $(recTableObj);
                    if (parseInt(json[node][0]) == 1) {
                        if (objTable.hasClass("listing-color")) {
                        }
                        else {
                            var classAttr = objTable.attr("class");
                            objTable.attr("listingClass", classAttr);
                            objTable.removeClass(classAttr);
                            objTable.addClass("listing-color");
                        }
                    }
                    else if (parseInt(json[node][0]) == 2) {
                        var imgRec = $(recTableObj).find("td:eq(4)").find("img:eq(4)");
                        var imgBtn = $(imgRec);
                        if (json[node][1] <= 35) {
                            imgBtn.attr("src", "images/new/r-red.png");
                            imgBtn.attr("original-title", json[node][1] + "% Done");
                            $().toastmessage('showWarningToast', json[node][1] + "% Done.Please Again Reconcile The Device");
                        }
                        else if (json[node][1] <= 90) {
                            imgBtn.attr("src", "images/new/r-black.png");
                            imgBtn.attr("original-title", json[node][1] + "% Done");
                            $().toastmessage('showWarningToast', json[node][1] + "% Done.Please Again Reconcile The Device");
                        }
                        else {
                            imgBtn.attr("src", "images/new/r-green.png");
                            imgBtn.attr("original-title", json[node][1] + "% Done");
                            $().toastmessage('showSuccessToast', 'Reconcilation Done SuccessFully');
                        }
                    }
                    else {
                        if (objTable.hasClass("listing-color")) {
                            var imgRec = $(recTableObj).find("td:eq(4)").find("img:eq(4)");
                            var imgBtn = $(imgRec);

                            if (parseInt(json[node][1]) <= 35) {
                                imgBtn.attr("src", "images/new/r-red.png");
                                imgBtn.attr("original-title", json[node][1] + "% Done");
                            }
                            else if (parseInt(json[node][1]) <= 90) {
                                imgBtn.attr("src", "images/new/r-black.png");
                                imgBtn.attr("original-title", json[node][1] + "% Done");
                            }
                            else {
                                imgBtn.attr("src", "images/new/r-green.png");
                                imgBtn.attr("original-title", json[node][1] + "% Done");
                            }
                            objTable.removeClass("listing-color");
                            objTable.addClass($(recTableObj).attr("listingClass"));
                            objTable.removeAttr("listingClass");
                        }

                    }
                }
            }
            callA = setTimeout(function () {

                chkReconciliationRun();

            }, timeSlot);
        }
    });

}


var callC = null;
function chkDeviceStatus() {
    host_id = $("input[name='host_id']").val();
    if (callC != null) {
        clearTimeout(callC);
    }
    $.ajax({
        type: "get",
        url: "device_status.py?host_id=" + host_id,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                json = result.result;
                for (var node in json) {
                    var recTableObj = $("#" + node).parent().parent().parent();
                    var objTable = $(recTableObj);
                    var tdObj = $(recTableObj).find("td:eq(0)");
                    var trObj = $(tdObj).parent();
                    var imgRec = $(tdObj).find("img:eq(0)");
                    var imgbtn = $(imgRec);
                    if (parseInt(json[node][0]) == 1) {
                        imgbtn.attr({"src": "images/temp/red_dot.png"});
                        imgbtn.attr({"original-title": "Device Unreachable since " + String(json[node][1])});
                        $(trObj).addClass("unreachable");
                        $(trObj).attr({"timer": String(json[node][1])});
                        unreachable = true;
                        timer = String(json[node][1])
                    }
                    else {
                        imgbtn.attr({"src": "images/temp/green_dot.png"});
                        imgbtn.attr({"original-title": "Device Reachable"});
                        $(trObj).removeClass("unreachable");
                        $(trObj).removeAttr("timer");
                        unreachable = false;
                    }
                }
            }

            callC = setTimeout(function () {

                chkDeviceStatus();

            }, timecheck);
        }
    });

}


//{'result': {'82': [[0, 0, 0, 0], 0, 'No Link Exists'], '81': [[0, 0, 0, 0], 0, 0]}, 'success': 0}


var callB = null;
function adminStatusCheck() {
    host_id = $("input[name='host_id']").val();
    if (callB != null) {
        clearTimeout(callB);
    }
    $.ajax({
        type: "get",
        url: "global_admin_request.py?host_id=" + host_id,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                json = result.result;
                for (var node in json) {
                    var recTableObj = $("#" + node).parent().parent().parent();
                    var objTable = $(recTableObj);
                    for (var item in json[node][0]) {
                        var imgRec = $(recTableObj).find("td:eq(7)").find("a:eq(" + item + ")");
                        var imgbtn = $(imgRec);
                        if (parseInt(json[node][0][item]) == 1) {
                            imgbtn.attr({"class": "green"});
                            imgbtn.attr({"original-title": "E1" + " " + "Port" + (parseInt(item) + 1) + " " + "Unlocked"});
                        }
                        else {
                            imgbtn.attr({"class": "red"});
                            imgbtn.attr({"original-title": "E1" + " " + "Port" + (parseInt(item) + 1) + " " + "Locked"});
                        }
                    }

                    var imgRec = $(recTableObj).find("td:eq(7)").find("a:eq(4)");
                    var imgbtn = $(imgRec);
                    if (parseInt(json[node][1]) == 1) {
                        imgbtn.attr({"original-title": "IDU Admin Unlocked"});
                        imgbtn.attr({"class": "green"});
                    }
                    else {
                        imgbtn.attr({"class": "red"});
                        imgbtn.attr({"original-title": "IDU Admin Locked"});
                    }
                    var imgRec = $(recTableObj).find("td:eq(7)").find("a:eq(5)");
                    var imgbtn = $(imgRec);
                    if (json[node][2] == "No Link Exists") {
                        imgbtn.attr({"original-title": "No Link Exists"});
                    }
                    else {
                        if (parseInt(json[node][2]) <= 35) {
                            imgbtn.attr({"class": "red"});
                            imgbtn.attr({"original-title": json[node][2] + "% Links Unlocked"});
                        }
                        else if (parseInt(json[node][2]) < 90) {
                            imgbtn.attr({"class": "yellow"});
                            imgbtn.attr({"original-title": json[node][2] + "% Links Unlocked"});
                        }
                        else {
                            imgbtn.attr({"class": "green"});
                            imgbtn.attr({"original-title": json[node][2] + "% Links Unlocked"});
                        }
                    }

                }
            }

            callB = setTimeout(function () {

                adminStatusCheck();

            }, timecheck);
        }
    });

}


