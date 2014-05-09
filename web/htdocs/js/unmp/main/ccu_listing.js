var timeSlot = 5000;
var loadingSpinCss = {"left": "28px", "top": "29px"};
var loadingSpinLines = 12;
var loadingSpinLength = 6;
var loadingSpinWidth = 3;
var loadingSpinRadius = 6;
var loadingSpinColor = '#FFF';
var loadingSpinSpeed = 1;
var loadingSpinTrail = 30;
var loadingSpinShadow = true;
var timecheck = 6000;
var errorMsg = "Some server problem occurred, Please try again later."
var globalLinkObj = null;
$(function () {
    //we call the devicelist function
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
    $("#filterOptions").hide();
    /*chkReconciliationRun();
     oduListingTableClick();
     chkDeviceStatus();
     adminStatusCheck();*/
    $("#hide_search").show();
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

        });
    //Here we call the click event of search button
    $("input[id='btnSearch']").click(function () {
        //call the device list function on click of search button
        deviceList();
    })
//	$("#page_tip").colorbox(
//	{
//		href:"page_tip_ccu_listing.py",
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
    else if (device_type == "idu4") {
        urlString = "idu_device_listing_table.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type;
        parent.main.location = "idu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + device_type;
    }
    else {


        var oTable = $('#device_data_table').dataTable({
            "bJQueryUI": true,
            "sPaginationType": "full_numbers",
            "bProcessing": true,
            "bServerSide": true,
            "oSearch": {"sSearch": ip_address},
            "aoColumns": [
                { "sWidth": "10%"},
                { "sWidth": "10%"},
                { "sWidth": "10%" },
                { "sWidth": "10%" },
                { "sWidth": "10%" },
                { "sWidth": "10%" },
                { "sWidth": "10%" },
                { "sWidth": "13%" }
            ],
            "bDestroy": true,
            "sAjaxSource": "ccu_device_listing_table.py?&ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + device_type,
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
                    oduListingTableClick();
                });
            }
        });
    }
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

function ccuReconcile(obj, hostId, deviceTypeId) {
    reconcileHostId = hostId;
    reconcileDeviceTypeId = deviceTypeId;
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
            $.prompt('Device Configuration data would be Synchronized with the UNMP server Database', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: ccuReconcilation});
        }
    }
}

function ccuReconcilation(v, m) {
    if (v != undefined && v == true && reconcileHostId && reconcileDeviceTypeId && imgReconcileBtnObj) {
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
                    url: "ccu_reconciliation.py?host_id=" + reconcileHostId + "&device_type=" + reconcileDeviceTypeId,
                    success: function (result) {
                        imgBtn.data("rec", 0);
                        flagClick = false;
                        objTableDetail.removeClass("listing-color");
                        objTableDetail.addClass(objTableDetail.attr("listClass"));
                        objTableDetail.removeAttr("listClass");
                        flagClick = false;
                        //{'result': {0: ['RMMaster', '172.22.0.102']}, 'success': 0}
                        if (parseInt(result.success) == 0) {
                            json = result.result
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
                });
                return false;
            }
        }
    }
    else {
        spinStop($spinLoading, $spinMainLoading);
    }

}
