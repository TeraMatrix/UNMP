var aSelectedAvg = [];
var oTableAvg = null;
var aSelectedTotal = [];
var oTableTotal = null;
var crcAverage = [];
var crcTotal = [];
var $spinLoading = null;
var $spinMainLoading = null;
var submitClicked = false;
var all_array = []
var flag_more_options = false;
var report_json = null;
/*var report_json = {
 'odu16': ['CRC PHY','RSSI','Network Outage','Network Usage','TRAP'],
 'odu100': ['CRC PHY','RSSI','Network Outage','Network Usage','TRAP'],
 'idu': ['CRC PHY','RSSI','Network Outage','Network Usage','TRAP'],
 'ap': ['CRC PHY','Network Outage','Network Usage','TRAP'],
 'unknown': []
 };
 */
/*
 var column_json = {
 'CRC_PHY': ["timestamp","HOSTGROUP NAME", "IP Address", "PHY ERRORS", "CRC ERRORS" ,"Host name", "Host alias"],
 'RSSI': ["timestamp","HOSTGROUP NAME", "IP Address", "PEER 1", "PEER 2" , "PEER 3" , "PEER 4" , "PEER 5" , "PEER 6" , "PEER 7" , "PEER 8" ,"Host name", "Host alias"],
 'Network_Outage': ["timestamp","HOSTGROUP NAME","Host name", "Host alias", "IP Address", "UPTIME", "DOWnTIME"],
 'Network_Usage': ["timestamp","HOSTGROUP NAME", "IP Address", "Host name", "Host alias","Eth(0) RX","Eth(0) TX","Eth(1) RX","Eth(1) TX","BR(0) RX","BR(0) TX"],
 'unknown': []
 };
 */
function convert_array() {
    var all_data = $("#all_data").text();
    all_array = all_data.split("), (");
    all_array[0] = all_array[0].substring(2);
    temp = all_array.length - 1;
    all_array[temp] = all_array[temp].substring(0, all_array[temp].length - 2);
}


function host_convert_to_array(result) {
    temp_array = result.split("), (");
    temp_array[0] = temp_array[0].substring(2);
    temp = temp_array.length - 1;
    temp_array[temp] = temp_array[temp].substring(0, temp_array[temp].length - 2);
    return temp_array;
}
function multiselect_hostgroup_func() {
    $("#multiselect_hostgroup").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Hostgroup', header: "Available Hostgroups", minWidth: 290});
    $("#multiselect_hostgroup").bind("multiselectclick", function (event, ui) {
        var sel = $("#multiselect_hostgroup").val();
        if (sel != ui.value) {
            var sel = $("#multiselect_hostgroup").val();
            if (sel != null) {
                var device_type_user_selected_id = $("#device_type_user_selected_id").html();
                if (device_type_user_selected_id == "None") {
                    $("#multiselect_device").multiselect("refresh");
                }
            }

            $("#multiselect_hosts").multiselect("uncheckAll");
            $("#HostsList").html("");
            $("#multiselect_hosts").multiselect("disable");
            $("#multiselect_report").multiselect("disable");
            $("#start_date").attr('disabled', 'disabled');
            $("#end_time").attr('disabled', 'disabled');
            $("#multiselect_range").multiselect("disable");
            $("#multiselect_type").multiselect("disable");
            $("#multiselect_dates").multiselect("disable");
            flag_more_options = false;
        }
    });


    $("#multiselect_hostgroup").bind("multiselectclose", function (event, ui) {
        var sel = $("#multiselect_hostgroup").val();
        if (sel != null) {
            html_string = "";
            var device_type_user_selected_id = $("#device_type_user_selected_id").html();
            if (device_type_user_selected_id == "None") {
                for (i = 0; i < all_array.length; i++) {
                    temp_arr = all_array[i].split(",");
                    //alert(temp_arr[0]);
                    //alert(sel);
                    if (parseInt(temp_arr[0]) == sel) {
                        if (String(temp_arr[2]).toLowerCase().indexOf('ccu') < 0)
                            html_string += "<option value=" + temp_arr[2] + ">" + String(temp_arr[3].substring(2, temp_arr[3].length - 1)) + "</option>";
                    }
                }

                //alert(html_string);
                $("#multiselect_device").html(html_string);
                $("#multiselect_device").multiselect("refresh");
                $("#multiselect_device").multiselect("enable");
            }
            $("#multiselect_hosts").multiselect("uncheckAll");
            $("#HostsList").html("");
            $("#multiselect_hosts").multiselect("disable");
            $("#multiselect_report").multiselect("disable");
            $("#start_date").attr('disabled', 'disabled');
            $("#end_date").attr('disabled', 'disabled');
            $("#multiselect_range").multiselect("disable");
            $("#multiselect_dates").multiselect("disable");
            $("#multiselect_type").multiselect("disable");
            flag_more_options = false;
            sel_device = $("#multiselect_device").val();
            if (sel_device != null && sel_device != "None") {
                device_click(sel_device);
            }
        }
    });

}
function multiselect_device_func() {
    var sel_text = "a";
    $("#multiselect_device").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Device Type', header: "Available Device Type", minWidth: 290});
    $("#multiselect_device").bind("multiselectclick", function (event, ui) {
        var sel = $("#multiselect_device").val();
        // sel_text=ui.label;
        if (sel != ui.value) {
            $("#multiselect_report").multiselect("disable");
            $("#multiselect_hosts").multiselect("uncheckAll");
            $("#HostsList").html("");
            $("#multiselect_hosts").multiselect("disable");
            $("#start_date").attr('disabled', 'disabled');
            $("#end_date").attr('disabled', 'disabled');
            $("#multiselect_dates").multiselect("disable");
            $("#multiselect_range").multiselect("disable");
            $("#multiselect_type").multiselect("disable");
            flag_more_options = false;

        }
    });

    $("#multiselect_device").bind("multiselectclose", function (event, ui) {
        var sel = $("#multiselect_device").val();
        //alert(sel_text);
        if (sel != null) {
            device_click(sel);

        }
        else {
            $("#multiselect_report").multiselect("disable");
        }
    });
}

