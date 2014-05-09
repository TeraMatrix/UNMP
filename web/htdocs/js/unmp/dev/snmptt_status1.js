//var starting_pag="alarm_option"
var option = 3;
var last_execution_time = 0;
var change_img_dict = {'Normal': 'images/gr.png', 'Minor': 'images/yel.png.png', 'Major': 'images/or.png', 'Critical': 'images/red.png'};
var main_img_dict = {'Normal': 'images/gr.png', 'Minor': 'images/yel.png.png', 'Major': 'images/or.png', 'Critical': 'images/red.png'};
var serevity_id = {'Informational': '#serevity1', 'Normal': '#serevity2', 'Minor': '#serevity3', 'Major': '#serevity4', 'Critical': '#serevity5'};
var image_div_id = {1: '#informational_div', 2: '#normal_div', 3: '#minor_div', 4: '#major_div', 5: '#critical_div'};
var serevity_value = ['0', '1', '2', '3', '4' , '5'];
// ip validataion function
var $spinLoading = null;
var $spinMainLoading = null;
var searchFlag = 0;
var countTimes = 0;
var eventRecursion = null;
var oTable = null;
var option_value = null;
var endDate = null;

$(document).ready(function () {
    $('#event_start_date, #event_start_time, #event_end_date,  #event_end_time').calendricalDateTimeRange({
        isoTime: true
    });
    option_value = $("input[name='option']:checked").val();
    btnClickEvent();
//	$("#page_tip").colorbox(
//	{
//	href:"page_tip_event_details.py",
//	title: "Page Tip",
//	opacity: 0.4,
//	maxWidth: "80%",
//	width:"650x",
//	height:"500px",
//	onComplte:function(){}
//	});
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
    $("#alarm_info_form").hide();
    $('a[rel*=facebox]').facebox({
        loadingImage: 'facebox/loading.gif',
        closeImage: "facebox/closelabel.png"
    });

    $("#serevity1").attr('checked', true);
    $("#serevity2").attr('checked', true);
    $("#serevity3").attr('checked', true);
    $("#serevity4").attr('checked', true);
    $("#serevity5").attr('checked', true);

    $("input[name='option']").click(function () {
        $("#alarm_info_form").submit();
    });

    $("div.trap_select_option_div").toggle(function () {
            image_name = $(this).find('img').attr('alt');
            if ($(this).find('span').hasClass('inactive-linkclass')) {
                $(this).find('img').attr('src', main_img_dict[image_name]);
                $(this).find('span').removeClass('inactive-linkclass');
                $(serevity_id[image_name]).attr("checked", true);
                serevity_value[($(serevity_id[image_name]).val())] = $(serevity_id[image_name]).val()
            }
            else {
                $(this).find('img').attr('src', change_img_dict[image_name]);
                $(this).find('span').addClass('inactive-linkclass');
                $(serevity_id[image_name]).attr("checked", false);
                serevity_value[($(serevity_id[image_name]).val())] = 'None'
            }
            $("#alarm_info_form").submit();

        },
        function () {
            image_name = $(this).find('img').attr('alt');
            if ($(this).find('span').hasClass('inactive-linkclass')) {
                $(this).find('img').attr('src', main_img_dict[image_name]);
                $(this).find('span').removeClass('inactive-linkclass');
                $(serevity_id[image_name]).attr("checked", true);
                serevity_value[($(serevity_id[image_name]).val())] = $(serevity_id[image_name]).val()
            }
            else {
                $(this).find('img').attr('src', change_img_dict[image_name]);
                $(this).find('span').addClass('inactive-linkclass');
                $(serevity_id[image_name]).attr("checked", false);
                serevity_value[($(serevity_id[image_name]).val())] = 'None'
            }
            $("#alarm_info_form").submit();
        });

    $("input[name='serevity']").change(function () {
        if ($(this).is(':checked')) {
            val = $(this).val();
            img_name = $(image_div_id[val]).find('img').attr('alt');
            $(image_div_id[val]).find('img').attr('src', main_img_dict[img_name]);
            $(image_div_id[val]).find('span').removeClass('inactive-linkclass');
            serevity_value[val] = val;


        }
        else {
            val = $(this).val();
            img_name = $(image_div_id[val]).find('img').attr('alt');
            $(image_div_id[val]).find('img').attr('src', change_img_dict[img_name]);
            $(image_div_id[val]).find('span').addClass('inactive-linkclass');
            serevity_value[val] = 'None';

        }
    });
    // advanced searching element
    $("input[id='agentId']").ccplAutoComplete("common_ip_mac_search.py?device_type=odu100&ip_mac_search=" + 1, {
        dataType: 'json',
        max: 30,
        selectedItem: $("input[id='agentId']").val()
    });
    $("input[id='eventType']").ccplAutoComplete("trap_search_elements.py?serarch_item=trap_event_type&option=" + option_value, {
        dataType: 'json',
        max: 30,
        selectedItem: $("input[id='eventType']").val()
    });
    $("input[id='M_obj']").ccplAutoComplete("trap_search_elements.py?serarch_item=manage_obj_id&option=" + option_value, {
        dataType: 'json',
        max: 10,
        selectedItem: $("input[id='M_obj']").val()
    });
    $("input[id='M_name']").ccplAutoComplete("trap_search_elements.py?serarch_item=manage_obj_name&option=" + option_value, {
        dataType: 'json',
        max: 10,
        selectedItem: $("input[id='M_name']").val()
    });
    $("input[id='camponent_id']").ccplAutoComplete("trap_search_elements.py?serarch_item=component_id&option=" + option_value, {
        dataType: 'json',
        max: 10,
        selectedItem: $("input[id='camponent_id']").val()
    });
});


