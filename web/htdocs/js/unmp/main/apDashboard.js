var chartAPNW;
var chartEvent;
var chartOutage;
var apRecursionVar = null;
var apIpAddress = null;
var limitFlag = 1;
var apNWBandwidth = null;
var $spinLoading = null;
var $spinMainLoading = null;
var mainObject = null;
$(function () {
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire

    $("input[id='current_rept_div']").attr("checked", "checked");
    $("#device_type").change(function () {
        $("#filter_ip").val("");
        $("#filter_mac").val("");
    });
    $('#odu_start_date, #odu_start_time, #odu_end_date,  #odu_end_time').calendricalDateTimeRange({
        isoTime: true
    });
    $("input[id='filter_ip']").keypress(function () {
        $("input[id='filter_mac']").val("");
    })
    $("input[id='btnSearch']").click(function () {
        //call the device list function on click of search button
        deviceList();
    })
    apIpAddress = $("input#filter_ip").val();
    oduGraphButtonClick();
    //graphInitiator();   // calling the function for graph showing
//	$("#page_tip").colorbox(
//	{
//	href:"page_tip_ap_monitor_dashboard.py",
//	title: "Page Tip",
//	opacity: 0.4,
//	maxWidth: "80%",
//	width:"650px",
//	height:"450px",
//	onComplte:function(){}
//	})
    // Slide up and slide down functionality starthere
    $("#tab_yo").slideUp('fast');
    $("#adSrhAP").toggle(
        function () {
            $('#tab_yo').slideDown('slow', function () {
                limitFlag = 0;
                $("#adSrhAP").val('Hide Search')
            });
        },
        function () {
            $('#tab_yo').slideUp('slow', function () {
                limitFlag = 1;
                $("#adSrhAP").val('Advance Graph')
                apAddDateTime();

            });
        });
    // Slide up and slide down functionality end here
    // This function bring the all graph information
    genericGraphJson();
});


// generic graph
function genericGraphJson() {
    $.ajax({
        type: "post",
        url: "generic_json.py",
        data: $(this).serialize(), // $(this).text?
        cache: false,
        success: function (result) {
            if (result.success == 0) {
                result.otherData = [
                    {name: 'start_date', value: function () {
                        return $('input#odu_start_date').val();
                    }},
                    {name: 'start_time', value: function () {
                        return $('input#odu_start_time').val();
                    }},
                    {name: 'end_date', value: function () {
                        return $('input#odu_end_date').val();
                    }},
                    {name: 'end_time', value: function () {
                        return $('input#odu_end_time').val();
                    }},
                    {name: 'flag', value: function () {
                        return limitFlag;
                    }},
                    {name: 'ip_address', value: function () {
                        return apIpAddress;
                    }}
                ];
                result.graphColumn = 1;
                mainObject = $("#main_graph").yoAllGenericDashboard(result);
                // $("#main_graph").html("");
                apDeviceDetail();
                updateDateTime();
            }
            else {
                $().toastmessage('showErrorToast', 'UNMP Server has encountered an error. Please retry after some time.');
            }
        }
    });
}


function apDeviceDetail(divObj) {
    spinStart($spinLoading, $spinMainLoading);

    $.ajax({
        type: "post",
        url: "ap_device_details.py?ip_address=" + apIpAddress,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showErrorToast', 'UNMP Server has encountered an error. Please retry after some time.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                $().toastmessage('showErrorToast', 'UNMP database Server or Services not running so please contact your Administrator.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 3 || result.success == '3') {
                $().toastmessage('showErrorToast', 'UNMP database Server has encountered an error. Please retry after some time.');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else {
                $("#ap_host_info_div").html(result.device_table);
                spinStop($spinLoading, $spinMainLoading);
            }
        },
        error: function (req, status, err) {
        }
    });
}


// This function update date and time
function apAddDateTime() {
    $.ajax({
        type: "post",
        url: "ap_add_date_time_on_slide.py",
        data: $(this).serialize(), // $(this).text?
        cache: false,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                $().toastmessage('showWarningToast', "Date time not receving in proper format.");
                return;
            }
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showWarningToast', "Date time not receving in proper format.");
                return;
            }
            else {
                $("#odu_start_date").val(result.start_date);
                $("#odu_end_date").val(result.end_date);
                $("#odu_start_time").val(result.start_time);
                $("#odu_end_time").val(result.end_time);
            }
        }
    });
    return false; //always remamber this
}


