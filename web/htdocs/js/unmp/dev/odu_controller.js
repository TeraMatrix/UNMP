var ruConfigForm = null;
var formObjIP = null;
var btnIp = null;
var formObjRUConfig = null;
var btnRuConfig = null;
var $spinLoading = null;
var $spinMainLoading = null;
var aclClickReconcile = null
var reconcile_chk_status_btn = null;
var timeSlot = 60000;
var ruState = null;
var formObjAcl = null;
var btnAcl = null;
var timecheck = 60000;
var timeGlobal = 10000;
var ipMacChange = 0;
var callB = null;
var ping_chk = 0;
var odu100_ru_channel_banwidth = null;
var odu100_ru_country_code = null;
var opStatusDic = {
    0: 'No operation',
    1: 'Firmware download',
    2: 'Firmware upgrade',
    3: 'Restore default config',
    4: 'Flash commit',
    5: 'Reboot',
    6: 'Site survey',
    7: 'Calculate BW',
    8: 'Uptime service',
    9: 'Statistics gathering',
    10: 'Reconciliation',
    11: 'Table reconciliation',
    12: 'Set operation',
    13: 'Live monitoring',
    14: 'Status capturing',
    15: 'Refreshing Site Survey',
    '16': 'Refreshing RA Channel List'
}
var channelNumber = null;
var calculate = null;
var listOfChannels = null;
var text_name = null;
var aclReconcile = true;

function resultDiv(resultJson, rDiv) {
    var resultArray = resultJson.result;
    var status = 1;
    var resultString = "";
    for (var i = 0; i < resultArray.length; i++) {
        var json = resultArray[i];
        var image = json.status == "1" || json.status == 1 ? "<img src=\"images/done.png\" alt=\"Done\" title=\"Done\" />" : "<img class=\"imgbutton\" src=\"images/alert_restart.png\" alt=\"Retry\" title=\"Retry\" table=\"" + resultJson.tableName + "\" textbox=\"" + json.textbox + "\" onclick=\"retrySet(this)\" style=\"height:20px;width:20px;\"  />"
        resultString += "<div class=\"row-elem\"><label class=\"lbl lbl-big\">" + json.name + "</label><label class=\"lbl lbl-big\">" + json.value + "</label>" + image + "</div>"
        if (json.status == 0 || json.status == "0") {
            status = 0;
        }
    }
    if (status == 0) {
        resultString += "<div class=\"row-elem\" style=\"clear:both;\"><input table=\"" + resultJson.tableName + "\" type=\"button\" class=\"retry yo-small yo-button\" value=\"Retry\" onclick=\"retryAllSet(this)\" /><input type=\"button\" value=\"Cancel\" onclick=\"cancelResult('" + resultJson.formAction + "',this);\" class=\"yo-small yo-button\"></div>"
    } else {
        resultString += "<div class=\"row-elem\" style=\"clear:both;\"><input type=\"button\" value=\"Ok\" onclick=\"resultOk(this);\" style=\"width:70px;\" class=\"yo-small yo-button\"/></div>";
    }
    $(rDiv).html(resultString);
    $(rDiv).show();
}

function retrySet(objId) {
    var retryBtnObj = $(objId);
    var host_id = $("input[id='host_id']").val();
    var textBox = retryBtnObj.attr("textbox");
    var tableName = $("input[id='" + textBox + "']").attr("tablename") != undefined ? $("input[id='" + textBox + "']").attr("tablename") : $("select[id='" + textBox + "']").attr("tablename");
    var textBoxValue = $("input[id='" + textBox + "']").val() != undefined ? $("input[id='" + textBox + "']").val() : $("select[id='" + textBox + "']").val();
    var textBoxField = $("input[id='" + textBox + "']").attr("field") != undefined ? $("input[id='" + textBox + "']").attr("field") : $("select[id='" + textBox + "']").attr("field");
    var index = $("input[id='" + textBox + "']").attr("index");
    retryBtnObj.attr("src", "images/icon_reloading.gif");
    $.ajax({
        type: "post",
        url: "retry_set_for_odu16.py?table_name=" + tableName + "&textbox=" + textBox + "&textbox_value=" + textBoxValue + "&textbox_field=" + textBoxField + "&index=" + index + "&host_id=" + host_id,
        success: function (result) {
            if (result == 0 || result == "0") {
                retryBtnObj.removeAttr("onclick");
                retryBtnObj.removeAttr("style");
                retryBtnObj.attr({
                    "src": "images/done.png",
                    "title": "Done",
                    "alt": "Done"
                });
                checkAllDone(objId);


            } else {
                $().toastmessage('showErrorToast', "Not Done, retry again.");
                retryBtnObj.attr("src", "images/alert_restart.png");
            }
        }
    })
}

function checkAllDone(objId) {
    var checkbtn = $(objId);
    var mainDiv = $(objId).parent().parent().parent();
    var totalRetry = mainDiv.find("img[alt='Retry']").size();
    if (totalRetry <= 1) {
        $(objId).parent().parent().find("input.retry").parent().html("<input type=\"button\" value=\"Ok\" onclick=\"resultOk(this);\" style=\"width:70px;\" class=\"yo-small yo-button\" />");
    }
}

function retryAllSet(objId) {

    var retryBtnObj = $(objId);
    var host_id = $("input[id='host_id']").val();
    var tableNameArray = new Array();
    var textBoxArray = new Array();
    var textBoxField = new Array();
    var textBoxValue = new Array();
    var indexArray = new Array();
    var retryBtns = retryBtnObj.parent().parent().find("img[alt='Retry']");
    spinStart($spinLoading, $spinMainLoading);
    for (var retry_i = 0; retry_i < retryBtns.size(); retry_i++) {

        tableNameArray.push($("input[id='" + retryBtns.eq(retry_i).attr("textbox") + "']").attr("tablename") != undefined ? $("input[id='" + retryBtns.eq(retry_i).attr("textbox") + "']").attr("tablename") : $("select[id='" + retryBtns.eq(retry_i).attr("textbox") + "']").attr("tablename"));


        textBoxArray.push(retryBtns.eq(retry_i).attr("textbox"));


        textBoxField.push($("input[id='" + retryBtns.eq(retry_i).attr("textbox") + "']").attr("field") != undefined ? $("input[id='" + retryBtns.eq(retry_i).attr("textbox") + "']").attr("field") : $("select[id='" + retryBtns.eq(retry_i).attr("textbox") + "']").attr("field"));


        textBoxValue.push($("input[id='" + retryBtns.eq(retry_i).attr("textbox") + "']").val() != undefined ? $("input[id='" + retryBtns.eq(retry_i).attr("textbox") + "']").val() : $("select[id='" + retryBtns.eq(retry_i).attr("textbox") + "']").val());


        indexArray.push($("input[id='" + retryBtns.eq(retry_i).attr("textbox") + "']").attr("index"));

    }
    $.ajax({
        type: "post",
        url: "retry_set_all_for_odu16.py?table_name=" + String(tableNameArray) + "&textbox_name=" + String(textBoxArray) + "&textbox_field=" + String(textBoxField) + "&textbox_value=" + String(textBoxValue) + "&index=" + String(indexArray) + "&host_id=" + host_id,
        success: function (result) {
            try {

                result = eval("(" + result + ")");

                var mainDiv = retryBtnObj.parent().parent();
                var allSet = 0;
                for (var tbI = (textBoxArray.length - 1); tbI >= 0; tbI--) {
                    if (result[textBoxArray[tbI]] == "0" || result[textBoxArray[tbI]] == 0) {
                        var imgBtn = mainDiv.find("img[textbox='" + textBoxArray[tbI] + "']");
                        imgBtn.removeAttr("onclick");
                        imgBtn.removeAttr("style");
                        imgBtn.attr({
                            "src": "images/done.png",
                            "title": "Done",
                            "alt": "Done"
                        });
                        spinStop($spinLoading, $spinMainLoading);
                    } else {
                        allSet = 1;
                        spinStop($spinLoading, $spinMainLoading);
                    }
                }
                if (allSet == 0) {
                    retryBtnObj.parent().html("<input type=\"button\" value=\"Ok\" onclick=\"resultOk(this);\" style=\"width:70px;\" class=\"yo-small yo-button\" />");
                    spinStop($spinLoading, $spinMainLoading);
                }
            } catch (err) {
                $().toastmessage('showWarningToast', "Device is rebooting.Please Wait.");

                spinStop($spinLoading, $spinMainLoading);
            }
        }

    });

}

function cancelResult(actionUrl, objId) {
    var host_id = $("input[id='host_id']").val();
    $.ajax({
        type: "post",
        url: "cancel_odu_form.py?action_name=" + actionUrl + "&host_id=" + host_id,
        //url:actionUrl+"?host_id=" + host_id,
        success: function (result) {
            var mainDiv = $(objId).parent().parent().parent();
            if (actionUrl == "omc_config_form.py") {
                mainDiv.find("form").remove();
                mainDiv.find("div#result_omc_config").hide();
                mainDiv.append(result);
                omcConfiguration();
                omcConfigurationForm();
            } else if (actionUrl == "RU_Cancel_Configuration.py") {
                mainDiv.find("form").remove();
                mainDiv.find("div#result_ru_config").hide();
                mainDiv.append(result);
                ruConfigurationconfirmCheck();
            } else if (actionUrl == "RU_Cancel_Date_Time.py") {
                mainDiv.find("form").remove();
                mainDiv.find("div#").hide();
                mainDiv.append(result);
                dateTime();
                oduRuDateTimeForm();

            } else if (actionUrl == "Tdd_Mac_Cancel_Configuration.py") {
                mainDiv.find("form").remove();
                mainDiv.find("div#tdd_mac_config").hide();
                mainDiv.append(result);
                tddMacConfiguration();
                tddMacConfigForm();
            } else if (actionUrl == "ip_packet_filter.py") {
                mainDiv.find("form").remove();
                mainDiv.find("div#").hide();
                mainDiv.append(result);
                ipPacketFilter();
            } else if (actionUrl == "mac_packet_filter.py") {
                mainDiv.find("form").remove();
                mainDiv.find("div#").hide();
                mainDiv.append(result);
                macPacketFilter();
            } else if (actionUrl == "packet_filter_mode.py") {
                mainDiv.find("form").remove();
                mainDiv.find("div#").hide();
                mainDiv.append(result);
                packetFilterMode();
            } else if (actionUrl == "Llc_Cancel_Configuration.py") {
                mainDiv.find("form").remove();
                mainDiv.find("div#").hide();
                mainDiv.append(result);
                llcConfiguration();
                raLlcConfigForm();
            } else if (actionUrl == "sys_registration_form.py") {
                mainDiv.find("form").remove();
                mainDiv.find("div#result_sys_omc_config").hide();
                mainDiv.append(result);
                omcRegistration();
                omcRegistrationForm();
            } else if (actionUrl == "Syn_Cancel_Omc_Registration_Configuration.py") {
                mainDiv.find("form").remove();
                mainDiv.find("div#result_syn_omc_config").hide();
                mainDiv.append(result);
                synConfiguration();
                synConfigurationForm();
            } else if (actionUrl == "Peer_mac_Cancel.py") {
                mainDiv.find("form").remove();
                mainDiv.find("div#peer_mac_config").hide();
                mainDiv.append(result);
                peerConfigForm();
            } else if (actionUrl == "Acl_Cancel_Configuration.py") {
                mainDiv.find("form").remove();
                mainDiv.find("div#result_acl_config").hide();
                mainDiv.append(result);
                aclConfigForm();
                aclAddMore();
            }
        }
    })
}

function filterEverything() {
    omcConfiguration();
    omcConfigurationForm();
    ruConfigurationconfirmCheck();
    dateTime();
    oduRuDateTimeForm();
    omdNetworkInterfaceConfigForm();
    tddMacConfiguration();
    tddMacConfigForm();
    llcConfiguration();
    ipPacketFilter();
    macPacketFilter();
    packetFilterMode();
    raLlcConfigForm();
    omcRegistration();
    omcRegistrationForm();
    synConfiguration();
    synConfigurationForm();
    raConfigForm();
    peerMacValid();
    peerConfigForm();
    aclConfigForm();
    aclAddMore();
}

function filterRadioUnit() {
    ruConfigurationconfirmCheck();
    dateTime();
    oduRuDateTimeForm();
    omcConfiguration();
    omcConfigurationForm();
    omcRegistration();
    omcRegistrationForm();
}

function filterSync() {
    synConfiguration();
    synConfigurationForm();
}

function filterRadioUnit() {
    aclConfigForm();
    aclAddMore();
    tddMacConfiguration();
    tddMacConfigForm();
    llcConfiguration();
    raLlcConfigForm();
}

function filterPeer() {
    peerMacValid();
    peerConfigForm();
}

function resultOk(objId) {
    var mainDiv = $(objId).parent().parent().parent();
    mainDiv.find("form").show();
    $("div#result_omc_config").hide();
    $("div#result_ru_config").hide();
    $("div#result_sys_omc_config").hide();
    $("div#result_syn_omc_config").hide();
    $("div#result_acl_config").hide();
    $("div#tdd_mac_config").hide();
    $("div#result_llc_config").hide();
    $("div#peer_mac_config").hide();
}

function filterAction() {
    $('.filterBtn').click(function () {
        var id = $(this).attr("id");
        if (id == 'syncFilter') {

            $("#list li").hide();
            var target = $("#list li[class='Sync']");
            target.show();
        } else if (id == 'radioUnitFilter') {

            $("#list li").hide();
            var target = $("#list li[class='RU']");
            target.show();
        } else if (id == 'radioAccessFilter') {

            $("#list li").hide();
            var target = $("#list li[class='RA']");
            target.show();
        } else if (id == 'peerFilter') {

            $("#list li").hide();
            var target = $("#list li[class='Peer']");
            target.show();
        } else {
            $("#list li").show();
        }
    });
}


function omcConfigurationForm() {
    $("#omc_configuration_form").submit(function () {
        var host_id = $("input[id='host_id']").val();
        var myForm = $(this);
        var url = $(this).attr("action");
        var method = $(this).attr("method");
        var data = $(this).serialize();
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
            if ($(this).valid()) {
                spinStart($spinLoading, $spinMainLoading);
                $.ajax({
                    type: method,
                    url: url + "?host_id=" + host_id,
                    data: data,
                    success: function (result) {
                        try {
                            result = eval("(" + result + ")");
                            resultDiv(result, "#result_omc_config");
                            myForm.hide();
                        } catch (err) {
                            $().toastmessage('showErrorToast', "Some Problem Occured.Contact Administrator");
                        }
                        spinStop($spinLoading, $spinMainLoading);
                    }
                });
            }
        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }
        return false;
    });
}

function ruConfigurationconfirmCheck() {
    $("#ru_configuration_form").submit(function () {
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
            ruConfigForm = $(this);
            $.prompt('Setting these values will cause Reboot.\n Are you sure you want to do this?', {
                buttons: {
                    Ok: true,
                    Cancel: false
                },
                prefix: 'jqismooth',
                callback: ruConfigurationForm
            });

        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }
        return false;
    });


}