$(function () {
    //data_table()
    //alarm_current_info();
    formValidation();
    trapFilterFunction();
    trap_status = $("#trap_status_id").val();
    if (trap_status == "current") {
        $("input[id='option1']").attr("checked", true);
    }
    else {
        $("input[id='option1']").attr("checked", true);
    }
    $("#alarm_info_form").submit();
    $("input[id='btn_filter']").toggle(function () {
            $("#alarm_info_form").show();
            $(this).val("Hide Search");
            $(this).hide();
        }
        , function () {
            $("#alarm_info_form").hide();
            $(this).val("Advanced Search");
            $(this).show();
            countTimes = 0;
            searchFlag = 0;
        });

    $("input[id='btn_hide']").click(function () {
        $("input[id='btn_filter']").click();
    });

});


function alarmDetail(trap_id) {
    $.colorbox(
        {
            href: "trap_detail_information.py?trap_id=" + trap_id + "&option=" + option,
            title: "",
            opacity: 0.4,
            maxWidth: "80%",
            width: "536px",
            height: "auto"
        });
}


function trapFilterFunction() {
    agent_Id = $("#agentId").val()
    $("#alarm_info_form").submit(function () {
        if ($(this).valid()) {
            /*		    $.ajax({
             type:"post",
             url:"update_date_time.py",
             cache:false,
             success:function(result){
             if (result.success==1 || result.success=="1")
             {
             $().toastmessage('showWarningToast', "Date time not receving in proper format.");
             return false;
             }
             else
             {
             endDate=result.end_date;
             alert('rak');
             endDateStr=endDate.split("/");
             var cdate = new Date(endDateStr[2],parseInt(endDateStr[1],10)-1, endDateStr[0]); */
            var cdate = new Date();
            var str1 = $("#event_start_date").val();
            var str2 = $("#event_end_date").val();
            var str3 = $("#event_start_time").val();
            var str4 = $("#event_end_time").val();
            str1 = str1.split("/");
            str2 = str2.split("/");
            str3 = str3.split(":");
            str4 = str4.split(":");
            last_minute = String(parseInt(str4[1]) - 5) // this variable is used for less 5 minutes from current time

            var date1 = new Date(str1[2], parseInt(str1[1], 10) - 1, str1[0], str3[0], str3[1]);
            var date2 = new Date(str2[2], parseInt(str2[1], 10) - 1, str2[0], str4[0], last_minute);

            if (date2 < date1) {
                $().toastmessage('showWarningToast', "End Date can't be greater than Start Date");
                return false;
            }
            else if (cdate < date1 || cdate < date2) {
                $().toastmessage('showWarningToast', "Dates can't be greater than current Date");
                return false;
            }
            else {
                option = $("input[name='option']:checked").val();
                str_paginate_table = '<table cellpadding="0" cellspacing="0" border="0" class="display" id="table_paginate" style="text-align:center;">\
								<thead>\
								<tr>\
									<th></th>\
									<th>Received Time</th>\
									<th>Event Type</th>\
									<th>Event Name</th>\
									<th>Device Type</th>\
									<th>Host Alias</th>\
									<th>IP Address</th>\
									<th>Manage Object ID</th>\
									<th>Manage Object Name</th>\
									<th>Component ID</th>\
									<th>Description</th>\
								</tr>\
							</thead></table>';
                url = "trap_filter_function.py?" + "&option=" + option + "&" + $(this).serialize() + "&serevity1=" + serevity_value[1] + "&serevity2=" + serevity_value[2] + "&serevity3=" + serevity_value[3] + "&serevity4=" + serevity_value[4] + "&serevity5=" + serevity_value[5] + "&searchFlag=" + searchFlag + "&countTimes=" + countTimes + "&last_execution_time=" + "";
                $('#div_table_paginate').html(str_paginate_table) + "&start_date=" + str1 + "&end_date=" + str2 + "&start_time=" + str3 + "&end_time=" + str4;
                oTable = $('#table_paginate').dataTable({
                    "bJQueryUI": true,
                    "sPaginationType": "full_numbers",
                    "bProcessing": true,
                    "bServerSide": true,
                    "sAjaxSource": url,
                    "bRetrieve": true,
                    "aaSorting": [
                        [1, 'desc']
                    ],
                    "aoColumns": [
                        { "sWidth": "2%"},
                        { "sWidth": "11%" },
                        { "sWidth": "8%" },
                        { "sWidth": "8%" },
                        { "sWidth": "8%" },
                        { "sWidth": "12%" },
                        { "sWidth": "8%" },
                        { "sWidth": "8%" },
                        { "sWidth": "8%" },
                        { "sWidth": "8%" },
                        { "sWidth": "25%" }
                    ]
                });
                /*$('#table_paginate').dataTable().fnAddData([["<label style='display:none;'>4</label><img src='images/yel.png' alt='Major' title='Major' class='imgbutton' style='width:12px' onclick='alarmDetail('728800')'/>", '29-Jun-2012 07:20:39 PM', 'DEVICE_UNREACHABLE', 'unmpSystemTrap', 'AP25', '172.22.0.156', '172.22.0.156', '601', 'device', '701', 'No response received from device before timeout', 4, 728800]]);

                 $('#table_paginate').show();*/
                return false;
            }
//		    }
//		}
//	});
        }

    });
}
function updateDatatable(last_execution_time) {
    if (eventRecursion != null) {
        clearTimeout(eventRecursion);
    }
    var time_interval_value = 1 // default value 1 minute
    var agent_Id = $("#agentId").val()
    var option = $("input[name='option']:checked").val();
    var agentId = $("#agentId").val();
//		var eventId=$("#eventId").val();
    var eventType = $("#eventType").val();
    var M_obj = $("#M_obj").val();
    var M_name = $("#M_name").val();
    var camponent_id = $("#camponent_id").val();
    var event_start_date = $("#event_start_date").val();
    var event_start_time = $("#event_start_time").val();
    var event_end_date = $("#event_end_date").val();
    var event_end_time = $("#event_end_time").val();
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "post",
        url: "trap_filter_function.py?option=" + option + "&serevity1=" + serevity_value[1] + "&serevity2=" + serevity_value[2] + "&serevity3=" + serevity_value[3] + "&serevity4=" + serevity_value[4] + "&serevity5=" + serevity_value[5] + "&agentId=" + agentId + "&eventType=" + eventType + "&M_obj=" + M_obj + "&M_name=" + M_name + "&camponent_id=" + camponent_id + "&last_execution_time=" + last_execution_time + "&time_interval_value=" + time_interval_value + "&event_start_date=" + event_start_date + "&event_start_time=" + event_start_time + "&event_end_date=" + event_end_date + "&event_end_time=" + event_end_time + "&searchFlag=" + searchFlag + "&countTimes=" + countTimes,
        cache: false,
        success: function (result) {
            try {
                result = eval('(' + result + ')');
            }
            catch (err) {
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
                if (result.data_table != "") {

                    $('#trap_detail').dataTable().fnAddData(result.data_table);
                }
                last_execution_time = result.last_execution_time;
            }
        },
        error: function (req, status, err) {
        }
    });
    spinStop($spinLoading, $spinMainLoading);
    eventRecursion = setTimeout(function () {
        updateDatatable(last_execution_time);
    }, 60000);

}

