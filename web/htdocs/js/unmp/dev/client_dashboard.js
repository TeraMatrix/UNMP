var $spinLoading = null;
var $spinMainLoading = null;
var spIpAddress = '';
var spMainObj = null;
var deviceTypeId = 'ap25';
var graph_type = 1;
var limitFlag = 1;
var spRecursionVar = null;
var refresh_time = 10; // default time for refreshing the hidden datatime value.
var spE1MainObj = null;
var linkObj = null;
var spEndDate = '';
var spEndTime = '';
var totalSelectedGraph = "";
var apMACAddress = '';
var totalSelectedGraph = "";
var flag = 0;

$(function () {
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
    $("input[id='current_rept_div']").attr("checked", "checked");
    refresh_time = $("#sp_refresh_time").val();
    pathValue = $("#path_no").val();
    apMACAddress = $("#sp_mac_address").val();
    $('#sp_start_date, #sp_start_time, #sp_end_date,  #sp_end_time').calendricalDateTimeRange({
        isoTime: true
    });
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
//	$("#page_tip").colorbox(
//	{
//	href:"page_tip_client_monitor_dashboard.py",
//	title: "Dashboard",
//	opacity: 0.4,
//	maxWidth: "80%",
//	width:"650px",
//	height:"500px",
//	onComplte:function(){}
//	})

    $('#sp_host_info_div').slideUp('fast');
    $("#tab_yo").slideUp('fast');
    $("#sp_show_graph_list").toggle(
        function () {
            $('#tab_yo').slideDown('slow', function () {
                $("#sp_show_graph_list").val('Dashboard Configuration')
            });
        },
        function () {
            $('#tab_yo').slideUp('slow', function () {
                $("#sp_show_graph_list").val('Dashboard Configuration')
            });
        });

    $("#back_to_ap").click(function () {
        if (pathValue == 1)
            parent.main.location = "sp_dashboard_profiling.py?host_id=" + $("#host_id").val() + "&device_type=ap25&device_list_state=enabled";
        else
            parent.main.location = "ap_listing.py?device_type=ap25&device_list_state=enabled&selected_device_type=";
    });
    clientGenericGraphJson();
});


function hostInformation() {
    $('#sp_host_info_div').animate({
            left: '+=50',
            height: 'toggle'
        }, 1000, function () {
            var $hostInfo = $("#host_info");
            if ($hostInfo.attr('src') == "images/new_icons/round_minus.png") {
                $hostInfo.attr('src', "images/new_icons/round_plus.png");
                $hostInfo.attr('original-title', 'Show Status');
            }
            else {
                $hostInfo.attr('src', "images/new_icons/round_minus.png");
                $hostInfo.attr('original-title', 'Hide Status');
            }
        }
    );
}


function clientGenericGraphJson() {
    $.ajax({
        type: "post",
        url: "client_generic_json.py?device_type_id=" + deviceTypeId + "&mac_address=" + apMACAddress,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            if (result.graphs.length == 0)
                $().toastmessage('showErrorToast', 'Graph Information not exists in database for this User.');
            else if (result.success == 0) {
                result.otherData = [
                    {name: 'start_date', value: function () {
                        return $('input#sp_start_date').val();
                    }},
                    {name: 'start_time', value: function () {
                        return $('input#sp_start_time').val();
                    }},
                    {name: 'end_date', value: function () {
                        return $('input#sp_end_date').val();
                    }},
                    {name: 'end_time', value: function () {
                        return $('input#sp_end_time').val();
                    }},
                    {name: 'flag', value: function () {
                        return limitFlag;
                    }},
                    {name: 'mac_address', value: function () {
                        return apMACAddress;
                    }},
                    {name: 'graph_type', value: function () {
                        return graph_type;
                    }}
                ];
                result.graphColumn = 1;
                clientUpdateDateTime();
                $("#sp_main_graph").html("");
                spMainObj = $("#sp_main_graph").yoAllGenericDashboard(result);
            }
            else {
                $().toastmessage('showErrorToast', result.error_msg);
            }
        }
    });
}


function disbaledReportButton() {
    $("#sp_pdf_report").addClass("disabled");
    $("#sp_pdf_report").attr("disabled", true);
    $("#sp_excel_report").addClass("disabled");
    $("#sp_excel_report").attr("disabled", true);
    $("#sp_csv_report").addClass("disabled");
    $("#sp_csv_report").attr("disabled", true);
    $("#sp_ad_graph").addClass("disabled");
    $("#sp_ad_graph").attr("disabled", true);
    $("#sp_show_graph_list").addClass("disabled");
    $("#sp_show_graph_list").attr("disabled", true);
}