function device_click(sel) {

    html_string = "";
    temp_arr = []
    if (sel == "odu16") {
        temp_arr = report_json.odu16;
    }
    else if (sel == "odu100") {
        temp_arr = report_json.odu100;
    }
    else if (sel == "idu") {
        temp_arr = report_json.idu;
    }
    else if (sel == "ap25") {
        temp_arr = report_json.ap25;
    }
    else if (sel == "idu4") {
        temp_arr = report_json.idu4;
    }
    if (temp_arr == undefined) {
        temp_arr = [];
    }
    for (i = 0; i < temp_arr.length; i++) {
        html_string += "<option value='" + temp_arr[i] + "'>" + temp_arr[i] + "</option>";
    }
    $("#multiselect_report").html(html_string);
    $("#multiselect_report").multiselect("refresh");
    $("#multiselect_report").multiselect("enable");
    $("#multiselect_hosts").multiselect("uncheckAll");
    $("#HostsList").html("");
    $("#multiselect_hosts").multiselect("disable");
    $("#start_date").attr('disabled', 'disabled');
    $("#end_date").attr('disabled', 'disabled');
    $("#multiselect_dates").multiselect("disable");
    $("#multiselect_range").multiselect("disable");
    $("#multiselect_type").multiselect("disable");
    flag_more_options = false;
    //$("#multiselect_report").multiselect("enable");

}
function toggle_options() {
    if (flag_more_options == false) {
        return;
    }
    if ($("div#more_options_columns").css("display") == "block") {
        $("#more_options").html("More Options >>:");

    }
    else {
        $("#more_options").html("More Options <<:");
    }

    $("div#more_options_columns").toggle();
}