function btnClickEvent() {
    $("#submit_html").click(function () {
        searchFlag = 1;
        countTimes = 0;
        last_execution_time = ""
    });
}


function formValidation() {
    $("#alarm_info_form").validate({
        rules: {
            agent_id: {
                ipv4Address: true
            },
            event_id: {
                number: true,
                min: 1
            },
            M_obj: {
                number: true,
                min: 1
            },
            camponent_id: {
                number: true,
                min: 1
            },
            event_start_date: {
                required: true
            },
            event_start_time: {
                required: true
            },
            event_end_date: {
                required: true
            },
            event_end_time: {
                required: true
            }
        },
        messages: {
            agent_id: "Please enter valid IP.",
            event_id: { number: " It must be a number",
                min: " It must be > 0 and <= 100000"
            },
            M_obj: { number: " It must be a number",
                min: " It must be > 0 "
            },
            camponent_id: { number: " It must be a number",
                min: " It must be > 0 "
            },
            event_start_date: {
                required: "Start Date is a required field"
            },
            event_start_time: {
                required: "Start Time is a required field"
            },
            event_end_date: {
                required: "End Date is a required field"
            },
            event_end_time: {
                required: "End Time is a required field"
            }
        }
    });
}


// Excel report creating function .
function trapExcelReportGeneration() {
    trapReportCreating('excelReport');
}

