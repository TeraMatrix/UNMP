var option = 3;
//var starting_pag="alarm_option"

var last_execution_time = 0;
var change_img_dict = {'Normal': 'images/gr.png', 'Minor': 'images/yel.png', 'Major': 'images/or.png', 'Critical': 'images/red.png'};
var main_img_dict = {'Normal': 'images/gr.png', 'Minor': 'images/yel.png', 'Major': 'images/or.png', 'Critical': 'images/red.png'};
var serevity_id = {'Informational': '#serevity1', 'Normal': '#serevity2', 'Minor': '#serevity3', 'Major': '#serevity4', 'Critical': '#serevity5'};
var image_div_id = {1: '#informational_div', 2: '#normal_div', 3: '#minor_div', 4: '#major_div', 5: '#critical_div'};
var serevity_value = ['None', 'None', 'None', 'None', 4, 5];
// ip validataion function
var $spinLoading = null;
var $spinMainLoading = null;
$(document).ready(function () {
    $('#event_start_date, #event_start_time, #event_end_date,  #event_end_time').calendricalDateTimeRange({
        isoTime: true
    });
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
        $("input[id='option3']").attr("checked", true);
    }
    $("#alarm_info_form").submit();
    $("input[id='btn_filter']").toggle(function () {
        $("#alarm_info_form").show();
        $(this).val("Hide Search");
    }, function () {
        $("#alarm_info_form").hide();
        $(this).val("Advanced Search");
    });
    $("input[id='btn_hide']").click(function () {
        $("input[id='btn_filter']").click();
    });
});


function alarmDetail(trap_id) {
    $.facebox({ ajax: "trap_detail_information.py?trap_id=" + trap_id + "&option=" + option });
}


function trapFilterFunction() {
    agent_Id = $("#agentId").val()
    $("#alarm_info_form").submit(function () {
        if ($(this).valid()) {
            option = $("input[name='option']:checked").val();
            spinStart($spinLoading, $spinMainLoading);
            $.ajax({
                type: "post",
                url: "trap_filter_function.py?" + $(this).serialize() + "&option=" + option + "&serevity1=" + serevity_value[1] + "&serevity2=" + serevity_value[2] + "&serevity3=" + serevity_value[3] + "&serevity4=" + serevity_value[4] + "&serevity5=" + serevity_value[5],
                cache: false,
                success: function (result) {
                    try {
                        result = eval("(" + result + ")");
                    } catch (err) {
                        $().toastmessage('showErrorToast', "Some unknown error occur,so please contact your Administrator");
                        spinStop($spinLoading, $spinMainLoading);
                        return;
                    }
                    if (result.success == 1 || result.success == '1') {
                        $().toastmessage('showErrorToast', 'Some system error occured, so please contact your Administrator');
                        spinStop($spinLoading, $spinMainLoading);
                        return;
                    }
                    else if (result.success == 2 || result.success == '2') {
                        $().toastmessage('showErrorToast', 'Some database error occured,so please contact your Administrator');
                        spinStop($spinLoading, $spinMainLoading);
                        return;
                    }
                    else {
                        $('#trap_detail').dataTable({
                            "bJQueryUI": true,
                            "bDestroy": true,
                            "sPaginationType": "full_numbers",
                            "aaSorting": [
                                [ 1, "desc" ]
                            ],
                            "aaData": result.data_table,
                            "aoColumns": [
                                { "sTitle": " ", "sClass": "center", "sWidth": "1%" },
                                { "sTitle": "Receive Date", "sClass": "center", "sWidth": "12%"},
                                { "sTitle": "Receive Time", "sClass": "center", "sWidth": "12%"},
                                { "sTitle": "Device Type", "sClass": "center", "sWidth": "9%" },
                                { "sTitle": "Host Name", "sClass": "center", "sWidth": "12%" },
                                { "sTitle": "Event Name", "sClass": "center", "sWidth": "12%" },
                                { "sTitle": "Agent Id", "sClass": "center", "sWidth": "12%" },
                                { "sTitle": "Event Id", "sClass": "center", "sWidth": "12%" },
                                { "sTitle": "Event Type", "sClass": "center", "sWidth": "12%",
                                    "fnRender": function (obj) {
                                        var sReturn = obj.aData[ obj.iDataColumn ];
                                        if (sReturn == "A") {
                                            sReturn = "<b>A</b>";
                                        }
                                        return sReturn;
                                    }

                                }

                            ]
                        });
                        $("#submit_html").show();
                        spinStop($spinLoading, $spinMainLoading);
                        if (!last_execution_time) {
                            last_execution_time = result.last_execution_time;
                            updateDatatable(last_execution_time);
                        }
                    }
                },
                error: function (req, status, err) {
                }
            });
        }
        return false;
    });
}


function updateDatatable(last_execution_time) {
    var time_interval_value = 1 // default value 1 minute
    var agent_Id = $("#agentId").val()
    var option = $("input[name='option']:checked").val();
    var agentId = $("#agentId").val();
    var eventId = $("#eventId").val();
    var eventType = $("#eventType").val();
    var M_obj = $("#M_obj").val();
    var M_name = $("#M_name").val();
    var camponent_id = $("#camponent_id").val();
    var event_start_date = $("#event_start_date").val();
    var event_start_time = $("#event_start_time").val();
    var event_end_date = $("#event_end_date").val();
    var event_end_time = $("#event_end_time").val();
    $.ajax({
        type: "post",
        url: "trap_filter_function.py?option=" + option + "&serevity1=" + serevity_value[1] + "&serevity2=" + serevity_value[2] + "&serevity3=" + serevity_value[3] + "&serevity4=" + serevity_value[4] + "&serevity5=" + serevity_value[5] + "&agentId=" + agentId + "&eventId=" + eventId + "&eventType=" + eventType + "&M_obj=" + M_obj + "&M_name=" + M_name + "&camponent_id=" + camponent_id + "&last_execution_time=" + last_execution_time + "&time_interval_value=" + time_interval_value + "&event_start_date=" + event_start_date + "&event_start_time=" + event_start_time + "&event_end_date=" + event_end_date + "&event_end_time=" + event_end_time,
        cache: false,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                $().toastmessage('showErrorToast', "Some unknown error occur,so please contact your Administrator");
                return;
            }
            if (result.success == 1 || result.success == '1') {
                $().toastmessage('showErrorToast', 'Some system error occured, so please contact your Administrator');
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                $().toastmessage('showErrorToast', 'Some database error occured,so please contact your Administrator');
                return;
            }
            else {
                if (result.data_table != "") {

                    $('#trap_detail').dataTable().fnAddData(result.data_table);
                    /*var resArry = result.data_table;
                     for(var j=0;j<resArry.length;j++)
                     {
                     $('#trap_detail').dataTable().fnAddData(resArry[j]);
                     }*/
                }
                last_execution_time = result.last_execution_time;
            }
        },
        error: function (req, status, err) {
        }
    });
    setTimeout(function () {
        updateDatatable(last_execution_time);
    }, 60000);
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
            }
        }
    });
}


