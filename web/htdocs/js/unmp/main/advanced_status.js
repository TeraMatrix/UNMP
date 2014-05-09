var user_id = '';
var advancedAPIpAddress = '';
var graph_type = 2;
var limitFlag = 1;
var apAdvancedObject = null;
var device_type_id = null;
var $spinLoading = null;
var $spinMainLoading = null;
var advancedGraphClickValue = null;
var endDate = '';
var endTime = '';

$(function () {
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
    advancedAPIpAddress = $("#advaced_ip_address").val();
    disbaledReportButton();
    $("input[id='current_rept_div']").attr("checked", "checked");
    device_type_id = $("#advaced_device_type").val();
    user_id = $("#user_id").val();
    graphNameShow();
    $('#odu_start_date, #odu_start_time, #odu_end_date,  #odu_end_time').calendricalDateTimeRange({
        isoTime: true
    });
    $("#page_tip").colorbox(
        {
            href: "page_tip_advanced_status.py",
            title: "Advanced Dashboard",
            opacity: 0.4,
            maxWidth: "80%",
            width: "650px",
            height: "500px",
            onComplte: function () {
            }
        })

});


// Update the date time in text Box
function advancedUpdateDateTime() {
    $.ajax({
        type: "post",
        url: "advanced_status_update_date_time.py?device_type_id=" + device_type_id,
        data: $(this).serialize(), // $(this).text?
        cache: false,
        success: function (result) {
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showWarningToast', "Date time not receving in proper format.");
                return;
            }
            else {
                endDate = result.end_date;
                endTime = result.end_time;
            }
        }
    });
    return false;
}


// This function brings total graph showing in advanced graph
function graphNameShow() {
    $.ajax({
        type: "post",
        url: "ap_total_status_name.py?device_type_id=" + device_type_id + "&ip_address=" + advancedAPIpAddress,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            if (result['success'] == 0) {
                $("#apGraphNameTable").html(result['result'])
                deviceStatistics();
                $('a', '#graph_name_table').click(function () {
                    $tbody = $(this).parent().parent().parent();
                    $tbody.find("tr.tr-graph td").css("background-color", "");
                    $(this).parent().css("background-color", "#AAA");
                    advancedUpdateDateTime(); // This is function update
                    endDateStr = endDate.split("/");
                    endTimeStr = endTime.split(":");
                    var cdate = new Date(endDateStr[2], parseInt(endDateStr[1], 10) - 1, endDateStr[0], endTimeStr[0], endTimeStr[1]);
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
                        var graph_id = $(this).attr('value');
                        apDataTableGeneration(graph_id);
                        advancedGraphClickValue = graph_id;
                    }
                });
                $("#apGraphNameTable").find('a').eq(0).click();
            }
            else {
                $().toastmessage('showErrorToast', result.error_msg);
            }
        }
    });
}

function deviceStatistics() {
    $("#device_status").parent().parent().parent().find("tr.tr-graph").show();
    $("#device_status").toggle(function () {
            var $this = $(this);
            $tbody = $this.parent().parent().parent();
            $tbody.find("tr.tr-graph").hide();
            $this.attr('src', "images/new_icons/round_plus.png");
            $this.attr('original-title', 'Hide Status')
        },
        function () {
            var $this = $(this);
            $tbody = $this.parent().parent().parent();
            $tbody.find("tr.tr-graph").show();
            $this.attr('src', "images/new_icons/round_minus.png");
            $this.attr('original-title', 'Hide Status')
        });
}


function disbaledReportButton() {

    $("#excel_report").addClass("disabled");
    $("#excel_report").attr("disabled", true);
    $("#csv_report").addClass("disabled");
    $("#csv_report").attr("disabled", true);
    $("#advancedSrh").addClass("disabled");
    $("#advancedSrh").attr("disabled", true);

}

function enabledReportButton() {
    $("#excel_report").removeClass("disabled");
    $("#excel_report").attr("disabled", false);
    $("#csv_report").removeClass("disabled");
    $("#csv_report").attr("disabled", false);
    $("#advancedSrh").removeClass("disabled");
    $("#advancedSrh").attr("disabled", false);
}