function ruConfigurationForm(v, m) {
    if (v != undefined && v == true && ruConfigForm) {
        spinStart($spinLoading, $spinMainLoading);
        var host_id = $("input[id='host_id']").val();
        var myForm = ruConfigForm;
        var url = ruConfigForm.attr("action");
        var method = ruConfigForm.attr("method");
        var data = ruConfigForm.serialize();
        $.ajax({
            type: method,
            url: url + "?host_id=" + host_id,
            data: data,
            success: function (result) {
                try {
                    result = eval("(" + result + ")");
                    resultDiv(result, "#result_ru_config");
                    myForm.hide();
                } catch (err) {
                    $().toastmessage('showErrorToast', "Device is not Connected.");
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
        return false;
    }
}

function oduRuDateTimeForm() {
    $("#odu_ru_date_time_form").submit(function () {
        var host_id = $("input[id='host_id']").val();
        var myForm = $(this);
        var url = $(this).attr("action");
        var method = $(this).attr("method");
        var data = $(this).serialize();
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
            if ($(this).valid()) {
                spinStart($spinLoading, $spinMainLoading);
                $.ajax({
                    type: method,
                    url: url + "?host_id=" + host_id,
                    data: data,
                    success: function (result) {
                        try {
                            result = eval("(" + result + ")");
                            resultDiv(result, "#result_ru_date_time")
                            myForm.hide();
                        } catch (err) {
                            $().toastmessage('showErrorToast', "Device is not Connected.");

                        }
                        spinStop($spinLoading, $spinMainLoading);
                    }
                });
            }
            return false;
        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }

    });
}

function omdNetworkInterfaceConfigForm() {
    $("#omd_network_interface_config_form").submit(function () {
        var url = $(this).attr("action");
        var method = $(this).attr("method");
        var data = $(this).serialize();
        $.ajax({
            type: method,
            url: url,
            data: data,
            success: function (result) {
                $().toastmessage('showSuccessToast', result);
            }
        });
        return false;
    });
}

function tddMacConfigForm() {
    $("#tdd_mac_config_form").submit(function () {
        var host_id = $("input[id='host_id']").val();
        var myForm = $(this);
        var url = $(this).attr("action");
        var method = $(this).attr("method");
        var data = $(this).serialize();
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
            if ($(this).valid()) {
                spinStart($spinLoading, $spinMainLoading);
                $.ajax({
                    type: method,
                    url: url + "?host_id=" + host_id,
                    data: data,
                    success: function (result) {
                        try {
                            result = eval("(" + result + ")");
                            resultDiv(result, "#tdd_mac_config");
                            myForm.hide();
                        } catch (err) {
                            $().toastmessage('showErrorToast', "Device is not Connected.");

                        }
                        spinStop($spinLoading, $spinMainLoading);
                    }
                });
            }
        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }
        return false;
    });
}

function raLlcConfigForm() {
    $("#ra_llc_config_form").submit(function () {
        var host_id = $("input[id='host_id']").val();
        var myForm = $(this);
        var url = $(this).attr("action");
        var method = $(this).attr("method");
        var data = $(this).serialize();
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
            if ($(this).valid()) {
                spinStart($spinLoading, $spinMainLoading);
                $.ajax({
                    type: method,
                    url: url + "?host_id=" + host_id,
                    data: data,
                    success: function (result) {
                        try {
                            result = eval("(" + result + ")");
                            resultDiv(result, "#result_llc_config");
                            myForm.hide();
                        } catch (err) {
                            $().toastmessage('showErrorToast', "Device is not Connected.");
                        }
                        spinStop($spinLoading, $spinMainLoading);
                    }
                });
            }
        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }
        return false;
    });
}

function omcRegistrationForm() {
    $("#omc_registration_form").submit(function () {
        var host_id = $("input[id='host_id']").val();
        var myForm = $(this);
        var url = $(this).attr("action");
        var method = $(this).attr("method");
        var data = $(this).serialize();
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
            if ($(this).valid()) {
                spinStart($spinLoading, $spinMainLoading);
                $.ajax({
                    type: method,
                    url: url + "?host_id=" + host_id,
                    data: data,
                    success: function (result) {
                        try {
                            result = eval("(" + result + ")");
                            resultDiv(result, "#result_sys_omc_config");
                            myForm.hide();
                        } catch (err) {
                            $().toastmessage('showErrorToast', "Device is not Connected.");
                        }
                        spinStop($spinLoading, $spinMainLoading);
                    }
                });
            }
        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }
        return false;
    });
}

function synConfigurationForm() {
    $("#syn_configuration_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves']").change(function () {
        var numslaves = $("#syn_configuration_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves']").val();
        $("#peer_config_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves'] option[value='" + numslaves + "']").attr("selected", true);
    })
    $("#syn_configuration_form").submit(function () {
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
            var host_id = $("input[id='host_id']").val();
            var myForm = $(this);
            var url = $(this).attr("action");
            var method = $(this).attr("method");
            var data = $(this).serialize();
            if ($(this).valid()) {
                spinStart($spinLoading, $spinMainLoading);
                var numslaves = $(this).find("select[id='RU.SyncClock.SyncConfigTable.numSlaves']").val();
                var data_slaves = $(this).find("input[id='database_slaves']").val();
                if (parseInt(numslaves) < parseInt(data_slaves)) {
                    if (confirm("Are You Sure You Want To delete the slaves value")) {
                        spinStart($spinLoading, $spinMainLoading);
                        $.ajax({
                            type: method,
                            url: "peer_delete_slaves.py?host_id=" + host_id,
                            data: data,
                            success: function (result) {
                                try {
                                    //console.log(result)
                                    result = eval("(" + result + ")");
                                    resultDiv(result, "#result_syn_omc_config");
                                    myForm.hide();
                                    $("input[id='database_slaves']").val(numslaves);
                                    for (i = (numslaves); i < 8; i++) {
                                        $("#peer_config_form").find("input[id='ru.np.ra.1.peer." + (parseInt(i) + 1) + ".config.macAddress']").val("");
                                    }
                                } catch (err) {
                                    $().toastmessage('showErrorToast', "Device is not Connected.");
                                    spinStop($spinLoading, $spinMainLoading);
                                }
                            }
                        });
                    } else {
                        $().toastmessage('showErrorToast', "Your Parameters are not saved.");
                        spinStop($spinLoading, $spinMainLoading);
                    }
                } else {
                    $.ajax({
                        type: method,
                        url: url + "?host_id=" + host_id,
                        data: data,
                        success: function (result) {
                            try {
                                result = eval("(" + result + ")");
                                resultDiv(result, "#result_syn_omc_config");
                                spinStop($spinLoading, $spinMainLoading);
                                myForm.hide();
                            } catch (err) {
                                $().toastmessage('showErrorToast', "Device is not connected.");
                                spinStop($spinLoading, $spinMainLoading);
                            }
                        }
                    });
                }
            }
        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }
        return false;
    });
}

function raConfigForm() {
    $("#ra_config_form").submit(function () {
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
            var host_id = $("input[id='host_id']").val();
            var url = $(this).attr("action");
            var method = $(this).attr("method");
            var data = $(this).serialize();
            $.ajax({
                type: method,
                url: url + "?host_id=" + host_id,
                data: data,
                success: function (result) {
                    $().toastmessage('showSuccessToast', result);
                }
            });
        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }
        return false;
    });
}

function peerConfigForm() {
    $("#peer_config_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves']").change(function () {
        var numslaves = $("#peer_config_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves']").val();
        $("#syn_configuration_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves'] option[value='" + numslaves + "']").attr("selected", true);
    })
    $("#peer_config_form").submit(function () {
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
            if ($(this).valid()) {
                var numslaves = $("#peer_config_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves']").val();
                $("#syn_configuration_form").find("input[id='database_slaves']").val(numslaves);
                var host_id = $("input[id='host_id']").val();
                var myForm = $(this);
                var url = $(this).attr("action");
                var method = $(this).attr("method");
                var data = $(this).serialize();
                if ($(this).valid()) {
                    spinStart($spinLoading, $spinMainLoading);
                    $.ajax({
                        type: method,
                        url: url + "?host_id=" + host_id,
                        data: data,
                        success: function (result) {
                            if (result == 'Timeslot is smaller than the number of slaves you want to fill') {
                                $().toastmessage('showErrorToast', result);
                            } else {
                                result = eval("(" + result + ")");
                                resultDiv(result, "#peer_mac_config");
                                myForm.hide();
                            }
                            spinStop($spinLoading, $spinMainLoading);
                        }
                    });
                }
            }
        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }
        return false;
    });
}

function aclConfigForm() {
    $("#acl_config_form").submit(function () {
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
            var host_id = $("input[id='host_id']").val();
            spinStart($spinLoading, $spinMainLoading);
            var myForm = $(this);
            var url = $(this).attr("action");
            var method = $(this).attr("method");
            var data = $(this).serialize();
            $.ajax({
                type: method,
                url: url + "?host_id=" + host_id,
                data: data,
                success: function (result) {
                    try {
                        result = eval("(" + result + ")");
                        resultDiv(result, "#result_acl_config");
                        myForm.hide();
                    } catch (err) {
                        $().toastmessage('showErrorToast', 'Device is Not Connected');

                    }
                    spinStop($spinLoading, $spinMainLoading);
                }
            });
        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }
        return false;
    });
}

function aclAddMore() {
    $("#aclAddMore").click(function (e) {
        e.preventDefault();
        var totalMacDiv = $(this).parent().parent().find("div.row-elem").size() - 3;
        var hiddenVal = $("#acl_count");
        hiddenVal.val(totalMacDiv);
        var nextMac = parseInt(hiddenVal.val()) + 1;
        var textBoxName = "RU.RA.1.RAACLConfig." + nextMac + ".macAddress";
        var textBoxId = "RU.RA.1.RAACLConfig." + nextMac + ".macAddress";
        var textBoxFact = ".1.3.6.1.4.1.26149.2.2.13.5.1.2.1." + nextMac;
        var textBoxIndex = nextMac;
        var textBoxValue = "";
        var divStr = $("#acl_row_element_10").clone(); //.attr("name"+textBoxName,"id"+textBoxId,"fact"+textBoxFact,"val"+textBoxVal,"value"+textBoxValue);;
        divStr.attr("id", "acl_row_element_" + nextMac);
        divStr.find("label").html("Mac Address " + String(nextMac));
        divStr.find("input").attr({
            "name": textBoxName,
            "id": textBoxId,
            "fact": textBoxFact,
            "value": textBoxValue,
            "index": textBoxIndex
        });
        divStr.append("<img onclick=\"deleteAclConfigMacAddress(" + nextMac + ")\" class=\"imgbutton\" title=\"Delete\" alt=\"Delete\" src=\"images/delete16.png\">");
        divStr.insertBefore($(this).parent());
        hiddenVal.val(nextMac);
    })
}


function chkCommitToFlash() {
    $.prompt('Do you want to store configuration data permanently on the device?\n Click Ok to confirm.', {
        buttons: {
            Ok: true,
            Cancel: false
        },
        prefix: 'jqismooth',
        callback: commitToFlash
    });
}

function commitToFlash(v, m) {
    if (v != undefined && v == true) {
        var host_id = $("input[name='host_id']").val();
        if (host_id == undefined || host_id == "") {
            host_id = $("input[name='host_id']").val();
        }

        var device_type_id = $("input[name='device_type']").val();
        spinStart($spinLoading, $spinMainLoading);
        try {
            $.ajax({
                type: "get",
                url: "commit_flash.py?host_id=" + host_id + "&device_type_id=" + device_type_id,
                success: function (result) {
                    if (result == "Device is not connected or Device is Rebooting.Please Retry Again.") {
                        $().toastmessage('showErrorToast', result);
                    } else if (result.search("Device is busy") != -1) {
                        $().toastmessage('showErrorToast', result);
                    } else {
                        $().toastmessage('showSuccessToast', result);
                    }
                    setTimeout(function () {
                        spinStop($spinLoading, $spinMainLoading);
                    }, 5000);
                }
            });
        } catch (err) {
            spinStop($spinLoading, $spinMainLoading);
            $().toastmessage('showErrorToast', err);

        }
    }

}