function enabledReportButton() {
    $("#sp_pdf_report").removeClass("disabled");
    $("#sp_pdf_report").attr("disabled", false);
    $("#sp_excel_report").removeClass("disabled");
    $("#sp_excel_report").attr("disabled", false);
    $("#sp_csv_report").removeClass("disabled");
    $("#sp_csv_report").attr("disabled", false);
    $("#sp_ad_graph").removeClass("disabled");
    $("#sp_ad_graph").attr("disabled", false);
    $("#sp_show_graph_list").removeClass("disabled");
    $("#sp_show_graph_list").attr("disabled", false);
    $("#tab_yo").slideUp('fast');

}


function redirectOnListing(redirctPath) {
    $().toastmessage('showWarningToast', "Searched Device Doesn't Exist");
    setTimeout(function () {
        parent.main.location = redirectPath + "?ip_address=" + "" + "&mac_address=" + "" + "&selected_device_type=" + "";
    }, 1500);
}

function clientDeviceDetail() {
    $.ajax({
        type: "post",
        url: "client_device_details.py?mac_address=" + apMACAddress + "&device_type_id=" + deviceTypeId,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            if (result.success >= 1 || result.success >= "1") {
                $().toastmessage('showErrorToast', result.error_msg);
            }
            else {
                $("#sp_host_info_div").html(result.device_table);
            }
        },
        error: function (req, status, err) {
        }
    });
}


// Update the date time in text Box
function advancedUpdateDateTime() {
    $.ajax({
        type: "post",
        url: "advanced_update_date_time.py?device_type_id=" + deviceTypeId,
        data: $(this).serialize(), // $(this).text?
        cache: false,
        success: function (result) {
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showWarningToast', "Date time not receving in proper format.");
                return;
            }
            else {
                $("#sp_end_date").val(result.end_date);
                $("#sp_end_time'").val(result.end_time);
            }
        }
    });
    return false;
}


// This function update date and time
function spAddDateTime() {
    $.ajax({
        type: "post",
        url: "client_add_date_time_on_slide.py?device_type_id=" + deviceTypeId,
        cache: false,
        success: function (result) {
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showWarningToast', "Date time not receving in proper format.");
            }
            else {
                $("#more_graph_columns").html(result.show_graph_table);
                totalSelectedGraph = $("#sp").val();
                if (flag == 0) {
                    $("#sp_start_date").val(result.start_date);
                    $("#sp_end_date").val(result.end_date);
                    $("#sp_start_time").val(result.start_time);
                    $("#sp_end_time").val(result.end_time);
                }
                flag = 0;
                multiSelectColumns();
            }
        }
    });
    return false;
}


function clientUpdateDateTime() {
    if (spRecursionVar != null) {
        clearInterval(spRecursionVar);
    }
    clientStateInformation()
    clientDeviceDetail();
    spAddDateTime();
    spRecursionVar = setInterval(function () {
        clientUpdateDateTime();
    }, refresh_time * 600000);
}

function advancedSrchBtn() {
    limitFlag = 0;
    var check_str_date = "";
    var check_str_time = "";
    var str1 = "";
    var str2 = "";
    var str3 = "";
    var str4 = "";
    $.ajax({
        type: "post",
        url: "advanced_update_date_time.py?device_type_id=" + deviceTypeId,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showWarningToast', "Error No: 121 Date time not receving in proper format.");
                return;
            }
            else {
                check_str_date = String(result.end_date).split("/");
                check_str_time = String(result.end_time).split(":");
                var cdate = new Date(check_str_date[2], parseInt(check_str_date[1], 10) - 1, check_str_date[0], check_str_time[0], check_str_time[1]);
                str1 = $("#sp_start_date").val();
                str2 = $("#sp_end_date").val();
                str3 = $("#sp_start_time").val();
                str4 = $("#sp_end_time").val();
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
                    clientGenericGraphJson();
                    flag = 1;
                }
            }
        }
    });
}


function clientStateInformation() {
    $.ajax({
        type: "post",
        url: "client_state_information.py?mac_address=" + apMACAddress + "&device_type_id=" + deviceTypeId,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            if (result.success >= 1 || result.success >= "1") {
                $().toastmessage('showErrorToast', result.error_msg);
            }
            else {
                $("#client_dashboard").html(result.client_table);
            }
        },
        error: function (req, status, err) {
        }
    });

}