function multiselect_report_func() {
    $("#multiselect_report").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Report', header: "Available Reports", minWidth: 290});
    $("#multiselect_report").bind("multiselectclick", function (event, ui) {
        var sel = $("#multiselect_report").val();
        if (sel != ui.value) {
            $("#multiselect_hosts").multiselect("refresh");
            $("#start_date").attr('disabled', 'disabled');
            $("#end_date").attr('disabled', 'disabled');
            $("#multiselect_dates").multiselect("disable");
            $("#multiselect_hosts").multiselect("uncheckAll");
            $("#multiselect_range").multiselect("disable");
            $("#multiselect_type").multiselect("disable");
            $("#HostsList").html("");
            flag_more_options = false;

        }
    });

    $("#multiselect_report").bind("multiselectclose", function (event, ui) {
        var sel = $("#multiselect_report").val();
        if (sel != null) {
            hostgroup_id = $("#multiselect_hostgroup").val();
            device_type_id = $("#multiselect_device").val();
            $.ajax({
                type: "get",
                url: "analyzed_reporting_get_host_data.py" + '?hostgroup_id=' + hostgroup_id + '&device_type_id=' + device_type_id + '&report_type=' + sel + '&range_type=1',
                data: "",
                cache: false,
                success: function (result) {
                    try {
                        result = eval("(" + result + ")");
                        $("#more_options_columns").html(result.html);
                        $("#more_options_columns").hide();
                        multiSelectColumns();
                        result = result.result;
                        temp_array = host_convert_to_array(result);
                        html_string = "";
                        if (temp_array == null || temp_array == "") {
                            temp_array = [];
                        }
                        for (i = 0; i < temp_array.length; i++) {
                            temp_arr = temp_array[i].split(",");
                            if (temp_array.length == 1) {
                                html_string += "<option value=" + temp_arr[0] + ">" + String(temp_arr[1].substring(2, temp_arr[1].length - 2)) + "</option>";
                            }
                            else {
                                html_string += "<option value=" + temp_arr[0] + ">" + String(temp_arr[1].substring(2, temp_arr[1].length - 1)) + "</option>";
                            }
                        }
                        $("#multiselect_hosts").html(html_string);
                        $("#multiselect_hosts").multiselect("refresh");
                        $("#multiselect_hosts").multiselect("uncheckAll");
                        $("#HostsList").html("");
                        $("#multiselect_hosts").multiselect("enable");
                        flag_more_options = false;
                        $("#start_date").attr('disabled', 'disabled');
                        $("#end_date").attr('disabled', 'disabled');
                        $("#multiselect_range").multiselect("disable");
                        $("#multiselect_dates").multiselect("disable");
                        $("#multiselect_type").multiselect("disable");
                    }
                    catch (err) {
                        result = [];
                    }
                    if (sel == "RSSI" || sel == "RSL") {
                        var type_html = "<option value=1>Minimum</option>\
							<option value=2>Maximum</option>\
							<option value=3>Average</option>\
							<option value=5>All Options</option>";
                        $("#multiselect_type").html(type_html);
                        $("#multiselect_type").multiselect("refresh");
                    }
                    else {
                        var type_html = "<option value=1>Minimum</option>\
							<option value=2>Maximum</option>\
							<option value=3>Average</option>\
							<option value=4>Total</option>\
							<option value=5>All Options</option>";
                        $("#multiselect_type").html(type_html);
                        $("#multiselect_type").multiselect("refresh");
                    }
                }
            });
        }
    });
}


function multiselect_host_func() {
    $("#multiselect_hosts").multiselect({noneSelectedText: 'Select Host', label: "Hosts:", selectedList: 2, minWidth: 290}).multiselectfilter();
    $("#multiselect_hosts").bind("multiselectclick", function (event, ui) {
        var srce = $("#HostsList").html();
        if (ui.checked == true) {
            if (srce.indexOf("<li host_id='" + ui.value + "' rel='" + ui.value + "'>" + ui.text + "<a class='closebutton1'>x</a></li>") <= 0) {
                addSingleHost(ui.value, ui.text);
            }
        }
        else {
            var str_hosts = $("#multiselect_hosts").val();
            var checkedHosts = $(this).multiselect("getChecked").map(function () {
                return this.value;
            }).get();
            var checkedValues = $.map($(this).multiselect("getChecked"), function (input) {
                return input.title;
            });
            arr_hosts = checkedHosts;
            arr_names = checkedValues;
            host_id_str = '';
            var i = 0;
            for (i = 0; i < arr_hosts.length; i++) {
                host_id_str += '<li host_id="' + arr_hosts[i] + '" rel="' + arr_hosts[i] + '">' + arr_names[i] + '<a class="closebutton1">x</a></li>';
            }
            $("#HostsList").html(host_id_str);
        }
    });


    $("#multiselect_hosts").bind("multiselectcheckall", function (event, ui) {
        var str_hosts = $("#multiselect_hosts").html().toUpperCase();
        var checkedHosts = $(this).multiselect("getChecked").map(function () {
            return this.value;
        }).get();
        var checkedValues = $.map($(this).multiselect("getChecked"), function (input) {
            return input.title;
        });
        arr_hosts = checkedHosts;
        arr_names = checkedValues;
        host_id_str = '';
        var i = 0;
        for (i = 0; i < arr_hosts.length; i++) {
            host_id_str += '<li host_id="' + arr_hosts[i] + '" rel="' + arr_hosts[i] + '">' + arr_names[i] + '<a class="closebutton1">x</a></li>';
        }
        $("#HostsList").html(host_id_str);
    });

    $("#multiselect_hosts").bind("multiselectuncheckall", function (event, ui) {
        $("#HostsList").html("");
    });


    $("#multiselect_hosts").bind("multiselectclose", function (event, ui) {
        var sel = $("#multiselect_hosts").val();
        if (sel != null) {
            $("#more_options").removeAttr('disabled');
            $("#multiselect_type").multiselect("enable");
            html_string = "";
        }
        else {
            $("#multiselect_type").multiselect("disable");
            $("#multiselect_dates").multiselect("disable");
            $("#multiselect_range").multiselect("disable");
            $("#start_date").attr('disabled', 'disabled');
            $("#end_date").attr('disabled', 'disabled');
            $("#excel_rpt").attr('disabled', 'disabled');
            $("#csv_rpt").attr('disabled', 'disabled');
            flag_more_options = false;
        }
    });

}