function deviceList() {
    $spinLoading = $("div#spin_loading"); // create object that hold loading circle
    $spinMainLoading = $("div#main_loading"); // create object that hold loading squire
    var device_type = "odu16,odu100";
    // this retreive the value of ipaddress textbox
    var ip_address = $("input[id='filter_ip']").val();
    // this retreive the value of macaddress textbox
    var mac_address = $("input[id='filter_mac']").val();
    // this retreive the value of selectdevicetype from select menu
    var selected_device_type = $("select[id='device_type']").val();
    spinStart($spinLoading, $spinMainLoading);
    urlString = ""
    if (selected_device_type == "idu4") {
        parent.main.location = "idu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + selected_device_type;
    } else if (selected_device_type == "ap25") {
        parent.main.location = "ap_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + selected_device_type;
    } else if (selected_device_type == "ccu") {
        parent.main.location = "ccu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&device_type=" + selected_device_type;
    } else {
        // this ajax return the call to function get_device_data_table which is in odu_view and pass the ipaddress,macaddress,devicetype with url
        $.ajax({
            type: "post",
            url: "get_device_list_odu.py?&ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type,
            success: function (result) {
                if (result == 0 || result == "0") {
                    //$("#odu16_form_div").html("No profiling exist");
                    $().toastmessage('showWarningToast', "Searched Device Doesn't Exist");
                    parent.main.location = "odu_listing.py?ip_address=" + "" + "&mac_address=" + "" + "&selected_device_type=" + "";
                    //$(".form-div-footer").hide();
                } else if (result == 1 || result == "1") {
                    parent.main.location = "odu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type;

                } else if (result == 2 || result == "2") {

                    $("#odu16_form_div").html("Please Try Again");
                    $(".form-div-footer").hide();
                } else {
                    $("#odu16_form_div").html(result);
                    if (ipMacChange == 1) {
                        if (selected_device_type == "odu16") {
                            $(".form-div-footer").find("#operationDiv").html("");
                            html_str = "<input type='button' id='RU.RUOMOperationsTable.omOperationsReq' name='odu16_commit_to_flash' value='Commit To Flash' class='yo-small yo-button'/><input type='button' id='odu16_reconcile' name='odu16_reconcile' value='Reconciliation' class='yo-small yo-button'/>"

                        } else {
                            html_str = "<input type='button' id='RU.RUOMOperationsTable.omOperationsReq' name='odu16_commit_to_flash' value='Commit To Flash' class='yo-small yo-button' host_id='" + $("input[name='host_id']").val() + "'/><input type='button' id='odu_reboot' name='odu_reboot' value='Reboot' class='yo-small yo-button'/><input type='button' id='odu16_reconcile' name='odu16_reconcile' value='Reconciliation'  class='yo-small yo-button'/><input type='button' id='site_survey_btn' name='site_survey_btn' value='Site Survey Results' class='yo-small yo-button' onClick='siteSurvey();'/><input type='button' id='bw_calculator_form' name='bw_calculator_form' value='BW Calculator' class='yo-small yo-button'  />"
                        }
                        $("input[name='device_type']").val(selected_device_type);
                        $(".form-div-footer").find("#operationDiv").html(html_str);
                        if (selected_device_type == "odu16") {
                            $("#header3_text").text(ip_address + " " + "RM18" + " Configuration");
                        } else {
                            $("#header3_text").text(ip_address + " " + "RM" + " Configuration");
                        }

                        globalAdminStatus();
                        ipMacChange = 0;
                    }

                    $(".form-div-footer").show();
                    var ddd = $("table#show_mac_edit_delete").dataTable({
                        "bDestroy": true,
                        "bJQueryUI": true,
                        "bProcessing": true,
                        "sPaginationType": "full_numbers",
                        "aLengthMenu": [
                            [20, 40, 60, -1],
                            [20, 40, 60, "All"]
                        ],
                        "iDisplayLength": 20,
                        "aaSorting": []
                    });
                    odu_profiling();
                    $('.n-reconcile').tipsy({
                        gravity: 'n'
                    });
                    ruState = $("select[id='ru.ruConfTable.synchSource']").val()
                    $("input[name='node_type']").val(ruState);
                    $("div#config_tabs", "div#container_body").yoTabs();
                    $("div#sub_config_tabs", "div#container_body").yoTabs();
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });

    }
}

function globalAdminStatus() {
    var host_id = $("input[name='host_id']").val();
    if (ipMacChange == 1) {
        clearTimeout(callB);

    }
    if (host_id == undefined) {
        clearTimeout(callB);
        callB = setTimeout(function () {
            globalAdminStatus();

        }, 1000);
    } else {
        $.ajax({
            type: "get",
            url: "global_admin_status.py?host_id=" + host_id,
            success: function (result) {
                if (parseInt(result.success) == 0) {
                    json = result.result;
                    for (var node in json) {
                        var recTableObj = $("#adminDiv")
                        var objTable = $(recTableObj);
                        if (parseInt(json[node][0]) == 1 && parseInt(json[node][6]) == 0) {
                            var imgRec = $(recTableObj).find("a:eq(0)");
                            var imgbtn = $(imgRec);
                            imgbtn.html("RU State Unlocked");
                            imgbtn.attr({
                                "original-title": "RU State Unlocked"
                            });
                            imgbtn.attr({
                                "class": "red"
                            });
                            imgbtn.attr({
                                "state": 1
                            });
                        } else if (parseInt(json[node][0]) == 1 && parseInt(json[node][6]) == 1) {
                            var imgRec = $(recTableObj).find("a:eq(0)");
                            var imgbtn = $(imgRec);
                            imgbtn.html("RU State Unlocked");
                            imgbtn.attr({
                                "original-title": "RU State Unlocked"
                            });
                            imgbtn.attr({
                                "class": "green"
                            });
                            imgbtn.attr({
                                "state": 1
                            });
                        } else {
                            var imgRec = $(recTableObj).find("a:eq(0)");
                            var imgbtn = $(imgRec);
                            imgbtn.html("RU State Locked");
                            imgbtn.attr({
                                "original-title": "RU State Locked"
                            });
                            imgbtn.attr({
                                "class": "red"
                            });
                            imgbtn.attr({
                                "state": 0
                            });
                        }
                        if (parseInt(json[node][1]) == 1 && parseInt(json[node][7]) == 0) {
                            var imgRec = $(recTableObj).find("a:eq(1)");
                            var imgbtn = $(imgRec);
                            imgbtn.html("SYNC State Unlocked");
                            imgbtn.attr({
                                "class": "red"
                            });
                            imgbtn.attr({
                                "original-title": "SYNC State Unlocked"
                            });
                            imgbtn.attr({
                                "state": 1
                            });
                        } else if (parseInt(json[node][1]) == 1 && parseInt(json[node][7]) == 1) {
                            var imgRec = $(recTableObj).find("a:eq(1)");
                            var imgbtn = $(imgRec);
                            imgbtn.html("SYNC State Unlocked");
                            imgbtn.attr({
                                "class": "green"
                            });
                            imgbtn.attr({
                                "original-title": "SYNC State Unlocked"
                            });
                            imgbtn.attr({
                                "state": 1
                            });
                        } else {
                            var imgRec = $(recTableObj).find("a:eq(1)");
                            var imgbtn = $(imgRec);
                            imgbtn.html("SYNC State Locked");
                            imgbtn.attr({
                                "class": "red"
                            });
                            imgbtn.attr({
                                "original-title": "SYNC State Locked"
                            });
                            imgbtn.attr({
                                "state": 0
                            });
                        }
                        if (parseInt(json[node][2]) == 1 && parseInt(json[node][8]) == 0) {
                            var imgRec = $(recTableObj).find("a:eq(2)");
                            var imgbtn = $(imgRec);
                            imgbtn.html("RA State Unlocked");
                            imgbtn.attr({
                                "original-title": "RA State Unlocked"
                            });
                            imgbtn.attr({
                                "class": "red"
                            });
                            imgbtn.attr({
                                "state": 1
                            });
                        } else if (parseInt(json[node][2]) == 1 && parseInt(json[node][8]) == 1) {
                            var imgRec = $(recTableObj).find("a:eq(2)");
                            var imgbtn = $(imgRec);
                            imgbtn.html("RA State Unlocked");
                            imgbtn.attr({
                                "original-title": "RA State Unlocked"
                            });
                            imgbtn.attr({
                                "class": "green"
                            });
                            imgbtn.attr({
                                "state": 1
                            });
                        } else {
                            var imgRec = $(recTableObj).find("a:eq(2)");
                            var imgbtn = $(imgRec);
                            imgbtn.html("RA State Locked");
                            imgbtn.attr({
                                "original-title": "RA State Locked"
                            });
                            imgbtn.attr({
                                "class": "red"
                            });
                            imgbtn.attr({
                                "state": 0
                            });
                        }

                        var opDiv = $("#operation_status")
                        var opImg = opDiv.find("img");
                        opDiv.html("");
                        opDiv.html('<span>Operation Status </span>&nbsp;&nbsp;&nbsp;<img class="n-reconcile" id="operation_status" name="operation_status" src="' + json[node][4] + '" title="' + opStatusDic[json[node][5]] + '" style="width:14px;height:14px;vertical-align: middle; "class="imgbutton n-reconcile" original-title="' + opStatusDic[json[node][5]] + '"/></center>&nbsp;&nbsp;')
                        //						        $(opImg).attr({"src":json[node][4],"original-title":opStatusDic[json[node][5]]});
                        //opDiv.html("");
                        /*opDiv.html('<span>Operation Status </span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img original-title="No operation" class="n-reconcile" style="width: 14px; height: 14px; vertical-align: middle;" title="No operation" src="images/host_status0.png" name="operation_status" id="operation_status_img0">&nbsp;&nbsp;');*/

                    }
                }

                callB = setTimeout(function () {

                    globalAdminStatus();

                }, timeGlobal);
            }
        });
    }

}

function adminStateCheck(event, obj, deviceTypeId, adminStateName) {
    if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
        //event.stopPropagation();
        //event.preventDefault();
        attrValue = $(obj).attr("state");
        if (parseInt(attrValue) == 0) {
            attrValue = 1;
        } else {
            attrValue = 0;

        }
        singleEvent = event;
        singleObj = obj;
        singleHostId = $("input[name='host_id']").val();
        singleDeviceTypeId = $("input[name='device_type']").val();
        singleAdminStateName = adminStateName;
        /*
         if((adminStateName=="ru.ruConfTable.adminstate") && (parseInt(attrValue)==1))
         {
         $.prompt('Unlock admin state may cause reboot of the device',{ buttons:{Ok:true,Cancel:false}, prefix:'jqismooth',callback: admin_state_change});
         }
         else
         {*/
        admin_state_change(true, null);
        /* } */
    } else {
        $.prompt('Reconciliation is Running.Please Wait', {
            buttons: {
                Ok: true
            },
            prefix: 'jqismooth'
        });
    }
}


function admin_state_change(v, m) {
    if (v != undefined && v == true && singleEvent && singleObj && singleHostId && singleDeviceTypeId && singleAdminStateName) {
        attrValue = $(singleObj).attr("state");
        var opDiv = $("#operation_status")
        //							        var opImg = opDiv.find("img");
        opDiv.html("");
        opDiv.html('<span>Operation Status </span>&nbsp;&nbsp;&nbsp;<div style="display:block;background:url(images/new/loading.gif) no-repeat scroll 0% 0% transparent; width: 16px; height: 16px; float:right;"><img class="n-reconcile" id="operation_status_img1" name="operation_status" src="images/host_status1.png" title="' + opStatusDic[12] + '" style="width:14px;height:14px;vertical-align: middle; "class="imgbutton n-reconcile" original-title="' + opStatusDic[12] + '"/></div>&nbsp;&nbsp;')
        if (parseInt(attrValue) == 0) {
            attrValue = 1;
        } else {
            attrValue = 0;

        }

        $.ajax({
            type: "get",
            url: "change_admin_state.py?host_id=" + singleHostId + "&device_type_id=" + singleDeviceTypeId + "&admin_state_name=" + singleAdminStateName + "&state=" + attrValue,
            success: function (result) {
                if (parseInt(result.success) == 0) {

                    clearTimeout(callB);
                    callB = null;
                    globalAdminStatus();

                } else {
                    $().toastmessage('showErrorToast', result.result);
                }
                opDiv.html("");
                opDiv.html('<span>Operation Status </span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img class="n-reconcile" id="operation_status_img1" name="operation_status" src="images/host_status0.png" title="' + opStatusDic[0] + '" style="width:14px;height:14px;vertical-align: middle; "class="imgbutton n-reconcile" original-title="' + opStatusDic[0] + '"/></center>&nbsp;&nbsp;')
            }

        });
    }
}


function ipSelectMacDeviceType(obj, ipMacVal) {
    var selectedVal = $(obj).val();
    $.ajax({
        type: "get",
        url: "get_ip_mac_selected_device.py?selected_val=" + selectedVal + "&ip_mac_val=" + ipMacVal,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                if (ipMacVal == 1) {
                    $("input[id='filter_mac']").val(String(result.mac_address).toUpperCase());
                    $("select[id='device_type']").val(result.selected_device);
                } else {
                    $("input[id='filter_ip']").val(result.ip_address);
                    $("select[id='device_type']").val(result.selected_device);
                }
                ipMacChange = 1;
                deviceList();
            } else {
                $().toastmessage('showErrorToast', result.error);
            }
        }
    });
}


$(function () {
    $("input[id='btnSearch']").click(function () {
        //call the device list function on click of search button
        deviceList();

    });
    $("input[id='filter_ip']").keypress(function () {
        $("input[id='filter_mac']").val("");
    });
    $("input[id='filter_mac']").keypress(function () {
        $("input[id='filter_ip']").val("");
    });
    $("input[id='filter_ip']").ccplAutoComplete("common_ip_mac_search.py?device_type=" + $("select[id='device_type']").val() + "&ip_mac_search=" + 1, {
        dataType: 'json',
        max: 30,
        selectedItem: $("input[id='filter_ip']").val(),
        callAfterSelect: function (obj) {
            ipSelectMacDeviceType(obj, 1);
        }
    });

    $("input[id='filter_mac']").ccplAutoComplete("common_ip_mac_search.py?device_type=" + $("select[id='device_type']").val() + "&ip_mac_search=" + 0, {
        dataType: 'json',
        max: 30,
        selectedItem: $("input[id='filter_mac']").val(),
        callAfterSelect: function (obj) {
            ipSelectMacDeviceType(obj, 0);
        }
    });
    deviceList();
    chk_reconcile_status("");
    globalAdminStatus();
    $("#filterOptions").hide();
    $("#hide_search").show();
    $("#odu16_form_div").css({
        'margin-top': '20px'
    });
    $("#hide_search").toggle(function () {
        var $this = $(this);
        var $span = $this.find("span").eq(0);
        $span.removeClass("dwn");
        $span.addClass("up");
        $("#filterOptions").show();
        $this.css({
            'background-color': "#F1F1F1",
            'display': "block",
            'height': '20px',
            'position': 'static',
            'overflow': 'hidden',
            'width': "100%"
        });
        $("#odu16_form_div").css({
            'margin-top': '76px'
        });
    }, function () {
        var $this = $(this);
        var $span = $this.find("span").eq(0);
        $span.removeClass("up");
        $span.addClass("dwn");
        $("#filterOptions").hide();
        $this.css({
            'background-color': "#F1F1F1",
            'display': "block",
            'height': '20px',
            'overflow': 'hidden',
            'position': 'static',
            'right': 1,
            'top': 1,
            'width': "100%",
            'z-index': 1000
        });
        $("#odu16_form_div").css({
            'margin-top': '20px'
        });

    }); //$("div#container_body").css("padding-bottom","20px");
    // spin loading object
    //spinStart($spinLoading,$spinMainLoading);
    //spinStop($spinLoading,$spinMainLoading);
//	$("#page_tip").colorbox({
//		href: "page_tip_odu_profiling.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width: "650px",
//		height: "600px",
//		onComplte: function() {}
//	});

});
var CallA = null;

function chk_reconcile_status(host_id) {
    var host_id = $("input[name='host_id']").val();
    if (host_id == undefined) {
        callA = setTimeout(function () {
            chk_reconcile_status(host_id);

        }, 1000);
    } else {
        $.ajax({
            type: "post",
            url: "chk_reconcilation_status.py?host_id=" + host_id,
            success: function (result) {
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    var json = result.result
                    if (json.length == 1) {
                        if (json[0] == 1) {
                            reconcile_chk_status_btn = 1;
                        } else if (json[0] == 0) {
                            reconcile_chk_status_btn = 0;
                            $("input[id='odu16_reconcile']").removeAttr("disabled");
                        } else {
                            reconcile_chk_status_btn = 0;
                            $().toastmessage('showWarningToast', "No Host Exist");
                        }
                    } else if (json.length > 1) {
                        if (json[0] == 2) {
                            if (json[1] <= 35) {
                                $().toastmessage('showWarningToast', json[1] + "% Done.Please Again Reconcile The Device");
                            } else if (json[1] <= 90) {
                                $().toastmessage('showWarningToast', json[1] + "% Done.Please Again Reconcile The Device");
                            } else {
                                $().toastmessage('showSuccessToast', 'Reconcilation Done SuccessFully');
                            }
                            deviceList();
                            $("input[id='odu16_reconcile']").removeAttr("disabled");
                        }

                    }
                    callA = setTimeout(function () {
                        chk_reconcile_status(host_id);

                    }, timeSlot);
                }
            }
        });
        return false;
    }
}


function odu_profiling() {
    $("a.tab-profile").click(function (e) {
        e.preventDefault();
        if ($(this).hasClass("tab-active") == false) {
            var anr = $(this).parent().find("a");
            anr.removeClass("tab-active");
            anr.addClass("tab-button");
            $(this).removeClass("tab-button");
            $(this).addClass("tab-active");
            var div = $(this).parent().next();
            div.find("div.form_div").hide();
            div.find($(this).attr("href")).show();
        }
    });
    $.validator.addMethod('positiveNumber', function (value, element) {
        return Number(value) > -1;
    }, ' Enter a positive number');
    hostId = $("input[name='host_id']").val();
    deviceType = $("input[name='device_type']").val();
    //ipv4AddressValidation($);
    //macAddressValidation($);
    //	raster_time
    $("select[id='RU.SyncClock.SyncConfigTable.rasterTime'] option[value='" + $("input[name='raster_time']").val() + "']").attr("selected", true);

    $("select[id='RU.RUConfTable.channelBandwidth'] option[value='" + $("input[name='channelBandwidth']").val() + "']").attr("selected", true);
    //$("select[id='RU.RUConfTable.synchSource'] option[value='"+ $("input[name='csynchSource']").val() +"']").attr("selected",true);
    $("select[id='RU.RUConfTable.countryCode'] option[value='" + $("input[name='countryCode']").val() + "']").attr("selected", true);
    $("select[id='RU.SyncClock.SyncConfigTable.numSlaves'] option[value='" + $("input[name='slaves']").val() + "']").attr("selected", true);
    //$("select[id='RU.SyncClock.SyncConfigTable.broadcastEnable'] option[value='"+ $("input[name='BroadcastEnable']").val() +"']").attr("selected",true);
    $("select[id='RU.RA.1.LLC.RALLCConfTable.llcArqEnable'] option[value='" + $("input[name='llcArqEnable']").val() + "']").attr("selected", true);
    $("select[id='RU.RA.1.RAConfTable.aclMode'] option[value='" + $("input[name='aclmode']").val() + "']").attr("selected", true);
    $("select[id ='ru.np.ra.1.tddmac.rfChannel'] option[value = '" + $("input[name = 'rfchannel']").val() + "']").attr("selected", true);
    //var numslaves=$("#peer_config_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves']").val();
    //$("syn_configuration_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves']) option[value='"+numslaves+"']").attr("selected",true);
    $("#peer_config_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves']").change(function () {
        var numslaves = $("#peer_config_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves']").val();
        $("#syn_configuration_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves'] option[value='" + numslaves + "']").attr("selected", true);
    })
    $("#syn_configuration_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves']").change(function () {
        var numslaves = $("#syn_configuration_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves']").val();
        $("#peer_config_form").find("select[id='RU.SyncClock.SyncConfigTable.numSlaves'] option[value='" + numslaves + "']").attr("selected", true);
    })

    //	$("#odu100_ra_configuration_form").find("input[id='ru.ra.tddMac.raTddMacConfigTable.passPhrase']").attr({"disabled":true});
    var encrypt = $("#odu100_ra_configuration_form").find("select[id='ru.ra.tddMac.raTddMacConfigTable.encryptionType']").val();
    if (encrypt == 0 || encrypt == '0') {
        //$("#odu100_ra_configuration_form").find("input[id='ru.ra.tddMac.raTddMacConfigTable.passPhrase']").attr({"disabled":true});
        $("#odu100_ra_configuration_form").find("input[id='ru.ra.tddMac.raTddMacConfigTable.passPhrase']").val("");
    }

    var odu100Timeslot = parseInt($("#odu100_ra_configuration_form").find("select[id='ru.ra.raConfTable.numSlaves']").val());

    $("#odu100_peer_configuration_form").find("input[name='timeslot_val']").val(odu100Timeslot);
    for (i = odu100Timeslot; i > 0; i--) {
        $("#odu100_peer_configuration_form").
            find("input[id='ru.ra.peerNode.peerConfigTable.peerMacAddress." + String(i) + "']").parent().show();
    }
    for (i = 16; i > odu100Timeslot; i--) {
        $("#odu100_peer_configuration_form").
            find("input[id='ru.ra.peerNode.peerConfigTable.peerMacAddress." + String(i) + "']").parent().hide();
    }
    var odu100AclVal = parseInt($("#odu100_acl_mode_form").find("select[id='ru.ra.raConfTable.aclMode']").val());
    $("#odu100_peer_configuration_form").find("input[name='acl_val']").val(odu100AclVal);
    omcConfiguration();
    omcConfigurationForm();
    ruConfigurationconfirmCheck();

    dateTime();
    oduRuDateTimeForm();

    omdNetworkInterfaceConfigForm();
    tddMacConfiguration();
    tddMacConfigForm();
    llcConfiguration();
    ipPacketFilter();
    macPacketFilter();
    packetFilterMode();
    raLlcConfigForm();
    omcRegistration();
    omcRegistrationForm();
    synConfiguration();
    synConfigurationForm();
    raConfigForm();
    peerMacValid();
    peerConfigForm();
    aclConfigForm();
    aclAddMore();
    $("input[name='odu16_commit_to_flash']").unbind().bind("click", function () {
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {

            chkCommitToFlash();
        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }
    });

    acl_reconciliation();

    $("#syncFilter").click(function () {
        filterSync();
    });

    $("#bw_calculator_form").unbind().bind("click", function () {
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
            bwCalculateForm(hostId, deviceType);
        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }
    });

    $("#alarm_recon").unbind().bind("click", function () {
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
            alarmRecon(hostId, deviceType);
        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }
    });

    $("#odu100_acl_add_mac_config_form").find("select[id='ru.ra.raConfTable.aclMode']").change(function () {
        if ($("input[id='total_rows']").val() == 0 && $("select[id='ru.ra.raConfTable.aclMode']").val() == 1) {
            $().toastmessage('showWarningToast', "ACL Mode cannot be ACCEPT if the ACL Config Table is empty");
            $("#odu100_acl_add_mac_config_form").find("select[id='ru.ra.raConfTable.aclMode'] option[value='']").attr("selected", true);
        }
    });

    $("#device_type").change(function () {
        $("#filter_ip").val("");
        $("#filter_mac").val("");
    });
    $("input[id='odu16_reconcile']").unbind().bind("click", function () {
        var host_id = $("input[name='host_id']").val();
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
            spinStart($spinLoading, $spinMainLoading);
            $.ajax({
                type: "post",
                url: "chk_reconcilation_status.py?host_id=" + host_id,
                success: function (result) {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        var json = result.result
                        if (json[0] == 0) {
                            reconcile_chk_status_btn = 0;
                            chk_common_rec(host_id);
                            spinStop($spinLoading, $spinMainLoading);
                        } else if (json[0] == 1) {
                            spinStop($spinLoading, $spinMainLoading);
                            reconcile_chk_status_btn = 1;
                            $.prompt('Reconciliation is already Running.Please Wait', {
                                buttons: {
                                    Ok: true
                                },
                                prefix: 'jqismooth'
                            });
                        } else if (json[0] == 2) {

                            if (json[1] <= 35) {
                                $().toastmessage('showWarningToast', json[1] + "% Done.Please Again Reconcile The Device");
                            } else if (json[1] <= 90) {
                                $().toastmessage('showWarningToast', json[1] + "% Done.Please Again Reconcile The Device");
                            } else {
                                $().toastmessage('showSuccessToast', 'Reconcilation Done SuccessFully');
                            }
                            reconcile_chk_status_btn = 0;
                            deviceList();
                            spinStop($spinLoading, $spinMainLoading);
                        } else {
                            $.prompt('No Hosts Exist', {
                                buttons: {
                                    Ok: true
                                },
                                prefix: 'jqismooth'
                            });
                        }
                    }
                    /*var recTableObj = $("#adminDiv")
                     var objTable = $(recTableObj);
                     if(parseInt(json[node][1]) == 1)
                     {
                     var imgRec = $(recTableObj).find("a:eq(1)");
                     var imgbtn = $(imgRec);
                     imgbtn.html("Radio Access Unlocked");
                     imgbtn.attr({"class":"green"});
                     }
                     else
                     {
                     var imgRec = $(recTableObj).find("a:eq(1)");
                     var imgbtn = $(imgRec);
                     imgbtn.attr({"class":"red"});
                     imgbtn.html("Radio Access Locked");
                     }*/

                }
            });
        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }
        return false;

    });
    filterAction();
    //peerSelectBasicRateMCSIndex();
    odu100OmcConfigurationValidation();
    //odu100OmcConfigFormSubmit();
    odu100SyncConfigurationValidation();
    //odu100SyncConfigFormSubmit()
    odu100IPConfigurationValidation();
    //odu100IpConfigFormSubmit();
    odu100RAConfigurationValidation();
    //odu100RAConfigurationSubmit();
    odu100RUConfigurationValidation();
    odu100peerMacValid();
    odu100AclValidation();

    $("input[name='odu_reboot']").unbind().bind("click", function () {
        if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
            rebootconfirm();
        } else {
            $.prompt('Reconciliation is Running.Please Wait', {
                buttons: {
                    Ok: true
                },
                prefix: 'jqismooth'
            });
        }
    });
    $("select", "#odu100_peer_configuration_form").change();
    //aclAddEdit();
    odu100_ru_channel_banwidth = $("#odu100_ru_configuration_form").find("select[name='ru.ruConfTable.channelBandwidth']").val();
    odu100_ru_country_code = $("#odu100_ru_configuration_form").find("select[name='ru.ruConfTable.countryCode']").val();
    $("#filter_mac").val($("input[name='mac_address']").val());
    $("#filter_ip").val($("input[name='ip_address']").val());
}

