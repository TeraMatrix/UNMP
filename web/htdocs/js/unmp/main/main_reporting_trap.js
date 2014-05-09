// New trap.js
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

function multiselect_report_func() {
    $("#multiselect_report").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Report', header: "Available Reports", minWidth: 290});
    $("#multiselect_report").bind("multiselectclick", function (event, ui) {
        var sel = $("#multiselect_report").val();
        if (sel != ui.value) {

            $("#excel_rpt").removeAttr('disabled');
            $("#csv_rpt").removeAttr('disabled');
            $("#multiselect_dates").multiselect("enable");
            /*$("#multiselect_hosts").multiselect("refresh");
             $("#start_date").attr('disabled','disabled');
             $("#start_time").attr('disabled','disabled');
             $("#end_date").attr('disabled','disabled');
             $("#end_time").attr('disabled','disabled');
             $("#multiselect_dates").multiselect("disable");
             $("#multiselect_hosts").multiselect("uncheckAll");
             $("#HostsList").html("");
             flag_more_options=false;	*/

        }
    });

    $("#multiselect_report").bind("multiselectclose", function (event, ui) {
        var sel = $("#multiselect_report").val();
        if (sel != null) {
        }
    });
}


function multiselect_hostgroup_func() {
    $("#multiselect_hostgroup").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Hostgroup', header: "Available Hostgroups", minWidth: 290});
    $("#multiselect_hostgroup").bind("multiselectclick", function (event, ui) {
        var sel = $("#multiselect_hostgroup").val();
        if (sel != ui.value) {
            var sel = $("#multiselect_hostgroup").val();
            $("#multiselect_hosts").multiselect("uncheckAll");
            $("#HostsList").html("");
            $("#multiselect_hosts").multiselect("disable");
            $("#start_date").attr('disabled', 'disabled');
            $("#start_time").attr('disabled', 'disabled');
            $("#end_date").attr('disabled', 'disabled');
            $("#end_time").attr('disabled', 'disabled');
            //$("#multiselect_dates").multiselect("disable");
            flag_more_options = false;
        }
    });


    $("#multiselect_hostgroup").bind("multiselectclose", function (event, ui) {
        var sel = $("#multiselect_hostgroup").val();
        if (sel != null) {
            html_string = "";
            var device_type_user_selected_id = "None";
            if (device_type_user_selected_id == "None") {
                for (i = 0; i < all_array.length; i++) {
                    temp_arr = all_array[i].split(",");
                    //alert(temp_arr[0]);
                    //alert(sel);
                    if (parseInt(temp_arr[0]) == sel) {
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
            //$("#multiselect_report").multiselect("disable");
            $("#start_date").attr('disabled', 'disabled');
            $("#start_time").attr('disabled', 'disabled');
            $("#end_date").attr('disabled', 'disabled');
            $("#end_time").attr('disabled', 'disabled');
            $("#multiselect_hosts").multiselect("disable");
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
            //$("#multiselect_report").multiselect("disable");
            $("#multiselect_hosts").multiselect("uncheckAll");
            $("#HostsList").html("");
            $("#multiselect_hosts").multiselect("disable");
            $("#start_date").attr('disabled', 'disabled');
            $("#start_time").attr('disabled', 'disabled');
            $("#end_date").attr('disabled', 'disabled');
            $("#end_time").attr('disabled', 'disabled');
            $("#multiselect_hosts").multiselect("disable");
            flag_more_options = false;

        }
    });

    $("#multiselect_device").bind("multiselectclose", function (event, ui) {
        var sel = $("#multiselect_device").val();
        //alert(sel_text);
        if (sel != null) {

            hostgroup_id = $("#multiselect_hostgroup").val();
            device_type_id = sel;
            $.ajax({
                type: "get",
                url: "trap_main_reporting_get_host_data.py" + '?hostgroup_id=' + hostgroup_id + '&device_type_id=' + device_type_id + '&report_type=' + $("#multiselect_report").val(),
                data: "",
                cache: false,
                success: function (result) {
                    try {
                        result = eval("(" + result + ")");
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
                        $("#start_time").attr('disabled', 'disabled');
                        $("#end_date").attr('disabled', 'disabled');
                        $("#end_time").attr('disabled', 'disabled');
                    }
                    catch (err) {
                        result = [];
                    }
                }
            });
            //$("#multiselect_report").multiselect("refresh");
            //$("#multiselect_report").multiselect("enable");
            $("#multiselect_hosts").multiselect("uncheckAll");
            $("#HostsList").html("");
            $("#multiselect_hosts").multiselect("disable");
            $("#start_date").attr('disabled', 'disabled');
            $("#start_time").attr('disabled', 'disabled');
            $("#end_date").attr('disabled', 'disabled');
            $("#end_time").attr('disabled', 'disabled');
            //$("#multiselect_dates").multiselect("disable");
            flag_more_options = false;
            //device_click(sel); commented
        }
        else {
            //$("#multiselect_report").multiselect("disable");
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
    //$("#multiselect_report").html(html_string);
    //$("#multiselect_report").multiselect("refresh");
    //$("#multiselect_report").multiselect("enable");
    $("#multiselect_hosts").multiselect("uncheckAll");
    $("#HostsList").html("");
    $("#multiselect_hosts").multiselect("disable");
    $("#start_date").attr('disabled', 'disabled');
    $("#start_time").attr('disabled', 'disabled');
    $("#end_date").attr('disabled', 'disabled');
    $("#end_time").attr('disabled', 'disabled');
    //$("#multiselect_dates").multiselect("disable");
    flag_more_options = false;
    //$("#multiselect_report").multiselect("enable");

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
        else {    /*if(srce.indexOf("sizcache")==-1):
         {
         var temp_str='<li host_id="'+ui.value+'" rel="'+ui.value+'">' +ui.text+'<a class="closebutton1">x</a></li>';
         var inde=srce.indexOf(temp_str);
         // <LI sizcache="201" sizset="0" rel="8" host_id="8" > 172.22.0.105<A class=closebutton1>x</a></LI>
         var dest=srce.substring(0,inde)+srce.substring(inde+temp_str.length,srce.length);
         $("#HostsList").html(dest);
         }
         }*/

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
            //$("#multiselect_device").multiselect("enable");
            $("#more_options").removeAttr('disabled');
            $("#start_date").removeAttr('disabled');
            $("#start_time").removeAttr('disabled');
            $("#end_date").removeAttr('disabled');
            $("#end_time").removeAttr('disabled');
            $("#multiselect_dates").multiselect("enable");
            $("#excel_rpt").removeAttr('disabled');
            $("#csv_rpt").removeAttr('disabled');
            flag_more_options = true;
            html_string = "";
            //html_string+="</ul";
            //$("#selectedList").html(html_string);
            //multiSelectColumns();


        }
        else {
            //$("#multiselect_dates").multiselect("disable");
            $("#start_date").attr('disabled', 'disabled');
            $("#start_time").attr('disabled', 'disabled');
            $("#end_date").attr('disabled', 'disabled');
            $("#end_time").attr('disabled', 'disabled');
            $("#excel_rpt").attr('disabled', 'disabled');
            $("#csv_rpt").attr('disabled');
            flag_more_options = false;
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
                    start_date.setMinutes(start_date.getMinutes() - 30);
                    break;
                case 2:
                    start_date.setMinutes(start_date.getMinutes() - 60);
                    break;
                case 3:
                    start_date.setHours(start_date.getHours() - 2);
                    break;
                case 4:
                    start_date.setHours(start_date.getHours() - 3);
                    break;
                case 5:
                    start_date.setHours(start_date.getHours() - 6);
                    break;
                case 6:
                    start_date.setHours(start_date.getHours() - 12);
                    break;
                case 7:
                    start_date.setHours(start_date.getHours() - 24);
                    start_date.setMinutes(0);
                    break;
                case 8:
                    start_date.setDate(start_date.getDate() - 7);
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 9:
                    start_date.setDate(start_date.getDate() - 14);
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 10:
                    var cur_date = new Date();
                    temp_date = new Date(cur_date.getYear(), cur_date.getMonth(), 0);
                    end_date.setDate(temp_date.getDate());
                    end_date.setMonth(cur_date.getMonth() - 1);
                    start_date.setDate(1);
                    start_date.setMonth((cur_date.getMonth() - 1));
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 11:
                    var cur_date = new Date();
                    temp_date = new Date(cur_date.getYear(), cur_date.getMonth() - 1, 0);
                    end_date.setDate(temp_date.getDate());
                    end_date.setMonth(cur_date.getMonth() - 1);
                    start_date.setDate(1);
                    start_date.setMonth((cur_date.getMonth() - 2));
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 12:
                    start_date.setMonth(start_date.getMonth() - 3);
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 15:
                    start_date.setDate(1);
                    start_date.setHours(0);
                    start_date.setMinutes(0);
                    break;
                case 20:
                    start_date.setMinutes(start_date.getMinutes() - 30);
                    $("#div_time_select").css("display", "block");
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
    $('#start_date, #start_time, #end_date,  #end_time').calendricalDateTimeRange({
        isoTime: true
    });
    report_json = eval("(" + $("#host_data_mapping").html() + ")");
    $spinLoading = $("div#spin_loading");        // create object that hold loading circle
    $spinMainLoading = $("div#main_loading");    // create object that hold loading squire
    convert_array();
    multiselect_report_func();
    multiselect_device_func();
    multiselect_hostgroup_func();
    multiselect_host_func();
    multiselect_dates_func();
    deleteHostAction();
    $("#multiselect_report").multiselect("enable");
    $("#multiselect_device").multiselect("disable");
    $("#multiselect_hosts").multiselect("disable");
    $("#multiselect_dates").multiselect("disable");

    $("#trap_get_main_reporting_data").submit(function () {
        var cur_date = new Date();
        var d = cur_date.getDate();
        var y = cur_date.getFullYear();
        var m = cur_date.getMonth();
        var cdate = new Date(y, m, d);
        var start_date = $("#start_date").val();
        var end_date = $("#end_date").val();
        var start_time = $("#start_time").val();
        var end_time = $("#end_time").val();
        if ($("#multiselect_report").val() == null) {
            $().toastmessage('showErrorToast', "Please select the report type.");
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
        str_paginate_table = '<table cellpadding="0" cellspacing="0" border="0" class="display" id="table_paginate" style=\"text-align:center;\"><thead>\
				<tr>\
					<th>Timestamp</th>\
					<th>IP Address</th>\
					<th>Host Alias</th>\
					<th>Hostgroup</th>\
					<th>Device Type</th>\
					<th>Severity</th>\
					<th>Event Name</th>\
					<th>Event ID</th>\
					<th>Event Type</th>\
					<th>Object ID</th>\
					<th>Object Name</th>\
					<th>Component ID</th>\
					<th>Description</th>\
				</tr>\
				</thead>\
				</table>';
        $('#div_table_paginate').html(str_paginate_table);
        all_hosts = $("#multiselect_hosts").val();
        hostgroup = $("#multiselect_hostgroup").val();
        device_type = $("#multiselect_device").val();
        if (all_hosts == null) {
            all_hosts = "";
        }
        if (hostgroup == null) {
            hostgroup = "";
        }
        if (device_type == null) {
            device_type = "";
        }
        var url = "trap_main_reporting_get_excel.py?start_date=" + start_date + "&end_date=" + end_date + "&start_time=" + start_time + "&end_time=" + end_time + "&all_host=" + all_hosts;
        url += "&report_type=" + $("#multiselect_report").val() + "&device_type=" + device_type + "&hostgroup=" + hostgroup + "&view_type=data_table";
        oTableTotal = $('#table_paginate').dataTable({
            "bJQueryUI": true,
            "sPaginationType": "full_numbers",
            "sScrollY": "250px",
            "bProcessing": true,
            "bServerSide": true,
            "sAjaxSource": url,//"data_table.py?yo=1",
            "bRetrieve": true,
            "sScrollX": "100%",
            "aaSorting": [
                [ 0, "desc" ]
            ],
            "aoColumns": [
                { "sWidth": "10%"},
                { "sWidth": "10%" },
                { "sWidth": "10%" },
                { "sWidth": "10%" },
                { "sWidth": "5%" },
                { "sWidth": "5%" },
                { "sWidth": "5%" },
                { "sWidth": "2%" },
                { "sWidth": "8%" },
                { "sWidth": "2%" },
                { "sWidth": "2%" },
                { "sWidth": "2%" },
                { "sWidth": "18%" }
            ]
        });
        return false;
        //$("#table_paginate").show();
    });
//$("#page_tip").colorbox(  			//page tip
//	    	{
//		href:"trap_view_page_tip_main_reporting.py",
//		title: "Page Tip",
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

    if ($("#multiselect_report").val() == null) {
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

    all_hosts = $("#multiselect_hosts").val();
    hostgroup = $("#multiselect_hostgroup").val();
    device_type = $("#multiselect_device").val();
    if (all_hosts == null) {
        all_hosts = "";
    }
    if (hostgroup == null) {
        hostgroup = "";
    }
    if (device_type == null) {
        device_type = "";
    }
    var url = "trap_main_reporting_get_excel.py?start_date=" + start_date + "&end_date=" + end_date + "&start_time=" + start_time + "&end_time=" + end_time + "&all_host=" + all_hosts;
    url += "&report_type=" + $("#multiselect_report").val() + "&device_type=" + device_type + "&hostgroup=" + hostgroup + "&view_type=" + report_type;
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
                //window.open("download"+"/"+result.file);
                window.location = "download/" + result.file;
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

