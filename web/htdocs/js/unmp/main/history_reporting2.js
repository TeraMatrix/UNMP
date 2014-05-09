var callA = null;
var timeSlot = 5000;
var checked_values = null;
function redirect() {
    window.location = "history_report_main.py";
}
function cleanup_data() {

    $.ajax
    ({
        type: "get",
        url: "clear_data_historical.py",
        success: function (result) {

        }
    });
    $("#last_loaded_info_div").hide();
    $("#view_month_label_value").val("");
    $("#view_month_label_value").html("");
}

function backDb() {
    checked_month = $("#multiselect_month").val();
    if (checked_month == null) {
        $().toastmessage('showErrorToast', 'Please select a month .');
        return;
    }
    $.ajax
    ({
        type: "get",
        url: "backup_data_check_historical.py?month_var=" + checked_month,
        success: function (result) {
            result = eval("(" + result + ")");
            function check_user_choice(v, m) {
                if (v != undefined && v == true) {
                    $.ajax
                    ({
                        type: "get",
                        url: "backup_data_historical.py?month_var=" + checked_month,
                        success: function (result) {
                            result = eval("(" + result + ")");
                            if (result.success == '0' || result.success == 0) {
                                $().toastmessage('showSuccessToast', 'The system has created a successful back up of the data of selected month.');
                            }
                            else {
                                $().toastmessage('showErrorToast', 'An error occurred while creating the backup of the selected month.');
                            }

                        }
                    }); // inner ajax request ends

                }
                else {
                }
            }

            if (result.success == '0' || result.success == 0) {
                //$().toastmessage('showSuccessToast', 'The data of selected month has been successfully backed up.');
                $.prompt('Another backup file of same month exists in the system. Do you want to over write it ?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: check_user_choice });


            } // result success ends
            else if (result.success == '1' || result.success == 1) {
                check_user_choice(true, true);
            }
            else {
                check_user_choice(true, true);
            }
        }
    });// outer ajax ends
}

function cleanDb() {
    checked_month = $("#multiselect_month").val();
    if (checked_month == null) {
        $().toastmessage('showErrorToast', 'Please select a month .');
        return;
    }
    function check_user_choice_clean(v, m) {
        if (v != undefined && v == true) {
            $.ajax
            ({
                type: "get",
                url: "cleanup_data_historical.py?month_var=" + checked_month,
                success: function (result) {
                    result = eval("(" + result + ")");
                    if (result.success == '0' || result.success == 0) {
                        $().toastmessage('showSuccessToast', 'The data of selected month has been successfully cleared from the system.');

                    }
                    else if (result.success == '1' || result.success == 1) {
                        $().toastmessage('showErrorToast', 'An error occurred while clearing the data of the selected month.');
                    }
                    else {
                        $().toastmessage('showErrorToast', 'An error occurred while clearing the data of the selected month.');
                    }
                }
            });
        }
        else {
        }
    }

    //$().toastmessage('showSuccessToast', 'The data of selected month has been successfully backed up.');
    $.prompt('Caution:Data will be cleared from the system for the selected month. It is suggested that you backup the data first. Do you want to continue with this process?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: check_user_choice_clean });

}


function checkDbStatus() {
    $.ajax
    ({
        type: "get",
        url: "check_db_status_historical.py",
        success: function (result) {
            result = eval("(" + result + ")");
            if (result.success == 0 || result.success == "0") {
                if (result.result == "1" || result.result == 1) {
                    clearTimeout(timeSlot);
                    $("#view_data").css("display", "block");
                    $().toastmessage('showSuccessToast', 'The historical data is ready for viewing.');
                    $("#view_month_label").html("");
                    $("#view_month_label_value").html("");
                    $("#view_data_label").html("view restored data");
                    $("#clean_data_label").html("clear restored data");
                    $("#view_data").html("view restored data");
                    $("#clean_data").html("clear restored data");
                    $("#last_loaded_info_div").show();
                    //$("#view_month_label_value").css("display","none");
                    $.ajax
                    ({
                        type: "get",
                        url: "update_db_status_historical.py",
                        success: function (result) {
                        }
                    });
                }
                else if (result.result == "3" || result.result == 3) {
                    clearTimeout(timeSlot);
                    $("#view_data_label").html("view restored data");
                    $("#clean_data_label").html("clear restored data");
                    $("#view_data").html("view restored data");
                    $("#clean_data").html("clear restored data");
                    $("#last_loaded_info_div").show();
                    //$("#view_month_label").css("display","none");
                    //$("#view_month_label_value").css("display","none");

                    //$().toastmessage('showSuccessToast', 'The Historical Reports are ready for viewing.');
                }
                else if (result.result == "2" || result.result == 2) {
                    clearTimeout(timeSlot);
                    $().toastmessage('showWarningToast', 'Sorry the historical reports are currently not available.');
                }
                else if (result.success == 5 || result.success == "5") {
                    clearTimeout(timeSlot);
                }
                else {
                    callA = setTimeout(function () {
                        checkDbStatus();
                    }, timeSlot);
                }


            }
            else {
                clearTimeout(timeSlot);
                $().toastmessage('showWarningToast', 'Sorry the historical reports are currently not available.');
            }

        }
    });
}
function checkDb() {
    $("#last_loaded_info_div").hide();

    if (checked_values == null) {
        $().toastmessage('showErrorToast', 'Please select a month .');
        if ($("#view_month_label_value").val() != "" || $("#view_month_label_value").html() != "") {
            $("#last_loaded_info_div").show();
        }
        return;
    }
    $().toastmessage('showWarningToast', 'Please be patient , Data for month ' + checked_values + ' is being restored .');
    //$("#view_data").css("display","none");
    checkDbStatus();
    $.ajax({
        type: "get",
        url: "history_reporting_make_db.py" + '?month_var=' + $("#multiselect_month").val(),
        data: "",
        cache: false,
        success: function (result) {
            result = eval("(" + result + ")");
            if (result.success == 5 || result.success == "5") {
                $().toastmessage('showWarningToast', ' The backup of month ' + checked_values + ' doesnt exists. ');
            }
        }
    });
}


function restore_db() {
    $("#last_loaded_info_div").hide();
    if ($("#view_month_label_value").val() != "" || $("#view_month_label_value").html() != "") {
        $("#last_loaded_info_div").show();
    }

    if ($("#status_value").val() == 1) {
        $().toastmessage('showSuccessToast', 'The restored data is ready for viewing.');
        $("#view_data_label").html("view restored data");
        $("#clean_data_label").html("clear restored data");
        $("#view_data").html("view restored data");
        $("#clean_data").html("clear restored data");
        $("#last_loaded_info_div").show();
        //$("#view_month_label").css("display","none");
        //$("#view_month_label_value").css("display","none");
        $.ajax
        ({
            type: "get",
            url: "update_db_status_historical.py",
            success: function (result) {
            }
        });
    }
    else if (String($("#status_value").val()) == "0") {
        checked_values = $("#view_month_value").val();
        $().toastmessage('showWarningToast', 'Please be patient , Data for month ' + checked_values + ' is being restored .');
        $("#last_loaded_info_div").hide();
        checkDbStatus();
    }
}
$(document).ready(function () {
    $("#multiselect_month").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Month', header: "Available Months", minWidth: 200});
    $("#multiselect_month").bind("multiselectclose", function (event, ui) {
        var checked_title = $.map($(this).multiselect("getChecked"), function (input) {
            return input.title;
        });
        checked_values = checked_title;
    });
    $("#multiselect_month").bind("multiselectclose", function (event, ui) {
        var sel = $("#multiselect_month").val();
    });
    $("#multiselect_action").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Action', header: "Available Actions", minWidth: 200});
    $("#multiselect_action").bind("multiselectclose", function (event, ui) {
        var checked_title = $.map($(this).multiselect("getChecked"), function (input) {
            return input.title;
        });
        action = $("#multiselect_action").val()
        if (action == "backup") {
            $("#backup_db_button").show();
            $("#restore_db_button").hide();
            $("#clean_db_button").hide();
            $("#last_loaded_info_div").hide();
        }
        else if (action == "restore") {
            $("#restore_db_button").show();
            restore_db();
            $("#clean_db_button").hide();
            $("#backup_db_button").hide();
        }
        else if (action == "clean") {
            $("#clean_db_button").show();
            $("#backup_db_button").hide();
            $("#restore_db_button").hide();
            $("#last_loaded_info_div").hide();
        }
    });

//		$("#page_tip").colorbox(  			//page tip
//	    	{
//		href:"view_page_tip_history_reporting.py",
//		title: "Help",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"600px",
//		height:"400px"
//	    });
    //checkDbStatus();
});
