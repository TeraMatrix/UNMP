var aSelectedLog = [];
var oTableLog = null;
var $spinLoading = null;
var $spinMainLoading = null;

$(document).ready(function () {
    $spinLoading = $("div#spin_loading");        // create object that hold loading circle
    $spinMainLoading = $("div#main_loading");    // create object that hold loading squire
    var cur_date = new Date();
    var d = cur_date.getDate();
    var y = cur_date.getFullYear();
    var m = cur_date.getMonth();
    var cdate = new Date(y, m, d);

    $('#start_date, #start_time, #end_date,  #end_time').calendricalDateTimeRange({
        isoTime: true
    });

    hideShow = $("#hide_show");
    searchFormTable = $("#search_form_table");
    $("#multiselect_month").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select month', header: "Available months", minWidth: 200});
    $("#multiselect_log").multiselect({selectedList: 1, multiple: false, minWidth: 200});
    $("#multiselect_users").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select user', header: "Available users", minWidth: 200});


    $("#multiselect_month").bind("multiselectclose", function (event, ui) {
        var sel = $("#multiselect_month").val();
        if (sel != null) {
            var end_date = new Date();
            var start_date = new Date();
            //$("#div_time_select").css("display","none");
            if (parseInt(sel) == 20) {
                start_date.setMinutes(0);
                start_date.setHours(0);
                $("#time_select_label_id").css("display", "");
                $("#time_select_info_id").css("display", "");
            }
            else {
                $("#time_select_label_id").css("display", "none");
                $("#time_select_info_id").css("display", "none");
            }
            var s_date = start_date.getDate() + "/" + parseInt(parseInt(start_date.getMonth()) + 1) + "/" + start_date.getFullYear();
            var s_time = start_date.getHours() + ":" + start_date.getMinutes();
            var e_date = end_date.getDate() + "/" + parseInt(parseInt(end_date.getMonth()) + 1) + "/" + end_date.getFullYear();
            var e_time = end_date.getHours() + ":" + end_date.getMinutes();
            $("#start_date").val(s_date);
            $("#end_date").val(e_date);
            $("#start_time").val(s_time);
            $("#end_time").val(e_time);
        }
    });

    hideShow.toggle(function () {
        var $this = $(this);
        $this.attr("src", "images/new/up.png");
        searchFormTable.find("tbody").slideDown();
        $this.attr("original-title", "Hide");
    }, function () {
        var $this = $(this);
        $this.attr("src", "images/new/down.png");
        searchFormTable.find("tbody").slideUp();
        $this.attr("original-title", "Show");
    });
    hideShow.tipsy({gravity: 'n'});
    $("#submit").click(function () {
        searchEvents();
    });

    searchEvents();

//	$("#page_tip").colorbox(  			//page tip
//	    {
//		href:"view_page_tip_log_user.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"600px",
//		height:"400px"
//	    });
});


function searchEvents() {
    //spinStart($spinLoading,$spinMainLoading);
    month = $("#multiselect_month").val();
    log_type = $("#multiselect_log").val();
    user_name = $("#multiselect_users").val();


    var start_date = $("#start_date").val();
    var end_date = $("#end_date").val();
    var start_time = $("#start_time").val();
    var end_time = $("#end_time").val();


    if (month == null) {
        month = "";
    }
    if (log_type == null) {
        log_type = "";
    }
    if (user_name == null) {
        user_name = "";
    }
    if (month == 20) {
        var start_date = $("#start_date").val();
        var end_date = $("#end_date").val();
        var start_time = $("#start_time").val();
        var end_time = $("#end_time").val();
        var str1 = $("#start_date").val();
        var str2 = $("#end_date").val();
        str1 = str1.split("/");
        str2 = str2.split("/");

        var cur_date = new Date();
        var d = cur_date.getDate();
        var y = cur_date.getFullYear();
        var m = cur_date.getMonth();
        var cdate = new Date(y, m, d);
        var date1 = new Date(str1[2], parseInt(str1[1], 10) - 1, str1[0]);
        var date2 = new Date(str2[2], parseInt(str2[1], 10) - 1, str2[0]);
        if (date2 < date1) {
            $().toastmessage('showErrorToast', "End Date can't be smaller than Start Date");
            return false;
        }
        else if (cdate < date1 || cdate < date2) {
            $().toastmessage('showErrorToast', "Dates can't be greater than current Date");
            return false;
        }
    }

    oTable = $('#log_table').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "bServerSide": true,
        "bDestroy": true,
        "sAjaxSource": "get_log_data.py?month=" + month + "&log_type=" + log_type + "&user_name=" + user_name + "&start_date=" + start_date + "&end_date=" + end_date + "&start_time=" + start_time + "&end_time=" + end_time,
        "aaSorting": [
            [0, 'desc']
        ]
    });

    if (log_type != "3" && log_type != "10") {
        oTable.fnSetColumnVis(1, false);
        oTable.fnAdjustColumnSizing();
    }
}

