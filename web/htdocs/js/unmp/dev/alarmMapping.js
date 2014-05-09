var $spinLoading = null;
var $spinMainLoading = null;
var deleteId = null;
$(function () {
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
    dataTable();


    addAlarmForm();
    $.validator.addMethod('positiveNumber', function (value, element) {
        return Number(value) > -1;
    }, ' Enter a positive number');


//	$("#page_tip").colorbox(
//	{
//	href:"page_tip_alarm_mapping.py",
//	title: "Page Tip",
//	opacity: 0.4,
//	maxWidth: "80%",
//	width:"450px",
//	height:"350px",
//	onComplte:function(){}
//	});
});


function addEditForm(uniqe_id, option) {
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "add_edit_form_show.py?uniqe_id=" + uniqe_id + "&option=" + option,
        data: $(this).serialize(), // $(this).text?
        cache: false,
        success: function (result) {
            //alert(result);
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            if (result.success == 1 || result.success == '1') {
                $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else if (result.success == 0 || result.success == "0") {

                spinStop($spinLoading, $spinMainLoading);
                $("#demo_id").hide();
                $("#alarm_editable_div").html(result.output.table);
                $("#header").hide();
                $("#alarm_editable_div").show();
                if (option == "ADD") {
                    formSubmit(uniqe_id, option);
                    $("#alarm_editable_div").find("select[id='device_type']").change(function () {
                        get_trap_types();
                    });
                    $("#device_type").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Device Type ', header: "Available Device Type", minWidth: 290});
                    $("#trap_event_type").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Event Type', header: "Available Event Type", minWidth: 290}).multiselectfilter();
                    $("#trap_severity").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Event Severity', header: "Available Event Severity", minWidth: 290});
                    $("#trap_event_clear_type").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Clear Event Type ', header: "Available Clear Event Type", minWidth: 290}).multiselectfilter();
                    $("#clear_severity").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Clear Event Severity', header: "Available Clear Event Severity", minWidth: 290});
                    $("#trap_event_type").multiselect("disable");
                    $("#trap_severity").multiselect("disable");
                    $("#trap_event_clear_type").multiselect("disable");
                    $("#clear_severity").multiselect("disable");
                    $("#device_type").bind("multiselectclick", function (event, ui) {
                        $("#trap_event_type").multiselect("enable");
                        $("#trap_severity").multiselect("enable");
                        $("#trap_event_clear_type").multiselect("enable");
                        $("#clear_severity").multiselect("enable");
                    });
                }
                else {
                    editFormSubmit(uniqe_id, option);
                    $("#device_type").multiselect({selectedList: 1, multiple: false, minWidth: 290});
                    $("#device_type").multiselect("disable");
                    $("#trap_event_type").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Event Type', header: "Available Event Type", minWidth: 290}).multiselectfilter();
                    $("#trap_severity").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Event Severity', header: "Available Event Severity", minWidth: 290});
                    $("#trap_event_clear_type").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Clear Event Type ', header: "Available Clear Event Type", minWidth: 290}).multiselectfilter();
                    $("#clear_severity").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select Clear Event Severity', header: "Available Clear Event Severity", minWidth: 290});

                }
                formCancel();
            }
        },
        error: function (req, status, err) {
        }
    });
    return false; //always remamber this
}

function get_trap_types() {
    device = $("#alarm_editable_div").find("select[id='device_type']").val();
    $.ajax({
        type: "get",
        url: "get_trap_lists.py?device_type=" + device,
        cache: false,
        success: function (result) {
            //alert(result);
            try {
                result = eval("(" + result + ")");
            }
            catch (err) {
                $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                return;
            }
            if (result.success == 1 || result.success == '1') {
                $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                return;
            }
            else if (result.success == 0 || result.success == "0") {
                //$("#alarm_editable_div").find("select[id='trap_event_type']").html(result.output);
                //$("#alarm_editable_div").find("select[id='trap_event_clear_type']").html(result.output);
                $("#trap_event_type").html(result.output);
                $("#trap_event_clear_type").html(result.output);
                $("#trap_event_type").multiselect("refresh");
                $("#trap_event_clear_type").multiselect("refresh");

            }
        }
    });
    return false;
}