function apDataTableGeneration(graph_id) {
    var start_date = $("#odu_start_date").val();
    var start_time = $("#odu_start_time").val();
    var end_date = $("#odu_end_date").val();
    var end_time = $("#odu_end_time").val();
    $.ajax({
        type: "post",
        url: "status_data_table_creation.py?ip_address=" + advancedAPIpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&device_type_id=" + device_type_id + "&graph_id=" + graph_id,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            var table_output = [];
            if (result['column'].length > 1)
                table_output = result.table;
            var column = [];
            for (i = 0; i < result['column'].length; i++)
                column[column.length] = { "sTitle": result['column'][i], "sClass": "center" };
            var tableDivObj = $("#apAdvancedDataTable");
            tableDivObj.html("<table id='apAdvancedGraphTableDiv' cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" class='display'>");
            //$('#apAdvancedGraphTableDiv').html("");
            $('#apAdvancedGraphTableDiv').dataTable({
                "bDestroy": true,
                "bJQueryUI": true,
                "bProcessing": true,
                "sPaginationType": "full_numbers",
                "bPaginate": true,
                "bStateSave": false,
                "aaData": table_output,
                "aLengthMenu": [
                    [20, 40, 60, -1],
                    [20, 40, 60, "All"]
                ],
                "bLengthChange": true,
                "iDisplayLength": 20,
                "oLanguage": {
                    "sInfo": "_START_ - _END_ of _TOTAL_",
                    "sInfoEmpty": "0 - 0 of 0",
                    "sInfoFiltered": "(of _MAX_)"
                },
                "aoColumns": column,
                "aaSorting": [
                    [0, 'desc']
                ]
            });
            enabledReportButton(); // enabled the report button
        }
    });
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
        url: "advanced_update_date_time.py?device_type_id=" + device_type_id,
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
                /*var cur_date=new Date();
                 var d=cur_date.getDate();
                 var y=cur_date.getFullYear();
                 var m=cur_date.getMonth();
                 var h = cur_date.getHours();
                 var mi = cur_date.getMinutes();
                 var cdate=new Date(y,m,d,h,mi);*/
                var cdate = new Date(check_str_date[2], parseInt(check_str_date[1], 10) - 1, check_str_date[0], check_str_time[0], check_str_time[1]);
                str1 = $("#odu_start_date").val();
                str2 = $("#odu_end_date").val();
                str3 = $("#odu_start_time").val();
                str4 = $("#odu_end_time").val();
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
                    $("#apGraphNameTable").find('a[value="' + advancedGraphClickValue + '"]').click();
                }
            }
        }
    });
}


// Excel reporting creating function 

function advacedExcelReportGeneration() {
    reportCreation('excelReport');

}
function advacedCSVReportGeneration() {
    reportCreation('csvReport');

}


function reportCreation(reportType) {
    // this is create the query string of parameter.
    var start_date = $("#odu_start_date").val();
    var start_time = $("#odu_start_time").val();
    var end_date = $("#odu_end_date").val();
    var end_time = $("#odu_end_time").val();
    var select_option = $("input[name='option']:checked").val();
    if (select_option == 0) {
        advancedUpdateDateTime(); // This is function update datetime.
        endDateStr = endDate.split("/");
        endTimeStr = endTime.split(":");
        var cdate = new Date(endDateStr[2], parseInt(endDateStr[1], 10) - 1, endDateStr[0], endTimeStr[0], endTimeStr[1]);
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
            spinStart($spinLoading, $spinMainLoading);
            $.ajax({
                type: "post",
                url: "advanced_status_excel_creating.py?ip_address=" + advancedAPIpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&select_option=" + select_option + "&device_type_id=" + device_type_id + "&type=" + reportType + "&graph_id=" + advancedGraphClickValue,
                data: $(this).serialize(),
                cache: false,
                success: function (result) {
                    try {
                        result = eval("(" + result + ")");
                    } catch (err) {
                        $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
                    }
                    if (result.success == 1 || result.success == "1") {
                        $().toastmessage('showWarningToast', result.error_msg);
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
    else {

        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "post",
            url: "advanced_status_excel_creating.py?ip_address=" + advancedAPIpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&select_option=" + select_option + "&device_type_id=" + device_type_id + "&type=" + reportType + "&graph_id=" + advancedGraphClickValue,
            data: $(this).serialize(),
            cache: false,
            success: function (result) {
                try {
                    result = eval("(" + result + ")");
                } catch (err) {
                    $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
                }
                if (result.success == 1 || result.success == "1") {
                    $().toastmessage('showWarningToast', result.error_msg);
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