function rebootconfirm() {
    if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
        $.prompt('Are you sure you want to reboot this device? \n Click Ok to confirm', {
            buttons: {
                Ok: true,
                Cancel: false
            },
            prefix: 'jqismooth',
            callback: reboot
        });
    } else {
        $.prompt('Reconciliation is Running.Please Wait', {
            buttons: {
                Ok: true
            },
            prefix: 'jqismooth'
        });
    }
}

function reboot(v, m) {
    if (v != undefined && v == true) {
        spinStart($spinLoading, $spinMainLoading);
        var host_id = $("input[name='host_id']").val();
        var device_type_id = $("input[id='device_type_id']").val();
        $.ajax({
            type: "post",
            url: "reboot_odu.py?host_id=" + host_id,
            success: function (result) {
                if (result.success == 0) {
                    json = result.result
                    for (var node in json) {
                        //console.log(json);
                        //console.log(json[node]);
                        if (json[node] == 0 || parseInt(node) == 553) {
                            ping_chk = 0;
                            pingCheck();
                        } else {
                            $().toastmessage('showErrorToast', result.result);
                            spinStop($spinLoading, $spinMainLoading);
                        }
                    }
                } else {
                    $().toastmessage('showErrorToast', result.result);
                    spinStop($spinLoading, $spinMainLoading);
                }
            }
        });
        return false
    }
}

function pingCheck() {
    var host_id = $("input[name='host_id']").val();
    var device_type_id = $("input[id='device_type_id']").val();
    $.ajax({
        type: "post",
        url: "ping_chk.py?host_id=" + host_id,
        success: function (result) {
            if (result == 0) {
                $().toastmessage('showSuccessToast', 'Device Rebooted SuccesFully');

                spinStop($spinLoading, $spinMainLoading);
            } else if (result == 2) {
                $().toastmessage('showErrorToast', 'Host does not Exist');
                spinStop($spinLoading, $spinMainLoading);
            } else {
                ping_chk = ping_chk + 1;
                if (ping_chk < 30) {
                    pingCheck();
                } else {
                    $().toastmessage('showErrorToast', 'Device Not Responding');
                    spinStop($spinLoading, $spinMainLoading);
                }

            }
        }
    });
    return false;
}


function peerSelectBasicRateMCSIndex() {
    var ch_bw_value = parseInt($("#odu100_ru_configuration_form").find("select[id='ru.ruConfTable.channelBandwidth']").val());
    $("#odu100_peer_configuration_form").find("input[name='ch_bw']").val(ch_bw_value);
    var ra_port_value = parseInt($("#odu100_ra_configuration_form").find("select[id='ru.ra.raConfTable.antennaPort']").val());
    $("#odu100_peer_configuration_form").find("input[name='ra_port']").val(ra_port_value);
    if (parseInt($("input[name='ch_bw']").val()) == 0 && (parseInt($("input[name='ra_port']").val()) == 1 || parseInt($("input[name='ra_port']").val()) == 2)) {
        var maxDownLinkBW = [1600, 3200, 4800, 6500, 9700, 13000, 14600, 16200];
    } else if (parseInt($("input[name='ch_bw']").val()) == 1 && (parseInt($("input[name='ra_port']").val()) == 1 || parseInt($("input[name='ra_port']").val()) == 2)) {
        var maxDownLinkBW = [3200, 6500, 9700, 13000, 19500, 26000, 29200, 32500];
    } else if (parseInt($("input[name='ch_bw']").val()) == 2 && (parseInt($("input[name='ra_port']").val()) == 1 || parseInt($("input[name='ra_port']").val()) == 2)) {
        var maxDownLinkBW = [6500, 13000, 19500, 26000, 39000, 52000, 58500, 65000];
    } else if (parseInt($("input[name='ch_bw']").val()) == 3 && (parseInt($("input[name='ra_port']").val()) == 1 || parseInt($("input[name='ra_port']").val()) == 2)) {
        var maxDownLinkBW = [13500, 27000, 40500, 54000, 81000, 108000, 121500, 135000];
    } else if (parseInt($("input[name='ch_bw']").val()) == 4 && (parseInt($("input[name='ra_port']").val()) == 1 || parseInt($("input[name='ra_port']").val()) == 2)) {
        var maxDownLinkBW = [15000, 30000, 45000, 60000, 90000, 120000, 135000, 150000];
    } else if (parseInt($("input[name='ch_bw']").val()) == 0 && parseInt($("input[name='ra_port']").val()) == 3) {
        var maxDownLinkBW = [1600, 3200, 4800, 6500, 9700, 13000, 14600, 16200, 3200, 6500, 9700, 13000, 19500, 26000, 29200, 32500];
    } else if (parseInt($("input[name='ch_bw']").val()) == 1 && parseInt($("input[name='ra_port']").val()) == 3) {
        var maxDownLinkBW = [3200, 6500, 9700, 13000, 19500, 26000, 29200, 32500, 6500, 13000, 19500, 26000, 39000, 52000, 58500, 65000];
    } else if (parseInt($("input[name='ch_bw']").val()) == 2 && parseInt($("input[name='ra_port']").val()) == 3) {
        var maxDownLinkBW = [6500, 13000, 19500, 26000, 39000, 52000, 58500, 65000];
    } else if (parseInt($("input[name='ch_bw']").val()) == 3 && parseInt($("input[name='ra_port']").val()) == 3) {
        var maxDownLinkBW = [13000, 27000, 40500, 54000, 81000, 108000, 121500, 135000, 27000, 54000, 81000, 10800, 162000, 216000, 243000, 270000];
    } else {
        var maxDownLinkBW = [15000, 30000, 45000, 60000, 90000, 120000, 135000, 150000, 30000, 60000, 90000, 120000, 180000, 240000, 270000, 300000];
    }
    $("select", "#odu100_peer_configuration_form").change(function () {
        var i = $(this).val();
        var maxUplinkBW = maxDownLinkBW;
        var attrI = $(this).attr("id").split(".");
        if (parseInt(i) == -1) {
            $("#odu100_peer_configuration_form").find("input[name='ru.ra.peerNode.peerConfigTable.maxDownlinkBW." + String(attrI[attrI.length - 1]) + "']").val(100000);
            $("#odu100_peer_configuration_form").find("input[name='ru.ra.peerNode.peerConfigTable.maxUplinkBW." + String(attrI[attrI.length - 1]) + "']").val(100000);
        } else {
            $("#odu100_peer_configuration_form").find("input[name='ru.ra.peerNode.peerConfigTable.maxDownlinkBW." + String(attrI[attrI.length - 1]) + "']").val(maxDownLinkBW[i]);
            $("#odu100_peer_configuration_form").find("input[name='ru.ra.peerNode.peerConfigTable.maxUplinkBW." + String(attrI[attrI.length - 1]) + "']").val(maxUplinkBW[i]);
        }
    });
}

function viewModulationRate() {
    var host_id = $("input[name='host_id']").val();
    $.colorbox({
        href: "view_modulation_rate.py?host_id=" + host_id,
        title: "View Modulation Rates",
        opacity: 0.4,
        maxWidth: "80%",
        width: "600px",
        height: "500px"
    });
}

function acl_reconciliation() {
    $("input[id='reconcileAcl']").click(function () {
        aclClickReconcile = $(this);
        $.prompt('Are you sure you want to reconcile the ACL MAC?', {
            buttons: {
                Ok: true,
                Cancel: false
            },
            prefix: 'jqismooth',
            callback: aclReconciliation
        });
    });
}

function aclReconciliation(v, m) {
    if (v != undefined && v == true && aclClickReconcile) {
        var host_id = $("input[name='host_id']").val();
        var selected_device_type = $("select[id='device_type']").val();
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "post",
            url: "acl_reconciliation.py?host_id=" + host_id + "&device_type=" + selected_device_type,
            success: function (result) {

                if (result == "") {
                    $.prompt('Device is Time Out.Please Try Again', {
                        buttons: {
                            Ok: true
                        },
                        prefix: 'jqismooth'
                    });
                    spinStop($spinLoading, $spinMainLoading);
                }
                if (result == 1) {
                    $.prompt('Problem Creating MAC Addresses.Please Reconcile The ACL MAC Again.', {
                        buttons: {
                            Ok: true
                        },
                        prefix: 'jqismooth'
                    });
                    spinStop($spinLoading, $spinMainLoading);
                }
                if (result == 2) {
                    $.prompt('There is no MAC Available in device', {
                        buttons: {
                            Ok: true
                        },
                        prefix: 'jqismooth'
                    });
                    spinStop($spinLoading, $spinMainLoading);
                }
                if (result == 0) {
                    var mainDiv = aclClickReconcile.parent().parent().parent();
                    $.ajax({
                        type: "post",
                        url: "cancel_odu_form.py?action_name=Acl_Cancel_Configuration.py" + "&host_id=" + host_id,
                        success: function (result) {
                            mainDiv.find("form").remove();
                            mainDiv.find("div#result_acl_config").hide();
                            mainDiv.append(result);
                            aclConfigForm();
                            aclAddMore();
                            acl_reconciliation();
                            spinStop($spinLoading, $spinMainLoading);
                            $.prompt('ACL Reconciliation Done Successfully', {
                                buttons: {
                                    Ok: true
                                },
                                prefix: 'jqismooth'
                            });
                        }
                    });

                }

            }
        });
        return false;
    }
}


function deleteAclConfigMacAddress(macAddrNo) {
    var hiddenVal = $("#acl_count");
    var maxMac = parseInt(hiddenVal.val());
    $("#acl_row_element_" + macAddrNo).remove();
    for (macCount = macAddrNo + 1; macCount <= maxMac; macCount++) {
        var divStr = $("#acl_row_element_" + macCount);
        var textBoxName = "RU.RA.1.RAACLConfig." + String(macCount - 1) + ".macAddress";
        var textBoxId = "RU.RA.1.RAACLConfig." + String(macCount - 1) + ".macAddress";
        var textBoxFact = ".1.3.6.1.4.1.26149.2.2.13.5.1.2.1." + String(macCount - 1);
        divStr.attr("id", "acl_row_element_" + String(macCount - 1));
        divStr.find("label").html("Mac Address " + String(macCount - 1));
        divStr.find("input").attr({
            "name": textBoxName,
            "id": textBoxId,
            "fact": textBoxFact
        });
        divStr.find("img").remove();
        divStr.append("<img onclick=\"deleteAclConfigMacAddress(" + String(macCount - 1) + ")\" class=\"imgbutton\" title=\"Delete\" alt=\"Delete\" src=\"images/delete16.png\">")
    }
    hiddenVal.val(maxMac - 1);
}

function chk_common_rec(host_id) {
    $.ajax({
        type: "get",
        url: "chk_common_reconcile.py?host_id=" + host_id,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                common_rec()
            } else {
                $().toastmessage('showWarningToast', result.result);
            }
        }
    });
    return false;
}

function common_rec() {
    text_name = $("a.active:first").text();
    console.log(text_name);
    var text_val = text_name.replace(/\s/g, "%20");
    $.colorbox({
        href: "local_reconciliation.py?textname=" + text_val,
        title: "Form Reconciliation",
        opacity: 0.4,
        maxWidth: "80%",
        width: "500px",
        height: "250px"
    });
}

function reconcileForm(obj, formid) {
    formObj = $(obj);
    formId = $("#" + formid);
    $.prompt('Device Configuration data would be Synchronized with the UNMP server Database', {
        buttons: {
            Ok: true,
            Cancel: false
        },
        prefix: 'jqismooth',
        callback: odu16Reconcilation
    });
    return false;
}


function aclReloadForm() {
    var host_id = $("input[name='host_id']").val();
    var device_type_id = $("input[name='device_type']").val();
    var divId = $("a.active").attr("href");
    formName = $(divId).find("input[name='common_rec']").attr("form_name");
    $.ajax({
        type: "get",
        url: "odu_form_reconcile.py?formName=" + formName + "&host_id=" + host_id + "&device_type=" + device_type_id,
        success: function (htmlResult) {
            $(divId).html();
            $(divId).html(htmlResult);
            spinStop($spinLoading, $spinMainLoading);
        }
    });
    $.colorbox.close();
}