function addAlarmForm() {
    $("#add_alarm").click(function () {
        addEditForm("", "ADD");


    });

}

function checkDeleteAlarm(event_uuid, click_flag) {

    if (click_flag != 'falseclick') {
        //$().toastmessage('showErrorToast', "you can't edit or delete default alarms");
        deleteId = event_uuid;
        $.prompt('Are you sure want to delete this Alarm ?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: deleteAlarm});
    }
}

function deleteAlarm(v, m) {
    //var answer = confirm("Are you sure want to delete this Alarm ?")
    if (v != undefined && v == true && deleteId) {
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "get",
            url: "delete_alarm_id.py?alarm_delete_id=" + deleteId,
            //data:$(this).serialize(), // $(this).text?
            cache: false,
            success: function (result) {
                try {
                    result = eval("(" + result + ")");
                } catch (err) {
                    $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                    spinStop($spinLoading, $spinMainLoading);
                    return;
                }
                if (result.success == 1 || result.success == '1') {
                    $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                    spinStop($spinLoading, $spinMainLoading);
                    return;
                }
                else if (result.success == 2 || result.success == '2') {
                    $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                    spinStop($spinLoading, $spinMainLoading);
                    return;
                }
                else {
                    spinStop($spinLoading, $spinMainLoading);
                    $().toastmessage('showSuccessToast', "Alarm is successfully deleted.");
                    $("#demo_id").show();
                    $("#alarm_editable_div").hide();
                    $("#demo_id").html("<table cellspacing=\"0\" cellpadding=\"0\" border=\"0\" id=\"example\" class=\"display\"></table>");
                    dataTable();
                }
            },
            error: function (req, status, err) {
            }
        });
        return false; //always remamber this	
    }
    else {
        return false;
    }
}


function editAlarm(uniqe_id, click_flag) {
    if (click_flag != 'falseclick') {
        addEditForm(uniqe_id, "Edit");
    }
}


function formCancel() {
    $("#cancel_button").click(function () {
        $("#header").show();
        $("#alarm_editable_div").hide();
        $("#demo_id").show();
    });
}


function formSubmit(uniqe_id, option) {
    maskingValidation("#alarm_form_detail");
    $("#alarm_form_detail").submit(function () {
        if ($(this).valid()) {
            spinStart($spinLoading, $spinMainLoading);
            $.ajax({
                type: "get",
                url: "add_form_entry.py",
                data: $(this).serialize(), // $(this).text?
                cache: false,
                success: function (result) {
                    try {
                        result = eval("(" + result + ")");
                    }
                    catch (error) {
                        $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                        spinStop($spinLoading, $spinMainLoading);
                        return;
                    }
                    if (result.success == "11" || result.success == 11) {
                        $().toastmessage('showWarningToast', "Event Type is Already Exist");
                        spinStop($spinLoading, $spinMainLoading);
                    }
                    else if (result.success == "12" || result.success == 12) {
                        $().toastmessage('showWarningToast', "Event Id is Already Exist");
                        spinStop($spinLoading, $spinMainLoading);
                    }
                    else if (result.success == "13" || result.success == 13) {
                        $().toastmessage('showWarningToast', "Event Type and Event Id is Already Exist");
                        spinStop($spinLoading, $spinMainLoading);
                    }
                    else if (result.success == "1" || result.success == 1) {
                        $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                        spinStop($spinLoading, $spinMainLoading);
                    }
                    else if (result.success == 2 || result.success == '2') {
                        $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                        spinStop($spinLoading, $spinMainLoading);
                        return;
                    }
                    else {
                        spinStop($spinLoading, $spinMainLoading);
                        $().toastmessage('showSuccessToast', "Alarm is successfully added.");
                        $("#demo_id").show();
                        $("#alarm_editable_div").hide();
                        $("#demo_id").html("<table cellspacing=\"0\" cellpadding=\"0\" border=\"0\" id=\"example\" class=\"display\"></table>");
                        dataTable();
                    }

                },
                error: function (req, status, err) {
                }
            });
        }

        return false; //always remamber this                   

    });

}


