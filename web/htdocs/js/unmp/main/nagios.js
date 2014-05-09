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
var oTable = null;
var aSelected = [];

$(document).ready(function () {

    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
    host_name = $("#host_name_nagios").val();
    if (host_name != undefined)
        editHost(host_name, 0);
    else {
        hostgroup_name = $("#hostgroup_name_nagios").val();
        if (hostgroup_name != undefined)
            editHostgroupInventory(hostgroup_name);
        else {
            nagios_module = $("#nagios_module").val();
            if (nagios_module == "nagios_hosts")
                main_hosts();
            else if (nagios_module == "nagios_service")
                main_services();
            else if (nagios_module == "nagios_hostgroup")
                main_hostgroups();
            else if (nagios_module == "nagios_host_template")
                main_host_template();
            else if (nagios_module == "nagios_service_template")
                main_service_template();
            else if (nagios_module == "nagios_command")
                main_command();
            else if (nagios_module == "nagios_servicegroup")
                main_servicegroup();
            else if (nagios_module == "nagios_hostdependency")
                main_hostdependency();
            else if (nagios_module == "nagios_servicedependency")
                main_servicedependency();
        }
    }
});

function verifyConfiguration() {

    $.colorbox(  			//page tip
        {
            href: "do_verify_nagios.py",
            title: "Verify Nagios Configuration",
            opacity: 0.4,
            maxWidth: "80%",
            width: "900px",
            height: "600px",
            iframe: true,
            html: true
        });
}


function backupRestore() {

    $.colorbox(
        {
            href: "restore_config_nagios.py",
            title: "Restore Configuration",
            opacity: 0.4,
            maxWidth: "80%",
            width: "800px",
            height: "500px",
            overflow: "hidden",
            onComplete: function () {
                /*oBackupTable = $('#backup_table').dataTable({
                 "bJQueryUI": true,
                 "sPaginationType": "full_numbers",
                 "bProcessing": true,
                 "bServerSide": true,
                 "bDestroy" : true,
                 //"sAjaxSource": "get_host_data_nagios.py",
                 "aaSorting": [[0,'desc']]
                 });*/
                $("#close_restore_config").click(function () {
                    $.colorbox.close()
                });

                $("#restore_config_button").click(function () {
                    if ($("input:radio[name=option]:checked").val() == undefined)
                        $().toastmessage('showErrorToast', "Please select the backup file to be restored.");
                    else {
                        $.ajax({
                            type: "post",
                            url: "restore_config_nagios_selected.py?file_name=" + $("input:radio[name=option]:checked").val(),
                            cache: false,
                            success: function (result) {
                                result = eval("(" + result + ")");
                                if (result.success == 0) {
                                    $().toastmessage('showSuccessToast', "Nagios configuration restored successfully.");
                                    $.colorbox.close()
                                }
                                else {
                                    $().toastmessage('showErrorToast', "Nagios configuration couldn't be restored.");
                                }
                            }
                        });
                    }

                });
            }
        });
}


function nagiosSettings() {
    //spinStart($spinLoading,$spinMainLoading);
    $.colorbox(  			//page tip
        {
            href: "settings_nagios.py",
            title: "Nagios Settings",
            opacity: 0.4,
            maxWidth: "80%",
            width: "500px",
            height: "300px",
            //iframe:true,
            onComplete: function () {
                $("#nagios_force_sync_anchor").click(function () {
                    $.ajax({
                        type: "post",
                        url: "nagios_force_sync.py",
                        cache: false,
                        success: function (result) {
                            result = eval("(" + result + ")");
                            if (result.success == 0) {
                                $.ajax({
                                    type: "post",
                                    url: "do_action_nagios.py?action=start",
                                    cache: false,
                                    success: function (result) {
                                        result = eval("(" + result + ")");
                                        if (result.success == 0) {
                                            $("#nagios_label").html("Running");
                                            $("#nagios_on").show();
                                            $("#nagios_off").hide();
                                            $("#nagios_restart").show();
                                            $("#nagios_stop").show();
                                            $("#nagios_start").hide();
                                            $("#sync_nagios").hide();

                                        }
                                        else if (result.success == 1) {
                                            $("#nagios_label").html("Please verify the configuration, Nagios couldn't be started.");
                                            $("#sync_nagios").show();

                                        }
                                    }
                                });

                            }
                            else if (result.success == 1) {
                                if (result.result != undefined)
                                    $("#nagios_label").html(result.result);
                                else
                                    $("#nagios_label").html(result.exception);
                            }
                        }
                    });


                });

                //buttons
                $(".start").click(function () {
                    $.ajax({
                        type: "post",
                        url: "do_action_nagios.py?action=start",
                        cache: false,
                        success: function (result) {
                            result = eval("(" + result + ")");
                            if (result.success == 0) {
                                $("#nagios_label").html("Running");
                                $("#nagios_on").show();
                                $("#nagios_off").hide();
                                $("#nagios_restart").show();
                                $("#nagios_stop").show();
                                $("#nagios_start").hide();
                                $("#sync_nagios").hide();

                            }
                            else if (result.success == 1) {
                                $("#nagios_label").html("Please verify the configuration, Nagios couldn't be started.");
                                $("#sync_nagios").show();

                            }
                        }
                    });

                });

                $(".stop").click(function () {
                    $.ajax({
                        type: "post",
                        url: "do_action_nagios.py?action=stop",
                        cache: false,
                        success: function (result) {
                            result = eval("(" + result + ")");
                            if (result.success == 1) {
                                $("#nagios_label").html("Stopped");
                                $("#nagios_off").show();
                                $("#nagios_on").hide();
                                $("#nagios_start").show();
                                $("#nagios_stop").hide();
                                $("#nagios_restart").hide();
                            }
                            else if (result.success == 0) {
                                $("#nagios_label").html("Nagios couldn't be stopped.");

                            }
                        }
                    });

                });
                $(".restart").click(function () {
                    $.ajax({
                        type: "post",
                        url: "do_action_nagios.py?action=restart",
                        cache: false,
                        success: function (result) {
                            result = eval("(" + result + ")");
                            if (result.success == 0) {
                                $("#nagios_label").html("Running");
                                $("#nagios_on").show();
                                $("#nagios_off").hide();
                                $("#nagios_restart").show();
                                $("#nagios_stop").show();
                                $("#nagios_start").hide();

                            }
                            else if (result.success == 1) {
                                $("#nagios_label").html("Please verify the configuration, Nagios couldn't be started.");
                                $("#nagios_off").show();
                                $("#nagios_on").hide();
                                $("#nagios_start").show();
                                $("#nagios_stop").hide();
                                $("#nagios_restart").hide();
                                $("#sync_nagios").show();

                            }
                        }
                    });
                });
            }
        });

}

function moveElementsUpDown(index, direction) {
    // code for appending li
    jQuery.fn.insertAt = function (index, element) {
        var lastIndex = this.children().size()
        if (index < 0) {
            index = Math.max(0, lastIndex + 1 + index)
        }
        this.append(element)
        if (index < lastIndex) {
            this.children().eq(index).before(this.children().last())
        }
        return this;
    }

    li_obj = $(".selected", "#multiSelectList", "#more_options_columns").find(".clicked");
    if (li_obj.hasClass("clicked")) {
        text_selected = li_obj.text();
        html_selected = li_obj.html();
        all_objects = $("#hd").val().split(",");
        max_length = all_objects.length;
        index_selected = all_objects.indexOf(text_selected);
        if (direction == "top")
            change_index = 0;
        else if (direction == "up")
            if (index_selected == 0)
                change_index = index_selected;
            else
                change_index = index_selected - 1;
        if (direction == "down")
            if (index_selected == max_length)
                change_index = index_selected;
            else
                change_index = index_selected + 1;
        else if (direction == "bottom")
            change_index = max_length;

        //alert(all_objects+" change_index "+change_index+" index_selected " + index_selected);
        parent_obj = li_obj.parent();
        li_obj.remove();
        parent_obj.insertAt(change_index, "<li class='clicked'>" + html_selected + "</li>");
        temp_var = all_objects[change_index];
        all_objects[change_index] = all_objects[index_selected];
        all_objects[index_selected] = temp_var;
        $("#hd").val(all_objects.join());
        //alert(all_objects);
        $(".minus").click(function () {
            minusHostParentOption(this);
        })
        click_check();
    }


}