function odu16Reconcilation(v, m) {

    if (v != undefined && v == true) {
        var host_id = $("input[name='host_id']").val();
        var device_type_id = $("input[name='device_type']").val();
        spinStart($spinLoading, $spinMainLoading);
        data = $(formId).serialize();
        form_rec = $("input[name='form_rec']:checked").val();
        var divId = $("a.active").attr("href");
        //var divId = attrText.replace("#","");
        formName = $(divId).find("input[name='common_rec']").attr("form_name");
        tableName = $(divId).find("input[name='common_rec']").attr("tablename");
        if (parseInt(form_rec) == 0) {
            if (formName == "odu100_acl_configuration") {
                odu100AclReconciliation(true, undefined);
                aclReconcile = true;

            } else {
                $.ajax({
                    type: "get",
                    url: "common_reconcile.py?host_id=" + host_id + "&device_type=" + device_type_id + "&tableName=" + tableName,
                    data: data,
                    success: function (result) {
                        if (parseInt(result.success) == 0) {
                            $.ajax({
                                type: "get",
                                url: "odu_form_reconcile.py?formName=" + formName + "&host_id=" + host_id + "&device_type=" + device_type_id,
                                success: function (htmlResult) {
                                    if (formName == "odu100_packet_filter") {
                                        var $htmlResult = $(htmlResult)
                                        $(divId).html($htmlResult.html());
                                        $("#sub_config_tabs").yoTabs();
                                    } else {
                                        //$(divId).html();
                                        //sub_config_tabs
                                        $(divId).html(htmlResult);
                                    }

                                }
                            });
                            $().toastmessage('showSuccessToast', text_name + " Reconciliation done successfully");
                        } else {
                            $().toastmessage('showErrorToast', result.result);
                        }
                        $.colorbox.close();
                        spinStop($spinLoading, $spinMainLoading);
                    }
                });
            }
        } else if (form_rec == undefined) {
            $().toastmessage('showErrorToast', "Please select the reconciliation mode");
            spinStop($spinLoading, $spinMainLoading);
        } else {
            $.ajax({

                type: "post",
                url: "odu16_reconcilation.py?host_id=" + host_id + "&device_type_id=" + device_type_id,
                success: function (result) {
                    if (parseInt(result.success) == 0) {
                        json = result.result
                        for (var node in json) {
                            if (parseInt(node) <= 35) {
                                $().toastmessage('showWarningToast', node + "% reconciliation done for device " + json[node][0] + "(" + json[node][1] + ")" + ".Please reconcile the device again");
                            } else if (parseInt(node) <= 90) {
                                $().toastmessage('showWarningToast', node + "% reconciliation done for device " + json[node][0] + "(" + json[node][1] + ")" + ".Please reconcile the device again");
                            } else {
                                $().toastmessage('showSuccessToast', "Reconciliation done successfully for device " + json[node][0] + "(" + json[node][1] + ")");
                            }
                            reconcile_chk_status_btn = 0;
                            deviceList();
                            url = "refresh_channel_list.py?host_id=" + host_id + "&selected_device=" + device_type_id + "&refresh=" + 2 + "&ra_list_refresh=" + 0;
                            method = "get";
                            showdiv = "#content_8";
                            //$(showdiv).html("");
                            /*$(showdiv).html("Channel list is refreshing.This take few minutes.");*/
                            $.ajax({
                                type: method,
                                url: url,
                                success: function (result) {
                                    $(showdiv).html(result);
                                    spinStop($spinLoading, $spinMainLoading);
                                }
                            });
                            break;
                        }
                    } else {
                        $().toastmessage('showErrorToast', result.result);
                    }
                    $.colorbox.close();
                    spinStop($spinLoading, $spinMainLoading);

                }

            });
        }
        getAdminStateOdu(host_id, device_type_id);
    }

}


function getAdminStateOdu(hostId, deviceType) {
    $.ajax({
        type: "get",
        url: "get_admin_state.py?host_id=" + hostId + "&device_type=" + deviceType,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                clearTimeout(callB);
                callB = null;
                globalAdminStatus();
            }
        }
    });
}


/*######################################################################################### odu100 Functions ####################################################################################*/

function odu100CommonFormSubmit(formObj, btn) {

    //if(reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null)
    //{
    if ($("#" + formObj).valid()) {
        spinStart($spinLoading, $spinMainLoading);
        odu100CommonSetAjaxRequest(formObj, btn);
    }
    //}
    //else
    //{
    //		$.prompt('Reconciliation is Running.Please Wait',{ buttons:{Ok:true}, prefix:'jqismooth'});
    //	}
    return false;

}


function odu100IpConfigFormSubmitCheck(formObj, btn) {
    formObjIP = formObj
    btnIp = btn
    if ($("#" + formObj).valid()) {
        if ($(btnIp).val() == "Cancel" || $(btnIp).val() == "Ok") {
            odu100IpConfigFormSubmit(true, null);
        } else {
            $.prompt('Set These Values Will Cause Reboot.\nAre You Sure You Want to Do this?', {
                buttons: {
                    Ok: true,
                    Cancel: false
                },
                prefix: 'jqismooth',
                callback: odu100IpConfigFormSubmit
            });
        }
        return false;
    }
}

function odu100IpConfigFormSubmit(v, m) {
    if (v != undefined && v == true && formObjIP && btnIp) {
        spinStart($spinLoading, $spinMainLoading);
        var btnName = $(btnIp).attr("name");
        var btnValue = $(btnIp).val();
        odu100CommonSetAjaxRequest(formObjIP, btnIp);
    }
    return false;

}

function odu100RuConfigFormSubmitCheck(formObj, btn) {
    formObjRUConfig = formObj
    btnRuConfig = btn
    if ($("#" + formObj).valid()) {
        if ($(btnRuConfig).val() == "Cancel" || $(btnRuConfig).val() == "Ok") {
            odu100RUConfigurationSubmit(true, null);
        } else {
            ru_channel_bandwidth = $("#odu100_ru_configuration_form").find("select[name='ru.ruConfTable.channelBandwidth']").val();
            ru_country_code = $("#odu100_ru_configuration_form").find("select[name='ru.ruConfTable.countryCode']").val();
            if (odu100_ru_channel_banwidth == ru_channel_bandwidth && odu100_ru_country_code == ru_country_code) {
                spinStart($spinLoading, $spinMainLoading);
                odu100CommonSetAjaxRequest(formObjRUConfig, btnRuConfig);
            } else {

                $.prompt('Setting these values will cause Reboot.Are you sure you want to do this?', {
                    buttons: {
                        Ok: true,
                        Cancel: false
                    },
                    prefix: 'jqismooth',
                    callback: odu100RUConfigurationSubmit
                });
            }

        }
        return false;
    }
}

function odu100RUConfigurationSubmit(v, m) {

    if (v != undefined && v == true && formObjRUConfig && btnRuConfig) {
        //var btn = event.originalEvent.explicitOriginalTarget
        var btnName = $(btnRuConfig).attr("name");
        var btnValue = $(btnRuConfig).val();
        spinStart($spinLoading, $spinMainLoading);
        odu100CommonSetAjaxRequest(formObjRUConfig, btnRuConfig);
    }
    return false;
}

function odu100AclConfig(formObj, btn) {
    aclReconcile = false;
    formObjAcl = formObj
    btnAcl = btn
    $.prompt('Are you sure you want to reconcile the ACL MAC?', {
        buttons: {
            Ok: true,
            Cancel: false
        },
        prefix: 'jqismooth',
        callback: odu100AclReconciliation
    });
}

function odu100AclReconciliation(v, m) {
    if (v != undefined && v == true) {
        spinStart($spinLoading, $spinMainLoading);
        var host_id = $("input[name='host_id']").val();
        var selected_device_type = $("select[id='device_type']").val();
        $.ajax({
            type: "post",
            url: "odu100_acl_reconcile.py?host_id=" + host_id + "&device_type=" + selected_device_type,
            success: function (result) {
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    if (aclReconcile) aclReloadForm();
                    $.ajax({
                        type: "post",
                        url: "update_mac_list.py?host_id=" + host_id,
                        success: function (result) {
                            $("#tableDiv").html(result);
                            $("table#show_mac_edit_delete").dataTable({
                                "bDestroy": true,
                                "bJQueryUI": true,
                                "bProcessing": true,
                                "sPaginationType": "full_numbers",
                                "aLengthMenu": [
                                    [20, 40, 60, -1],
                                    [20, 40, 60, "All"]
                                ],
                                "iDisplayLength": 20,
                                "aaSorting": []
                            });
                        }

                    });
                    $().toastmessage('showSuccessToast', result.result);

                } else {
                    $().toastmessage('showErrorToast', result.result);
                }
                spinStop($spinLoading, $spinMainLoading);
            }

        });
    }
    return false;
}

//{'result': {'tx_time': '90', 'tx_rate': '100', 'tx_bw': '-324'}, 'success': 0}


function odu100BWCalc(formObj, hostId, deviceType) {
    if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
        spinStart($spinLoading, $spinMainLoading);
        var myForm = $("#" + formObj);
        var data = myForm.serialize() + "&hostId=" + hostId + "&deviceType=" + deviceType;
        var url = myForm.attr("action");
        var method = myForm.attr("method");
        var id = myForm.attr("id");
        $.ajax({
            type: method,
            url: url,
            data: data,
            success: function (result) {
                if (parseInt(result.success) == 0) {
                    json = result.result;
                    for (var node in json) {
                        $("#" + node).val(json[node]);
                    }
                    $().toastmessage('showSuccessToast', "Bandwidth calculation operation completed");
                } else {
                    $().toastmessage('showErrorToast', result.result);
                }
                spinStop($spinLoading, $spinMainLoading);
            }

        });
        return false;
    } else {
        $.prompt('Reconciliation is Running.Please Wait', {
            buttons: {
                Ok: true
            },
            prefix: 'jqismooth'
        });
    }
}


function odu100PeerForm(formObj, btn) {
    if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
        if ($("#" + formObj).valid()) {
            spinStart($spinLoading, $spinMainLoading);
            odu100PeerConfig(formObj, btn);
        }
    } else {
        $.prompt('Reconciliation is Running.Please Wait', {
            buttons: {
                Ok: true
            },
            prefix: 'jqismooth'
        });
    }

    return false;
}

function odu100PeerConfig(formObj, btn) {
    var btnName = $(btn).attr("name");
    var btnValue = $(btn).val();
    var myForm = $("#" + formObj);
    var data = myForm.serialize() + "&" + btnName + "=" + btnValue;
    var url = myForm.attr("action");
    var method = myForm.attr("method");
    var id = myForm.attr("id");
    var status = 0;
    if (btnValue == "Ok") {
        if (parseInt($("input[name='node_type']").val()) % 2 == 1) {
            myForm.find("input:not(input[type=hidden])").attr({
                "disabled": true
            });
            myForm.find("select:not(input[type=hidden])").attr({
                "disabled": true
            });
        } else {
            myForm.find("input").removeAttr("disabled");
            myForm.find("select").removeAttr("disabled");
        }
        myForm.find("input:eq(0)").removeAttr("disabled");
        myForm.find("input:eq(1)").removeAttr("disabled");
        myForm.find("input:eq(2)").removeAttr("disabled");
        myForm.find("input.img-submit-button").remove();
        myForm.find("input.img-done-button").remove();
        myForm.find("input[id='id_omc_button_retry_all']").removeAttr("disabled");
        myForm.find("input[id='id_omc_button_retry_all']").hide();
        myForm.find("input[id='id_omc_button_cancel']").removeAttr("disabled");
        myForm.find("input[id='id_omc_button_cancel']").hide();
        myForm.find("input[id='id_omc_button_ok']").removeAttr("disabled");
        myForm.find("input[id='id_omc_button_ok']").hide();
        myForm.find("input[id='id_omc_submit_save']").removeAttr("disabled");
        myForm.find("input[name='modulation_rate_table']").removeAttr("disabled");
        myForm.find("input[id='id_omc_submit_save']").show();
        spinStop($spinLoading, $spinMainLoading);
    } else {
        if (btnValue == "") {
            data = "host_id=" + myForm.find("input[name='host_id']").val() + "&device_type=" + myForm.find("input[name='device_type']").val() + "&" + $(btn).attr("oid") + "=" + myForm.find("input[name='" + $(btn).attr("oid") + "']").val() + "&" + btnName + "=" + btnValue;

        }
        $.ajax({
            type: method,
            url: url,
            data: data,
            success: function (result) {
                try {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        if ((btnValue == "Save") || (btnValue == "Retry")) {
                            var json = result.result;
                            var admin = parseInt(result.admin.success);
                            if (admin == 1) {
                                $().toastmessage('showErrorToast', result.admin.result);
                                var recTableObj = $("#adminDiv")
                                var objTable = $(recTableObj);
                                var imgRec = $(recTableObj).find("a:eq(1)");
                                var imgbtn = $(imgRec);
                                imgbtn.attr({
                                    "class": "red"
                                });
                                imgbtn.html("Radio Access Locked");
                            } else {
                                var recTableObj = $("#adminDiv")
                                var objTable = $(recTableObj);
                                var imgRec = $(recTableObj).find("a:eq(1)");
                                var imgbtn = $(imgRec);
                                imgbtn.attr({
                                    "class": "green"
                                });
                                imgbtn.html("Radio Access Unlocked");
                            }
                            myForm.find("input.img-submit-button").remove();
                            for (var node in json) {
                                var selectListName = $("select[id='" + node + "']");
                                var inputTextboxName = $("input[id='" + node + "']");
                                var imageCreate = $("<input/>");
                                if (json[node] == 0) {
                                    imageCreate.attr({
                                        "type": "button",
                                        "title": "Done",
                                        "class": "img-done-button",
                                        "oid": node
                                    });
                                    inputTextboxName.attr({
                                        "disabled": true
                                    });
                                    selectListName.attr({
                                        "disabled": true
                                    });
                                    inputTextboxName.show();
                                    selectListName.show();
                                } else {
                                    imageCreate.attr({
                                        "type": "button",
                                        "title": json[node],
                                        "class": "img-submit-button",
                                        "oid": node
                                    });
                                    imageCreate.val("");
                                    inputTextboxName.attr({
                                        "disabled": false
                                    });
                                    selectListName.attr({
                                        "disabled": false
                                    });
                                    status = 1
                                }
                                $(imageCreate).insertAfter(inputTextboxName);
                                $(imageCreate).insertAfter(selectListName);
                                if (status == 1) {
                                    myForm.find("#id_omc_button_ok").hide();
                                    myForm.find("#id_omc_submit_save").hide();
                                    myForm.find("#id_omc_button_retry_all").show();
                                    myForm.find("#id_omc_button_cancel").show();
                                } else {

                                    myForm.find("#id_omc_button_retry_all").hide();
                                    myForm.find("#id_omc_button_cancel").hide();
                                    myForm.find("#id_omc_submit_save").hide();
                                    myForm.find("#id_omc_button_ok").show();
                                }
                            }
                        } else if (btnValue == "Cancel") {

                            var json = result.result;
                            myForm.find("input").removeAttr("disabled");
                            myForm.find("select").removeAttr("disabled");
                            myForm.find("select").show();
                            myForm.find("input.img-submit-button").remove();
                            myForm.find("input.img-done-button").remove();
                            myForm.find("input[id='id_omc_button_retry_all']").hide();
                            myForm.find("input[id='id_omc_button_cancel']").hide();
                            myForm.find("input[id='id_omc_button_ok']").hide();
                            myForm.find("input[id='id_omc_submit_save']").show();
                            for (var node in json) {
                                var inputTextboxName = $("input[id='" + node + "']");
                                inputTextboxName.val(json[node]);
                            }
                        } else if (btnValue == "") {
                            $(btn).attr("oid");
                            var attrvalue = $(btn).attr("oid");
                            var json = result.result;
                            var imageFind = myForm.find("input[id='" + $(btn).attr("oid") + "']").next();
                            imageFind.remove();
                            for (var node in json) {
                                var selectListName = $("select[id='" + node + "']");
                                var inputTextboxName = $("input[id='" + node + "']");
                                var imageCreate = $("<input/>");
                                if (json[node] == 0) {
                                    imageCreate.attr({
                                        "type": "button",
                                        "title": "Done",
                                        "class": "img-done-button",
                                        "oid": node
                                    });
                                    inputTextboxName.attr({
                                        "disabled": true
                                    });
                                    selectListName.attr({
                                        "disabled": true
                                    });
                                    inputTextboxName.show();
                                    selectListName.show();
                                } else {

                                    imageCreate.attr({
                                        "type": "button",
                                        "title": json[node],
                                        "class": "img-submit-button",
                                        "oid": node
                                    });
                                    imageCreate.val("");
                                    selectListName.attr({
                                        "disabled": false
                                    });
                                    inputTextboxName.attr({
                                        "disabled": false
                                    });
                                    selectListName.attr({
                                        "disabled": false
                                    });
                                    status = 1
                                }

                                $(imageCreate).insertAfter(inputTextboxName);
                                $(imageCreate).insertAfter(selectListName);
                            }
                            if (status == 1) {
                                myForm.find("#id_omc_button_ok").hide();
                                myForm.find("#id_omc_submit_save").hide();
                                myForm.find("#id_omc_button_retry_all").show();
                                myForm.find("#id_omc_button_cancel").show()
                            } else {
                                myForm.find("#id_omc_button_retry_all").hide();
                                myForm.find("#id_omc_button_cancel").hide()
                                myForm.find("#id_omc_submit_save").hide();
                                myForm.find("#id_omc_button_ok").show();
                            }

                        }
                    } else {
                        $().toastmessage('showErrorToast', result.result);
                    }
                    spinStop($spinLoading, $spinMainLoading);
                } catch (err) {
                    $().toastmessage('showErrorToast', err);
                    spinStop($spinLoading, $spinMainLoading);
                }
            }
        });
    }
}