// reporting function start
function excel_report(report_type) {
    if (report_type == 1) {
        report_type = "excel";
    }
    else {
        report_type = "csv";
    }
    month = $("#multiselect_month").val();
    log_type = $("#multiselect_log").val();
    user_name = $("#multiselect_users").val();
    if (month == null) {
        month = "";
    }
    if (log_type == null) {
        log_type = "";
    }
    if (user_name == null) {
        user_name = "";
    }

    var start_date = $("#start_date").val();
    var end_date = $("#end_date").val();
    var start_time = $("#start_time").val();
    var end_time = $("#end_time").val();
    if (month == 20) {
        var start_date = $("#start_date").val();
        var end_date = $("#end_date").val();
        var start_time = $("#start_time").val();
        var end_time = $("#end_time").val();
        var str1 = $("#start_date").val();
        var str2 = $("#end_date").val();
        str1 = str1.split("/");
        str2 = str2.split("/");

        var cur_date = new Date();
        var d = cur_date.getDate();
        var y = cur_date.getFullYear();
        var m = cur_date.getMonth();
        var cdate = new Date(y, m, d);
        var date1 = new Date(str1[2], parseInt(str1[1], 10) - 1, str1[0]);
        var date2 = new Date(str2[2], parseInt(str2[1], 10) - 1, str2[0]);
        if (date2 < date1) {
            $().toastmessage('showErrorToast', "End Date can't be smaller than Start Date");
            return false;
        }
        else if (cdate < date1 || cdate < date2) {
            $().toastmessage('showErrorToast', "Dates can't be greater than current Date");
            return false;
        }
    }


    spinStart($spinLoading, $spinMainLoading);
    var method = 'post';
    var url = "get_log_data_excel.py?month=" + month + "&log_type=" + log_type + "&report_type=" + report_type + "&user_name=" + user_name + "&start_date=" + start_date + "&end_date=" + end_date + "&start_time=" + start_time + "&end_time=" + end_time;
    $.ajax({
        type: method,
        url: url,
        cache: false,
        success: function (result) {
            result = eval("(" + result + ")");
            if (result.success == 0 || result.success == '0') {
                spinStop($spinLoading, $spinMainLoading);
                $().toastmessage('showSuccessToast', "Report Generated Successfully.");
                //window.location="download_file.py?file_name="+result.file+"&path="+result.path_report;
                window.location = "download/" + result.file;
                //window.open("download"+"/"+result.file);
            }
            else if (result.success == 1 || result.success == '1') {
                spinStop($spinLoading, $spinMainLoading);
                $().toastmessage('showWarningToast', 'No Data Available for the Time Specified .');
            }
            else {
                spinStop($spinLoading, $spinMainLoading);
                $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
            }

        }
    });
}
// reporting function end


function LogSettings() {

    $.colorbox(
        {
            href: "edit_log_settings.py",
            title: "Log Settings",
            opacity: 0.4,
            //maxWidth: "90%",
            width: "450px",
            height: "300px",
            //overlayClose:false,
            onComplete: function () {
                $("#user_trail_state").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select State', minWidth: 50});
                function applyChanges() {
                    if ($("#user_trail_state").val() != "None" && $("#user_trail_state").val() != null) {
                        user_trail_state = $("#user_trail_state").val();
                        spinStart($spinLoading, $spinMainLoading);
                        $.ajax({
                            type: "get",
                            url: "apply_log_settings.py?user_trail_state=" + user_trail_state,
                            cache: false,
                            success: function (result) {
                                result = eval("(" + result + ")");
                                if (result.success == 0 || result.success == '0') {
                                    spinStop($spinLoading, $spinMainLoading);
                                    $().toastmessage('showSuccessToast', "Log settings modified Successfully.");
                                    $.colorbox.close();
                                }
                                else {
                                    spinStop($spinLoading, $spinMainLoading);
                                    $().toastmessage('showErrorToast', 'Log settings couldnt be modified currently.');
                                }
                            }
                        });
                    }
                    else {
                        $().toastmessage('showWarningToast', "Please select at least one state.");
                    }
                }

                function clearOldLogs(v, m) {
                    if (v != undefined && v == true) {
                        spinStart($spinLoading, $spinMainLoading);
                        $.ajax({
                            type: "get",
                            url: "clear_old_logs.py",
                            cache: false,
                            success: function (result) {
                                result = eval("(" + result + ")");
                                if (result.success == 0 || result.success == '0') {
                                    spinStop($spinLoading, $spinMainLoading);
                                    $().toastmessage('showSuccessToast', "Old logs cleared successfully.");
                                    $.colorbox.close();
                                }
                                else {
                                    spinStop($spinLoading, $spinMainLoading);
                                    $().toastmessage('showErrorToast', "Old logs couldn't be cleared.");
                                }
                            }
                        });
                    }
                }

                $("#apply_log_settings").click(function () {
                    applyChanges();
                });
                $("#clear_old_logs").click(function () {
                    $.prompt(' All the log data will be cleared from the system except of past 30 days.Do you want to continue with this process?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: clearOldLogs});
                    //clearOldLogs();
                });
            }
        });
}