// editButtonClick()

function editFormSubmit(uniqe_id, option) {
    //alert(event_type,event_id)
    maskingValidation("#alarm_form_detail");
    $("select[id='prityid'] option[value='" + $("input[id='priority_id']").val() + "']").attr("selected", true);

    $("#alarm_form_detail").submit(function () {
        if ($(this).valid()) {
            spinStart($spinLoading, $spinMainLoading);
            $.ajax({
                type: "get",
                url: "edit_form_entry.py?uniqe_id=" + uniqe_id,
                data: $(this).serialize(), // $(this).text?
                cache: false,
                success: function (result) {
                    try {
                        result = eval("(" + result + ")");
                    }
                    catch (error) {
                        $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                        spinStop($spinLoading, $spinMainLoading);
                        return;
                    }
                    if (result.success == "1" || result.success == 1) {
                        $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                        spinStop($spinLoading, $spinMainLoading);
                    }
                    else if (result.success == 2 || result.success == '2') {
                        $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                        spinStop($spinLoading, $spinMainLoading);
                        return;
                    }

                    else {
                        spinStop($spinLoading, $spinMainLoading);
                        $().toastmessage('showSuccessToast', "Alarm is successfully edited.");
                        $("#demo_id").show();
                        $("#alarm_editable_div").hide();
                        $("#demo_id").html("<table cellspacing=\"0\" cellpadding=\"0\" border=\"0\" id=\"example\" class=\"display\"></table>");
                        dataTable();
                        formCancel();
                    }
                },
                error: function (req, status, err) {
                }
            });
        }
        return false; //always remamber this                   
    });

}


function maskingValidation(formid) {

    $(formid).validate({
        rules: {
            'trap_event_type': {
                required: true
            },
            'trap_severity': {
                required: true
            },
            'trap_event_clear_type': {
                required: true,
                notEqualTo: "#trap_event_type"
            },
            'clear_severity': {
                required: true
            },
            'device_type': "required"
        },
        messages: {
            'trap_event_type': {
                required: " *Required field "
            },
            'trap_severity': {
                required: " *Required field "
            },
            'trap_event_clear_type': {
                required: " *Required field ",
                notEqualTo: "Alarm Type and Alarm Clear Type can't be same"
            },
            'clear_severity': {
                required: " *Required field "
            },
            'device_type': {
                required: " *Required field "
            }

        }
    });
}

function dataTable() {
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "alarm_datail_function.py",
        cache: false,
        success: function (result) {
            $("#header").show();
            try {
                result = eval("(" + result + ")");
            }
            catch (err) {
                $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                spinStop($spinLoading, $spinMainLoading);
                return;
            }
            else {
                try {
                    tableData = result.output;
                }
                catch (err) {
                    $().toastmessage('showErrorToast', 'UNMP server has encounterd an error. Please contact support team');
                    spinStop($spinLoading, $spinMainLoading);
                    return;
                }
                $('#example').dataTable({
                    "bJQueryUI": true,
                    "bDestroy": true,
                    "sPaginationType": "full_numbers",
                    "aaData": tableData,
                    "aoColumns": [
                        { "bSearchable": false, "bVisible": false, "aTargets": [ 0 ] },
                        { "sTitle": " Alarm Type", "sWidth": "18%"},
                        { "sTitle": " Alarm Severity", "sClass": "center", "sWidth": "10%"},
                        { "sTitle": " Alarm Clear Type", "sClass": "center", "sWidth": "18%" },
                        { "sTitle": " Clear Severity", "sClass": "center", "sWidth": "14%" },
                        { "sTitle": " Device Type ", "sClass": "center", "sWidth": "10%" },
                        { "sTitle": " Is Alarm ", "sClass": "center", "sWidth": "10%" },
                        { "sTitle": " Actions ", "sClass": "center", "sWidth": "10%", "bSortable": false,

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
                spinStop($spinLoading, $spinMainLoading);
            }

        },
        error: function (req, status, err) {
        }
    });
}