function odu100CommonSetAjaxRequest(formObj, btn) {
    //var btn = evt.originalEvent.explicitOriginalTarget
    ruState = $("select[id='ru.ruConfTable.synchSource']").val()
    $("input[name='node_type']").val(ruState);
    var btnName = $(btn).attr("name");
    var btnValue = $(btn).val();
    var myForm = $("#" + formObj);
    //myForm.children("div[style*='display:none']").remove();
    var data = myForm.serialize() + "&" + btnName + "=" + btnValue;
    var url = myForm.attr("action");
    url += "?aclindex=" + $("select[id='aclindex']").val(); // add the acl index value
    var method = myForm.attr("method");
    var id = myForm.attr("id");
    var host_id = myForm.find("input[name='host_id']").val();
    var device_type = myForm.find("input[name='device_type']").val();
    var status = 0;
    if (btnValue == "Ok") {
        ruState = $("select[id='ru.ruConfTable.synchSource']").val()
        $("input[name='node_type']").val(ruState);
        myForm.find("input").removeAttr("disabled");
        myForm.find("select").removeAttr("disabled");
        myForm.find("select").show();
        myForm.find("input.img-submit-button").remove();
        myForm.find("input.img-done-button").remove();
        myForm.find("input").show();
        myForm.find("input[id='id_omc_button_retry_all']").hide();
        myForm.find("input[id='id_omc_button_cancel']").hide();
        myForm.find("input[id='id_omc_button_ok']").hide();
        myForm.find("input[id='id_omc_submit_save']").show();
        $("#odu100_ra_configuration_form").find("select[id='ru.ra.tddMac.raTddMacConfigTable.encryptionType']").change();
        if (parseInt($("input[name='node_type']").val()) % 2 == 1) {
            myForm.find("select[id='ru.ra.raConfTable.acm']").attr({
                "disabled": true
            });
            myForm.find("select[id='ru.ra.raConfTable.dba']").attr({
                "disabled": true
            });
            myForm.find("select[id='ru.ra.raConfTable.acs']").attr({
                "disabled": true
            });
            myForm.find("select[id='ru.syncClock.syncConfigTable.rasterTime']").attr({
                "disabled": true
            });
            myForm.find("select[id='ru.ra.raConfTable.numSlaves']").attr({
                "disabled": true
            });
            myForm.find("select[id='ru.ra.raConfTable.dfs']").attr({
                "disabled": true
            });
            myForm.find("input[name='ru.syncClock.syncConfigTable.syncConfigTimerAdjust']").attr({
                "disabled": true
            });
            myForm.find("input[name='ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime']").attr({
                "disabled": true
            });
            myForm.find("input[name='ru.ra.raConfTable.linkDistance']").attr({
                "disabled": true
            });
        } else {
            myForm.find("select[id='ru.ra.raConfTable.acm']").removeAttr("disabled");
            myForm.find("select[id='ru.ra.raConfTable.dba']").removeAttr("disabled");
            myForm.find("select[id='ru.ra.raConfTable.acs']").removeAttr("disabled");
            myForm.find("select[id='ru.syncClock.syncConfigTable.rasterTime']").removeAttr("disabled");
            myForm.find("select[id='ru.ra.raConfTable.numSlaves']").removeAttr("disabled");
            myForm.find("select[id='ru.ra.raConfTable.dfs']").removeAttr("disabled");
            myForm.find("input[name='ru.syncClock.syncConfigTable.syncConfigTimerAdjust']").removeAttr("disabled");
            myForm.find("input[name='ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime']").removeAttr("disabled");
            myForm.find("input[name='ru.ra.raConfTable.linkDistance']").removeAttr("disabled");


        }
        spinStop($spinLoading, $spinMainLoading);
    } else if (btnValue == "Cancel ") {
        //$("a#viewButton2").click();
        myForm.find("input").removeAttr("disabled");
        myForm.find("select").removeAttr("disabled");
        myForm.find("select").show();
        myForm.find("input.img-submit-button").remove();
        myForm.find("input.img-done-button").remove();
        myForm.find("input").show();
        myForm.find("input[id='id_omc_button_retry_all']").hide();
        myForm.find("input[id='id_omc_button_cancel']").hide();
        myForm.find("input[id='id_omc_button_ok']").hide();
        myForm.find("input[id='id_omc_submit_save']").show();
        myForm.find("select[id='ru.ra.raConfTable.numSlaves']").attr({
            "disabled": true
        });
        myForm.find("select[id='ru.ra.raConfTable.dba']").attr({
            "disabled": true
        });
        myForm.find("select[id='ru.ruConfTable.synchSource']").attr({
            "disabled": true
        });
        spinStop($spinLoading, $spinMainLoading);
    } else {
        if (btnValue == "") {
            data = "host_id=" + myForm.find("input[name='host_id']").val() + "&device_type=" + myForm.find("input[name='device_type']").val() + "&" + $(btn).attr("oid") + "=" + myForm.find("input[name='" + $(btn).attr("oid") + "']").val() + "&" + btnName + "=" + btnValue;

        }

        $.ajax({
            type: method,
            url: url,
            data: data,
            success: function (result) {
                try {
                    result = eval("(" + result + ")");

                    if (result.success == 0) {
                        try {
                            var admin = parseInt(result.result_admin.success);
                            var admin_name = result.result_admin.admin_name;
                            var recTableObj = $("#adminDiv");
                            var objTable = $(recTableObj);
                            if (admin_name == "ru.ra.raConfTable.raAdminState") {
                                var imgRec = $(recTableObj).find("a:eq(1)");
                            }
                            if (admin_name == "ru.ruConfTable.adminstate") {
                                var imgRec = $(recTableObj).find("a:eq(0)");
                            }
                            var imgbtn = $(imgRec);
                            if (admin == 1) {
                                $().toastmessage('showErrorToast', result.result_admin.result);
                                imgbtn.attr({
                                    "class": "red"
                                });
                                imgbtn.html("Radio Access Locked");
                            } else {
                                imgbtn.attr({
                                    "class": "green"
                                });
                                imgbtn.html("Radio Access Unlocked");
                            }
                        } catch (err) {
                        }
                        if ((btnValue == "Save") || (btnValue == "Retry") || (btnValue == "Add") || (btnValue == "Edit") || (btnValue == "Retry ")) {

                            myForm.find("select[id='ru.ruConfTable.synchSource']").attr({
                                "disabled": true
                            });
                            var json = result.result;
                            myForm.find("input.img-submit-button").remove();
                            for (var node in json) {
                                var selectListName = $("select[id='" + node + "']");
                                var inputTextboxName = $("input[id='" + node + "']");
                                var selectAclList = $("select[id='aclindex']");

                                var imageCreate = $("<input/>");
                                if (json[node] == 0) {
                                    /*if(node == 'ru.ra.raConfTable.numSlaves')
                                     {
                                     var odu100Timeslot = parseInt($("#odu100_ra_configuration_form").find("select[id='ru.ra.raConfTable.numSlaves']").val());
                                     $("#odu100_peer_configuration_form").find("input[name='timeslot_val']").val(odu100Timeslot);
                                     for(i=odu100Timeslot;i>0;i--)
                                     {
                                     $("#odu100_peer_configuration_form").
                                     find("input[id='ru.ra.peerNode.peerConfigTable.peerMacAddress."+String(i)+"']").parent().show();
                                     }
                                     for(i=16;i>odu100Timeslot;i--)
                                     {
                                     $("#odu100_peer_configuration_form").
                                     find("input[id='ru.ra.peerNode.peerConfigTable.peerMacAddress."+String(i)+"']").parent().hide();
                                     }
                                     var odu100AclValue = parseInt($("#odu100_acl_mode_form").find("select[id='ru.ra.raConfTable.aclMode']").val());
                                     $("#odu100_peer_configuration_form").find("input[name='acl_val']").val(odu100AclValue);
                                     }*/

                                    imageCreate.attr({
                                        "type": "button",
                                        "title": "Done",
                                        "class": "img-done-button",
                                        "oid": node
                                    });
                                    inputTextboxName.attr({
                                        "disabled": true
                                    });
                                    selectListName.attr({
                                        "disabled": true
                                    });
                                    if (btnValue == "Add" || (btnValue == "Edit") || (btnValue == "Retry")) {
                                        if ($("#odu100_acl_add_mac_config_form").find("input[id='id_omc_submit_save']").val() == "Edit") {
                                            $("#odu100_acl_add_mac_config_form").find("input[id='id_omc_submit_save']").val("Add");
                                        }
                                        $(imageCreate).insertAfter(selectListName);
                                        host_id = myForm.find("input[name='host_id']").val();
                                        $.ajax({
                                            type: "post",
                                            url: "update_mac_list.py?host_id=" + host_id,
                                            success: function (result) {
                                                $("#tableDiv").html(result);
                                                $("table#show_mac_edit_delete").dataTable({
                                                    "bDestroy": true,
                                                    "bJQueryUI": true,
                                                    "bProcessing": true,
                                                    "sPaginationType": "full_numbers",
                                                    "aLengthMenu": [
                                                        [20, 40, 60, -1],
                                                        [20, 40, 60, "All"]
                                                    ],
                                                    "iDisplayLength": 20,
                                                    "aaSorting": []
                                                });
                                            }

                                        });

                                    }
                                    inputTextboxName.show();
                                    selectListName.show();

                                } else {
                                    if (btnValue == "Add" || (btnValue == "Edit") || (btnValue == "Retry")) {

                                        if ($("#odu100_acl_add_mac_config_form").find("input[id='id_omc_submit_save']").val() == "Edit") {
                                            $("#odu100_acl_add_mac_config_form").find("input[id='id_omc_submit_save']").val("Add");
                                        }
                                        imageCreate.attr({
                                            "type": "button",
                                            "title": json[node],
                                            "class": "img-submit-button",
                                            "oid": node,
                                            "name": "odu100_submit"
                                        });
                                        selectAclList.attr({
                                            "disabled": false
                                        });
                                        $(imageCreate).insertAfter(selectListName);
                                    } else {
                                        imageCreate.attr({
                                            "type": "button",
                                            "title": json[node],
                                            "class": "img-submit-button",
                                            "oid": node,
                                            "name": "odu100_submit"
                                        });
                                    }
                                    imageCreate.val("");
                                    inputTextboxName.attr({
                                        "disabled": false
                                    });
                                    selectListName.attr({
                                        "disabled": false
                                    });
                                    status = 1;

                                }
                                $(imageCreate).insertAfter(inputTextboxName);
                                $(imageCreate).insertAfter(selectListName);
                                if (node == 'ru.ra.raConfTable.aclMode') {
                                    var odu100AclVal = parseInt($("#odu100_acl_mode_form").find("select[id='ru.ra.raConfTable.aclMode']").val());
                                    $("#odu100_peer_configuration_form").find("input[name='acl_val']").val(odu100AclVal);
                                }
                                myForm.find("select[id='ru.ra.raConfTable.numSlaves']").attr({
                                    "disabled": true
                                });
                                myForm.find("select[id='ru.ra.raConfTable.dba']").attr({
                                    "disabled": true
                                });

                            }
                            if (status == 1) {
                                myForm.find("#id_omc_button_ok").hide();
                                myForm.find("#id_omc_submit_save").hide();
                                myForm.find("#id_omc_button_retry_all").show();
                                myForm.find("#id_omc_button_cancel").show();
                            } else {
                                myForm.find("#id_omc_button_retry_all").hide();
                                myForm.find("#id_omc_button_cancel").hide();
                                myForm.find("#id_omc_submit_save").hide();
                                myForm.find("#id_omc_button_ok").show();
                                spinStart($spinLoading, $spinMainLoading);
                                if (formObj == "odu100_ru_configuration_form") {
                                    // peerSelectBasicRateMCSIndex();
                                    if (odu100_ru_channel_banwidth == ru_channel_bandwidth && odu100_ru_country_code == ru_country_code) {
                                    } else {
                                        url = "refresh_channel_list.py?host_id=" + host_id + "&selected_device=" + device_type + "&refresh=" + 0 + "&ra_list_refresh=" + 1;
                                        ;
                                        method = "get";
                                        showdiv = "#content_8";
                                        //$(showdiv).html("");
                                        //$(showdiv).html("Channel list is refreshing.This take few minutes.");*/
                                        $.ajax({
                                            type: method,
                                            url: url,
                                            success: function (result) {
                                                $(showdiv).html(result);
                                                spinStop($spinLoading, $spinMainLoading);
                                            }
                                        });
                                    }
                                    odu100_ru_channel_banwidth = $("#odu100_ru_configuration_form").find("select[name='ru.ruConfTable.channelBandwidth']").val();
                                    odu100_ru_country_code = $("#odu100_ru_configuration_form").find("select[name='ru.ruConfTable.countryCode']").val();
                                    $("#channel_configuration_form").find("select").attr({
                                        "diabled": true
                                    });
                                }
                                if (formObj == "odu100_ra_configuration_form") {
                                    url = "refresh_peer_form.py?host_id=" + host_id + "&selected_device=" + device_type;
                                    method = "get";
                                    showdiv = "#content_7";
                                    $.ajax({
                                        type: method,
                                        url: url,
                                        success: function (result) {

                                            $(showdiv).html(result);
                                            //$("select","#odu100_peer_configuration_form").change();
                                            var odu100Timeslot = parseInt($("#odu100_ra_configuration_form").find("select[id='ru.ra.raConfTable.numSlaves']").val());
                                            $("#odu100_peer_configuration_form").find("input[name='timeslot_val']").val(odu100Timeslot);
                                            for (i = odu100Timeslot; i > 0; i--) {
                                                $("#odu100_peer_configuration_form").
                                                    find("input[id='ru.ra.peerNode.peerConfigTable.peerMacAddress." + String(i) + "']").parent().show();
                                            }
                                            for (i = 16; i > odu100Timeslot; i--) {
                                                $("#odu100_peer_configuration_form").
                                                    find("input[id='ru.ra.peerNode.peerConfigTable.peerMacAddress." + String(i) + "']").parent().hide();
                                            }
                                            var odu100AclValue = parseInt($("#odu100_acl_mode_form").find("select[id='ru.ra.raConfTable.aclMode']").val());
                                            $("#odu100_peer_configuration_form").find("input[name='acl_val']").val(odu100AclValue);
                                            // peerSelectBasicRateMCSIndex();
                                            spinStop($spinLoading, $spinMainLoading);
                                        }
                                    });
                                }
                                if (formObj == "odu100_acl_mode_form") {
                                    host_id = myForm.find("input[name='host_id']").val();
                                    $.ajax({
                                        type: "post",
                                        url: "update_mac_list.py?host_id=" + host_id,
                                        success: function (result) {
                                            $("#tableDiv").html(result);
                                            $("table#show_mac_edit_delete").dataTable({
                                                "bDestroy": true,
                                                "bJQueryUI": true,
                                                "bProcessing": true,
                                                "sPaginationType": "full_numbers",
                                                "aLengthMenu": [
                                                    [20, 40, 60, -1],
                                                    [20, 40, 60, "All"]
                                                ],
                                                "iDisplayLength": 20,
                                                "aaSorting": []
                                            });
                                        }

                                    });
                                }

                            }
                        } else if (btnValue == "Cancel") {

                            var json = result.result;
                            ruState = $("select[id='ru.ruConfTable.synchSource']").val()
                            $("input[name='node_type']").val(ruState);
                            myForm.find("input").removeAttr("disabled");
                            myForm.find("select").removeAttr("disabled");
                            myForm.find("select").show();
                            myForm.find("input.img-submit-button").remove();
                            myForm.find("input.img-done-button").remove();
                            myForm.find("input").show();
                            myForm.find("input[id='id_omc_button_retry_all']").hide();
                            myForm.find("input[id='id_omc_button_cancel']").hide();
                            myForm.find("input[id='id_omc_button_ok']").hide();
                            myForm.find("input[id='id_omc_submit_save']").show();
                            myForm.find("select[id='ru.ra.raConfTable.numSlaves']").attr({
                                "disabled": true
                            });
                            myForm.find("select[id='ru.ruConfTable.synchSource']").attr({
                                "disabled": true
                            });
                            for (var node in json) {
                                var inputTextboxName = $("input[id='" + node + "']");
                                inputTextboxName.val(json[node]);
                            }
                            if (parseInt($("input[name='node_type']").val()) % 2 == 1) {
                                myForm.find("select[id='ru.ruConfTable.synchSource']").removeAttr("disabled");
                                myForm.find("select[id='ru.ra.raConfTable.acm']").attr({
                                    "disabled": true
                                });
                                myForm.find("select[id='ru.ra.raConfTable.dba']").attr({
                                    "disabled": true
                                });
                                myForm.find("select[id='ru.ra.raConfTable.acs']").attr({
                                    "disabled": true
                                });
                                myForm.find("select[id='ru.syncClock.syncConfigTable.rasterTime']").attr({
                                    "disabled": true
                                });
                                myForm.find("select[id='ru.ra.raConfTable.numSlaves']").attr({
                                    "disabled": true
                                });
                                myForm.find("select[id='ru.ra.raConfTable.dfs']").attr({
                                    "disabled": true
                                });
                                myForm.find("input[name='ru.syncClock.syncConfigTable.syncConfigTimerAdjust']").attr({
                                    "disabled": true
                                });
                                myForm.find("input[name='ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime']").attr({
                                    "disabled": true
                                });
                            } else {
                                myForm.find("select[id='ru.ruConfTable.synchSource']").attr({
                                    "disabled": true
                                });
                                myForm.find("select[id='ru.ra.raConfTable.acm']").removeAttr("disabled");
                                myForm.find("select[id='ru.ra.raConfTable.dba']").removeAttr("disabled");
                                myForm.find("select[id='ru.ra.raConfTable.acs']").removeAttr("disabled");
                                myForm.find("select[id='ru.syncClock.syncConfigTable.rasterTime']").removeAttr("disabled");
                                myForm.find("select[id='ru.ra.raConfTable.numSlaves']").removeAttr("disabled");
                                myForm.find("select[id='ru.ra.raConfTable.dfs']").removeAttr("disabled");
                                myForm.find("input[name='ru.syncClock.syncConfigTable.syncConfigTimerAdjust']").removeAttr("disabled");
                                myForm.find("input[name='ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime']").removeAttr("disabled");
                            }

                        } else if (btnValue == "") {
                            $(btn).attr("oid");

                            var attrvalue = $(btn).attr("oid");
                            var json = result.result;
                            var imageFind = myForm.find("input[id='" + $(btn).attr("oid") + "']").next();
                            imageFind.remove();
                            for (var node in json) {
                                var selectListName = $("select[id='" + node + "']");
                                var inputTextboxName = $("input[id='" + node + "']");
                                var aclSelectList = $("select[id='aclindex']");
                                var imageCreate = $("<input/>");
                                if (json[node] == 0) {
                                    imageCreate.attr({
                                        "type": "button",
                                        "title": "Done",
                                        "class": "img-done-button",
                                        "oid": node
                                    });
                                    inputTextboxName.attr({
                                        "disabled": true
                                    });
                                    selectListName.attr({
                                        "disabled": true
                                    });
                                    inputTextboxName.show();
                                    selectListName.show();
                                } else {

                                    imageCreate.attr({
                                        "type": "button",
                                        "title": json[node],
                                        "class": "img-submit-button",
                                        "oid": node,
                                        "name": "odu100_submit"
                                    });
                                    imageCreate.val("");
                                    selectListName.attr({
                                        "disabled": false
                                    });
                                    inputTextboxName.attr({
                                        "disabled": false
                                    });
                                    selectListName.attr({
                                        "disabled": false
                                    });
                                    status = 1
                                }

                                $(imageCreate).insertAfter(inputTextboxName);
                                $(imageCreate).insertAfter(selectListName);
                                myForm.find("select[id='ru.ra.raConfTable.numSlaves']").attr({
                                    "disabled": true
                                });
                                myForm.find("select[id='ru.ra.raConfTable.dba']").attr({
                                    "disabled": true
                                });
                            }
                            if (status == 1) {
                                myForm.find("#id_omc_button_ok").hide();
                                myForm.find("#id_omc_submit_save").hide();
                                myForm.find("#id_omc_button_retry_all").show();
                                myForm.find("#id_omc_button_cancel").show()
                            } else {

                                myForm.find("#id_omc_button_retry_all").hide();
                                myForm.find("#id_omc_button_cancel").hide()
                                myForm.find("#id_omc_submit_save").hide();
                                myForm.find("#id_omc_button_ok").show();
                                if (formObj == "odu100_ru_configuration_form") {
                                    //peerSelectBasicRateMCSIndex();
                                    url = "refresh_channel_list.py?host_id=" + host_id + "&selected_device=" + device_type + "&refresh=" + 0 + "&ra_list_refresh=" + 1;
                                    method = "get";
                                    showdiv = "#content_8";
                                    //$(showdiv).html("");
                                    /*$(showdiv).html("Channel list is refreshing.This take few minutes.");*/
                                    $.ajax({
                                        type: method,
                                        url: url,
                                        success: function (result) {
                                            $(showdiv).html(result);
                                            spinStop($spinLoading, $spinMainLoading);
                                        }
                                    });
                                }

                            }

                        }

                    } else {

                        try {
                            $().toastmessage('showErrorToast', result.result);

                        } catch (err) {
                            $().toastmessage('showErrorToast', result.result);
                            spinStop($spinLoading, $spinMainLoading);
                        }

                    }
                    spinStop($spinLoading, $spinMainLoading);
                    //loading.hide();
                } catch (err) {
                    $().toastmessage('showErrorToast', err);
                    spinStop($spinLoading, $spinMainLoading);
                }
            }
        });
    }
}