// CSV report creating function .
function trapCSVReportGeneration() {
    trapReportCreating('csvReport');
}

// commmon report creating function.
function trapReportCreating(reportType) {

    var start_date = $("#event_start_date").val();
    var end_date = $("#event_end_date").val();
    var option = $("input[name='option']:checked").val();
    var agentId = $("#agentId").val();
    var eventType = $("#eventType").val();
    var M_obj = $("#M_obj").val();
    var M_name = $("#M_name").val();
    var camponent_id = $("#camponent_id").val();
    spinStart($spinLoading, $spinMainLoading);
    var cdate = new Date();
    var str1 = $("#event_start_date").val();
    var str2 = $("#event_end_date").val();
    var str3 = $("#event_start_time").val();
    var str4 = $("#event_end_time").val();

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
        $.ajax({
            type: "post",
            url: "trap_report_creating.py?option=" + option + "&serevity1=" + serevity_value[1] + "&serevity2=" + serevity_value[2] + "&serevity3=" + serevity_value[3] + "&serevity4=" + serevity_value[4] + "&serevity5=" + serevity_value[5] + "&agentId=" + agentId + "&eventType=" + eventType + "&M_obj=" + M_obj + "&M_name=" + M_name + "&camponent_id=" + camponent_id + "&report_type=" + reportType + "&start_date=" + start_date + "&end_date=" + end_date + "&start_time=" + $("#event_start_time").val() + "&end_time=" + $("#event_end_time").val(),
            cache: false,
            success: function (result) {
                if (result.success == 1 || result.success == "1") {
                    $().toastmessage('showWarningToast', result.error_msg);
                }
                else {
                    $().toastmessage('showSuccessToast', 'Report Generated Successfully');
                    window.location = "download/" + result.file_name;
                    setTimeout("$('#alarm_info_form').submit()", 1250);
                }
            },
            error: function (req, status, err) {
            }
        });
    }
    spinStop($spinLoading, $spinMainLoading);
}