function multiselect_type_func() {

    $("#multiselect_type").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Type', header: "Available Types", minWidth: 290});
    $("#multiselect_type").bind("multiselectclick", function (event, ui) {
    });
    $("#multiselect_type").bind("multiselectclose", function (event, ui) {
        var sel = $("#multiselect_type").val();
        var date_html = "";
        if (sel != null) {
            hostgroup_id = $("#multiselect_hostgroup").val();
            device_type_id = $("#multiselect_device").val();
            report_type = $("#multiselect_report").val();
            $.ajax({
                type: "get",
                url: "analyzed_reporting_get_column_range.py" + '?hostgroup_id=' + hostgroup_id + '&device_type_id=' + device_type_id + '&report_type=' + report_type + '&range_type=' + sel,
                data: "",
                cache: false,
                success: function (result) {
                    try {
                        result = eval("(" + result + ")");
                        $("#more_options_columns").html(result.html);
                        $("#more_options_columns").hide();
                        multiSelectColumns();
                    }
                    catch (err) {
                        result = [];
                    }
                }});

        }
        if (sel != null) {
            $("#more_options").removeAttr('disabled');
            $("#multiselect_range").multiselect("enable");
            $("#multiselect_dates").multiselect("enable");
            $("#excel_rpt").removeAttr('disabled');
            $("#csv_rpt").removeAttr('disabled');
            flag_more_options = true;
            html_string = "";
        }
        else {
            $("#multiselect_dates").multiselect("disable");
            $("#multiselect_range").multiselect("disable");
            $("#start_date").attr('disabled', 'disabled');
            $("#end_date").attr('disabled', 'disabled');
            $("#excel_rpt").attr('disabled', 'disabled');
            $("#csv_rpt").attr('disabled', 'disabled');
            flag_more_options = false;
        }
    });
}