function oduGraphButtonClick() {

    $("#ap_graph_show").click(function () {
        $("#main_graph").html("");
        limitFlag = 0;
        var cur_date = new Date();
        var d = cur_date.getDate();
        var y = cur_date.getFullYear();
        var m = cur_date.getMonth();
        var h = cur_date.getHours();
        var mi = cur_date.getMinutes();
        var cdate = new Date(y, m, d, h, mi);
        var str1 = $("#odu_start_date").val();
        var str2 = $("#odu_end_date").val();
        var str3 = $("#odu_start_time").val();
        var str4 = $("#odu_end_time").val();
        str1 = str1.split("/");
        str2 = str2.split("/");
        str3 = str3.split(":");
        str4 = str4.split(":");
        var date1 = new Date(str1[2], parseInt(str1[1], 10) - 1, str1[0], str3[0], str3[1]);
        var date2 = new Date(str2[2], parseInt(str2[1], 10) - 1, str2[0], str4[0], str4[1]);
        if (date2 < date1) {
            $().toastmessage('showWarningToast', "End Date can't be greater than Start Date");
            return false;
        }
        else if (cdate < date1 || cdate < date2) {
            $().toastmessage('showWarningToast', "Dates can't be greater than current Date");
            return false;
        }
        else {
            $("#main_graph").html("");
            genericGraphJson();

        }

    });
}


function deviceList() {
    var device_type = "ap25";
    // this retreive the value of ipaddress textbox
    var ip_address = $("input[id='filter_ip']").val();
    // this retreive the value of macaddress textbox
    var mac_address = $("input[id='filter_mac']").val();
    // this retreive the value of selectdevicetype from select menu
    var selected_device_type = $("select[id='device_type']").val();
    // this ajax return the call to function get_device_data_table which is in odu_view and pass the ipaddress,macaddress,devicetype with url
    apIpAddress = ip_address
    $.ajax({
        type: "post",
        url: "get_device_list_ap_for_monitoring.py?&ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type,
        cache: false,
        success: function (result) {
            if (result == 0 || result == "0") {
                $("#ap_show_msg").html("No Data exist for this device.")
                $("#adSrhap").hide(); // hide the button
                $("#tab_yo").hide();
                $("#ap_host_info_div").hide();
                $("#main_graph").html("");


            }
            else if (result == 1 || result == "1") {
                parent.main.location = "ap_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type;

            }
            else if (result == 2 || result == "2") {

                $("#ap_show_msg").html("Please Try Again.")
                $("#adSrhap").hide(); // hide the button
                $("#tab_yo").hide();
                $("#ap_device_graph").hide();
                $("#ap_host_info_div").hide();
                $("#main_graph").html("");


            }
            else {
                $("#ap_show_msg").html("")
                $("#adSrhap").show(); // show the button
                $("#tab_yo").show();
                $("input#filter_ip").val(result);
                apIpAddress = result;
                $("#ap_device_graph").show();
                $("#ap_host_info_div").show();
                $("#main_graph").html("");
                genericGraphJson();
                apDeviceDetail();
            }
        }
    });
}

function updateDateTime() {
    if (apRecursionVar != null) {
        clearTimeout(apRecursionVar);
    }
    apAddDateTime();
//	apRecursionVar=setTimeout(function (){apAddDateTime();},refresh_time*60000);
    apRecursionVar = setTimeout(function () {
        updateDateTime();
    }, 60000);
}