// This is function create the Excel Report
function spExcelReportGeneration() {
    spCommonReportCreating('client_excel_report_genrating.py', 'UBR_excel.xls');
}
// This is create the PDF Report.
function spPDFReportGeneration() {
    spCommonReportCreating('sp_pdf_report_genrating.py', 'UBR_PDF_Report.pdf');
}

// This is create the CSV Report.
function spCSVReportGeneration() {
    spCommonReportCreating('client_csv_report_genrating.py', 'UBR_CSV_Report.csv');
}


function spCommonReportCreating(redirectPath, file_name) {
    graph_json = {};
    var field = [];
    var cal_type = null;
    var graph = null;
    var tab_option = null;
    var totalGraph = 0;
    var graphQuerySrting = "";
    var ajaxData = {};
    var start_date = $("#sp_start_date").val();
    var start_time = $("#sp_start_time").val();
    var end_date = $("#sp_end_date").val();
    var end_time = $("#sp_end_time").val();

    for (node in spMainObj.options.db) {
        totalGraph += 1;
        field = [];
        var tempFileds = spMainObj.options.db[node]["options"].fields;
        for (var i = 0; i < tempFileds.length; i++) {
            if (tempFileds[i].isChecked == 1) {
                field[field.length] = tempFileds[i].name;
            }
        }

        calculationType = spMainObj.options.db[node]["options"].calType;
        for (var j = 0; j < calculationType.length; j++) {
            if (calculationType[j].isChecked == 1) {
                cal_type = calculationType[j].name;
            }
        }
        graphType = spMainObj.options.db[node]["options"].type;
        for (var j = 0; j < graphType.length; j++) {
            if (graphType[j].isChecked == 1) {
                graph = graphType[j].value;
            }
        }

        tab_option = spMainObj.options.db[node]["options"].tabList.selected;
        ajaxData = spMainObj.options.db[node]["options"].ajax.data['table_name'];

        graphQuerySrting += "&start" + String(totalGraph) + "=" + spMainObj.options.db[node]["options"].startFrom;
        graphQuerySrting += "&limit" + String(totalGraph) + "=" + spMainObj.options.db[node]["options"].itemLimit;

        graphQuerySrting += "&table_name" + String(totalGraph) + "=" + ajaxData;
        graphQuerySrting += "&type" + String(totalGraph) + "=" + graph;

        graphQuerySrting += "&field" + String(totalGraph) + "=" + field;
        graphQuerySrting += "&cal" + String(totalGraph) + "=" + cal_type;
        graphQuerySrting += "&tab" + String(totalGraph) + "=" + tab_option;
        graphQuerySrting += "&graph_name" + String(totalGraph) + "=" + spMainObj.options.db[node]["options"].displayName;
    }
    graphQuerySrting += "&total_graph=" + String(totalGraph)
    var select_option = $("input[name='option']:checked").val();
    if (select_option == 0) {
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "post",
            url: "advanced_update_date_time.py?device_type_id=" + deviceTypeId,
            data: $(this).serialize(), // $(this).text?
            cache: false,
            success: function (result) {
                if (result.success == 1 || result.success == "1") {
                    $().toastmessage('showWarningToast', "Date time not receving in proper format.");
                    return;
                }
                else {
                    $.ajax({
                        type: "post",
                        url: redirectPath + "?mac_address=" + apMACAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + result.end_date + "&end_time=" + result.end_time + "&device_type_id=" + deviceTypeId + "&select_option=" + select_option + "&limitFlag=" + limitFlag + graphQuerySrting,
                        data: $(this).serialize(),
                        cache: false,
                        success: function (result) {
                            if (result.success >= 1 || result.success >= "1") {
                                $().toastmessage('showErrorToast', result.error_msg);
                            }
                            else {
                                $().toastmessage('showSuccessToast', 'Report Generated Successfully');
                                window.location = "download/" + result.file_name;

                            }
                            spinStop($spinLoading, $spinMainLoading);

                        }
                    });
                }
            }
        });
    }
    else {
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "post",
            url: redirectPath + "?mac_address=" + apMACAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&device_type_id=" + deviceTypeId + "&select_option=" + select_option + "&limitFlag=" + limitFlag + graphQuerySrting,
            data: $(this).serialize(),
            cache: false,
            success: function (result) {
                if (result.success >= 1 || result.success >= "1") {
                    $().toastmessage('showErrorToast', result.error_msg);
                }
                else {
                    $().toastmessage('showSuccessToast', 'Report Generated Successfully');
                    window.location = "download/" + result.file_name;

                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }
}

// Selectded list function start here
function multiSelectColumns() {
    $(".plus").click(function () {
        plusHostParentOption(this);
    })
    $(".minus").click(function () {
        minusHostParentOption(this);
    })
    var hostParentArray = [];
    var tempHostParent = $("input[name='spTemp']").val();
    if (tempHostParent != undefined) {
        hostParentArray = tempHostParent.split(",");
    }
    for (k = 0; k < hostParentArray.length; k++) {
        $("div[id='multiSelectList']").find("img[id='" + $.trim(hostParentArray[k]) + "']").click();
    }
    $("#rm").click(function (e) {
        e.preventDefault();
        $("div[id='multiSelectList']").find("div.selected").find("img").click();
    })
    $("#add").click(function (e) {
        e.preventDefault();
        $("div[id='multiSelectList']").find("div.nonSelected").find("img").click();
    })
}
function minusHostParentOption(Obj) {
    liObj = $("<li/>");
    imgObj = $("<img/>");
    liObj.append($(Obj).attr("name"));
    imgObj.attr("src", "images/add16.png").attr("class", "plus plus").attr("alt", "+").attr("id", $(Obj).attr("id")).attr("name", $(Obj).attr("name")).click(function () {
        plusHostParentOption(this)
    })
    liObj.append(imgObj);
    $(Obj).parent().parent().parent().parent().find("div.nonSelected").find("ul").append(liObj);
    $(Obj).parent().parent().parent().parent().find("input[name='sp']").val("");
    j = 0
    for (i = 0; i < $(Obj).parent().parent().find("li").size(); i++) {
        var addedHostParent = $(Obj).parent().parent().find("li").eq(i).find("img").attr("id");
        if (addedHostParent != $(Obj).attr("id")) {
            if (j == 0) {
                $(Obj).parent().parent().parent().parent().find("input[name='sp']").val($.trim(addedHostParent));
            }
            else {
                $(Obj).parent().parent().parent().parent().find("input[name='sp']").val($(Obj).parent().parent().parent().parent().find("input[name='sp']").val() + "," + $.trim(addedHostParent));
            }
            j++;
        }
    }
    $(Obj).parent().parent().parent().parent().find("span#count").html(j)
    $(Obj).parent().remove();
}

function plusHostParentOption(Obj) {
    var countParent = 0;
    liObj = $("<li/>");
    imgObj = $("<img/>");
    liObj.append($(Obj).attr("name"));
    imgObj.attr("src", "images/minus16.png").attr("class", "minus").attr("alt", "-").attr("id", $(Obj).attr("id")).attr("name", $(Obj).attr("name")).click(function () {
        minusHostParentOption(this)
    })
    liObj.append(imgObj);
    $(Obj).parent().parent().parent().parent().find("div.selected").find("ul").append(liObj);
    hdval = $(Obj).parent().parent().parent().parent().find("input[name='sp']").val()
    if ($.trim(hdval) == "") {
        $(Obj).parent().parent().parent().parent().find("input[name='sp']").val($(Obj).attr("id"))
    }
    else {
        $(Obj).parent().parent().parent().parent().find("input[name='sp']").val(hdval + "," + $(Obj).attr("id"))
    }
    countParent = $(Obj).parent().parent().parent().parent().find("span#count").html();
    $(Obj).parent().parent().parent().parent().find("span#count").html(parseInt(countParent) + 1);
    $(Obj).parent().remove();
}


function show_graph_click() {
    totalSelectedGraph = $("#sp").val();
    if (totalSelectedGraph == "") {
        $().toastmessage('showWarningToast', "Please select atleast one graph from dashboard configuration.");
        return false;
    }
    $.ajax({
        type: "post",
        url: "update_client_graph.py?device_type_id=" + deviceTypeId + "&selected_graph=" + $("#sp").val(),
        cache: false,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                $().toastmessage('showWarningToast', "UNMP Server has encountered an error. Please retry after some time.");
                return;
            }
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showWarningToast', messages[result.msg]);
                return;
            }
            else {
                clientGenericGraphJson();
            }
        }
    });
}