function multiselect_range_func() {

    $("#multiselect_range").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Duration', header: "Available Durations", minWidth: 290});
    $("#multiselect_range").bind("multiselectclick", function (event, ui) {
    });
    $("#multiselect_range").bind("multiselectclose", function (event, ui) {
        var sel = $("#multiselect_range").val();
        var date_html = "";
        if (sel != null) {
            var end_date = new Date();
            var start_date = new Date();
            //$("#div_time_select").css("display","none");
            switch (parseInt(sel)) {
                case 1:
                    date_html = "     <option value=1>Last 3 hours</option>\
							<option value=2>Last 6 hours</option>\
							<option value=3>Last 12 hours</option>\
							<option value=4>Last 1 day</option>\
							<option value=5>Last 2 days</option>\
							<option value=6>Last 3 days</option>\
							<option value=7>Last 1 week</option>\
							<option value=8>Last 2 weeks</option>\
							<option value=9>Previous month</option>\
							<option value=10>Previous 2 months</option>\
							<option value=11>Previous 3 months</option>\
							<option value=12>Previous 6 months</option>\
							<option value=20>Custom Time Range</option>";
                    break;
                case 2:
                    date_html = "     <option value=4>Last 1 day</option>\
							<option value=5>Last 2 days</option>\
							<option value=6>Last 3 days</option>\
							<option value=7>Last 1 week</option>\
							<option value=8>Last 2 weeks</option>\
							<option value=9>Previous  month</option>\
							<option value=10>Previous 2 months</option>\
							<option value=11>Previous 3 months</option>\
							<option value=12>Previous 6 months</option>\
							<option value=20>Custom Time Range</option>";
                    break;
                case 3:
                    date_html = "	<option value=7>Last 1 week</option>\
							<option value=8>Last 2 weeks</option>\
							<option value=9>Previous month</option>\
							<option value=10>Previous 2 months</option>\
							<option value=11>Previous 3 months</option>\
							<option value=12>Previous 6 months</option>\
							<option value=20>Custom Time Range</option>";
                    break;
                case 4:
                    date_html = "     <option value=9>Previous month</option>\
							<option value=10>Previous 2 months</option>\
							<option value=11>Previous 3 months</option>\
							<option value=12>Previous 6 months</option>\
							<option value=20>Custom Time Range</option>";
                    break;
            }
            $("#multiselect_dates").html(date_html);
            $("#multiselect_dates").multiselect("enable");
            $("#multiselect_dates").multiselect("refresh");
            $("#start_date").removeAttr('disabled');
            $("#end_date").removeAttr('disabled');
            $("#div_time_select").css("display", "none");

        }

    });
}

function multiselect_dates_func() {

    $("#multiselect_dates").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Time Range', header: "Available Time Range", minWidth: 290});
    $("#multiselect_dates").bind("multiselectclick", function (event, ui) {
    });
    $("#multiselect_dates").bind("multiselectclose", function (event, ui) {
        var sel = $("#multiselect_dates").val();
        if (sel != null) {
            var end_date = new Date();
            var start_date = new Date();
            //$("#div_time_select").css("display","none");
            switch (parseInt(sel)) {
                case 1:
                    start_date.setHours(start_date.getHours() - 3);
                    break;
                case 2:
                    start_date.setHours(start_date.getHours() - 6);
                    break;
                case 3:
                    start_date.setHours(start_date.getHours() - 12);
                    break;
                case 4:
                    start_date.setDate(start_date.getDate() - 1);
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 5:
                    start_date.setDate(start_date.getDate() - 2);
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 6:
                    start_date.setDate(start_date.getDate() - 3);
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 7:
                    var temp_d = new Date();
                    var day = temp_d.getDay(), diff = temp_d.getDate() - day + (day == 0 ? -7 : 0); // adjust when day is sunday
                    start_date = new Date(temp_d.setDate(diff));
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 8:
                    var temp_d = new Date();
                    var day = temp_d.getDay(), diff = temp_d.getDate() - day + (day == 0 ? -7 : 0); // adjust when day is sunday
                    temp_d = new Date(temp_d.setDate(diff));
                    day = temp_d.getDay(), diff = temp_d.getDate() - day + (day == 0 ? -7 : 0); // adjust when day is sunday
                    start_date = new Date(temp_d.setDate(diff));
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    //start_date.setDate(start_date.getDate()-14);
                    break;
                case 9:
                    var cur_date = new Date();
                    start_date.setDate(1);
                    start_date.setMonth((cur_date.getMonth() - 1));
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 10:
                    var cur_date = new Date();
                    start_date.setDate(1);
                    start_date.setMonth((cur_date.getMonth() - 2));
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 11:
                    var cur_date = new Date();
                    start_date.setDate(1);
                    start_date.setMonth((cur_date.getMonth() - 3));
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 12:
                    var cur_date = new Date();
                    start_date.setDate(1);
                    start_date.setMonth((cur_date.getMonth() - 6));
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 15:
                    start_date.setDate(1);
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 20:
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    $("#div_time_select").css("display", "block");
                    $("#start_date").removeAttr('disabled');
                    $("#end_date").removeAttr('disabled');
                    break;
            }
            if (parseInt(sel) != 20) {
                $("#div_time_select").css("display", "none");
            }
            var s_date = start_date.getDate() + "/" + parseInt(parseInt(start_date.getMonth()) + 1) + "/" + start_date.getFullYear();
            var s_time = start_date.getHours() + ":" + start_date.getMinutes();
            var e_date = end_date.getDate() + "/" + parseInt(parseInt(end_date.getMonth()) + 1) + "/" + end_date.getFullYear();
            var e_time = end_date.getHours() + ":" + end_date.getMinutes();
            $("#start_date").val(s_date);
            $("#end_date").val(e_date);
            $("#start_time").val(s_time);
            $("#end_time").val(e_time);
            //$("#div_time_select").css("display","block");
        }
    });
}