function sleep(milliseconds) {
    var start = new Date().getTime();
    for (var i = 0; i < 1e7; i++) {
        if ((new Date().getTime() - start) > milliseconds) {
            break;
        }
    }
}

function siteSurvey() {
    if (reconcile_chk_status_btn == 0 || reconcile_chk_status_btn == null) {
        spinStart($spinLoading, $spinMainLoading);
        nodeType = parseInt($("input[name='node_type']").val());
        hostId = parseInt($("input[name='host_id']").val());
        /*       $.ajax({
         type:"get",
         url:"site_survey_data.py?host_id="+hostId,
         success:function(result)
         {
         if(parseInt(result)==0)
         {*/
        $.colorbox({
            href: "site_survey_result.py?host_id=" + hostId,
            title: "Site Survey",
            opacity: 0.4,
            maxWidth: "80%",
            width: "750px",
            height: "650px",
            overlayClose: false,
            onComplete: function () {
                $("#refresh_scan_list").click(function () {
                    //$.colorbox.close();
                    siteSnmpSurvey(hostId, nodeType);
                    $().toastmessage('showSuccessToast', "Calculating Site Survey results may take several minutes.");
                });
                $("#get_scan_list").click(function () {
                    //$.colorbox.close();
                    getSiteSurvey(hostId);
                    $().toastmessage('showSuccessToast', "Refreshing Site Survey results may take several minutes.");
                });
                if (calculate == 1) {
                    var rowCount = $('#site_survey_table tr').length;
                    var channellist = [];
                    if (listOfChannels != "" || rowCount >= 2) {
                        $('#site_survey_table tr').each(function () {
                            channellist.push($(this).find("td").eq(7).text());
                        });
                        if (rowCount > 2) {
                            //channellist.pop(channellist[0]);
                            if (channellist[0] == '') {
                                channellist.shift();
                            }
                            channelNumber = channellist.join(', ');
                        } else {
                            channelNumber = channellist[1];
                        }
                    }
                    $("input[id='listOfChannels']").val(channelNumber);
                    channelNumber = '';
                    calculate = 0;
                    listOfChannels = '';
                }
            }
        });
        // sleep(3000);
        spinStop($spinLoading, $spinMainLoading);

    } else {
        $.prompt('Reconciliation is Running.Please Wait', {
            buttons: {
                Ok: true
            },
            prefix: 'jqismooth'
        });

    }
}


function siteSnmpSurvey(hostId, nodeType) {
    listOfChannels = $("input[id='listOfChannels']").val();
    $.ajax({
        type: "post",
        url: "site_survey_snmp.py?node_type=" + nodeType + "&host_id=" + hostId + "&listOfChannels=" + listOfChannels,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                calculate = 1;
                siteSurvey();
                $().toastmessage('showSuccessToast', "Calculating Site Survey Results has successfully completed.");
            } else {
                $().toastmessage('showErrorToast', result.result);
            }
        }

    });
    return false;
}

function getSiteSurvey(hostId) {

    $.ajax({
        type: "post",
        url: "get_site_survey.py?host_id=" + hostId,
        success: function (result) {
            if (result.success == 0) {
                siteSurvey();
                $().toastmessage('showSuccessToast', "Site Survey Refresh Successfully");
            } else {
                $().toastmessage('showErrorToast', result.result);
            }
        }

    });
    return false;
}

function bwCalculateForm(host_id, device_type) {
    $.colorbox({
        href: "bw_calculate_form.py?hostId=" + host_id + "&device_type=" + device_type,
        title: "BW Calculator",
        opacity: 0.4,
        maxWidth: "100%",
        width: "500px",
        height: "300px",
        overlayClose: false
    });
}


function alarmRecon(host_id, device_type) {
    $.colorbox({
        href: "recon_display.py?host_id=" + host_id + "&device_type=" + device_type,
        title: "Alarm Reconcilation  *testing-Phase",
        overlayClose: false,
        escKey: false,
        opacity: 0.4,
        maxWidth: "100%",
        width: "600px",
        height: "300px",
        onClosed: function () {
            clearTimeout(upVar);
        }
    });
}


function editMac(uniqueid, editDelete, host_id, obj, aclVal, aclMacLen, macAddress) {
    if (editDelete == '0') {
        $.ajax({
            type: "post",
            url: "acl_data_bind.py?uuid=" + uniqueid,
            success: function (result) {

                try {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        var json = result.result;
                        $("input.img-submit-button").remove();
                        $("select").find('.img-submit-button').remove();
                        $("select[id='aclindex']").val(json.aclIndex);
                        $("select[id='aclindex']").attr('disabled', 'disabled');
                        $("select[id='ru.ra.raConfTable.aclMode']").val(json.aclMode);
                        $("input[id='ru.ra.raAclConfigTable.macaddress']").val(json.macaddress);
                        $("#odu100_acl_add_mac_config_form").find("input[id='id_omc_submit_save']").val("Edit");
                    }
                    $("a#viewButton").click();
                } catch (err) {
                    $().toastmessage('showErrorToast', "Some Problem Occurred");

                }
            }

        });
    } else {

        $.ajax({
            type: "post",
            url: "acl_delete.py?uuid=" + uniqueid + "&host_id=" + host_id + "&aclMode=" + aclVal + "&aclLen=" + aclMacLen + "&macAddress=" + macAddress,
            success: function (result) {
                try {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        aclReloadForm(); // Reload the again the ACL page
                        $(obj).parent().parent().remove();
                        $.ajax({
                            type: "post",
                            url: "update_mac_list.py?host_id=" + host_id,
                            success: function (result) {
                                $("#tableDiv").html(result);
                                $("table#show_mac_edit_delete").dataTable({
                                    "bDestroy": true,
                                    "bJQueryUI": true,
                                    "bProcessing": true,
                                    "sPaginationType": "full_numbers",
                                    "aLengthMenu": [
                                        [20, 40, 60, -1],
                                        [20, 40, 60, "All"]
                                    ],
                                    "iDisplayLength": 20,
                                    "aaSorting": []
                                });
                            }

                        });
                        $().toastmessage('showSuccessToast', 'The MAC has been deleted');
                    } else {
                        $().toastmessage('showErrorToast', result.result);
                    }
                } catch (err) {
                    $().toastmessage('showErrorToast', 'Some Problem Occured,Please Contact Your Administrator');

                }
            }
        });
    }
}

function refreshchannelList() {
    //        spinStart($spinLoading,$spinMainLoading);
    var host_id = $("#channel_configuration_form").find("input[name='host_id']").val();
    var device_type = $("#channel_configuration_form").find("input[name='device_type']").val();
    $.colorbox({
        href: "ra_channel_list_table.py?host_id=" + hostId,
        title: "RA Channel List",
        opacity: 0.4,
        maxWidth: "80%",
        width: "574px",
        height: "550px",
        overlayClose: false,
        onComplete: function () {
            $("#refresh_channel_list").click(function () {
                //$.colorbox.close();
                channelList(hostId, device_type);
                $().toastmessage('showSuccessToast', "Calculating Channel List may take several minutes.");
            });

        }
    });


    return false;

}

function channelList(hostId, device_type) {
    $.ajax({
        type: "post",
        url: "refresh_channel_freq_list.py?host_id=" + hostId + "&selected_device=" + device_type,
        success: function (result) {
            if (result.success == 1) {
                $().toastmessage('showErrorToast', result.result);
            } else {
                $.colorbox({
                    href: "ra_channel_list_table.py?host_id=" + hostId,
                    title: "RA Channel List",
                    opacity: 0.4,
                    maxWidth: "80%",
                    width: "574px",
                    height: "550px",
                    overlayClose: false,
                    onComplete: function () {
                        $("#refresh_channel_list").click(function () {
                            //$.colorbox.close();
                            channelList(hostId, device_type);
                        });
                    }
                });
                url = "refresh_channel_list.py?host_id=" + hostId + "&selected_device=" + device_type + "&ra_list_refresh=" + 0 + "&refresh=" + 0;
                method = "get";
                showdiv = "#content_8";
                //$(showdiv).html("");
                //$(showdiv).html("Channel list is refreshing.This take few minutes.");*/
                $.ajax({
                    type: method,
                    url: url,
                    success: function (result) {
                        $(showdiv).html(result);
                        spinStop($spinLoading, $spinMainLoading);
                    }
                });
                $().toastmessage('showSuccessToast', result.result);
            }
        }

    });

}

function odu100AclModeSubmit(formObj, obj) {

}


//############################################################################# Validation functions of odu100 #####################################################################################


function odu100OmcConfigurationValidation() {
    $("#odu100_omc_config_form").validate({
        rules: {
            'ru.omcConfTable.omcIpAddress': {
                required: true,
                ipv4Address: true
            },
            'ru.omcConfTable.periodicStatsTimer': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 5,
                max: 1440
            }
        },

        messages: {
            'ru.omcConfTable.omcIpAddress': {
                required: "*",
                ipv4Address: "Invalid IP Address"
            },
            'ru.omcConfTable.periodicStatsTimer': {
                required: "*",
                number: " It must be a number",
                positiveNumber: "It must be greater then zero",
                min: " It must be >= 5 and <= 1440",
                max: " It must be >= 5 and <= 1440"
            }
        }
    });
}

function odu100RUConfigurationValidation() {
    $("#odu100_ru_configuration_form").validate({
        rules: {
            'ru.ruConfTable.channelBandwidth': {
                required: true

            },
            'ru.ruConfTable.synchSource': {
                required: true

            },
            'ru.ruConfTable.countryCode': {
                required: true

            },
            'ru.ruConfTable.poeState': {
                required: true

            },
            'RU.RUConfTable.alignmentControl': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 0,
                max: 300

            }
        },

        messages: {
            'ru.ruConfTable.channelBandwidth': {
                required: "*"

            },
            'ru.ruConfTable.synchSource': {
                required: "*"

            },
            'ru.ruConfTable.countryCode': {
                required: "*"

            },
            'ru.ruConfTable.poeState': {
                required: "*"

            },
            'RU.RUConfTable.alignmentControl': {
                required: "*",
                number: " It must be a number",
                positiveNumber: "It must be greater then and equal to zero",
                min: " It must be >= 0 and <= 300",
                max: " It must be >= 0 and <= 300"
            }
        }
    });
}


function odu100IPConfigurationValidation() {
    $("#odu100_ip_config_form").validate({
        rules: {
            'ru.ipConfigTable.ipAddress': {
                required: true,
                ipv4Address: true
            },
            'ru.ipConfigTable.ipNetworkMask': {
                required: true,
                ipv4Address: true
            },
            'ru.ipConfigTable.ipDefaultGateway': {
                required: true,
                ipv4Address: true
            },
            'ru.ipConfigTable.autoIpConfig': {
                required: true
            }
        },
        messages: {
            'ru.ipConfigTable.ipAddress': {
                required: "*",
                ipv4Address: "Invalid IP Address"
            },
            'ru.ipConfigTable.ipNetworkMask': {
                required: "*",
                ipv4Address: "Invalid IP Address"

            },
            'ru.ipConfigTable.ipDefaultGateway': {
                required: "*",
                ipv4Address: "Invalid IP Address"

            },
            'ru.ipConfigTable.autoIpConfig': {
                required: "*"

            }
        }
    });
}

function odu100SyncConfigurationValidation() {
    $("#odu100_sync_config_form").validate({
        rules: {
            'ru.syncClock.syncConfigTable.rasterTime': {
                required: true
            },

            'ru.syncClock.syncConfigTable.syncLossThreshold': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 1,
                max: 100
            },
            'ru.syncClock.syncConfigTable.leakyBucketTimer': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 1,
                max: 60
            },
            'ru.syncClock.syncConfigTable.syncLostTimeout': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 30,
                max: 600
            },
            'ru.syncClock.syncConfigTable.syncConfigTimerAdjust': {
                required: true,
                number: true,
                min: -127,
                max: 127
            },
            'ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime': {
                required: true,
                number: true,
                min: 20,
                max: 80
            }


        },
        messages: {

            'ru.syncClock.syncConfigTable.rasterTime': {
                required: "*"
            },
            'ru.syncClock.syncConfigTable.syncLossThreshold': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 1 and <= 100",
                max: " It must be >= 1 and <= 100"
            },
            'ru.syncClock.syncConfigTable.leakyBucketTimer': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 1 and <= 60",
                max: " It must be >= 1 and <= 60"
            },
            'ru.syncClock.syncConfigTable.syncLostTimeout': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 30 and <= 600",
                max: " It must be >= 30 and <= 600"
            },
            'ru.syncClock.syncConfigTable.syncConfigTimerAdjust': {
                required: " *",
                number: " It must be a number",
                min: " It must be >= -127 and <= 127",
                max: " It must be >= -127 and <= 127"
            },
            'ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime': {
                required: " *",
                number: " It must be a number",
                min: " It must be >= 20 and <= 80",
                max: " It must be >= 20 and <= 80"
            }
        }
    });
}