// Excel reprot genration
function apExcelReportGeneration() {
    graph_json = {};
    var field = [];
    var cal_type = null;
    var graph = null;
    var tab_option = null;
    var totalGraph = 0;
    var graphQuerySrting = "";
    var ajaxData = {};
    for (node in mainObject.options.db) {
        totalGraph += 1;
        field = [];
        //alert(mainObject.options.db[node]["options"].calType[0].name);
        var tempFileds = mainObject.options.db[node]["options"].fields;
        for (var i = 0; i < tempFileds.length; i++) {
            if (tempFileds[i].isChecked == 1) {
                field[i] = tempFileds[i].name;
            }
        }

        calculationType = mainObject.options.db[node]["options"].calType;
        for (var j = 0; j < calculationType.length; j++) {
            if (calculationType[j].isChecked == 1) {
                cal_type = calculationType[j].name;
            }
        }
        graphType = mainObject.options.db[node]["options"].type;
        for (var j = 0; j < graphType.length; j++) {
            if (graphType[j].isChecked == 1) {
                graph = graphType[j].value;
            }
        }

        tab_option = mainObject.options.db[node]["options"].tabList.selected;
        ajaxData = mainObject.options.db[node]["options"].ajax.data['table_name'];

        graphQuerySrting += "&table_name" + String(totalGraph) + "=" + ajaxData;
        graphQuerySrting += "&type" + String(totalGraph) + "=" + graph;

        graphQuerySrting += "&field" + String(totalGraph) + "=" + field;
        graphQuerySrting += "&cal" + String(totalGraph) + "=" + cal_type;
        graphQuerySrting += "&tab" + String(totalGraph) + "=" + tab_option;
        graphQuerySrting += "&graph_name" + String(totalGraph) + "=" + mainObject.options.db[node]["options"].displayName;
    }
    graphQuerySrting += "&total_graph=" + String(totalGraph)
    var select_option = $("input[name='option']:checked").val();
    if (select_option == 0) {
        var cur_date = new Date();
        var d = cur_date.getDate();
        var y = cur_date.getFullYear();
        var m = cur_date.getMonth();
        var h = cur_date.getHours();
        var mi = cur_date.getMinutes();
        var cdate = new Date(y, m, d, h, mi);
        var str1 = $("#odu_start_date").val();
        var str2 = $("#odu_end_date").val();
        var str3 = $("#odu_start_time").val();
        var str4 = $("#odu_end_time").val();
        str1 = str1.split("/");
        str2 = str2.split("/");
        str3 = str3.split(":");
        str4 = str4.split(":");
        var date1 = new Date(str1[2], parseInt(str1[1], 10) - 1, str1[0], str3[0], str3[1]);
        var date2 = new Date(str2[2], parseInt(str2[1], 10) - 1, str2[0], str4[0], str4[1]);
        if (date2 < date1) {
            $().toastmessage('showWarningToast', "End Date can't be greater than Start Date");
        }
        else if (cdate < date1 || cdate < date2) {

            $().toastmessage('showWarningToast', "Dates can't be greater than current Date");
        }
        else {
            var start_date = $("#odu_start_date").val();
            var start_time = $("#odu_start_time").val();
            var end_date = $("#odu_end_date").val();
            var end_time = $("#odu_end_time").val();
            var subObj = mainObject.options.db;
            spinStart($spinLoading, $spinMainLoading);
            $.ajax({
                type: "post",
                url: "ap_excel_report_genrating.py?ip_address=" + apIpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&select_option=" + select_option + "&limitFlag=" + limitFlag + graphQuerySrting,
                data: $(this).serialize(),
                cache: false,
                success: function (result) {
                    try {
                        result = eval("(" + result + ")");
                    } catch (err) {
                        $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
                    }
                    if (result.success == 1 || result.success == "1") {
                        $().toastmessage('showErrorToast', 'UNMP Server has encountered an error. Please retry after some time.');
                    }
                    else if (result.success == 2 || result.success == '2') {
                        $().toastmessage('showErrorToast', 'UNMP database Server or Services not running so please contact your Administrator.');
                    }
                    else if (result.success == 3 || result.success == '3') {
                        $().toastmessage('showErrorToast', 'UNMP database Server has encountered an error. Please retry after some time.');
                    }
                    else {
                        $().toastmessage('showSuccessToast', 'Report Generated Successfully');
                        window.location = "download/AP_excel.xls";

                    }
                    spinStop($spinLoading, $spinMainLoading);

                }
            });
        }

    }
    else {
        var start_date = $("#odu_start_date").val();
        var start_time = $("#odu_start_time").val();
        var end_date = $("#odu_end_date").val();
        var end_time = $("#odu_end_time").val();
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "post",
            url: "ap_excel_report_genrating.py?ip_address=" + apIpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&select_option=" + select_option + "&limitFlag=" + limitFlag + graphQuerySrting,
            data: $(this).serialize(),
            cache: false,
            success: function (result) {
                try {
                    result = eval("(" + result + ")");
                } catch (err) {
                    $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
                }
                if (result.success == 1 || result.success == "1") {
                    $().toastmessage('showErrorToast', 'UNMP Server has encountered an error. Please retry after some time.');
                }
                else if (result.success == 2 || result.success == '2') {
                    $().toastmessage('showErrorToast', 'UNMP database Server or Services not running so please contact your Administrator.');
                }
                else if (result.success == 3 || result.success == '3') {
                    $().toastmessage('showErrorToast', 'UNMP database Server has encountered an error. Please retry after some time.');
                }
                else {
                    $().toastmessage('showSuccessToast', 'Report Generated Successfully');
                    window.location = "download/AP_excel.xls";

                }
                spinStop($spinLoading, $spinMainLoading);

            }
        });
    }
}