$(document).ready(function () {
    $('#start_date,  #end_date').calendricalDateRange({
        isoTime: true
    });
    report_json = eval("(" + $("#host_data_mapping").html() + ")");
    $spinLoading = $("div#spin_loading");        // create object that hold loading circle
    $spinMainLoading = $("div#main_loading");    // create object that hold loading squire
    convert_array();
    multiselect_device_func();
    multiselect_hostgroup_func();
    multiselect_report_func();
    multiselect_host_func();
    multiselect_type_func();
    multiselect_range_func();
    multiselect_dates_func();
    deleteHostAction();
    $("#multiselect_device").multiselect("disable");
    $("#multiselect_report").multiselect("disable");
    $("#multiselect_hosts").multiselect("disable");
    $("#multiselect_type").multiselect("disable");
    $("#multiselect_dates").multiselect("disable");
    $("#multiselect_range").multiselect("disable");
    var device_type_user_selected_id = $("#device_type_user_selected_id").html();
    var device_type_user_selected_name = $("#device_type_user_selected_name").html();
    if (device_type_user_selected_id != "None") {
        html_str = "<option value=" + device_type_user_selected_id + " selected=\"selected\">" + device_type_user_selected_name + "</option>";
        $("#multiselect_device").html(html_str);
        $("#multiselect_device").multiselect("enable");
        $("#multiselect_device").multiselect("refresh");
    }

    $("#get_main_reporting_data").submit(function () {
        var cur_date = new Date();
        var d = cur_date.getDate();
        var y = cur_date.getFullYear();
        var m = cur_date.getMonth();
        var cdate = new Date(y, m, d);
        var start_date = $("#start_date").val();
        var end_date = $("#end_date").val();
        var start_time = $("#start_time").val();
        var end_time = $("#end_time").val();
        if ($("#multiselect_hosts").val() == null) {
            return false;
        }
        var str1 = $("#start_date").val();
        var str2 = $("#end_date").val();
        str1 = str1.split("/");
        str2 = str2.split("/");
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
        else if ($("#hd").val() == "") {
            $().toastmessage('showErrorToast', "Select At Least One Column");
            return false;
        }
        else if ($("#multiselect_type").val() == null || $("#multiselect_type").val() == "") {
            $().toastmessage('showErrorToast', "Please select the report type");
            return false;
        }
        columns_name = $("#hd").val().split(",");
        str_paginate_table = '<table cellpadding="0" cellspacing="0" border="0" class="display" id="table_paginate" style=\"text-align:center;\"><thead>\
				<tr>';
        for (var k = 0; k < columns_name.length; k++) {
            str_paginate_table += '<th>' + columns_name[k] + '</th>';
        }
        str_paginate_table += '		</tr>\
					</thead>\
				</table>';
        $('#div_table_paginate').html(str_paginate_table);
        var url = "analyzed_reporting_get_excel.py?start_date=" + start_date + "&end_date=" + end_date + "&start_time=" + start_time + "&end_time=" + end_time + "&all_host=" + $("#multiselect_hosts").val() + "&columns=" + $("#hd").val();
        url += "&report_type=" + $("#multiselect_report").val() + "&device_type=" + $("#multiselect_device").val() + "&hostgroup=" + $("#multiselect_hostgroup").val() + "&range_type=" + $("#multiselect_type").val() + "&range_duration=" + $("#multiselect_range").val() + "&view_type=data_table";
        oTableTotal = $('#table_paginate').dataTable({
            "bJQueryUI": true,
            "sPaginationType": "full_numbers",
            "bProcessing": true,
            "bServerSide": true,
            "sAjaxSource": url,//"data_table.py?yo=1",
            "sServerMethod": "POST",
            "bRetrieve": true,
            "sScrollX": "100%"
            //"bSort": false

        });
        return false;
        //$("#table_paginate").show();
    });
//$("#page_tip").colorbox(  			//page tip
//	    	{
//		href:"view_page_tip_analyzed_reporting.py",
//		title: "Help",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"600px",
//		height:"600px"
//	    });
});