function odu100RAConfigurationValidation() {

    $("#odu100_ra_configuration_form").validate({

        rules: {

            'ru.ra.tddMac.raTddMacConfigTable.encryptionType': {
                required: true
            },
            'ru.ra.tddMac.raTddMacConfigTable.txPower': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 0,
                max: 30

            },
            'ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 0,
                max: 50000
            },
            'ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 1,
                max: 60
            },
            'ru.ra.raConfTable.acm': {
                required: true
            },
            'ru.ra.raConfTable.dba': {
                required: true
            },
            'ru.ra.raConfTable.guaranteedBroadcastBW': {
                required: true
            },
            'ru.ra.raConfTable.acs': {
                required: true
            },
            'ru.ra.raConfTable.dfs': {
                required: true
            },
            'ru.ra.raConfTable.anc': {
                required: true
            },
            'ru.ra.raConfTable.forceMimo': {
                required: true
            }
        },
        messages: {
            'ru.ra.tddMac.raTddMacConfigTable.encryptionType': {
                required: "*"
            },
            'ru.ra.tddMac.raTddMacConfigTable.txPower': {
                required: "*",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 1 and <= 30",
                max: " It must be >= 1 and <= 30"

            },
            'ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors': {
                required: "*",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 1 and <= 50000",
                max: " It must be >= 1 and <= 50000"
            },
            'ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue': {
                required: "*",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 1 and <= 60",
                max: " It must be >= 1 and <= 60"
            },
            'ru.ra.raConfTable.acm': {
                required: "*"
            },
            'ru.ra.raConfTable.dba': {
                required: "*"
            },
            'ru.ra.raConfTable.guaranteedBroadcastBW': {
                required: "*"
            },
            'ru.ra.raConfTable.acs': {
                required: "*"
            },
            'ru.ra.raConfTable.dfs': {
                required: "*"
            },
            'ru.ra.raConfTable.anc': {
                required: "*"
            },
            'ru.ra.raConfTable.forceMimo': {
                required: "*"
            }
        }
    });
}

function odu100AclValidation() {

    $("#odu100_acl_add_mac_config_form").validate({
        rules: {
            'ru.ra.raAclConfigTable.macaddress': {
                required: true,
                macAddress: true
            },
            'ru.ra.raConfTable.aclMode': {
                required: true
            },
            'aclindex': {
                required: true
            }
        },
        messages: {
            'ru.ra.raAclConfigTable.macaddress': {
                required: "*",
                macAddress: "Please enter valid MAC Address"
            },
            'ru.ra.raConfTable.aclMode': {
                required: "*"
            },
            'aclindex': {
                required: '*'
            }
        }
    });

}


//#################################################################################################################################################################################################
/*################################################################################################################################################################################################*/


function dateTime() {
    $("#odu_ru_date_time_form").validate({
        rules: {

            'RU.RUDateTimeTable.Year': {
                required: true,
                number: true,
                min: 1900,
                max: 2037
            },
            'RU.RUDateTimeTable.Month': {
                required: true,
                number: true,
                min: 1,
                max: 12
            },
            'RU.RUDateTimeTable.Day': {
                required: true,
                number: true,
                min: 1,
                max: 31
            },
            'RU.RUDateTimeTable.Hour': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 0,
                max: 23
            },
            'RU.RUDateTimeTable.Minutes': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 0,
                max: 59
            },
            'RU.RUDateTimeTable.Seconds': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 0,
                max: 59
            }

        },
        messages: {
            'RU.RUDateTimeTable.Year': {
                required: " *",
                number: " It must be a number",
                min: " It must be >= 1900 and <= 2037",
                max: " It must be >= 1900 and <= 2037"
            },
            'RU.RUDateTimeTable.Month': {
                required: " *",
                number: " It must be a number",
                min: " It must be >= 1 and <= 12",
                max: " It must be >= 12 and <= 12"
            },
            'RU.RUDateTimeTable.Day': {
                required: " *",
                number: " It must be a number",
                min: " It must be >= 1 and <= 31",
                max: " It must be >= 1 and <= 31"
            },
            'RU.RUDateTimeTable.Hour': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 0 and <= 23",
                max: " It must be >= 0 and <= 23"
            },
            'RU.RUDateTimeTable.Minutes': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 0 and <= 59",
                max: " It must be >= 0 and <= 59"
            },
            'RU.RUDateTimeTable.Seconds': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 0 and <= 59",
                max: " It must be >= 0 and <= 59"
            }
        }
    });
}

function omcConfiguration() {
    $("#omc_configuration_form").validate({
        rules: {
            'RU.OMCConfTable.omcIPAddress': {
                required: true,
                ipv4Address: true
            },
            'RU.OMCConfTable.periodicStatisticsTimer': {
                required: true,
                number: true,
                min: 5,
                max: 1440
            }
        },
        messages: {
            'RU.OMCConfTable.omcIPAddress': {
                required: " *",
                ipv4Address: 'Not Valid Ip Address'
            },
            'RU.OMCConfTable.periodicStatisticsTimer': {
                required: " *",
                number: " It must be a number",
                min: " It must be >= 5 and <= 1440",
                max: " It must be >= 5 and <= 1440"
            }
        }
    });
}


function packetFilterMode() {
    $("#packet_filter_mode_form").validate({
        rules: {
            'ru.ruConfTable.ethFiltering': {
                required: true
            }
        }
    })
}

function ipPacketFilter() {
    $("#ip_packet_filter_form").validate({
        rules: {
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.1': {
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.2': {
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.3': {
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.4': {
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.5': {
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.6': {
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.7': {
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.8': {
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.1': {
                required: true,
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.2': {
                required: true,
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.3': {
                required: true,
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.4': {
                required: true,
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.5': {
                required: true,
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.6': {
                required: true,
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.7': {
                required: true,
                ipv4Address: true
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.8': {
                required: true,
                ipv4Address: true
            }
        },
        messages: {

            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.1': {
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.2': {
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.3': {
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.4': {
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.5': {
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.6': {
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.7': {
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterIpAddress.8': {
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.1': {
                required: "*",
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.2': {
                required: "*",
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.3': {
                required: "*",
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.4': {
                required: "*",
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.5': {
                required: "*",
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.6': {
                required: "*",
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.7': {
                required: "*",
                ipv4Address: 'Not Valid Ip Address'
            },
            'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.8': {
                required: "*",
                ipv4Address: 'Not Valid Ip Address'
            }
        }
    });
}


function macPacketFilter() {
    $("#mac_packet_filter_form").validate({
        rules: {
            'ru.packetFilters.macFilterTable.filterMacAddress.1': {
                macAddress: true
            },
            'ru.packetFilters.macFilterTable.filterMacAddress.2': {
                macAddress: true
            },
            'ru.packetFilters.macFilterTable.filterMacAddress.3': {
                macAddress: true
            },
            'ru.packetFilters.macFilterTable.filterMacAddress.4': {
                macAddress: true
            },
            'ru.packetFilters.macFilterTable.filterMacAddress.5': {
                macAddress: true
            },
            'ru.packetFilters.macFilterTable.filterMacAddress.6': {
                macAddress: true
            },
            'ru.packetFilters.macFilterTable.filterMacAddress.7': {
                macAddress: true
            },
            'ru.packetFilters.macFilterTable.filterMacAddress.8': {
                macAddress: true
            }
        },
        messages: {

            'ru.packetFilters.macFilterTable.filterMacAddress.1': {
                macAddress: 'Not Valid MAC Address'
            },
            'ru.packetFilters.macFilterTable.filterMacAddress.2': {
                macAddress: 'Not Valid MAC Address'
            },
            'ru.packetFilters.macFilterTable.filterMacAddress.3': {
                macAddress: 'Not Valid MAC Address'
            },
            'ru.packetFilters.macFilterTable.filterMacAddress.4': {
                macAddress: 'Not Valid MAC Address'
            },
            'ru.packetFilters.macFilterTable.filterMacAddress.5': {
                macAddress: 'Not Valid MAC Address'
            },
            'ru.packetFilters.macFilterTable.filterMacAddress.6': {
                macAddress: 'Not Valid MAC Address'
            },
            'ru.packetFilters.macFilterTable.filterMacAddress.7': {
                macAddress: 'Not Valid MAC Address'
            },
            'ru.packetFilters.macFilterTable.filterMacAddress.8': {
                macAddress: 'Not Valid MAC Address'
            }
        }
    });
}


function omcRegistration() {
    $("#omc_registration_form").validate({
        rules: {
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactAddr': {
                required: true
            },
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactEmail': {
                required: true,
                email: true

            },
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactMobile': {
                required: true,
                number: true


            },
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactPerson': {
                required: true

            },
            'RU.SysOmcRegistrationTable.sysOmcRegisteralternateCont': {
                required: true
            }
        },

        messages: {
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactAddr': {
                required: " *"
            },
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactEmail': {
                required: " *",
                email: "invalid email"

            },
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactMobile': {
                required: " *",
                number: " It must be a number"

            },
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactPerson': {
                required: " *"
            },
            'RU.SysOmcRegistrationTable.sysOmcRegisteralternateCont': {
                required: " *"
            }
        }
    });
}

function synConfiguration() {
    $("#syn_configuration_form").validate({
        rules: {
            'RU.SyncClock.SyncConfigTable.rasterTime': {
                required: true
            },

            'RU.SyncClock.SyncConfigTable.numSlaves': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 1,
                max: 8
            },
            'RU.SyncClock.SyncConfigTable.syncLossThreshold': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 1,
                max: 100
            },
            'RU.SyncClock.SyncConfigTable.leakyBucketTimer': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 1,
                max: 60
            },
            'RU.SyncClock.SyncConfigTable.syncLostTimeout': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 30,
                max: 600
            },
            'RU.SyncClock.SyncConfigTable.timerAdjust': {
                required: true,
                number: true,
                min: -127,
                max: 127
            }


        },
        messages: {

            'RU.SyncClock.SyncConfigTable.rasterTime': {
                required: "*"
            },
            'RU.SyncClock.SyncConfigTable.numSlaves': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 1 and <= 8",
                max: " It must be >= 1 and <= 8"
            },
            'RU.SyncClock.SyncConfigTable.syncLossThreshold': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 1 and <= 100",
                max: " It must be >= 1 and <= 100"
                //lessThan: " It should be less than IP Range End Value"
            },
            'RU.SyncClock.SyncConfigTable.leakyBucketTimer': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 1 and <= 60",
                max: " It must be >= 1 and <= 60"
            },
            'RU.SyncClock.SyncConfigTable.syncLostTimeout': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 30 and <= 600",
                max: " It must be >= 30 and <= 600"
            },
            'RU.SyncClock.SyncConfigTable.timerAdjust': {
                required: " *",
                number: " It must be a number",
                min: " It must be >= -127 and <= 127",
                max: " It must be >= -127 and <= 127"
            }
        }
    });
}

function networkInterfaceConfig() {
    $("#omd_network_interface_config_form").validate({
        rules: {
            'RU.NetworkInterface.1.NetworkInterfaceConfigTable.ssId': {
                required: true
            },
            'RU.NetworkInterface.2.NetworkInterfaceConfigTable.ssId': {
                required: true
            }
        },
        messages: {
            'RU.NetworkInterface.1.NetworkInterfaceConfigTable.ssId': {
                required: " *"
            },
            'RU.NetworkInterface.2.NetworkInterfaceConfigTable.ssId': {
                required: " *"
            }
        }
    });
}

function llcConfiguration() {
    $("#ra_llc_config_form").validate({
        rules: {
            'RU.RA.1.LLC.RALLCConfTable.arqWin': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 0,
                max: 5
            },

            'RU.RA.1.LLC.RALLCConfTable.frameLossThreshold': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 0,
                max: 429497295
            },
            'RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 1,
                max: 60
            },
            'RU.RA.1.LLC.RALLCConfTable.frameLossTimeout': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 30,
                max: 600
            }

        },
        messages: {

            'RU.RA.1.LLC.RALLCConfTable.arqWin': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then -1",
                min: " It must be >= 0 and <= 5",
                max: " It must be >= 0 and <= 5"
            },
            'RU.RA.1.LLC.RALLCConfTable.frameLossThreshold': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then -1",
                min: " It must be >= 0 and <= 429497295",
                max: " It must be >= 0 and <= 429497295"
            },
            'RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then -1",
                min: " It must be >= 1 and <= 60",
                max: " It must be >= 1 and <= 60"
                //lessThan: " It should be less than IP Range End Value"
            },
            'RU.RA.1.LLC.RALLCConfTable.frameLossTimeout': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 30 and <= 600",
                max: " It must be >= 30 and <= 600"
            }
        }
    });
}

function tddMacConfiguration() {
    $("#tdd_mac_config_form").validate({
        rules: {
            'ru.np.ra.1.tddmac.rfChannel': {
                required: true
            },

            'ru.np.ra.1.tddmac.txPower': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 0,
                max: 19
            },
            'RU.RA.1.TddMac.RATDDMACConfigTable.maxCrcErrors': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 0,
                max: 50000
            },
            'RU.RA.1.TddMac.RATDDMACConfigTable.leakyBucketTimer': {
                required: true,
                number: true,
                positiveNumber: true,
                min: 1,
                max: 60
            }

        },
        messages: {

            'ru.np.ra.1.tddmac.rfChannel': {
                required: " *"
            },
            'ru.np.ra.1.tddmac.txPower': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then -1",
                min: " It must be >= 0 and <= 19",
                max: " It must be >= 0 and <= 19"
            },
            'RU.RA.1.TddMac.RATDDMACConfigTable.maxCrcErrors': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then -1",
                min: " It must be >= 1 and <= 50000",
                max: " It must be >= 1 and <= 50000"
            },
            'RU.RA.1.TddMac.RATDDMACConfigTable.leakyBucketTimer': {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero",
                min: " It must be >= 1 and <= 60",
                max: " It must be >= 1 and <= 60"
            }
        }
    });
}

function peerMacValid() {
    $("#peer_config_form").validate({
        rules: {
            'ru.np.ra.1.peer.1.config.macAddress': {
                macAddress: true
            },
            'ru.np.ra.1.peer.2.config.macAddress': {
                macAddress: true
            },
            'ru.np.ra.1.peer.3.config.macAddress': {
                macAddress: true
            },
            'ru.np.ra.1.peer.4.config.macAddress': {
                macAddress: true
            },
            'ru.np.ra.1.peer.5.config.macAddress': {
                macAddress: true
            },
            'ru.np.ra.1.peer.6.config.macAddress': {
                macAddress: true
            },
            'ru.np.ra.1.peer.7.config.macAddress': {
                macAddress: true
            },
            'ru.np.ra.1.peer.8.config.macAddress': {
                macAddress: true
            }
        },
        messages: {
            'ru.np.ra.1.peer.1.config.macAddress': {
                macAddress: "Invalid Mac Address"
            },
            'ru.np.ra.1.peer.2.config.macAddress': {
                mmacAddress: "Invalid Mac Address"
            },
            'ru.np.ra.1.peer.3.config.macAddress': {
                macAddress: "Invalid Mac Address"
            },
            'ru.np.ra.1.peer.4.config.macAddress': {
                macAddress: "Invalid Mac Address"
            },
            'ru.np.ra.1.peer.5.config.macAddress': {
                macAddress: "Invalid Mac Address"
            },
            'ru.np.ra.1.peer.6.config.macAddress': {
                macAddress: "Invalid Mac Address"
            },
            'ru.np.ra.1.peer.7.config.macAddress': {
                macAddress: "Invalid Mac Address"
            },
            'ru.np.ra.1.peer.8.config.macAddress': {
                macAddress: "Invalid Mac Address"
            }
        }
    });
}

function odu100peerMacValid() {
    $("#odu100_peer_configuration_form").validate({
        rules: {
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.1': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.2': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.3': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.4': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.5': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.6': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.7': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.8': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.9': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.10': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.11': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.12': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.13': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.14': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.15': {
                macAddress: true
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.16': {
                macAddress: true
            }
        },
        messages: {
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.1': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.2': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.3': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.4': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.5': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.6': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.7': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.8': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.9': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.10': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.11': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.12': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.13': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.14': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.15': {
                macAddress: "Invalid Mac Address"
            },
            'ru.ra.peerNode.peerConfigTable.peerMacAddress.16': {
                macAddress: "Invalid Mac Address"
            }
        }
    });
}