function fill_multiple_values_hostgroup_inventory(result, hostDetails, form_id) {

    try {
////////////////////////// code for single or multi select
        json_var_array = ["check_command", "notifications_enabled", "initial_state", "active_checks_enabled", "passive_checks_enabled",
            "check_freshness", "process_perf_data", "flap_detection_enabled", "event_handler_enabled", "notification_options", "flap_detection_options"];
        corresponding_fields = ["#check_command", "#notifications_enabled", "#initial_state", "#active_checks_enabled", "#passive_checks_enabled",
            "#check_freshness", "#process_perf_data", "#flap_detection_enabled", "#event_handler_enabled", "#notification_options", "#flap_detection_options"];
        for (json_var = 0; json_var < json_var_array.length; json_var++) {
            var_name = json_var_array[json_var]; // use
            if (result[var_name] != undefined)// && hostDetails[var_name]!=undefined)
            {
                host_templates = result[var_name]; // list of host templates
                cur_selected_array = {};
                currently_selected_host_templates = hostDetails[var_name]; // selected list
                html_string = "";
                if (currently_selected_host_templates) {
                    if (currently_selected_host_templates.indexOf(",") != -1)
                        cur_selected_array = currently_selected_host_templates.split(",");
                }
                for (i = 0; i < host_templates.length; i++) {
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) {
                        for (k = 0; k < cur_selected_array.length; k++) {
                            if (cur_selected_array[k] == host_templates[i][0] || cur_selected_array[k] == host_templates[i][1]) {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    if (flag)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else if (host_templates[i][0] == currently_selected_host_templates || host_templates[i][1] == currently_selected_host_templates)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else
                        html_string += "<option value=" + host_templates[i][0] + ">" + host_templates[i][1] + "</option>";
                }
//				alert(html_string);
                $(corresponding_fields[json_var], form_id).html(html_string);
                $(corresponding_fields[json_var], form_id).multiselect("refresh");
            }
        }
////////////////////////////////////////////////// special case for different names
        json_var_array = ["timeperiod", "timeperiod", "contactgroup"];
        corresponding_names = ["check_period", "notification_period", "contact_groups"];
        corresponding_fields = ["#check_period", "#notification_period", "#contact_groups"];
        for (json_var = 0; json_var < json_var_array.length; json_var++) {
            var_name = json_var_array[json_var];
            if (result[var_name] != undefined)// && hostDetails[var_name]!=undefined)
            {
                host_templates = result[var_name];
                currently_selected_host_templates = hostDetails[corresponding_names[json_var]];
                cur_selected_array = {};
                html_string = "";
                if (currently_selected_host_templates) {
                    if (currently_selected_host_templates.indexOf(",") != -1)
                        cur_selected_array = currently_selected_host_templates.split(",");
                }
                for (i = 0; i < host_templates.length; i++) {
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) {
                        for (k = 0; k < cur_selected_array.length; k++) {
                            if (cur_selected_array[k] == host_templates[i][0] || cur_selected_array[k] == host_templates[i][1]) {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    if (flag)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else if (host_templates[i][0] == currently_selected_host_templates || host_templates[i][1] == currently_selected_host_templates)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else
                        html_string += "<option value=" + host_templates[i][0] + ">" + host_templates[i][1] + "</option>";
                }
                $(corresponding_fields[json_var], form_id).html(html_string);
                $(corresponding_fields[json_var], form_id).multiselect("refresh");
            }
        }
    }
    catch (err) {
        //alert(err);
    }
}

function editHostgroupInventory(hostgroup_name) {
    spinStart($spinLoading, $spinMainLoading);
    $("#check_command").multiselect({selectedList: 1, multiple: false, minWidth: 230});
    //$("#members").multiselect({selectedList: 1,multiple:true,minWidth:230});
    $("#check_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select check period', header: "Available check periods", minWidth: 230});
    $("#notification_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select notification period', header: "Available notification periods", minWidth: 230});
    $("#notification_options").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select notification options', minWidth: 230});
    $("#contact_groups").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select contact groups', minWidth: 230});
    $("#notifications_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select notifications enabled', minWidth: 230});
    $("#initial_state").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select initial state', minWidth: 230});
    $("#active_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select active checks enabled', minWidth: 230});
    $("#passive_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select passive checks enabled', minWidth: 230});
    $("#check_freshness").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select check freshness', minWidth: 230});
    $("#process_perf_data").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select process performance enabled', minWidth: 230});
    $("#flap_detection_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select flap detection enabled', minWidth: 230});
    $("#flap_detection_options").multiselect({selectedList: 2, multiple: true, noneSelectedText: 'Select flap detection options', minWidth: 230});
    $("#event_handler_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select event handler enabled', minWidth: 230});
    $.ajax({
        type: "get",
        url: "edit_nagios_hostgroup_inventory.py?hostgroup_name=" + hostgroup_name,
        cache: false,
        success: function (result) {
            spinStop($spinLoading, $spinMainLoading);
            result = eval("(" + result + ")");
            if (result.success == 0) {
                var form_id = "#edit_nagios_hostgroup_inventory_form";
                hostDetails = result.data;

                $("#hostgroup_name", form_id).val(hostgroup_name);
                $("#contacts", form_id).val(hostDetails["contacts"]);
                $("#notes", form_id).val(hostDetails["notes"]);
                $("#notes_url", form_id).val(hostDetails["notes_url"]);
                $("#action_url", form_id).val(hostDetails["action_url"]);
                $("#max_check_attempts", form_id).val(hostDetails["max_check_attempts"]);
                $("#check_interval", form_id).val(hostDetails["check_interval"]);
                $("#retry_interval", form_id).val(hostDetails["retry_interval"]);
                $("#notifications_enabled", form_id).val(hostDetails["notifications_enabled"]);
                $("#notification_interval", form_id).val(hostDetails["notification_interval"]);
                $("#first_notification_delay", form_id).val(hostDetails["first_notification_delay"]);
                $("#active_checks_enabled", form_id).val(hostDetails["active_checks_enabled"]);
                $("#passive_checks_enabled", form_id).val(hostDetails["passive_checks_enabled"]);
                $("#event_handler", form_id).val(hostDetails["event_handler"]);
                $("#event_handler_enabled", form_id).val(hostDetails["event_handler_enabled"]);
                $("#check_freshness", form_id).val(hostDetails["check_freshness"]);
                $("#freshness_threshold", form_id).val(hostDetails["freshness_threshold"]);
                $("#process_perf_data", form_id).val(hostDetails["process_perf_data"]);
                $("#flap_detection_enabled", form_id).val(hostDetails["flap_detection_enabled"]);
                $("#high_flap_threshold", form_id).val(hostDetails["high_flap_threshold"]);
                $("#initial_state", form_id).val(hostDetails["initial_state"]);
                $("#low_flap_threshold", form_id).val(hostDetails["low_flap_threshold"]);
                fill_multiple_values_hostgroup_inventory(result.options, hostDetails, form_id);
                //$("#more_options_columns").html(result.html);
                //multiSelectColumns();
                $("#close_edit_hostgroup_inventory").click(function () {
                    //host_name=$("#host_name_nagios").val();
                    //if(host_name!=undefined)
                    history.go(-1);

                });
                $("#save_edit_hostgroup_inventory").click(function () {
                    var form = $("#edit_nagios_hostgroup_inventory_form");
                    //if(form.valid())
                    //{
                    var method = form.attr("method");
                    var action = "save_nagios_hostgroup_inventory.py";//form.attr("action");
                    var data = form.serialize() + "&notification_options=" + $("#notification_options").val() + "&flap_detection_options=" + $("#flap_detection_options").val()
                        + "&contact_groups=" + $("#contact_groups").val() + "&hostgroup_name=" + $("#hostgroup_name").val();
                    $.ajax({
                        type: method,
                        url: action,
                        data: data,
                        cache: false,
                        success: function (result) {
                            result = eval("(" + result + ")");
                            if (result.success == 0) {
                                $().toastmessage('showSuccessToast', "Hostgroup details saved successfully.");
                                //main_hosts();
                                $("#close_edit_hostgroup_inventory").click();

                            }
                            else if (result.success == 1) {

                                $().toastmessage('showErrorToast', "Some error occurred(" + String(result.exception) + ")");
                            }
                        }
                    });
                    //}
                });


                // javascript


            }
            //{"data": {"use": "generic-host", "check_command": "check-host-alive", "hostgroups": "sample",
            // "alias": "172.22.0.104", "parents": "host3", "host_name": "host4", "address": "172.22.0.104"}, "success": 0}

            else {
                $().toastmessage('showErrorToast', 'Some error occured.');
            }

        }
    });
    $("#page_tip").colorbox(  			//page tip
        {
            href: "view_page_tip_nagios_inventory_hostgroups.py",
            title: "Page Tip",
            opacity: 0.4,
            maxWidth: "80%",
            width: "450px",
            height: "400px"
        });
}
//////////////////// hosts start	
function main_hosts() {

    oTable = $('#host_table_paginate').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "bServerSide": true,
        "bDestroy": true,
        "sAjaxSource": "get_host_data_nagios.py",
        "aaSorting": [
            [0, 'desc']
        ]
    });
    oTable.fnSetColumnVis(0, false, false);

    // save_cancel_buttons();	
    $("#page_tip").colorbox(  			//page tip
        {
            href: "view_page_tip_nagios_host.py",
            title: "Page Tip",
            opacity: 0.4,
            maxWidth: "80%",
            width: "450px",
            height: "400px"
        });

    $("#edit_nagios_host_form").validate({
        rules: {
            alias: {
                required: true//,

            },
            address: {
                required: true//,
            },
            hostgroups: {
                required: true//,
            }
        },
        messages: {
            alias: {
                required: "*"//,
            },

            address: {
                required: "*"//,
            },
            hostgroups: {
                required: "*"//,
            }

        }
    });
}
function save_cancel_buttons() {
    $("#close_edit_host").click(function () {
        host_name = $("#host_name_nagios").val();
        if (host_name != undefined)
            history.go(-1);
        else {
            $("#div_table_paginate").css({"display": "block"});
            $("#edit_nagios_host_form").css({"display": "none"});
        }
    });
    $("#save_edit_host").click(function (e) {
        e.stopImmediatePropagation();
        //e.preventDefault();
        var form = $("#edit_nagios_host_form");
        if (form.valid()) {
            var method = form.attr("method");
            var action = form.attr("action");
            var data = form.serialize() + "&notification_options=" + $("#notification_options").val() + "&flap_detection_options=" + $("#flap_detection_options").val()
                + "&contact_groups=" + $("#contact_groups").val() + "&address=" + $("#address").val() + "&use=" + $("#hd").val() + "&alias=" + $("#alias").val() + "&contacts=" + $("#contacts").val();
            $.ajax({
                type: method,
                url: action,
                data: data,
                cache: false,
                success: function (result) {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        $().toastmessage('showSuccessToast', "Host details saved successfully.");
                        //main_hosts();
                        $("#close_edit_host").click();
                        host_name = $("#host_name_nagios").val();
                        if (host_name == undefined) {
                            oTable.fnDraw();
                        }

                    }
                    else if (result.success == 1) {

                        $().toastmessage('showErrorToast', "Some error occurred(" + String(result.exception) + ")");
                    }
                }
            });
        }
    });

}

function fill_multiple_values_host(result, hostDetails, form_id) {

    try {
////////////////////////// code for single or multi select
        json_var_array = ["check_command", "use", "hostgroups", "notifications_enabled", "initial_state", "active_checks_enabled", "passive_checks_enabled",
            "check_freshness", "process_perf_data", "flap_detection_enabled", "event_handler_enabled", "parents", "notification_options", "flap_detection_options"];
        corresponding_fields = ["#check_command", "#use", "#hostgroups", "#notifications_enabled", "#initial_state", "#active_checks_enabled", "#passive_checks_enabled",
            "#check_freshness", "#process_perf_data", "#flap_detection_enabled", "#event_handler_enabled", "#parents", "#notification_options", "#flap_detection_options"];
        for (json_var = 0; json_var < json_var_array.length; json_var++) {
            var_name = json_var_array[json_var]; // use
            if (result[var_name] != undefined)// && hostDetails[var_name]!=undefined)
            {
                host_templates = result[var_name]; // list of host templates
                cur_selected_array = {};
                currently_selected_host_templates = hostDetails[var_name]; // selected list
                html_string = "";
                if (currently_selected_host_templates) {
                    if (currently_selected_host_templates.indexOf(",") != -1)
                        cur_selected_array = currently_selected_host_templates.split(",");
                }
                for (i = 0; i < host_templates.length; i++) {
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) {
                        for (k = 0; k < cur_selected_array.length; k++) {
                            if (cur_selected_array[k] == host_templates[i][0] || cur_selected_array[k] == host_templates[i][1]) {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    if (flag)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else if (host_templates[i][0] == currently_selected_host_templates || host_templates[i][1] == currently_selected_host_templates)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else
                        html_string += "<option value=" + host_templates[i][0] + ">" + host_templates[i][1] + "</option>";
                }
//				alert(html_string);
                $(corresponding_fields[json_var], form_id).html(html_string);
                $(corresponding_fields[json_var], form_id).multiselect("refresh");
            }
        }
////////////////////////////////////////////////// special case for different names
        json_var_array = ["timeperiod", "timeperiod", "contactgroup", "contacts"];
        corresponding_names = ["check_period", "notification_period", "contact_groups", "contacts"];
        corresponding_fields = ["#check_period", "#notification_period", "#contact_groups", "#contacts"];
        for (json_var = 0; json_var < json_var_array.length; json_var++) {
            var_name = json_var_array[json_var];
            if (result[var_name] != undefined)// && hostDetails[var_name]!=undefined)
            {
                host_templates = result[var_name];
                currently_selected_host_templates = hostDetails[corresponding_names[json_var]];
                cur_selected_array = {};
                html_string = "";
                if (currently_selected_host_templates) {
                    if (currently_selected_host_templates.indexOf(",") != -1)
                        cur_selected_array = currently_selected_host_templates.split(",");
                }
                for (i = 0; i < host_templates.length; i++) {
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) {
                        for (k = 0; k < cur_selected_array.length; k++) {
                            if (cur_selected_array[k] == host_templates[i][0] || cur_selected_array[k] == host_templates[i][1]) {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    if (flag)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else if (host_templates[i][0] == currently_selected_host_templates || host_templates[i][1] == currently_selected_host_templates)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else
                        html_string += "<option value=" + host_templates[i][0] + ">" + host_templates[i][1] + "</option>";
                }
                $(corresponding_fields[json_var], form_id).html(html_string);
                $(corresponding_fields[json_var], form_id).multiselect("refresh");
            }
        }
    }
    catch (err) {
        //alert(err);
    }
}


function editHost(host_name, is_localhost) {
    if (is_localhost == 1) {
        $.prompt("Updation of localhost is restricted.", {prefix: 'jqismooth'});

    }
    else {
        spinStart($spinLoading, $spinMainLoading);

        $("#check_command").multiselect({selectedList: 1, multiple: false, minWidth: 230});
        $("#contacts").multiselect({selectedList: 1, multiple: true, minWidth: 230});
        $("#check_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select check period', header: "Available check periods", minWidth: 230});
        $("#notification_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select notification period', header: "Available notification periods", minWidth: 230});
        //$("#use").multiselect({selectedList: 1,multiple:true,noneSelectedText: 'Select templates',header:"Available templates",minWidth:230});
        //$("#check_command").multiselect({selectedList: 1,multiple:false,noneSelectedText: 'Select check command',header:"Available check commands",minWidth:230});
        $("#hostgroups").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select hostgroups', header: "Available hostgroups", minWidth: 230}).multiselectfilter();
        $("#parents").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select parent', header: "Available parents", minWidth: 230}).multiselectfilter();
        $("#notification_options").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select notification options', minWidth: 230});
        $("#contact_groups").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select contact groups', minWidth: 230});
        $("#notifications_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select notifications enabled', minWidth: 230});
        $("#initial_state").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select initial state', minWidth: 230});
        $("#active_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select active checks enabled', minWidth: 230});
        $("#passive_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select passive checks enabled', minWidth: 230});
        $("#check_freshness").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select check freshness', minWidth: 230});
        $("#process_perf_data").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select process performance enabled', minWidth: 230});
        $("#flap_detection_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select flap detection enabled', minWidth: 230});
        $("#flap_detection_options").multiselect({selectedList: 2, multiple: true, noneSelectedText: 'Select flap detection options', minWidth: 230});
        $("#event_handler_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select event handler enabled', minWidth: 230});
        //$("#div_table_paginate").display("none");
        //$formEditButton.css({"display":"inline-block"});
        $.ajax({
            type: "get",
            url: "edit_nagios_host.py?host_name=" + host_name,
            cache: false,
            success: function (result) {
                //alert(result);
                spinStop($spinLoading, $spinMainLoading);
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    var form_id = "#edit_nagios_host_form";
                    hostDetails = result.data;

                    host_name = $("#host_name_nagios").val();
                    if (host_name == undefined) {
                        $("#div_table_paginate").css({"display": "none"});
                        $("#edit_nagios_host_form").css({"display": "inline-block"});

                    }
                    else {
                        $("#page_tip").colorbox(  			//page tip
                            {
                                href: "view_page_tip_nagios_inventory_hosts.py",
                                title: "Page Tip",
                                opacity: 0.4,
                                maxWidth: "80%",
                                width: "450px",
                                height: "400px"
                            });
                    }
                    $("input[id=host_name]", form_id).val(hostDetails["host_name"]);
                    $("input[id=old_ip_address]", form_id).val(hostDetails["address"]);
                    $("input[id=old_host_alias]", form_id).val(hostDetails["alias"]);
                    $("input[id=old_hostgroup]", form_id).val(hostDetails["hostgroups"]);


                    //$("#check_command",form_id).val(hostDetails["check_command"]);
                    $("#address", form_id).val(hostDetails["address"]);
                    $("#alias", form_id).val(hostDetails["alias"]);
                    //$("#use",form_id).val(hostDetails["use"]);
                    //$("#contacts",form_id).val(hostDetails["contacts"]);
                    $("#notes", form_id).val(hostDetails["notes"]);
                    $("#notes_url", form_id).val(hostDetails["notes_url"]);
                    $("#action_url", form_id).val(hostDetails["action_url"]);
                    $("#max_check_attempts", form_id).val(hostDetails["max_check_attempts"]);
                    $("#check_interval", form_id).val(hostDetails["check_interval"]);
                    $("#retry_interval", form_id).val(hostDetails["retry_interval"]);
                    $("#notifications_enabled", form_id).val(hostDetails["notifications_enabled"]);
                    $("#notification_interval", form_id).val(hostDetails["notification_interval"]);
                    $("#first_notification_delay", form_id).val(hostDetails["first_notification_delay"]);
                    $("#active_checks_enabled", form_id).val(hostDetails["active_checks_enabled"]);
                    $("#passive_checks_enabled", form_id).val(hostDetails["passive_checks_enabled"]);
                    $("#event_handler", form_id).val(hostDetails["event_handler"]);
                    $("#event_handler_enabled", form_id).val(hostDetails["event_handler_enabled"]);
                    $("#check_freshness", form_id).val(hostDetails["check_freshness"]);
                    $("#freshness_threshold", form_id).val(hostDetails["freshness_threshold"]);
                    $("#process_perf_data", form_id).val(hostDetails["process_perf_data"]);
                    $("#flap_detection_enabled", form_id).val(hostDetails["flap_detection_enabled"]);
                    $("#high_flap_threshold", form_id).val(hostDetails["high_flap_threshold"]);
                    $("#initial_state", form_id).val(hostDetails["initial_state"]);
                    $("#low_flap_threshold", form_id).val(hostDetails["low_flap_threshold"]);
                    fill_multiple_values_host(result.options, hostDetails, form_id);
                    $("#more_options_columns").html(result.html);
                    multiSelectColumns();

                    // javascript

                    $("#address").attr('disabled', 'disabled');
                    save_cancel_buttons();

                }
                //{"data": {"use": "generic-host", "check_command": "check-host-alive", "hostgroups": "sample",
                // "alias": "172.22.0.104", "parents": "host3", "host_name": "host4", "address": "172.22.0.104"}, "success": 0}

                else {
                    $().toastmessage('showErrorToast', 'Some error occured.');
                }

            }
        });
    }

}
////////////////////////////// host end 
///////////////////////////// host template starts

function main_host_template() {
    $('#host_template_table_paginate tbody tr').live('click', function () {
        var id = this.id;
        var index = jQuery.inArray(id, aSelected);

        if (index === -1) {
            aSelected.push(id);
        } else {
            aSelected.splice(index, 1);
        }
        $(this).toggleClass('row_selected');
    });
    aSelected = [];
    oTable = $('#host_template_table_paginate').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "bServerSide": true,
        "bDestroy": true,
        "fnRowCallback": function (nRow, aData, iDisplayIndex) {
            if (jQuery.inArray(aData.DT_RowId, aSelected) !== -1) {
                $(nRow).addClass('row_selected');
            }
            return nRow;
        },
        "sAjaxSource": "get_host_template_data_nagios.py",
        "aaSorting": [
            [0, 'desc']
        ]
    });
    //oTable.fnSetColumnVis( 0, false,false );

    $("#close_edit_host_template").click(function () {
        $("#div_table_paginate").css({"display": "block"});
        $("#edit_nagios_host_template_form").css({"display": "none"});
    });
    $("#save_edit_host_template").click(function () {
        var form = $("#edit_nagios_host_template_form");
        if (form.valid()) {
            var method = form.attr("method");
            var action = form.attr("action");
            var data = form.serialize() + "&notification_options=" + $("#notification_options").val() + "&flap_detection_options=" + $("#flap_detection_options").val()
                + "&contact_groups=" + $("#contact_groups").val() + "&use=" + $("#hd").val() + "&contacts=" + $("#contacts").val();
            $.ajax({
                type: method,
                url: action,
                data: data,
                cache: false,
                success: function (result) {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        $().toastmessage('showSuccessToast', "Host template details saved successfully.");
                        //main_hosts();
                        $("#close_edit_host_template").click();
                        oTable.fnDraw();

                    }
                    else if (result.success == 1) {

                        $().toastmessage('showErrorToast', "Some error occurred(" + String(result.exception) + ")");
                    }
                }
            });
        }
    });


    $("#page_tip").colorbox(  			//page tip
        {
            href: "view_page_tip_nagios_host_template.py",
            title: "Page Tip",
            opacity: 0.4,
            maxWidth: "80%",
            width: "450px",
            height: "400px"
        });

}


function fill_multiple_values_host_template(result, hostDetails, form_id) {
    try {
////////////////////////// code for single or multi select
        json_var_array = ["check_command", "register", "use", "hostgroups", "notifications_enabled", "initial_state", "active_checks_enabled", "passive_checks_enabled",
            "check_freshness", "process_perf_data", "flap_detection_enabled", "event_handler_enabled", "parents", "notification_options", "flap_detection_options"];
        corresponding_fields = ["#check_command", "#register", "#use", "#hostgroups", "#notifications_enabled", "#initial_state", "#active_checks_enabled", "#passive_checks_enabled",
            "#check_freshness", "#process_perf_data", "#flap_detection_enabled", "#event_handler_enabled", "#parents", "#notification_options", "#flap_detection_options"];
        for (json_var = 0; json_var < json_var_array.length; json_var++) {
            var_name = json_var_array[json_var]; // use
            if (result[var_name] != undefined)// && hostDetails[var_name]!=undefined)
            {
                host_templates = result[var_name]; // list of host templates
                cur_selected_array = {};
                currently_selected_host_templates = hostDetails[var_name]; // selected list
                html_string = "";
                if (currently_selected_host_templates) {
                    if (currently_selected_host_templates.indexOf(",") != -1)
                        cur_selected_array = currently_selected_host_templates.split(",");
                }
                for (i = 0; i < host_templates.length; i++) {
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) {
                        for (k = 0; k < cur_selected_array.length; k++) {
                            if (cur_selected_array[k] == host_templates[i][0] || cur_selected_array[k] == host_templates[i][1]) {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    if (flag)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else if (host_templates[i][0] == currently_selected_host_templates || host_templates[i][1] == currently_selected_host_templates)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else
                        html_string += "<option value=" + host_templates[i][0] + ">" + host_templates[i][1] + "</option>";
                }
//				alert(html_string);
                $(corresponding_fields[json_var], form_id).html(html_string);
                $(corresponding_fields[json_var], form_id).multiselect("refresh");
            }
        }
////////////////////////////////////////////////// special case for different names
        json_var_array = ["timeperiod", "timeperiod", "contactgroup", "contacts"];
        corresponding_names = ["check_period", "notification_period", "contact_groups", "contacts"];
        corresponding_fields = ["#check_period", "#notification_period", "#contact_groups", "#contacts"];
        for (json_var = 0; json_var < json_var_array.length; json_var++) {
            var_name = json_var_array[json_var];
            if (result[var_name] != undefined)// && hostDetails[var_name]!=undefined)
            {
                host_templates = result[var_name];
                currently_selected_host_templates = hostDetails[corresponding_names[json_var]];
                cur_selected_array = {};
                html_string = "";
                if (currently_selected_host_templates) {
                    if (currently_selected_host_templates.indexOf(",") != -1)
                        cur_selected_array = currently_selected_host_templates.split(",");
                }
                for (i = 0; i < host_templates.length; i++) {
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) {
                        for (k = 0; k < cur_selected_array.length; k++) {
                            if (cur_selected_array[k] == host_templates[i][0] || cur_selected_array[k] == host_templates[i][1]) {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    if (flag)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else if (host_templates[i][0] == currently_selected_host_templates || host_templates[i][1] == currently_selected_host_templates)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else
                        html_string += "<option value=" + host_templates[i][0] + ">" + host_templates[i][1] + "</option>";
                }
                $(corresponding_fields[json_var], form_id).html(html_string);
                $(corresponding_fields[json_var], form_id).multiselect("refresh");
            }
        }
    }
    catch (err) {
        //alert(err);
    }
}


function editHostTemplate(host_template_name) {
    spinStart($spinLoading, $spinMainLoading);
    $("#register").multiselect({selectedList: 1, multiple: false, minWidth: 230});
    $("#check_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select check period', header: "Available check periods", minWidth: 230});
    $("#notification_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select notification period', header: "Available notification periods", minWidth: 230});
    //$("#use").multiselect({selectedList: 1,multiple:true,noneSelectedText: 'Select templates',header:"Available templates",minWidth:230});
    $("#check_command").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select check command', header: "Available check commands", minWidth: 230});
    $("#hostgroups").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select hostgroups', header: "Available hostgroups", minWidth: 230}).multiselectfilter();
    $("#parents").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select parent', header: "Available parents", minWidth: 230}).multiselectfilter();
    $("#notification_options").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select notification options', minWidth: 230});
    $("#contact_groups").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select contact groups', minWidth: 230});
    $("#notifications_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select notifications enabled', minWidth: 230});
    $("#initial_state").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select initial state', minWidth: 230});
    $("#active_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select active checks enabled', minWidth: 230});
    $("#passive_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select passive checks enabled', minWidth: 230});
    $("#check_freshness").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select check freshness', minWidth: 230});
    $("#process_perf_data").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select process performance enabled', minWidth: 230});
    $("#flap_detection_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select flap detection enabled', minWidth: 230});
    $("#flap_detection_options").multiselect({selectedList: 2, multiple: true, noneSelectedText: 'Select flap detection options', minWidth: 230});
    $("#event_handler_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select event handler enabled', minWidth: 230});
    $("#contacts").multiselect({selectedList: 1, multiple: true, minWidth: 230});
    //$("#div_table_paginate").display("none");
    //$formEditButton.css({"display":"inline-block"});
    $.ajax({
        type: "get",
        url: "edit_nagios_host_template.py?host_template_name=" + host_template_name,
        cache: false,
        success: function (result) {

            spinStop($spinLoading, $spinMainLoading);
            result = eval("(" + result + ")");

            if (result.success == 0) {
                var form_id = "#edit_nagios_host_template_form";
                hostDetails = result.data;
                $("#div_table_paginate").css({"display": "none"});
                $("#edit_nagios_host_template_form").css({"display": "inline-block"});

                $("input[id=name]", form_id).val(hostDetails["name"]);
                $("input[id=old_host_template_name]", form_id).val(hostDetails["name"]);

                //$("#check_command",form_id).val(hostDetails["check_command"]);
                //$("#use",form_id).val(hostDetails["use"]);
                //$("#contacts",form_id).val(hostDetails["contacts"]);
                $("#notes", form_id).val(hostDetails["notes"]);
                $("#notes_url", form_id).val(hostDetails["notes_url"]);
                $("#action_url", form_id).val(hostDetails["action_url"]);
                $("#max_check_attempts", form_id).val(hostDetails["max_check_attempts"]);
                $("#check_interval", form_id).val(hostDetails["check_interval"]);
                $("#retry_interval", form_id).val(hostDetails["retry_interval"]);
                $("#notifications_enabled", form_id).val(hostDetails["notifications_enabled"]);
                $("#notification_interval", form_id).val(hostDetails["notification_interval"]);
                $("#first_notification_delay", form_id).val(hostDetails["first_notification_delay"]);
                $("#active_checks_enabled", form_id).val(hostDetails["active_checks_enabled"]);
                $("#passive_checks_enabled", form_id).val(hostDetails["passive_checks_enabled"]);
                $("#event_handler", form_id).val(hostDetails["event_handler"]);
                $("#event_handler_enabled", form_id).val(hostDetails["event_handler_enabled"]);
                $("#check_freshness", form_id).val(hostDetails["check_freshness"]);
                $("#freshness_threshold", form_id).val(hostDetails["freshness_threshold"]);
                $("#process_perf_data", form_id).val(hostDetails["process_perf_data"]);
                $("#flap_detection_enabled", form_id).val(hostDetails["flap_detection_enabled"]);
                $("#high_flap_threshold", form_id).val(hostDetails["high_flap_threshold"]);
                $("#initial_state", form_id).val(hostDetails["initial_state"]);
                $("#low_flap_threshold", form_id).val(hostDetails["low_flap_threshold"]);
                fill_multiple_values_host_template(result.options, hostDetails, form_id);
                $("#more_options_columns").html(result.html);
                multiSelectColumns();

            }
            //{"data": {"use": "generic-host", "check_command": "check-host-alive", "hostgroups": "sample",
            // "alias": "172.22.0.104", "parents": "host3", "host_name": "host4", "address": "172.22.0.104"}, "success": 0}

            else {
                $().toastmessage('showErrorToast', 'Some error occured.');
            }
        }
    });
}


function addHostTemplate() {

    $("#register").multiselect({selectedList: 1, multiple: false, minWidth: 230});
    $("#check_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select check period', header: "Available check periods", minWidth: 230});
    $("#notification_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select notification period', header: "Available notification periods", minWidth: 230});
    //$("#use").multiselect({selectedList: 1,multiple:true,noneSelectedText: 'Select templates',header:"Available templates",minWidth:230});
    $("#check_command").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select check command', header: "Available check commands", minWidth: 230});
    $("#hostgroups").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select hostgroups', header: "Available hostgroups", minWidth: 230}).multiselectfilter();
    $("#parents").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select parent', header: "Available parents", minWidth: 230}).multiselectfilter();
    $("#notification_options").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select notification options', minWidth: 230});
    $("#contact_groups").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select contact groups', minWidth: 230});
    $("#notifications_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select notifications enabled', minWidth: 230});
    $("#initial_state").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select initial state', minWidth: 230});
    $("#active_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select active checks enabled', minWidth: 230});
    $("#passive_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select passive checks enabled', minWidth: 230});
    $("#check_freshness").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select check freshness', minWidth: 230});
    $("#process_perf_data").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select process performance enabled', minWidth: 230});
    $("#flap_detection_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select flap detection enabled', minWidth: 230});
    $("#flap_detection_options").multiselect({selectedList: 2, multiple: true, noneSelectedText: 'Select flap detection options', minWidth: 230});
    $("#event_handler_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select event handler enabled', minWidth: 230});
    $("#contacts").multiselect({selectedList: 1, multiple: true, minWidth: 230});
    //$("#div_table_paginate").display("none");
    //$formEditButton.css({"display":"inline-block"});
    $.ajax({
        type: "get",
        url: "edit_nagios_host_template.py?addnew=true",
        cache: false,
        success: function (result) {
            result = eval("(" + result + ")");
            if (result.success == 0) {
                var form_id = "#edit_nagios_host_template_form";
                hostDetails = result.data;
                $("#div_table_paginate").css({"display": "none"});
                $("#edit_nagios_host_template_form").css({"display": "inline-block"});

                $("input[id=name]", form_id).val("");
                $("input[id=old_host_template_name]", form_id).val("");

                //$("#check_command",form_id).val(hostDetails["check_command"]);
                //$("#use",form_id).val(hostDetails["use"]);
                /*	$("#contacts",form_id).val("");
                 $("#notes",form_id).val("");
                 $("#notes_url",form_id).val(hostDetails["notes_url"]);
                 $("#action_url",form_id).val(hostDetails["action_url"]);
                 $("#max_check_attempts",form_id).val(hostDetails["max_check_attempts"]);
                 $("#check_interval",form_id).val(hostDetails["check_interval"]);
                 $("#retry_interval",form_id).val(hostDetails["retry_interval"]);
                 $("#notifications_enabled",form_id).val(hostDetails["notifications_enabled"]);
                 $("#notification_interval",form_id).val(hostDetails["notification_interval"]);
                 $("#first_notification_delay",form_id).val(hostDetails["first_notification_delay"]);
                 $("#active_checks_enabled",form_id).val(hostDetails["active_checks_enabled"]);
                 $("#passive_checks_enabled",form_id).val(hostDetails["passive_checks_enabled"]);
                 $("#event_handler",form_id).val(hostDetails["event_handler"]);
                 $("#event_handler_enabled",form_id).val(hostDetails["event_handler_enabled"]);
                 $("#check_freshness",form_id).val(hostDetails["check_freshness"]);
                 $("#freshness_threshold",form_id).val(hostDetails["freshness_threshold"]);
                 $("#process_perf_data",form_id).val(hostDetails["process_perf_data"]);
                 $("#flap_detection_enabled",form_id).val(hostDetails["flap_detection_enabled"]);
                 $("#high_flap_threshold",form_id).val(hostDetails["high_flap_threshold"]);
                 $("#initial_state",form_id).val(hostDetails["initial_state"]);
                 $("#low_flap_threshold",form_id).val(hostDetails["low_flap_threshold"]);
                 fill_multiple_values_host_template(result.options,hostDetails,form_id);*/

                fill_multiple_values_host_template(result.options, {}, form_id);
                $("#more_options_columns").html(result.html);
                multiSelectColumns();


            }
            //{"data": {"use": "generic-host", "check_command": "check-host-alive", "hostgroups": "sample",
            // "alias": "172.22.0.104", "parents": "host3", "host_name": "host4", "address": "172.22.0.104"}, "success": 0}

            else {
                $().toastmessage('showErrorToast', 'Some error occured.');
            }
        }
    });

}


function deleteHostTemplateCallback(v, m) {
    if (v != undefined && v == true) {

        spinStart($spinLoading, $spinMainLoading);
        var selectedRow = fnGetSelected(oTable);
        var rLength = selectedRow.length;
        var idStr = "";
        var usrStr = "";
        var selectedDeletedRowArray = [];
        for (var i = 0; i < selectedRow.length; i++) {
            var iRow = oTable.fnGetPosition(selectedRow[i]);
            var aData = oTable.fnGetData(iRow);
            if (i > 0) {
                idStr += ",";
                usrStr += ",";
            }
            idStr += String(aData[0]);
//			usrStr += String(aData[1]);
            selectedDeletedRowArray.push(iRow);
            // if delete successfully then call this function

        }
        var action = "nagios_delete_host_template.py";
        var data = "host_template_names=" + idStr;
        var method = "get";
        $.ajax({
            url: action,
            type: method,
            data: data,
            cache: false,
            success: function (result) {
                spinStop($spinLoading, $spinMainLoading);
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    for (var j = 0; j < selectedDeletedRowArray.length; j++)
                        oTable.fnDeleteRow(selectedDeletedRowArray[j]);
                    //alert("Deleted Successfully");
                    $().toastmessage('showSuccessToast', "Host Template(s) Deleted Successfully.");
                    oTable.fnDraw();
                }
                else {
                    $().toastmessage('showWarningToast', result.result);
                }

            }
        });
        return false;

    }

}


function delHostTemplate() {
    var selectedRow = fnGetSelected(oTable);
    var rLength = selectedRow.length;
    if (rLength == 0) {
        $.prompt("Select atleast one host template", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to delete this host template?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: deleteHostTemplateCallback });
    }
}

////////////////////////////// host_template end 

////////////////////////////// service begins

function main_services() {
    $('#service_table_paginate tbody tr').live('click', function () {
        var id = this.id;
        var index = jQuery.inArray(id, aSelected);

        if (index === -1) {
            aSelected.push(id);
        } else {
            aSelected.splice(index, 1);
        }
        $(this).toggleClass('row_selected');
    });
    aSelected = [];
    oTable = $('#service_table_paginate').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "bServerSide": true,
        "bDestroy": true,
        "fnRowCallback": function (nRow, aData, iDisplayIndex) {
            if (jQuery.inArray(aData.DT_RowId, aSelected) !== -1) {
                $(nRow).addClass('row_selected');
            }
            return nRow;
        },
        "sAjaxSource": "get_service_data_nagios.py",
        "aaSorting": [
            [0, 'desc']
        ]
    });
    oTable.fnSetColumnVis(0, false, false);


    /*oTable = $('#service_table_paginate').dataTable({
     "bJQueryUI": true,
     "sPaginationType": "full_numbers",
     "bProcessing": true,
     "bServerSide": true,
     "bDestroy" : true,
     "sAjaxSource": "get_service_data_nagios.py",
     "aaSorting": [[0,'desc']]
     });
     oTable.fnSetColumnVis( 0, false,false );*/

    $("#close_edit_service").click(function () {
        $("#div_table_paginate").css({"display": "block"});
        $("#edit_nagios_service_form").css({"display": "none"});
    });
    $("#save_edit_service").click(function () {
        var form = $("#edit_nagios_service_form");
        if (form.valid()) {
            var method = form.attr("method");
            var action = form.attr("action");
            var data = form.serialize() + "&notification_options=" + $("#notification_options").val() + "&flap_detection_options=" + $("#flap_detection_options").val()
                + "&contact_groups=" + $("#contact_groups").val() + "&host_name=" + $("#host_name").val() + "&use=" + $("#hd").val() + "&contacts=" + $("#contacts").val();
            $.ajax({
                type: method,
                url: action,
                data: data,
                cache: false,
                success: function (result) {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        $().toastmessage('showSuccessToast', "Service details saved successfully.");
                        //main_services();
                        $("#close_edit_service").click();
                        oTable.fnDraw();

                    }
                    else if (result.success == 1) {

                        $().toastmessage('showErrorToast', "Some error occurred(" + String(result.exception) + ")");
                    }
                }
            });
        }
    });


    $("#page_tip").colorbox(  			//page tip
        {
            href: "view_page_tip_nagios_service.py",
            title: "Page Tip",
            opacity: 0.4,
            maxWidth: "80%",
            width: "450px",
            height: "400px"
        });

    $("#edit_nagios_service_form").validate({
        rules: {
            service_description: {
                required: true//,

            },
            host_name: {
                required: true//,
            }
        },
        messages: {
            service_description: {
                required: "*"//,
            },

            host_name: {
                required: "*"//,
            }

        }
    });
}
function fill_multiple_values_service(result, hostDetails, form_id) {

    try {
////////////////////////// code for single or multi select
//"check_command",
        json_var_array = ["use", "host_name", "hostgroups", "notifications_enabled", "initial_state", "active_checks_enabled", "passive_checks_enabled",
            "check_freshness", "process_perf_data", "flap_detection_enabled", "event_handler_enabled", "parents", "notification_options", "flap_detection_options",
            "parallelize_check", "failure_prediction_enabled", "stalking_options", "retain_status_information", "retain_nonstatus_information",
            "obsess_over_service", "is_volatile"];
        corresponding_fields = ["#use", "#host_name", "#hostgroups", "#notifications_enabled", "#initial_state", "#active_checks_enabled", "#passive_checks_enabled",
            "#check_freshness", "#process_perf_data", "#flap_detection_enabled", "#event_handler_enabled", "#parents", "#notification_options", "#flap_detection_options",
            "#parallelize_check", "#failure_prediction_enabled", "#stalking_options", "#retain_status_information", "#retain_nonstatus_information",
            "#obsess_over_service", "#is_volatile"];
        for (json_var = 0; json_var < json_var_array.length; json_var++) {
            var_name = json_var_array[json_var]; // use
            if (result[var_name] != undefined)// && hostDetails[var_name]!=undefined)
            {
                host_templates = result[var_name]; // list of host templates
                cur_selected_array = {};
                currently_selected_host_templates = hostDetails[var_name]; // selected list
                html_string = "";
                if (currently_selected_host_templates) {
                    if (currently_selected_host_templates.indexOf(",") != -1)
                        cur_selected_array = currently_selected_host_templates.split(",");
                }
                for (i = 0; i < host_templates.length; i++) {
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) {
                        for (k = 0; k < cur_selected_array.length; k++) {

                            //if(var_name=="host_name")
                            //alert("looping variable "+$.trim(cur_selected_array[k]));
                            //alert("user selected "+$.trim(host_templates[i][0])+$.trim(host_templates[i][1]));
                            if ($.trim(cur_selected_array[k]) == $.trim(host_templates[i][0]))// || $.trim(cur_selected_array[k])==$.trim(host_templates[i][1]))
                            {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    if (flag)
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else if (host_templates[i][0] == currently_selected_host_templates || host_templates[i][1] == currently_selected_host_templates)
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + ">" + host_templates[i][1] + "</option>";
                }
//				alert(html_string);
                $(corresponding_fields[json_var], form_id).html(html_string);
                $(corresponding_fields[json_var], form_id).multiselect("refresh");
            }
        }
////////////////////////////////////////////////// special case for different names
        json_var_array = ["timeperiod", "timeperiod", "contactgroup", "contacts"];
        corresponding_names = ["check_period", "notification_period", "contact_groups", "contacts"];
        corresponding_fields = ["#check_period", "#notification_period", "#contact_groups", "#contacts"];
        for (json_var = 0; json_var < json_var_array.length; json_var++) {
            var_name = json_var_array[json_var];
            if (result[var_name] != undefined)// && hostDetails[var_name]!=undefined)
            {
                host_templates = result[var_name];
                currently_selected_host_templates = hostDetails[corresponding_names[json_var]];
                cur_selected_array = {};
                html_string = "";
                if (currently_selected_host_templates) {
                    if (currently_selected_host_templates.indexOf(",") != -1)
                        cur_selected_array = currently_selected_host_templates.split(",");
                }
                for (i = 0; i < host_templates.length; i++) {
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) {
                        for (k = 0; k < cur_selected_array.length; k++) {
                            if (cur_selected_array[k] == host_templates[i][0] || cur_selected_array[k] == host_templates[i][1]) {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    if (flag)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else if (host_templates[i][0] == currently_selected_host_templates || host_templates[i][1] == currently_selected_host_templates)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else
                        html_string += "<option value=" + host_templates[i][0] + ">" + host_templates[i][1] + "</option>";
                }
                $(corresponding_fields[json_var], form_id).html(html_string);
                $(corresponding_fields[json_var], form_id).multiselect("refresh");
            }
        }
    }
    catch (err) {
        //alert(err);
    }
}


function editService(service_unique_key) {
    spinStart($spinLoading, $spinMainLoading);
    $("#host_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select hosts', minWidth: 230}).multiselectfilter();
    $("#check_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select check period', header: "Available check periods", minWidth: 230});
    $("#notification_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select notification period', header: "Available notification periods", minWidth: 230});
    //$("#use").multiselect({selectedList: 1,multiple:true,noneSelectedText: 'Select templates',header:"Available templates",minWidth:230});
    //$("#check_command").multiselect({selectedList: 1,multiple:false,noneSelectedText: 'Select check command',header:"Available check commands",minWidth:230});
    $("#hostgroups").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select hostgroups', header: "Available hostgroups", minWidth: 230}).multiselectfilter();
    $("#notification_options").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select notification options', minWidth: 230});
    $("#contact_groups").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select contact groups', minWidth: 230});
    $("#notifications_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select notifications enabled', minWidth: 230});
    $("#initial_state").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select initial state', minWidth: 230});
    $("#active_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select active checks enabled', minWidth: 230});
    $("#passive_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select passive checks enabled', minWidth: 230});
    $("#check_freshness").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select check freshness', minWidth: 230});
    $("#process_perf_data").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select process performance enabled', minWidth: 230});
    $("#flap_detection_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select flap detection enabled', minWidth: 230});
    $("#flap_detection_options").multiselect({selectedList: 2, multiple: true, noneSelectedText: 'Select flap detection options', minWidth: 230});
    $("#event_handler_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select event handler enabled', minWidth: 230});

    $("#parallelize_check").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select parallelize check', minWidth: 230});
    $("#failure_prediction_enabled").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select failure prediction enabled', minWidth: 230});
    $("#stalking_options").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select stalking options', minWidth: 230});
    $("#retain_status_information").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select retain status information', minWidth: 230});
    $("#retain_nonstatus_information").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select retain non status information', minWidth: 230});
    $("#obsess_over_service").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select obsess over service', minWidth: 230});
    $("#is_volatile").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select is volatile', minWidth: 230});

    $("#contacts").multiselect({selectedList: 1, multiple: true, minWidth: 230});
    //$("#div_table_paginate").display("none");
    //$formEditButton.css({"display":"inline-block"});
    $.ajax({
        type: "get",
        url: "edit_nagios_service.py?service_unique_key=" + service_unique_key,
        cache: false,
        success: function (result) {
            //alert(result);
            spinStop($spinLoading, $spinMainLoading);
            result = eval("(" + result + ")");
            if (result.success == 0) {
                var form_id = "#edit_nagios_service_form";
                hostDetails = result.data;

                $("#div_table_paginate").css({"display": "none"});
                $("#edit_nagios_service_form").css({"display": "inline-block"});

                $("#service_unique_key", form_id).val(service_unique_key);
                $("#service_description", form_id).val(hostDetails["service_description"]);

                $("#address", form_id).val(hostDetails["address"]);
                $("#alias", form_id).val(hostDetails["alias"]);
                //$("#use",form_id).val(hostDetails["use"]);
                $("#check_command", form_id).val(hostDetails["check_command"]);
                //$("#contacts",form_id).val(hostDetails["contacts"]);
                $("#notes", form_id).val(hostDetails["notes"]);
                $("#notes_url", form_id).val(hostDetails["notes_url"]);
                $("#action_url", form_id).val(hostDetails["action_url"]);
                $("#max_check_attempts", form_id).val(hostDetails["max_check_attempts"]);
                $("#normal_check_interval", form_id).val(hostDetails["normal_check_interval"]);
                $("#retry_interval", form_id).val(hostDetails["retry_interval"]);
                $("#notification_interval", form_id).val(hostDetails["notification_interval"]);
                $("#first_notification_delay", form_id).val(hostDetails["first_notification_delay"]);
                $("#event_handler", form_id).val(hostDetails["event_handler"]);
                $("#check_freshness", form_id).val(hostDetails["check_freshness"]);
                $("#freshness_threshold", form_id).val(hostDetails["freshness_threshold"]);
                $("#process_perf_data", form_id).val(hostDetails["process_perf_data"]);
                $("#flap_detection_enabled", form_id).val(hostDetails["flap_detection_enabled"]);
                $("#high_flap_threshold", form_id).val(hostDetails["high_flap_threshold"]);
                $("#low_flap_threshold", form_id).val(hostDetails["low_flap_threshold"]);
                fill_multiple_values_service(result.options, hostDetails, form_id);

                $("#more_options_columns").html(result.html);
                multiSelectColumns();


            }
            else {
                $().toastmessage('showErrorToast', 'Some error occured.');
            }
        }
    });
}


function addService() {
    $("#host_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select hosts', minWidth: 230}).multiselectfilter();
    $("#check_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select check period', header: "Available check periods", minWidth: 230});
    $("#notification_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select notification period', header: "Available notification periods", minWidth: 230});
    //$("#use").multiselect({selectedList: 1,multiple:true,noneSelectedText: 'Select templates',header:"Available templates",minWidth:230});
    //$("#check_command").multiselect({selectedList: 1,multiple:false,noneSelectedText: 'Select check command',header:"Available check commands",minWidth:230});
    $("#hostgroups").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select hostgroups', header: "Available hostgroups", minWidth: 230}).multiselectfilter();
    $("#notification_options").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select notification options', minWidth: 230});
    $("#contact_groups").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select contact groups', minWidth: 230});
    $("#notifications_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select notifications enabled', minWidth: 230});
    $("#initial_state").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select initial state', minWidth: 230});
    $("#active_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select active checks enabled', minWidth: 230});
    $("#passive_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select passive checks enabled', minWidth: 230});
    $("#check_freshness").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select check freshness', minWidth: 230});
    $("#process_perf_data").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select process performance enabled', minWidth: 230});
    $("#flap_detection_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select flap detection enabled', minWidth: 230});
    $("#flap_detection_options").multiselect({selectedList: 2, multiple: true, noneSelectedText: 'Select flap detection options', minWidth: 230});
    $("#event_handler_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select event handler enabled', minWidth: 230});

    $("#parallelize_check").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select parallelize check', minWidth: 230});
    $("#failure_prediction_enabled").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select failure prediction enabled', minWidth: 230});
    $("#stalking_options").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select stalking options', minWidth: 230});
    $("#retain_status_information").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select retain status information', minWidth: 230});
    $("#retain_nonstatus_information").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select retain non status information', minWidth: 230});
    $("#obsess_over_service").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select obsess over service', minWidth: 230});
    $("#is_volatile").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select is volatile', minWidth: 230});

    $("#contacts").multiselect({selectedList: 1, multiple: true, minWidth: 230});
    //$("#div_table_paginate").display("none");
    //$formEditButton.css({"display":"inline-block"});
    $.ajax({
        type: "get",
        url: "edit_nagios_service.py?addnew=true",
        cache: false,
        success: function (result) {
            //alert(result);
            result = eval("(" + result + ")");
            if (result.success == 0) {
                var form_id = "#edit_nagios_service_form";
                hostDetails = result.data;

                $("#div_table_paginate").css({"display": "none"});
                $("#edit_nagios_service_form").css({"display": "inline-block"});

                $("#service_unique_key", form_id).val("");
                $("#service_description", form_id).val(hostDetails["service_description"]);

                $("#address", form_id).val(hostDetails["address"]);
                $("#alias", form_id).val(hostDetails["alias"]);
                //$("#use",form_id).val(hostDetails["use"]);
                $("#check_command", form_id).val(hostDetails["check_command"]);
                //$("#contacts",form_id).val(hostDetails["contacts"]);
                $("#notes", form_id).val(hostDetails["notes"]);
                $("#notes_url", form_id).val(hostDetails["notes_url"]);
                $("#action_url", form_id).val(hostDetails["action_url"]);
                $("#max_check_attempts", form_id).val(hostDetails["max_check_attempts"]);
                $("#normal_check_interval", form_id).val(hostDetails["normal_check_interval"]);
                $("#retry_interval", form_id).val(hostDetails["retry_interval"]);
                $("#notification_interval", form_id).val(hostDetails["notification_interval"]);
                $("#first_notification_delay", form_id).val(hostDetails["first_notification_delay"]);
                $("#event_handler", form_id).val(hostDetails["event_handler"]);
                $("#check_freshness", form_id).val(hostDetails["check_freshness"]);
                $("#freshness_threshold", form_id).val(hostDetails["freshness_threshold"]);
                $("#process_perf_data", form_id).val(hostDetails["process_perf_data"]);
                $("#flap_detection_enabled", form_id).val(hostDetails["flap_detection_enabled"]);
                $("#high_flap_threshold", form_id).val(hostDetails["high_flap_threshold"]);
                $("#low_flap_threshold", form_id).val(hostDetails["low_flap_threshold"]);
                fill_multiple_values_service(result.options, hostDetails, form_id);

                $("#more_options_columns").html(result.html);
                multiSelectColumns();


            }
            else {
                $().toastmessage('showErrorToast', 'Some error occured.');
            }
        }
    });
}


function deleteServiceCallback(v, m) {
    if (v != undefined && v == true) {

        spinStart($spinLoading, $spinMainLoading);
        var selectedRow = fnGetSelected(oTable);
        var rLength = selectedRow.length;
        var idStr = "";
        var usrStr = "";
        var selectedDeletedRowArray = [];
        for (var i = 0; i < selectedRow.length; i++) {
            var iRow = oTable.fnGetPosition(selectedRow[i]);
            var aData = oTable.fnGetData(iRow);
            if (i > 0) {
                idStr += ",";
                usrStr += ",";
            }
            idStr += String(aData[0]);
//			usrStr += String(aData[1]);
            selectedDeletedRowArray.push(iRow);
            // if delete successfully then call this function

        }
        var action = "nagios_delete_service.py";
        var data = "service_names=" + idStr;
        var method = "get";
        $.ajax({
            url: action,
            type: method,
            data: data,
            cache: false,
            success: function (result) {

                spinStop($spinLoading, $spinMainLoading);
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    for (var j = 0; j < selectedDeletedRowArray.length; j++)
                        oTable.fnDeleteRow(selectedDeletedRowArray[j]);
                    //alert("Deleted Successfully");
                    $().toastmessage('showSuccessToast', "Service(s) Deleted Successfully.");
                    oTable.fnDraw();
                }
                else {
                    $().toastmessage('showWarningToast', result.result);
                }
            }
        });
        return false;

    }

}


function delService() {
    var selectedRow = fnGetSelected(oTable);
    var rLength = selectedRow.length;
    if (rLength == 0) {
        $.prompt("Select atleast one service", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to delete the selected service(s)?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: deleteServiceCallback });
    }
}

///////////////////////////////////////////////////service  ends


function main_service_template() {

    $('#service_template_table_paginate tbody tr').live('click', function () {
        var id = this.id;
        var index = jQuery.inArray(id, aSelected);

        if (index === -1) {
            aSelected.push(id);
        } else {
            aSelected.splice(index, 1);
        }
        $(this).toggleClass('row_selected');
    });
    aSelected = [];
    oTable = $('#service_template_table_paginate').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "bServerSide": true,
        "bDestroy": true,
        "fnRowCallback": function (nRow, aData, iDisplayIndex) {
            if (jQuery.inArray(aData.DT_RowId, aSelected) !== -1) {
                $(nRow).addClass('row_selected');
            }
            return nRow;
        },
        "sAjaxSource": "get_service_template_data_nagios.py",
        "aaSorting": [
            [0, 'desc']
        ]
    });
    //oTable.fnSetColumnVis( 0, false,false );

    $("#close_edit_service_template").click(function () {
        $("#div_table_paginate").css({"display": "block"});
        $("#edit_nagios_service_template_form").css({"display": "none"});
    });
    $("#save_edit_service_template").click(function () {
        var form = $("#edit_nagios_service_template_form");
        if (form.valid()) {
            var method = form.attr("method");
            var action = form.attr("action");
            var data = form.serialize() + "&notification_options=" + $("#notification_options").val() + "&flap_detection_options=" + $("#flap_detection_options").val()
                + "&contact_groups=" + $("#contact_groups").val() + "&host_name=" + $("#host_name").val() + "&use=" + $("#hd").val() + "&contacts=" + $("#contacts").val();
            $.ajax({
                type: method,
                url: action,
                data: data,
                cache: false,
                success: function (result) {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        $().toastmessage('showSuccessToast', "Service template details saved successfully.");
                        //main_services();
                        $("#close_edit_service_template").click();
                        oTable.fnDraw();

                    }
                    else if (result.success == 1) {

                        $().toastmessage('showErrorToast', "Some error occurred(" + String(result.exception) + ")");
                    }
                }
            });
        }
    });


    $("#page_tip").colorbox(  			//page tip
        {
            href: "view_page_tip_nagios_service_template.py",
            title: "Page Tip",
            opacity: 0.4,
            maxWidth: "80%",
            width: "450px",
            height: "400px"
        });


}
function fill_multiple_values_service_template(result, hostDetails, form_id) {

    try {
////////////////////////// code for single or multi select
//"check_command",
        json_var_array = ["register", "use", "host_name", "hostgroups", "notifications_enabled", "initial_state", "active_checks_enabled", "passive_checks_enabled",
            "check_freshness", "process_perf_data", "flap_detection_enabled", "event_handler_enabled", "parents", "notification_options", "flap_detection_options",
            "parallelize_check", "failure_prediction_enabled", "stalking_options", "retain_status_information", "retain_nonstatus_information",
            "obsess_over_service", "is_volatile"];
        corresponding_fields = ["#register", "#use", "#host_name", "#hostgroups", "#notifications_enabled", "#initial_state", "#active_checks_enabled", "#passive_checks_enabled",
            "#check_freshness", "#process_perf_data", "#flap_detection_enabled", "#event_handler_enabled", "#parents", "#notification_options", "#flap_detection_options",
            "#parallelize_check", "#failure_prediction_enabled", "#stalking_options", "#retain_status_information", "#retain_nonstatus_information",
            "#obsess_over_service", "#is_volatile"];
        for (json_var = 0; json_var < json_var_array.length; json_var++) {
            var_name = json_var_array[json_var]; // use
            if (result[var_name] != undefined)// && hostDetails[var_name]!=undefined)
            {
                host_templates = result[var_name]; // list of host templates
                cur_selected_array = {};
                currently_selected_host_templates = hostDetails[var_name]; // selected list
                html_string = "";
                if (currently_selected_host_templates) {
                    if (currently_selected_host_templates.indexOf(",") != -1)
                        cur_selected_array = currently_selected_host_templates.split(",");
                }
                for (i = 0; i < host_templates.length; i++) {
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) {
                        for (k = 0; k < cur_selected_array.length; k++) {

                            //if(var_name=="host_name")
                            //alert("looping variable "+$.trim(cur_selected_array[k]));
                            //alert("user selected "+$.trim(host_templates[i][0])+$.trim(host_templates[i][1]));
                            if ($.trim(cur_selected_array[k]) == $.trim(host_templates[i][0]) || $.trim(cur_selected_array[k]) == $.trim(host_templates[i][1])) {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    if (flag)
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else if (host_templates[i][0] == currently_selected_host_templates || host_templates[i][1] == currently_selected_host_templates)
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + ">" + host_templates[i][1] + "</option>";
                }
//				alert(html_string);
                $(corresponding_fields[json_var], form_id).html(html_string);
                $(corresponding_fields[json_var], form_id).multiselect("refresh");
            }
        }
////////////////////////////////////////////////// special case for different names
        json_var_array = ["timeperiod", "timeperiod", "contactgroup", "contacts"];
        corresponding_names = ["check_period", "notification_period", "contact_groups", "contacts"];
        corresponding_fields = ["#check_period", "#notification_period", "#contact_groups", "#contacts"];
        for (json_var = 0; json_var < json_var_array.length; json_var++) {
            var_name = json_var_array[json_var];
            if (result[var_name] != undefined)// && hostDetails[var_name]!=undefined)
            {
                host_templates = result[var_name];
                currently_selected_host_templates = hostDetails[corresponding_names[json_var]];
                cur_selected_array = {};
                html_string = "";
                if (currently_selected_host_templates) {
                    if (currently_selected_host_templates.indexOf(",") != -1)
                        cur_selected_array = currently_selected_host_templates.split(",");
                }
                for (i = 0; i < host_templates.length; i++) {
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) {
                        for (k = 0; k < cur_selected_array.length; k++) {
                            if (cur_selected_array[k] == host_templates[i][0] || cur_selected_array[k] == host_templates[i][1]) {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    if (flag)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else if (host_templates[i][0] == currently_selected_host_templates || host_templates[i][1] == currently_selected_host_templates)
                        html_string += "<option value=" + host_templates[i][0] + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else
                        html_string += "<option value=" + host_templates[i][0] + ">" + host_templates[i][1] + "</option>";
                }
                $(corresponding_fields[json_var], form_id).html(html_string);
                $(corresponding_fields[json_var], form_id).multiselect("refresh");
            }
        }
    }
    catch (err) {
        //alert(err);
    }
}


function editServiceTemplate(service_unique_key) {

    spinStart($spinLoading, $spinMainLoading);
    $("#register").multiselect({selectedList: 1, multiple: false, minWidth: 230});
    $("#host_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select hosts', minWidth: 230}).multiselectfilter();
    $("#check_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select check period', header: "Available check periods", minWidth: 230});
    $("#notification_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select notification period', header: "Available notification periods", minWidth: 230});
    $("#use").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select templates', header: "Available templates", minWidth: 230});
    //$("#check_command").multiselect({selectedList: 1,multiple:false,noneSelectedText: 'Select check command',header:"Available check commands",minWidth:230});
    $("#hostgroups").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select hostgroups', header: "Available hostgroups", minWidth: 230}).multiselectfilter();
    $("#notification_options").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select notification options', minWidth: 230});
    $("#contact_groups").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select contact groups', minWidth: 230});
    $("#notifications_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select notifications enabled', minWidth: 230});
    $("#initial_state").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select initial state', minWidth: 230});
    $("#active_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select active checks enabled', minWidth: 230});
    $("#passive_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select passive checks enabled', minWidth: 230});
    $("#check_freshness").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select check freshness', minWidth: 230});
    $("#process_perf_data").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select process performance enabled', minWidth: 230});
    $("#flap_detection_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select flap detection enabled', minWidth: 230});
    $("#flap_detection_options").multiselect({selectedList: 2, multiple: true, noneSelectedText: 'Select flap detection options', minWidth: 230});
    $("#event_handler_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select event handler enabled', minWidth: 230});

    $("#parallelize_check").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select parallelize check', minWidth: 230});
    $("#failure_prediction_enabled").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select failure prediction enabled', minWidth: 230});
    $("#stalking_options").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select stalking options', minWidth: 230});
    $("#retain_status_information").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select retain status information', minWidth: 230});
    $("#retain_nonstatus_information").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select retain non status information', minWidth: 230});
    $("#obsess_over_service").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select obsess over service', minWidth: 230});
    $("#is_volatile").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select is volatile', minWidth: 230});
    $("#contacts").multiselect({selectedList: 1, multiple: true, minWidth: 230});
    //$("#div_table_paginate").display("none");
    //$formEditButton.css({"display":"inline-block"});
    $.ajax({
        type: "get",
        url: "edit_nagios_service_template.py?service_unique_key=" + service_unique_key,
        cache: false,
        success: function (result) {
            //alert(result);
            spinStop($spinLoading, $spinMainLoading);
            result = eval("(" + result + ")");
            if (result.success == 0) {
                var form_id = "#edit_nagios_service_template_form";
                hostDetails = result.data;
                $("#div_table_paginate").css({"display": "none"});
                $("#edit_nagios_service_template_form").css({"display": "inline-block"});

                $("#service_unique_key", form_id).val(service_unique_key);
                $("#service_description", form_id).val(hostDetails["service_description"]);

                $("#name", form_id).val(hostDetails["name"]);
                //$("#use",form_id).val(hostDetails["use"]);
                $("#check_command", form_id).val(hostDetails["check_command"]);
                //$("#contacts",form_id).val(hostDetails["contacts"]);
                $("#notes", form_id).val(hostDetails["notes"]);
                $("#notes_url", form_id).val(hostDetails["notes_url"]);
                $("#action_url", form_id).val(hostDetails["action_url"]);
                $("#max_check_attempts", form_id).val(hostDetails["max_check_attempts"]);
                $("#normal_check_interval", form_id).val(hostDetails["normal_check_interval"]);
                $("#retry_interval", form_id).val(hostDetails["retry_interval"]);
                $("#notification_interval", form_id).val(hostDetails["notification_interval"]);
                $("#first_notification_delay", form_id).val(hostDetails["first_notification_delay"]);
                $("#event_handler", form_id).val(hostDetails["event_handler"]);
                $("#check_freshness", form_id).val(hostDetails["check_freshness"]);
                $("#freshness_threshold", form_id).val(hostDetails["freshness_threshold"]);
                $("#process_perf_data", form_id).val(hostDetails["process_perf_data"]);
                $("#flap_detection_enabled", form_id).val(hostDetails["flap_detection_enabled"]);
                $("#high_flap_threshold", form_id).val(hostDetails["high_flap_threshold"]);
                $("#low_flap_threshold", form_id).val(hostDetails["low_flap_threshold"]);
                fill_multiple_values_service_template(result.options, hostDetails, form_id);

                $("#more_options_columns").html(result.html);
                multiSelectColumns();

            }
            else {
                $().toastmessage('showErrorToast', 'Some error occured.');
            }
        }
    });
}


function addServiceTemplate() {

    $("#register").multiselect({selectedList: 1, multiple: false, minWidth: 230});
    $("#host_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select hosts', minWidth: 230}).multiselectfilter();
    $("#check_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select check period', header: "Available check periods", minWidth: 230});
    $("#notification_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select notification period', header: "Available notification periods", minWidth: 230});
    $("#use").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select templates', header: "Available templates", minWidth: 230});
    //$("#check_command").multiselect({selectedList: 1,multiple:false,noneSelectedText: 'Select check command',header:"Available check commands",minWidth:230});
    $("#hostgroups").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select hostgroups', header: "Available hostgroups", minWidth: 230}).multiselectfilter();
    $("#notification_options").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select notification options', minWidth: 230});
    $("#contact_groups").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select contact groups', minWidth: 230});
    $("#notifications_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select notifications enabled', minWidth: 230});
    $("#initial_state").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select initial state', minWidth: 230});
    $("#active_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select active checks enabled', minWidth: 230});
    $("#passive_checks_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select passive checks enabled', minWidth: 230});
    $("#check_freshness").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select check freshness', minWidth: 230});
    $("#process_perf_data").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select process performance enabled', minWidth: 230});
    $("#flap_detection_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select flap detection enabled', minWidth: 230});
    $("#flap_detection_options").multiselect({selectedList: 2, multiple: true, noneSelectedText: 'Select flap detection options', minWidth: 230});
    $("#event_handler_enabled").multiselect({selectedList: 4, multiple: false, noneSelectedText: 'Select event handler enabled', minWidth: 230});

    $("#parallelize_check").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select parallelize check', minWidth: 230});
    $("#failure_prediction_enabled").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select failure prediction enabled', minWidth: 230});
    $("#stalking_options").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select stalking options', minWidth: 230});
    $("#retain_status_information").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select retain status information', minWidth: 230});
    $("#retain_nonstatus_information").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select retain non status information', minWidth: 230});
    $("#obsess_over_service").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select obsess over service', minWidth: 230});
    $("#is_volatile").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select is volatile', minWidth: 230});

    $("#contacts").multiselect({selectedList: 1, multiple: true, minWidth: 230});
    //$("#div_table_paginate").display("none");
    //$formEditButton.css({"display":"inline-block"});
    $.ajax({
        type: "get",
        url: "edit_nagios_service_template.py?add_new=true",
        cache: false,
        success: function (result) {
            //alert(result);
            result = eval("(" + result + ")");
            if (result.success == 0) {
                var form_id = "#edit_nagios_service_template_form";
                hostDetails = result.data;
                $("#div_table_paginate").css({"display": "none"});
                $("#edit_nagios_service_template_form").css({"display": "inline-block"});

                $("#service_unique_key", form_id).val("");
                $("#service_description", form_id).val("");
                /*
                 $("#name",form_id).val(hostDetails["name"]);
                 //$("#use",form_id).val(hostDetails["use"]);
                 $("#check_command",form_id).val(hostDetails["check_command"]);
                 $("#contacts",form_id).val(hostDetails["contacts"]);
                 $("#notes",form_id).val(hostDetails["notes"]);
                 $("#notes_url",form_id).val(hostDetails["notes_url"]);
                 $("#action_url",form_id).val(hostDetails["action_url"]);
                 $("#max_check_attempts",form_id).val(hostDetails["max_check_attempts"]);
                 $("#normal_check_interval",form_id).val(hostDetails["normal_check_interval"]);
                 $("#retry_interval",form_id).val(hostDetails["retry_interval"]);
                 $("#notification_interval",form_id).val(hostDetails["notification_interval"]);
                 $("#first_notification_delay",form_id).val(hostDetails["first_notification_delay"]);
                 $("#event_handler",form_id).val(hostDetails["event_handler"]);
                 $("#check_freshness",form_id).val(hostDetails["check_freshness"]);
                 $("#freshness_threshold",form_id).val(hostDetails["freshness_threshold"]);
                 $("#process_perf_data",form_id).val(hostDetails["process_perf_data"]);
                 $("#flap_detection_enabled",form_id).val(hostDetails["flap_detection_enabled"]);
                 $("#high_flap_threshold",form_id).val(hostDetails["high_flap_threshold"]);
                 $("#low_flap_threshold",form_id).val(hostDetails["low_flap_threshold"]);*/
                fill_multiple_values_service_template(result.options, hostDetails, form_id);

                $("#more_options_columns").html(result.html);
                multiSelectColumns();

            }
            else {
                $().toastmessage('showErrorToast', 'Some error occured.');
            }
        }
    });

}


function deleteServiceTemplateCallback(v, m) {
    if (v != undefined && v == true) {

        spinStart($spinLoading, $spinMainLoading);
        var selectedRow = fnGetSelected(oTable);
        var rLength = selectedRow.length;
        var idStr = "";
        var usrStr = "";
        var selectedDeletedRowArray = [];
        for (var i = 0; i < selectedRow.length; i++) {
            var iRow = oTable.fnGetPosition(selectedRow[i]);
            var aData = oTable.fnGetData(iRow);
            if (i > 0) {
                idStr += ",";
                usrStr += ",";
            }
            idStr += String(aData[0]);
//			usrStr += String(aData[1]);
            selectedDeletedRowArray.push(iRow);
            // if delete successfully then call this function

        }
        var action = "nagios_delete_service_template.py";
        var data = "service_template_names=" + idStr;
        var method = "get";
        $.ajax({
            url: action,
            type: method,
            data: data,
            cache: false,
            success: function (result) {
                spinStop($spinLoading, $spinMainLoading);
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    for (var j = 0; j < selectedDeletedRowArray.length; j++)
                        oTable.fnDeleteRow(selectedDeletedRowArray[j]);
                    //alert("Deleted Successfully");
                    $().toastmessage('showSuccessToast', "Service Template(s) Deleted Successfully.");
                    oTable.fnDraw();
                }
                else {
                    $().toastmessage('showWarningToast', result.result);
                }
            }
        });
        return false;

    }

}


function delServiceTemplate() {
    var selectedRow = fnGetSelected(oTable);
    var rLength = selectedRow.length;
    if (rLength == 0) {
        $.prompt("Select atleast one service template", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to delete the service template(s)?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: deleteServiceTemplateCallback });
    }
}
///////////////////////////////////////////////////service template ends


////////////////////////////////////////////////// hostgroup begins

function main_hostgroups() {

    oTable = $('#hostgroup_table_paginate').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "bServerSide": true,
        "bDestroy": true,
        "sAjaxSource": "get_hostgroup_data_nagios.py",
        "aaSorting": [
            [0, 'desc']
        ]
    });
    //oTable.fnSetColumnVis( 0, false,false );

    $("#close_edit_hostgroup").click(function () {
        $("#div_table_paginate").css({"display": "block"});
        $("#edit_nagios_hostgroup_form").css({"display": "none"});
    });
    $("#save_edit_hostgroup").click(function () {
        var form = $("#edit_nagios_hostgroup_form");
        if (form.valid()) {
            var method = form.attr("method");
            var action = form.attr("action");
            var data = form.serialize() + "&members=" + $("#members").val();
            $.ajax({
                type: method,
                url: action,
                data: data,
                cache: false,
                success: function (result) {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        $().toastmessage('showSuccessToast', "hostgroup details saved successfully.");
                        $("#close_edit_hostgroup").click();
                        oTable.fnDraw();
                        //main_hostgroups();

                    }
                    else if (result.success == 1) {

                        $().toastmessage('showErrorToast', "Some error occurred");
                    }
                }
            });
        }
    });


    $("#page_tip").colorbox(  			//page tip
        {
            href: "view_page_tip_nagios_hostgroup.py",
            title: "Page Tip",
            opacity: 0.4,
            maxWidth: "80%",
            width: "450px",
            height: "400px"
        });
    $("#edit_nagios_hostgroup_form").validate({
        rules: {
            hostgroup_name: {
                required: true//,

            },
            alias: {
                required: true//,
            }
        },
        messages: {
            hostgroup_name: {
                required: "*"//,
            },
            alias: {
                required: "*"//,
            }
        }
    });
}


function fill_multiple_values_hostgroup(result, hostDetails, form_id) {

    try {
////////////////////////// code for single or multi select
        json_var_array = ["members"];
        corresponding_fields = ["#members"];
        for (json_var = 0; json_var < json_var_array.length; json_var++) {
            var_name = json_var_array[json_var]; // use
            if (result[var_name] != undefined)// && hostDetails[var_name]!=undefined)
            {
                host_templates = result[var_name]; // list of host templates
                cur_selected_array = {};
                currently_selected_host_templates = hostDetails[var_name]; // selected list
                html_string = "";
                if (currently_selected_host_templates) {
                    if (currently_selected_host_templates.indexOf(",") != -1)
                        cur_selected_array = currently_selected_host_templates.split(",");
                }
                for (i = 0; i < host_templates.length; i++) {
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) {
                        for (k = 0; k < cur_selected_array.length; k++) {
                            if ($.trim(cur_selected_array[k]) == $.trim(host_templates[i][0]) || $.trim(cur_selected_array[k]) == $.trim(host_templates[i][1])) {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    if (flag)
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else if (host_templates[i][0] == currently_selected_host_templates || host_templates[i][1] == currently_selected_host_templates)
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + ">" + host_templates[i][1] + "</option>";
                }
//				alert(html_string);
                $(corresponding_fields[json_var], form_id).html(html_string);
                $(corresponding_fields[json_var], form_id).multiselect("refresh");
            }
        }
    }
    catch (err) {
        //alert(err);
    }
}


function editHostgroup(hostgroup_name) {
    spinStart($spinLoading, $spinMainLoading);
    $("#members").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select members', minWidth: 230}).multiselectfilter();

    //$("#div_table_paginate").display("none");
    //$formEditButton.css({"display":"inline-block"});
    $.ajax({
        type: "get",
        url: "edit_nagios_hostgroup.py?hostgroup_name=" + hostgroup_name,
        cache: false,
        success: function (result) {
            //alert(result);
            spinStop($spinLoading, $spinMainLoading);
            result = eval("(" + result + ")");
            if (result.success == 0) {
                var form_id = "#edit_nagios_hostgroup_form";
                hostDetails = result.data;
                $("#div_table_paginate").css({"display": "none"});
                $("#edit_nagios_hostgroup_form").css({"display": "inline-block"});

                $("input[id=hostgroup_name_unique]", form_id).val(hostDetails["hostgroup_name"]);
                $("input[id=old_members]", form_id).val(hostDetails["members"]);
                $("#hostgroup_name", form_id).val(hostDetails["hostgroup_name"]);
                $("#alias", form_id).val(hostDetails["alias"]);
                $("#notes", form_id).val(hostDetails["notes"]);
                $("#notes_url", form_id).val(hostDetails["notes_url"]);
                $("#action_url", form_id).val(hostDetails["action_url"]);
                fill_multiple_values_hostgroup(result.options, hostDetails, form_id);

            }
            //{"data": {"use": "generic-host", "check_command": "check-host-alive", "hostgroups": "sample",
            // "alias": "172.22.0.104", "parents": "host3", "host_name": "host4", "address": "172.22.0.104"}, "success": 0}

            else {
                $().toastmessage('showErrorToast', 'Some error occured.');
            }
        }
    });
}
//////////////////////////// hostgroup ends

////////////////////////////////////////////////// servicegroup begins

function main_servicegroup() {

    oTable = $('#servicegroup_table_paginate').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "bServerSide": true,
        "bDestroy": true,
        "sAjaxSource": "get_servicegroup_data_nagios.py",
        "aaSorting": [
            [0, 'desc']
        ]
    });
    //oTable.fnSetColumnVis( 0, false,false );

    $("#close_edit_servicegroup").click(function () {
        $("#div_table_paginate").css({"display": "block"});
        $("#edit_nagios_servicegroup_form").css({"display": "none"});
    });
    $("#save_edit_servicegroup").click(function () {
        var form = $("#edit_nagios_servicegroup_form");
        if (form.valid()) {
            var method = form.attr("method");
            var action = form.attr("action");
            var data = form.serialize() + "&members=" + $("#members").val();
            $.ajax({
                type: method,
                url: action,
                data: data,
                cache: false,
                success: function (result) {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        $().toastmessage('showSuccessToast', "servicegroup details saved successfully.");
                        $("#close_edit_servicegroup").click();
                        oTable.fnDraw();
                        //main_hostgroups();

                    }
                    else if (result.success == 1) {

                        $().toastmessage('showErrorToast', "Some error occurred");
                    }
                }
            });
        }
    });


    $("#page_tip").colorbox(  			//page tip
        {
            href: "view_page_tip_nagios_servicegroup.py",
            title: "Page Tip",
            opacity: 0.4,
            maxWidth: "80%",
            width: "450px",
            height: "400px"
        });
    $("#edit_nagios_servicegroup_form").validate({
        rules: {
            servicegroup_name: {
                required: true//,

            },
            alias: {
                required: true//,
            }
        },
        messages: {
            servicegroup_name: {
                required: "*"//,
            },
            alias: {
                required: "*"//,
            }
        }
    });
}


function fill_multiple_values_servicegroup(result, hostDetails, form_id) {

    try {
////////////////////////// code for single or multi select
        json_var_array = ["members"];
        corresponding_fields = ["#members"];
        for (json_var = 0; json_var < json_var_array.length; json_var++) {
            var_name = json_var_array[json_var]; // use
            if (result[var_name] != undefined)// && hostDetails[var_name]!=undefined)
            {
                host_templates = result[var_name]; // list of host templates
                cur_selected_array = {};
                currently_selected_host_templates = hostDetails[var_name]; // selected list
                html_string = "";
                if (currently_selected_host_templates) {
                    if (currently_selected_host_templates.indexOf(",") != -1)
                        cur_selected_array = currently_selected_host_templates.split(",");
                }
                for (i = 0; i < host_templates.length; i++) {
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) {
                        for (k = 0; k < cur_selected_array.length; k++) {
                            if ($.trim(cur_selected_array[k]) == $.trim(host_templates[i][0]) || $.trim(cur_selected_array[k]) == $.trim(host_templates[i][1])) {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    if (flag)
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else if (host_templates[i][0] == currently_selected_host_templates || host_templates[i][1] == currently_selected_host_templates)
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + ">" + host_templates[i][1] + "</option>";
                }
//				alert(html_string);
                $(corresponding_fields[json_var], form_id).html(html_string);
                $(corresponding_fields[json_var], form_id).multiselect("refresh");
            }
        }
    }
    catch (err) {
        //alert(err);
    }
}


function editServicegroup(servicegroup_name) {
    spinStart($spinLoading, $spinMainLoading);
    $("#members").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select members', minWidth: 230});

    //$("#div_table_paginate").display("none");
    //$formEditButton.css({"display":"inline-block"});
    $.ajax({
        type: "get",
        url: "edit_nagios_servicegroup.py?servicegroup_name=" + servicegroup_name,
        cache: false,
        success: function (result) {
            //alert(result);
            spinStop($spinLoading, $spinMainLoading);
            result = eval("(" + result + ")");
            if (result.success == 0) {
                var form_id = "#edit_nagios_servicegroup_form";
                hostDetails = result.data;
                $("#div_table_paginate").css({"display": "none"});
                $("#edit_nagios_servicegroup_form").css({"display": "inline-block"});

                $("input[id=servicegroup_name_unique]", form_id).val(hostDetails["servicegroup_name"]);
                $("input[id=old_members]", form_id).val(hostDetails["members"]);
                $("#servicegroup_name", form_id).val(hostDetails["servicegroup_name"]);
                $("#alias", form_id).val(hostDetails["alias"]);
                $("#notes", form_id).val(hostDetails["notes"]);
                $("#notes_url", form_id).val(hostDetails["notes_url"]);
                $("#action_url", form_id).val(hostDetails["action_url"]);
                fill_multiple_values_hostgroup(result.options, hostDetails, form_id);

            }
            //{"data": {"use": "generic-host", "check_command": "check-host-alive", "hostgroups": "sample",
            // "alias": "172.22.0.104", "parents": "host3", "host_name": "host4", "address": "172.22.0.104"}, "success": 0}

            else {
                $().toastmessage('showErrorToast', 'Some error occured.');
            }
        }
    });
}
//////////////////////////// servicegroup ends

//////////////////// command start	
function main_command() {

    $('#command_table_paginate tbody tr').live('click', function () {
        var id = this.id;
        var index = jQuery.inArray(id, aSelected);

        if (index === -1) {
            aSelected.push(id);
        } else {
            aSelected.splice(index, 1);
        }
        $(this).toggleClass('row_selected');
    });
    aSelected = [];
    oTable = $('#command_table_paginate').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "bServerSide": true,
        "bDestroy": true,
        "fnRowCallback": function (nRow, aData, iDisplayIndex) {
            if (jQuery.inArray(aData.DT_RowId, aSelected) !== -1) {
                $(nRow).addClass('row_selected');
            }
            return nRow;
        },
        "sAjaxSource": "get_command_data_nagios.py",
        "aaSorting": [
            [0, 'desc']
        ]
    });

    $("#close_edit_command").click(function () {
        $("#div_table_paginate").css({"display": "block"});
        $("#edit_nagios_command_form").css({"display": "none"});
    });
    $("#save_edit_command").click(function () {
        var form = $("#edit_nagios_command_form");
        if (form.valid()) {
            var method = form.attr("method");
            var action = form.attr("action");
            var data = form.serialize();
            $.ajax({
                type: method,
                url: action,
                data: data,
                cache: false,
                success: function (result) {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        $().toastmessage('showSuccessToast', "Command details saved successfully.");
                        //main_hosts();
                        $("#close_edit_command").click();
                        oTable.fnDraw();

                    }
                    else if (result.success == 1) {

                        $().toastmessage('showErrorToast', "Some error occurred(" + String(result.exception) + ")");
                    }
                }
            });
        }
    });


    $("#page_tip").colorbox(  			//page tip
        {
            href: "view_page_tip_nagios_command.py",
            title: "Page Tip",
            opacity: 0.4,
            maxWidth: "80%",
            width: "450px",
            height: "400px"
        });


}


function editCommand(command_name) {
    spinStart($spinLoading, $spinMainLoading);
    //$("#div_table_paginate").display("none");
    //$formEditButton.css({"display":"inline-block"});
    $.ajax({
        type: "get",
        url: "edit_nagios_command.py?command_name=" + command_name,
        cache: false,
        success: function (result) {
            //alert(result);
            spinStop($spinLoading, $spinMainLoading);
            result = eval("(" + result + ")");
            if (result.success == 0) {
                var form_id = "#edit_nagios_command_form";
                hostDetails = result.data;
                $("#div_table_paginate").css({"display": "none"});
                $("#edit_nagios_command_form").css({"display": "inline-block"});

                $("input[id=command_name]", form_id).val(hostDetails["command_name"]);
                $("input[id=old_command_name]", form_id).val(hostDetails["command_name"]);
                $("input[id=command_line]", form_id).val(hostDetails["command_line"]);

            }

            else {
                $().toastmessage('showErrorToast', 'Some error occured.');
            }
        }
    });
}


function addCommand() {
    var form_id = "#edit_nagios_command_form";
    $("#div_table_paginate").css({"display": "none"});
    $("#edit_nagios_command_form").css({"display": "inline-block"});
    $("input[id=command_name]", form_id).val("");
    $("input[id=old_command_name]", form_id).val("");
    $("input[id=command_line]", form_id).val("");
}


function deleteCommandCallback(v, m) {
    if (v != undefined && v == true) {

        spinStart($spinLoading, $spinMainLoading);
        var selectedRow = fnGetSelected(oTable);
        var rLength = selectedRow.length;
        var idStr = "";
        var usrStr = "";
        var selectedDeletedRowArray = [];
        for (var i = 0; i < selectedRow.length; i++) {
            var iRow = oTable.fnGetPosition(selectedRow[i]);
            var aData = oTable.fnGetData(iRow);
            if (i > 0) {
                idStr += ",";
                usrStr += ",";
            }
            idStr += String(aData[0]);
//			usrStr += String(aData[1]);
            selectedDeletedRowArray.push(iRow);
            // if delete successfully then call this function

        }
        var action = "nagios_delete_command.py";
        var data = "command_names=" + idStr;
        var method = "get";
        $.ajax({
            url: action,
            type: method,
            data: data,
            cache: false,
            success: function (result) {
                spinStop($spinLoading, $spinMainLoading);
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    for (var j = 0; j < selectedDeletedRowArray.length; j++)
                        oTable.fnDeleteRow(selectedDeletedRowArray[j]);
                    //alert("Deleted Successfully");
                    $().toastmessage('showSuccessToast', "Command(s) Deleted Successfully.");
                    oTable.fnDraw();
                }
                else {
                    $().toastmessage('showWarningToast', result.result);
                }
            }
        });
        return false;

    }

}


function delCommand() {
    var selectedRow = fnGetSelected(oTable);
    var rLength = selectedRow.length;
    if (rLength == 0) {
        $.prompt("Select atleast one command to delete.", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to delete this command?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: deleteCommandCallback });
    }
}

////////////////////////////// command end 	

////////////////////////////// hostdependency begins

function main_hostdependency() {


    $('#hostdependency_table_paginate tbody tr').live('click', function () {
        var id = this.id;
        var index = jQuery.inArray(id, aSelected);

        if (index === -1) {
            aSelected.push(id);
        } else {
            aSelected.splice(index, 1);
        }
        $(this).toggleClass('row_selected');
    });
    aSelected = [];
    oTable = $('#hostdependency_table_paginate').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "bServerSide": true,
        "bDestroy": true,
        "fnRowCallback": function (nRow, aData, iDisplayIndex) {
            if (jQuery.inArray(aData.DT_RowId, aSelected) !== -1) {
                $(nRow).addClass('row_selected');
            }
            return nRow;
        },
        "sAjaxSource": "get_hostdependency_data_nagios.py",
        "aaSorting": [
            [0, 'desc']
        ]
    });
    oTable.fnSetColumnVis(0, false, false);

    $("#close_edit_hostdependency").click(function () {
        $("#div_table_paginate").css({"display": "block"});
        $("#edit_nagios_hostdependency_form").css({"display": "none"});
    });
    $("#save_edit_hostdependency").click(function () {
        var form = $("#edit_nagios_hostdependency_form");
        if (form.valid()) {
            var method = form.attr("method");
            var action = form.attr("action");
            var data = form.serialize() + "&notification_failure_criteria=" + $("#notification_failure_criteria").val() + "&execution_failure_criteria=" + $("#execution_failure_criteria").val() + "&dependent_host_name=" + $("#dependent_host_name").val() + "&host_name=" + $("#host_name").val();
            $.ajax({
                type: method,
                url: action,
                data: data,
                cache: false,
                success: function (result) {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        $().toastmessage('showSuccessToast', "hostdependency details saved successfully.");
                        //main_services();
                        $("#close_edit_hostdependency").click();
                        oTable.fnDraw();

                    }
                    else if (result.success == 1) {

                        $().toastmessage('showErrorToast', "Some error occurred(" + String(result.exception) + ")");
                    }
                }
            });
        }
    });


    $("#page_tip").colorbox(  			//page tip
        {
            href: "view_page_tip_nagios_hostdependency.py",
            title: "Page Tip",
            opacity: 0.4,
            maxWidth: "80%",
            width: "450px",
            height: "400px"
        });

    $("#edit_nagios_hostdependency_form").validate({
        rules: {
            host_name: {
                required: true//,
            }
        },
        messages: {
            host_name: {
                required: "*"//,
            }

        }
    });
}
function fill_multiple_values_hostdependency(result, hostDetails, form_id) {

    try {
////////////////////////// code for single or multi select
//"check_command",
        json_var_array = ["host_name", "dependent_host_name", "dependent_hostgroup_name", "inherits_parent", "notification_failure_criteria", "execution_failure_criteria", "dependency_period"];
        corresponding_fields = ["#host_name", "#dependent_host_name", "#dependent_hostgroup_name", "#inherits_parent", "#notification_failure_criteria", "#execution_failure_criteria", "#dependency_period"];
        for (json_var = 0; json_var < json_var_array.length; json_var++) {
            var_name = json_var_array[json_var]; // use
            if (result[var_name] != undefined)// && hostDetails[var_name]!=undefined)
            {
                host_templates = result[var_name]; // list of host templates
                cur_selected_array = {};
                currently_selected_host_templates = hostDetails[var_name]; // selected list
                html_string = "";
                if (currently_selected_host_templates) {
                    if (currently_selected_host_templates.indexOf(",") != -1)
                        cur_selected_array = currently_selected_host_templates.split(",");
                }
                for (i = 0; i < host_templates.length; i++) {
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) {
                        for (k = 0; k < cur_selected_array.length; k++) {

                            //if(var_name=="host_name")
                            //alert("looping variable "+$.trim(cur_selected_array[k]));
                            //alert("user selected "+$.trim(host_templates[i][0])+$.trim(host_templates[i][1]));
                            if ($.trim(cur_selected_array[k]) == $.trim(host_templates[i][0]) || $.trim(cur_selected_array[k]) == $.trim(host_templates[i][1])) {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    if (flag)
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else if (host_templates[i][0] == currently_selected_host_templates || host_templates[i][1] == currently_selected_host_templates)
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + ">" + host_templates[i][1] + "</option>";
                }
//				alert(html_string);
                $(corresponding_fields[json_var], form_id).html(html_string);
                $(corresponding_fields[json_var], form_id).multiselect("refresh");
            }
        }
        all_options = $.map($("#dependent_host_name").multiselect("widget").find(":checkbox"), function (input) {
            return input.value;
        });
        all_indexes = $.map($("#dependent_host_name").multiselect("widget").find(":checkbox"), function (input) {
            return input.title;
        });
        originally_selected = $("#dependent_host_name").multiselect("getChecked").map(function () {
            return this.value;
        }).get();

        all_options_values = $.map($("#dependent_host_name").multiselect("widget").find(":checkbox"), function (input) {
            return input.value;
        });
        $("#host_name").bind("multiselectclick", function (event, ui) {
            var checkedHosts = $(this).multiselect("getChecked").map(function () {
                return this.value;
            }).get();
            var checkedValues = $.map($(this).multiselect("getChecked"), function (input) {
                return input.title;
            });

            html_string = "";
            for (var i = 0; i < all_options.length; i++) {
                if (checkedHosts.indexOf(all_options[i]) == -1) {
                    if (originally_selected.indexOf(all_options[i]) != -1)
                        html_string += "<option value=" + all_options[i] + " selected='selected' >" + all_indexes[i] + "</option>";
                    else
                        html_string += "<option value=" + all_options[i] + " >" + all_indexes[i] + "</option>";
                }
            }
            $("#dependent_host_name").html(html_string);
            $("#dependent_host_name").multiselect("refresh");
        });
        $("#host_name").bind("multiselectcheckall", function (event, ui) {
            $("#dependent_host_name").html("");
            $("#dependent_host_name").multiselect("refresh");
        });
        $("#host_name").bind("multiselectuncheckall", function (event, ui) {
            html_string = "";
            for (var i = 0; i < all_options.length; i++) {
                if (originally_selected.indexOf(all_options[i]) != -1)
                    html_string += "<option value=" + all_options[i] + " selected='selected' >" + all_indexes[i] + "</option>";
                else
                    html_string += "<option value=" + all_options[i] + " >" + all_indexes[i] + "</option>";
            }
            $("#dependent_host_name").html(html_string);
            $("#dependent_host_name").multiselect("refresh");
        });
    }
    catch (err) {
        //alert(err);
    }
}


function editHostdependency(hostdependency_name) {

    spinStart($spinLoading, $spinMainLoading);
    $("#host_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select hosts', minWidth: 230}).multiselectfilter();
    $("#dependent_host_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select dependent hosts', header: "Available hosts", minWidth: 230}).multiselectfilter();
    $("#notification_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select notification period', header: "Available notification periods", minWidth: 230});
    //$("#use").multiselect({selectedList: 1,multiple:true,noneSelectedText: 'Select templates',header:"Available templates",minWidth:230});
    //$("#check_command").multiselect({selectedList: 1,multiple:false,noneSelectedText: 'Select check command',header:"Available check commands",minWidth:230});
    $("#dependent_hostgroup_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select hostgroups', header: "Available hostgroups", minWidth: 230}).multiselectfilter();
    $("#notification_failure_criteria").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select notification options', minWidth: 230});
    $("#execution_failure_criteria").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select execution options', minWidth: 230});
    $("#inherits_parent").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select inherits parent', minWidth: 230});
    $("#dependency_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select dependency period', minWidth: 230});

    //$("#div_table_paginate").display("none");
    //$formEditButton.css({"display":"inline-block"});
    $.ajax({
        type: "get",
        url: "edit_nagios_hostdependency.py?hostdependency_name=" + hostdependency_name,
        cache: false,
        success: function (result) {
            //alert(result);
            spinStop($spinLoading, $spinMainLoading);
            result = eval("(" + result + ")");
            if (result.success == 0) {
                var form_id = "#edit_nagios_hostdependency_form";
                hostDetails = result.data;
                $("#div_table_paginate").css({"display": "none"});
                $("#edit_nagios_hostdependency_form").css({"display": "inline-block"});

                $("#hostdependency_name", form_id).val(hostdependency_name);

                fill_multiple_values_hostdependency(result.options, hostDetails, form_id);

                /////////////////


            }
            else {
                $().toastmessage('showErrorToast', 'Some error occured.');
            }
        }
    });
}

function addHostdependency() {

    $("#host_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select hosts', minWidth: 230}).multiselectfilter();
    $("#dependent_host_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select dependent hosts', header: "Available hosts", minWidth: 230}).multiselectfilter();
    $("#notification_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select notification period', header: "Available notification periods", minWidth: 230});
    //$("#use").multiselect({selectedList: 1,multiple:true,noneSelectedText: 'Select templates',header:"Available templates",minWidth:230});
    //$("#check_command").multiselect({selectedList: 1,multiple:false,noneSelectedText: 'Select check command',header:"Available check commands",minWidth:230});
    $("#dependent_hostgroup_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select hostgroups', header: "Available hostgroups", minWidth: 230}).multiselectfilter();
    $("#notification_failure_criteria").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select notification options', minWidth: 230});
    $("#execution_failure_criteria").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select execution options', minWidth: 230});
    $("#inherits_parent").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select inherits parent', minWidth: 230});
    $("#dependency_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select dependency period', minWidth: 230});

    //$("#div_table_paginate").display("none");
    //$formEditButton.css({"display":"inline-block"});
    $.ajax({
        type: "get",
        url: "edit_nagios_hostdependency.py?add_new=true",
        cache: false,
        success: function (result) {
            //alert(result);
            result = eval("(" + result + ")");
            if (result.success == 0) {
                var form_id = "#edit_nagios_hostdependency_form";
                hostDetails = result.data;
                $("#div_table_paginate").css({"display": "none"});
                $("#edit_nagios_hostdependency_form").css({"display": "inline-block"});

                $("#hostdependency_name", form_id).val("");

                fill_multiple_values_hostdependency(result.options, hostDetails, form_id);

            }
            else {
                $().toastmessage('showErrorToast', 'Some error occured.');
            }
        }
    });
}


function deleteHostDependencyCallback(v, m) {
    if (v != undefined && v == true) {

        spinStart($spinLoading, $spinMainLoading);
        var selectedRow = fnGetSelected(oTable);
        var rLength = selectedRow.length;
        var idStr = "";
        var usrStr = "";
        var selectedDeletedRowArray = [];
        for (var i = 0; i < selectedRow.length; i++) {
            var iRow = oTable.fnGetPosition(selectedRow[i]);
            var aData = oTable.fnGetData(iRow);
            if (i > 0) {
                idStr += ",";
                usrStr += ",";
            }
            idStr += String(aData[0]);
//			usrStr += String(aData[1]);
            selectedDeletedRowArray.push(iRow);
            // if delete successfully then call this function

        }
        var action = "nagios_delete_host_dependency.py";
        var data = "host_dependency_names=" + idStr;
        var method = "get";
        $.ajax({
            url: action,
            type: method,
            data: data,
            cache: false,
            success: function (result) {
                spinStop($spinLoading, $spinMainLoading);
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    for (var j = 0; j < selectedDeletedRowArray.length; j++)
                        oTable.fnDeleteRow(selectedDeletedRowArray[j]);
                    //alert("Deleted Successfully");
                    $().toastmessage('showSuccessToast', "Host dependency(s) Deleted Successfully.");
                    oTable.fnDraw();
                }
                else {
                    $().toastmessage('showWarningToast', result.result);
                }
            }
        });
        return false;

    }

}


function delHostDependency() {
    var selectedRow = fnGetSelected(oTable);
    var rLength = selectedRow.length;
    if (rLength == 0) {
        $.prompt("Select atleast one host dependency", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to delete this host dependency?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: deleteHostDependencyCallback });
    }
}

//////////////////////// hostdependency ends
////////////////////////////// servicedependency begins

function main_servicedependency() {

    $('#servicedependency_table_paginate tbody tr').live('click', function () {
        var id = this.id;
        var index = jQuery.inArray(id, aSelected);

        if (index === -1) {
            aSelected.push(id);
        } else {
            aSelected.splice(index, 1);
        }
        $(this).toggleClass('row_selected');
    });
    aSelected = [];
    oTable = $('#servicedependency_table_paginate').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "bServerSide": true,
        "bDestroy": true,
        "fnRowCallback": function (nRow, aData, iDisplayIndex) {
            if (jQuery.inArray(aData.DT_RowId, aSelected) !== -1) {
                $(nRow).addClass('row_selected');
            }
            return nRow;
        },
        "sAjaxSource": "get_servicedependency_data_nagios.py",
        "aaSorting": [
            [0, 'desc']
        ]
    });
    oTable.fnSetColumnVis(0, false, false);

    $("#close_edit_servicedependency").click(function () {
        $("#div_table_paginate").css({"display": "block"});
        $("#edit_nagios_servicedependency_form").css({"display": "none"});
    });
    $("#save_edit_servicedependency").click(function () {
        var form = $("#edit_nagios_servicedependency_form");
        if (form.valid()) {
            var method = form.attr("method");
            var action = form.attr("action");
            var data = form.serialize() + "&notification_failure_criteria=" + $("#notification_failure_criteria").val() + "&execution_failure_criteria=" + $("#execution_failure_criteria").val() + "&dependent_host_name=" + $("#dependent_host_name").val() + "&host_name=" + $("#host_name").val() + "&dependent_service_description=" + $("#dependent_service_description").val() + "&service_description=" + $("#service_description").val();
            $.ajax({
                type: method,
                url: action,
                data: data,
                cache: false,
                success: function (result) {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        $().toastmessage('showSuccessToast', "service dependency details saved successfully.");
                        //main_services();
                        $("#close_edit_servicedependency").click();
                        oTable.fnDraw();

                    }
                    else if (result.success == 1) {

                        $().toastmessage('showErrorToast', "Some error occurred(" + String(result.exception) + ")");
                    }
                }
            });
        }
    });


    $("#page_tip").colorbox(  			//page tip
        {
            href: "view_page_tip_nagios_servicedependency.py",
            title: "Page Tip",
            opacity: 0.4,
            maxWidth: "80%",
            width: "450px",
            height: "400px"
        });

    $("#edit_nagios_servicedependency_form").validate({
        rules: {
            host_name: {
                required: true//,
            },
            service_description: {
                required: true//,
            },
            dependent_host_name: {
                required: true//,
            },
            dependent_service_description: {
                required: true//,
            }
        },
        messages: {
            host_name: {
                required: "*"//,
            },
            service_description: {
                required: "*"//,
            },
            dependent_host_name: {
                required: "*"//,
            },
            dependent_service_description: {
                required: "*"//,
            }

        }
    });
}
function fill_multiple_values_servicedependency(result, hostDetails, form_id, host_service_json) {

    try {
        ////////////////////////// code for single or multi select
        //"check_command",
        json_var_array = ["host_name", "dependent_host_name", "dependent_hostgroup_name", "inherits_parent", "notification_failure_criteria", "execution_failure_criteria", "dependency_period", "service_description",
            "dependent_service_description"];
        corresponding_fields = ["#host_name", "#dependent_host_name", "#dependent_hostgroup_name", "#inherits_parent", "#notification_failure_criteria", "#execution_failure_criteria", "#dependency_period", "#service_description",
            "#dependent_service_description"];
        for (json_var = 0; json_var < json_var_array.length; json_var++) {
            var_name = json_var_array[json_var]; // use
            if (result[var_name] != undefined)// && hostDetails[var_name]!=undefined)
            {
                host_templates = result[var_name]; // list of host templates
                cur_selected_array = {};
                currently_selected_host_templates = hostDetails[var_name]; // selected list
                html_string = "";
                if (currently_selected_host_templates) {
                    if (currently_selected_host_templates.indexOf(",") != -1)
                        cur_selected_array = currently_selected_host_templates.split(",");
                }
                for (i = 0; i < host_templates.length; i++) {
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) {
                        for (k = 0; k < cur_selected_array.length; k++) {

                            //if(var_name=="host_name")
                            //alert("looping variable "+$.trim(cur_selected_array[k]));
                            //alert("user selected "+$.trim(host_templates[i][0])+$.trim(host_templates[i][1]));
                            if ($.trim(cur_selected_array[k]) == $.trim(host_templates[i][0]) || $.trim(cur_selected_array[k]) == $.trim(host_templates[i][1])) {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    if (flag)
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else if (host_templates[i][0] == currently_selected_host_templates || host_templates[i][1] == currently_selected_host_templates)
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + " selected='selected'>" + host_templates[i][1] + "</option>";
                    else
                        html_string += "<option value=" + $.trim(host_templates[i][0]) + ">" + host_templates[i][1] + "</option>";
                }
//				alert(html_string);
                $(corresponding_fields[json_var], form_id).html(html_string);
                $(corresponding_fields[json_var], form_id).multiselect("refresh");
            }
        }

        var sel = $("#host_name").val();
        //alert(sel_text);
        html_string = convert_service_description(sel, host_service_json, hostDetails, "service_description");
        $("#service_description").html(html_string);
        $("#service_description").multiselect("refresh");
        var sel = $("#dependent_host_name").val();
        html_string = convert_service_description(sel, host_service_json, hostDetails, "dependent_service_description");
        $("#dependent_service_description").html(html_string);
        $("#dependent_service_description").multiselect("refresh");

        $("#host_name").bind("multiselectclose", function (event, ui) {
            //var service_names=[];
            var sel = $("#host_name").val();
            //alert(sel_text);
            html_string = convert_service_description(sel, host_service_json, hostDetails, "service_description");
            $("#service_description").html(html_string);
            $("#service_description").multiselect("refresh");
        });
        $("#dependent_host_name").bind("multiselectclose", function (event, ui) {
//		        var service_names=[];
            var sel = $("#dependent_host_name").val();
            html_string = convert_service_description(sel, host_service_json, hostDetails, "dependent_service_description");
            $("#dependent_service_description").html(html_string);
            $("#dependent_service_description").multiselect("refresh");
        });

    }
    catch (err) {
        //alert(err);
    }
}
function convert_service_description(sel, host_service_json, hostDetails, service_description) {
    html_string = "";
    cur_selected_array = {};
    currently_selected_host_templates = hostDetails[service_description]; // selected list [sd1,sd2]
    if (currently_selected_host_templates) // not undefined
    {
        if (currently_selected_host_templates.indexOf(",") != -1)       // contains comma 
            cur_selected_array = currently_selected_host_templates.split(","); // make array 
    }
    var service_names = [];
    if (sel != null)// sel not null
    {
        temp_arr_sel = String(sel).split(",");// contains comma 
        for (j = 0; j < temp_arr_sel.length; j++) {
            temp_arr = host_service_json[temp_arr_sel[j]]; // get corresponding service for host
            for (i = 0; i < temp_arr.length; i++) {
                if (service_names.indexOf(temp_arr[i]) == -1)	//  if its a new service, not previously in service_names then 
                {

                    ////////// new code 
                    flag = 0;
                    if (currently_selected_host_templates && cur_selected_array.length > 0) // if selected list is an array 
                    {
                        for (k = 0; k < cur_selected_array.length; k++) {
                            if ($.trim(cur_selected_array[k]) == $.trim(temp_arr[i])) // if its present set flag to 1
                            {
                                flag = 1;
                                break;
                            }
                        }
                    }

                    ////////// new code ends

                    if (flag)//if(hostDetails[service_description]==temp_arr[i]) // if flag is set ie present in list
                        html_string += "<option selected='selected' value='" + temp_arr[i] + "'>" + temp_arr[i] + "</option>";
                    else if ($.trim(temp_arr[i]) == currently_selected_host_templates) // if no list 
                        html_string += "<option selected='selected' value='" + temp_arr[i] + "'>" + temp_arr[i] + "</option>";
                    else
                        html_string += "<option value='" + temp_arr[i] + "'>" + temp_arr[i] + "</option>";
                    service_names.push(temp_arr[i]); // insert in array service_names
                }

            }
        }
    }
    return html_string;
}

function editServicedependency(servicedependency_name) {

    spinStart($spinLoading, $spinMainLoading);
    $("#host_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select hosts', minWidth: 230}).multiselectfilter();
    $("#service_description").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select service', minWidth: 230});
    $("#dependent_service_description").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select dependent services', minWidth: 230});
    $("#dependent_host_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select dependent hosts', header: "Available hosts", minWidth: 230}).multiselectfilter();
    $("#notification_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select notification period', header: "Available notification periods", minWidth: 230});
    //$("#use").multiselect({selectedList: 1,multiple:true,noneSelectedText: 'Select templates',header:"Available templates",minWidth:230});
    //$("#check_command").multiselect({selectedList: 1,multiple:false,noneSelectedText: 'Select check command',header:"Available check commands",minWidth:230});
    $("#dependent_hostgroup_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select hostgroups', header: "Available hostgroups", minWidth: 230});
    $("#notification_failure_criteria").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select notification options', minWidth: 230});
    $("#execution_failure_criteria").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select execution options', minWidth: 230});
    $("#inherits_parent").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select inherits parent', minWidth: 230});
    $("#dependency_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select dependency period', minWidth: 230});

    //$("#div_table_paginate").display("none");
    //$formEditButton.css({"display":"inline-block"});
    $.ajax({
        type: "get",
        url: "edit_nagios_servicedependency.py?servicedependency_name=" + servicedependency_name,
        cache: false,
        success: function (result) {
            //alert(result);
            spinStop($spinLoading, $spinMainLoading);
            result = eval("(" + result + ")");
            if (result.success == 0) {
                var form_id = "#edit_nagios_servicedependency_form";
                hostDetails = result.data;
                host_service_json = result.host_service_json;
                $("#div_table_paginate").css({"display": "none"});
                $("#edit_nagios_servicedependency_form").css({"display": "inline-block"});

                $("#servicedependency_name", form_id).val(servicedependency_name);

                fill_multiple_values_servicedependency(result.options, hostDetails, form_id, host_service_json);

            }
            else {
                $().toastmessage('showErrorToast', 'Some error occured.');
            }
        }
    });
}

function addServicedependency() {
    $("#host_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select hosts', minWidth: 230}).multiselectfilter();
    $("#service_description").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select service', minWidth: 230});
    $("#dependent_service_description").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select dependent services', minWidth: 230});
    $("#dependent_host_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select dependent hosts', minWidth: 230}).multiselectfilter();
    $("#notification_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select notification period', minWidth: 230});
    //$("#use").multiselect({selectedList: 1,multiple:true,noneSelectedText: 'Select templates',header:"Available templates",minWidth:230});
    //$("#check_command").multiselect({selectedList: 1,multiple:false,noneSelectedText: 'Select check command',header:"Available check commands",minWidth:230});
    $("#dependent_hostgroup_name").multiselect({selectedList: 1, multiple: true, noneSelectedText: 'Select hostgroups', minWidth: 230});
    $("#notification_failure_criteria").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select notification options', minWidth: 230});
    $("#execution_failure_criteria").multiselect({selectedList: 4, multiple: true, noneSelectedText: 'Select execution options', minWidth: 230});
    $("#inherits_parent").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select inherits parent', minWidth: 230});
    $("#dependency_period").multiselect({selectedList: 1, multiple: false, noneSelectedText: 'Select dependency period', minWidth: 230});

    //$("#div_table_paginate").display("none");
    //$formEditButton.css({"display":"inline-block"});
    $.ajax({
        type: "get",
        url: "edit_nagios_servicedependency.py?addnew=true",
        cache: false,
        success: function (result) {
            //alert(result);
            result = eval("(" + result + ")");
            if (result.success == 0) {
                var form_id = "#edit_nagios_servicedependency_form";
                hostDetails = result.data;
                host_service_json = result.host_service_json;
                $("#div_table_paginate").css({"display": "none"});
                $("#edit_nagios_servicedependency_form").css({"display": "inline-block"});

                $("#servicedependency_name", form_id).val("");

                fill_multiple_values_servicedependency(result.options, hostDetails, form_id, host_service_json);

            }
            else {
                $().toastmessage('showErrorToast', 'Some error occured.');
            }
        }
    });
}


function deleteServiceDependencyCallback(v, m) {
    if (v != undefined && v == true) {

        spinStart($spinLoading, $spinMainLoading);
        var selectedRow = fnGetSelected(oTable);
        var rLength = selectedRow.length;
        var idStr = "";
        var usrStr = "";
        var selectedDeletedRowArray = [];
        for (var i = 0; i < selectedRow.length; i++) {
            var iRow = oTable.fnGetPosition(selectedRow[i]);
            var aData = oTable.fnGetData(iRow);
            if (i > 0) {
                idStr += ",";
                usrStr += ",";
            }
            idStr += String(aData[0]);
//			usrStr += String(aData[1]);
            selectedDeletedRowArray.push(iRow);
            // if delete successfully then call this function

        }
        var action = "nagios_delete_service_dependency.py";
        var data = "service_dependency_names=" + idStr;
        var method = "get";
        $.ajax({
            url: action,
            type: method,
            data: data,
            cache: false,
            success: function (result) {
                spinStop($spinLoading, $spinMainLoading);
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    for (var j = 0; j < selectedDeletedRowArray.length; j++)
                        oTable.fnDeleteRow(selectedDeletedRowArray[j]);
                    //alert("Deleted Successfully");
                    $().toastmessage('showSuccessToast', "Service dependency(s) Deleted Successfully.");
                    oTable.fnDraw();
                }
                else {
                    $().toastmessage('showWarningToast', result.result);
                }
            }
        });
        return false;

    }

}


function delServiceDependency() {
    var selectedRow = fnGetSelected(oTable);
    var rLength = selectedRow.length;
    if (rLength == 0) {
        $.prompt("Select atleast one service dependency", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to delete this service dependency?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: deleteServiceDependencyCallback });
    }
}

//////////////////////// servicedependency ends


function fnGetSelected(oTableLocal) {
    var aReturn = new Array();
    var aTrs = oTableLocal.fnGetNodes();
    for (var i = 0; i < aTrs.length; i++) {
        if ($(aTrs[i]).hasClass('row_selected')) {
            aReturn.push(aTrs[i]);
        }
    }
    return aReturn;
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function multiSelectColumns() {
    click_check();

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
    click_check();
}
function click_check() {
    $("#more_options_columns li").click(function (e) {
        // e.stopPropagation();
        e.stopImmediatePropagation();
        if ($(this).find("img").hasClass("minus"))
            if ($(this).hasClass("clicked"))
                $(this).removeClass("clicked");
            else {
                $(this).addClass("clicked");
                $(this).siblings().removeClass("clicked");
            }

    });
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