// reporting function start
function excel_report(report_type) {
    if (report_type == 1) {
        report_type = "excel";
    }
    else {
        report_type = "csv";
    }
    if ($("#multiselect_hosts").val() == null) {
        return false;
    }
    else if ($("#hd").val() == "") {
        $().toastmessage('showErrorToast', "Select At Least One Column");
        return false;
    }
    spinStart($spinLoading, $spinMainLoading);
    var cur_date = new Date();
    var d = cur_date.getDate();
    var y = cur_date.getFullYear();
    var m = cur_date.getMonth();
    var cdate = new Date(y, m, d);
    var method = 'post';
    var start_date = $("#start_date").val();
    var end_date = $("#end_date").val();
    var start_time = $("#start_time").val();
    var end_time = $("#end_time").val();
    var str1 = $("#start_date").val();
    var str2 = $("#end_date").val();
    str1 = str1.split("/");
    str2 = str2.split("/");
    var date1 = new Date(str1[2], parseInt(str1[1], 10) - 1, str1[0]);
    var date2 = new Date(str2[2], parseInt(str2[1], 10) - 1, str2[0]);
    if (date2 < date1) {
        $().toastmessage('showErrorToast', "End Date can't be smaller than Start Date");
        spinStop($spinLoading, $spinMainLoading);
        return false;
    }
    else if (cdate < date1 || cdate < date2) {
        $().toastmessage('showErrorToast', "Dates can't be greater than current Date");
        spinStop($spinLoading, $spinMainLoading);
        return false;
    }
    var url = "analyzed_reporting_get_excel.py?start_date=" + start_date + "&end_date=" + end_date + "&start_time=" + start_time + "&end_time=" + end_time + "&all_host=" + $("#multiselect_hosts").val() + "&columns=" + $("#hd").val();
    url += "&report_type=" + $("#multiselect_report").val() + "&device_type=" + $("#multiselect_device").val() + "&hostgroup=" + $("#multiselect_hostgroup").val() + "&range_type=" + $("#multiselect_type").val() + "&range_duration=" + $("#multiselect_range").val() + "&view_type=" + report_type;
    $.ajax({
        type: method,
        url: url,
        cache: false,
        success: function (result) {
            result = eval("(" + result + ")");
            if (result.success == 0 || result.success == '0') {
                spinStop($spinLoading, $spinMainLoading);
                $().toastmessage('showSuccessToast', "Report Generated Successfully.");
                window.location = "download" + "/" + result.file;
            }
            else if (result.success == 1 || result.success == '1') {
                spinStop($spinLoading, $spinMainLoading);
                $().toastmessage('showWarningToast', 'No Data Available for the Time Specified. ');
            }
            else {
                spinStop($spinLoading, $spinMainLoading);
                $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
            }

        }
    });
}
// reporting function end

function multiSelectColumns() {
    $(".plus").click(function () {
        plusHostParentOption(this);
    })
    $(".minus").click(function () {
        minusHostParentOption(this);
    })
    var hostParentArray = [];
    var tempHostParent = $("input[name='hdTemp']").val();
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
    $(Obj).parent().parent().parent().parent().find("input[name='hd']").val("");
    j = 0
    for (i = 0; i < $(Obj).parent().parent().find("li").size(); i++) {
        var addedHostParent = $(Obj).parent().parent().find("li").eq(i).find("img").attr("id");
        if (addedHostParent != $(Obj).attr("id")) {
            if (j == 0) {
                $(Obj).parent().parent().parent().parent().find("input[name='hd']").val($.trim(addedHostParent));
            }
            else {
                $(Obj).parent().parent().parent().parent().find("input[name='hd']").val($(Obj).parent().parent().parent().parent().find("input[name='hd']").val() + "," + $.trim(addedHostParent));
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
    hdval = $(Obj).parent().parent().parent().parent().find("input[name='hd']").val()
    if ($.trim(hdval) == "") {
        $(Obj).parent().parent().parent().parent().find("input[name='hd']").val($(Obj).attr("id"))
    }
    else {
        $(Obj).parent().parent().parent().parent().find("input[name='hd']").val(hdval + "," + $(Obj).attr("id"))
    }
    countParent = $(Obj).parent().parent().parent().parent().find("span#count").html();
    $(Obj).parent().parent().parent().parent().find("span#count").html(parseInt(countParent) + 1);
    $(Obj).parent().remove();
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function addHosts(s, val) {
    var objectString = s;                //  json string of hosts
    var content = '';
    $.each(objectString, function (i, item) {
        $("div#hostsList").find("li[host_id='" + objectString[i].value + "']").remove();
        content += "<li host_id='" + objectString[i].value + "' rel='" + val + "'>" + objectString[i].title + "<a class='closebutton1'>x</a></li>";
    });
    $('#HostsList').append(content);  // append list to conatiner
    var len = filterHoststring();
}

function addSingleHost(val, text) {
    var content = '';
    content += "<li host_id='" + val + "' rel='" + val + "'>" + text + "<a class='closebutton1'>x</a></li>";
    $('#HostsList').append(content);  // append list to conatiner
    var len = filterHoststring();
}

// delete action of host


//function to delete group from facebox list
function del_gp_from_fb(id) {
    $('#fb_gp .bit-box[rel="' + id + '"]').find("a").click();
//	$("ul#fb_gp .bit-box[rel='" + id + "']").find("a").click();
    var len = filterHoststring();
    if (len.length == 0) {
        $("#no_of_devices").attr('disabled', false);
    }
}
function del_hostGroup(id) {
    var target = id;
    $('#HostsList li').each(function () {
        if ($(this).attr('rel') == target) {
            $(this).remove();
            del_host_from_fb($(this).attr('host_id'));
        }
    });
    var len = filterHoststring();
}

//delete action of Host
function deleteHostAction() {
    del_hostOnSpanClick();
}

function del_hostOnSpanClick() {
    $('#HostsList li a.closebutton1').live('click', function () {
        var str_host_id = $(this).parent().attr('host_id');//2L
        var str_host_name = $(this).parent().text();
        $("#multiselect_hosts").multiselect("widget").find("input[value='" + str_host_id + "']").each(function () {
            this.click();
        })
        //commenting here
        //del_host_from_fb($(this).parent().attr('host_id'));
        //<option aria-selected="true" value="2L">172.22.0.110</option><option aria-selected="true" value="6L">172.22.0.115</option>
//		del_host_from_fb(target);
    });
}

//function to delete group from facebox list
function del_host_from_fb(id) {
    $('#fb_host li.bit-box[rel="' + id + '"]').find("a").click();

}
// function to delete group

function del_group(id) {
    $("ul#fb_gp li[rel='" + id + "']").find("a").click();
    $('#GroupsList li[gp_id="' + id + '"]').find("a").click();
    var len = filterHoststring();
}

// function for check host of same group
function checkHostOfSameGroup(rel) {
    var count = 0;
//var flag = 1;
    $('#HostsList li').each(function () {
        if ($(this).attr('rel') == rel) {
            count++;
        }
    });
    return count;
}


function selectGroup() {
    $('#GroupsList li').live('click', function () {
        $('#GroupsList li').removeClass('Highlight');
        $('#hostsList li').removeClass('Highlight');
        var target = $(this);
        var id = target.attr('gp_id');
        if ($(this).hasClass('Highlight')) {
            target.removeClass('Highlight');
            $('#hostsList li[rel="' + id + '"]').removeClass('Highlight');
        }
        else {
            target.addClass('Highlight');
            $('#hostsList li[rel="' + id + '"]').addClass('Highlight');
        }
        //$(this).toggleClass('Highlight');
    });
}
//function returns group string from container
function filterGroupstring() {
    var groupString = '';
    $('#GroupsList').find('li').each(function () {
        groupString += $(this).attr('gp_id') + ',';

    });
    return groupString;
}
//function returns host string from container
function filterHoststring() {
    var hostString = '';
    $('#HostsList').find('li').each(function () {
        hostString += $(this).attr('host_id') + ',';

    });
    return hostString;
}


// function for searching group
function searchGroup(gp_id) {
    var id = gp_id;
    var count = 0;
    $('#GroupsList li').each(function () {
        if ($(this).attr('gp_id') == id) {
            count = 1
        }
        else {
            count = 0
        }
    });
    return count;
}

