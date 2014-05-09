var chosseDeviceForAdd = 0;
var lastTab = "#viewButton";
var currentVap = "1";
var wep = "<table><tbody><tr><td class=\"headerBLK\" colspan=\"2\">Simple WEP Security(64 0r 128 bit hardware key)</td></tr><tr><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MODE:</td><td><input type=\"radio\" id=\"wepmode1\" value=\"1\" name=\"AP_WEP_MODE_0\">Open<input type=\"radio\" id=\"wepmode2\" value=\"2\" name=\"AP_WEP_MODE_0\">Shared<input type=\"radio\" id=\"wepmode4\" value=\"4\" name=\"AP_WEP_MODE_0\">Auto</td></tr><tr><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Key 1</td><td><input type=\"text\" onblur=\"wepkeycheck('1')\" maxlength=\"32\" name=\"WEPKEY_1\" id=\"WEPKEY_1\"><input type=\"radio\" id=\"Wepkey1_chk\" value=\"1\" name=\"AP_PRIMARY_KEY_0\"> Primary Key</td></tr><tr><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Key 2</td><td><input type=\"text\" onblur=\"wepkeycheck('2')\" maxlength=\"32\" name=\"WEPKEY_2\" id=\"WEPKEY_2\"><input type=\"radio\" id=\"Wepkey2_chk\" value=\"2\" name=\"AP_PRIMARY_KEY_0\"> Primary Key</td></tr><tr><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Key 3</td><td><input type=\"text\" onblur=\"wepkeycheck('3')\" maxlength=\"32\" name=\"WEPKEY_3\" id=\"WEPKEY_3\"><input type=\"radio\" id=\"Wepkey3_chk\" value=\"3\" name=\"AP_PRIMARY_KEY_0\"> Primary Key</td></tr><tr><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Key 4</td><td><input type=\"text\" onblur=\"wepkeycheck('4')\" maxlength=\"32\" name=\"WEPKEY_4\" id=\"WEPKEY_4\"><input type=\"radio\" id=\"Wepkey4_chk\" value=\"4\" name=\"AP_PRIMARY_KEY_0\"> Primary Key</td></tr></tbody></table>";

var repeaterToClient = 0;

$(function () {
    $(document).click(function () {
        $("#addDivHover").hide();
        if (chosseDeviceForAdd != 1) {
            $("div.main-head").find("a.tab-active").removeClass("tab-active").addClass("tab-button");
            $(lastTab).removeClass("tab-button").addClass("tab-active");
        }
    });
    $("div.device-hover-menu").find("a").click(function (e) {
        e.preventDefault();
        e.stopPropagation();
        $("#editButton").hide();
        $("#editDiv").html("");
        chosseDeviceForAdd = 1;
        $.ajax({
            type: "post",
            url: "add_configuration_template.py?deviceId=" + $(this).attr("id") + "&deviceName=" + $(this).text(),
            success: function (result) {
                $("div.tab-body").hide();
                // Apply jQuery
                result = $(result);
                result.find("div.tab-yo").find("div.tab-head").find("a").click(function (e) {
                    e.preventDefault();
                    $(this).parent().find("a.tab-active").removeClass("tab-active").addClass("tab-button");
                    $(this).removeClass("tab-button").addClass("tab-active");
                    $(this).parent().parent().find("div.tab-body").hide();
                    $($(this).attr("href")).show();
                    if ($(this).attr("href") == "#vapDiv")
                        vapLoad();
                });
                validateCreateTemplate(result.find("#createTemplate"));
                result.find("#createTemplate").submit(function () {
                    validationForm = vapValidation();
                    if ($(this).valid() && validationForm) {
                        $("div.loading").show();
                        formAction = $(this).attr("action") + "?" + $(this).serialize();
                        $.ajax({
                            type: "post",
                            url: formAction,
                            success: function (result) {
                                if (result == "0") {
                                    alert("Configuration Profile Added successfully");
                                    cancelAddProfile();
                                    $("div.loading").hide();
                                }
                                else {
                                    alert("Some error occured, please refresh the page and try again");
                                    $("div.loading").hide();
                                }
                            }
                        });
                    }
                    return false;
                });
                $("#addDiv").html(result);
                $("#addDiv").show();
                callAfterCreateTemplateForm();
                setValuesInWep();
            }
        });
        $("div.device-hover-menu").hide();
    })
    $("div.tab-head").find("a").click(function (e) {
        e.preventDefault();
        if ($(this).attr("href") == "#addDiv") {
            e.stopPropagation();
            if ($(this).parent().find("a.tab-active").attr("href") != "#addDiv")
                lastTab = $(this).parent().find("a.tab-active");
            $(this).parent().find("a.tab-active").removeClass("tab-active").addClass("tab-button");
            $(this).removeClass("tab-button").addClass("tab-active");
            $($(this).attr("href") + "Hover").show();
        }
        else if ($(this).attr("href") == "#editDiv") {
            chosseDeviceForAdd = 0;
        }
        else {
            var myObj = $(this);
            $.ajax({
                type: "post",
                url: "view_configuration_template.py",
                success: function (result) {
                    $(myObj.attr("href")).html(result);
                }
            });
            chosseDeviceForAdd = 0;
            $(this).parent().find("a.tab-active").removeClass("tab-active").addClass("tab-button");
            $(this).removeClass("tab-button").addClass("tab-active");
            $("div.tab-body").hide();
            $($(this).attr("href")).show();
            lastTab = "#viewButton";
            $("#editButton").hide()
        }
    });

});
function editConfigurationProfile(id) {
    $("#addDiv").html("");
    chosseDeviceForAdd = 0;
    lastTab = "#editButton";
    $.ajax({
        type: "post",
        url: "edit_configuration_template.py?templateId=" + id,
        success: function (result) {
            $("div.tab-body").hide();
            // Apply jQuery
            result = $(result);
            result.find("div.tab-yo").find("div.tab-head").find("a").click(function (e) {
                e.preventDefault();
                $(this).parent().find("a.tab-active").removeClass("tab-active").addClass("tab-button");
                $(this).removeClass("tab-button").addClass("tab-active");
                $(this).parent().parent().find("div.tab-body").hide();
                $($(this).attr("href")).show();
                if ($(this).attr("href") == "#vapDiv")
                    vapLoad();
            });
            validateCreateTemplate(result.find("#createTemplate"));
            result.find("#createTemplate").submit(function () {
                validationForm = vapValidation();
                if ($(this).valid() && validationForm) {
                    $("div.loading").show();
                    formAction = $(this).attr("action") + "?" + $(this).serialize();
                    $.ajax({
                        type: "post",
                        url: formAction,
                        success: function (result) {
                            if (result == "0") {
                                alert("Configuration Profile Updated successfully");
                                cancelEditProfile();
                                $("div.loading").hide();
                            }
                            else {
                                alert("Some error occured, please refresh the page and try again");
                                $("div.loading").hide();
                            }
                        }
                    });
                }
                return false;
            });
            $("#addButton, #viewButton").removeClass("tab-active").addClass("tab-button");
            $("#editDiv").html(result);
            $("#editDiv").show();
            $("#editButton").show().removeClass("tab-button").addClass("tab-active");
            callAfterCreateTemplateForm();
            setValuesInWep();
        }
    });
}
function deleteConfigurationProfile(id) {
    if (confirm("Are you sure, you want to delete this configuration profile?")) {
        $("div.loading").show();
        $.ajax({
            type: "post",
            url: "delete_configuration_template.py?templateId=" + id,
            success: function (result) {
                if (result == "0") {
                    $.ajax({
                        type: "post",
                        url: "view_configuration_template.py",
                        success: function (result) {
                            $("#viewDiv").html(result);
                        }
                    });
                    alert("Configuration Profile Deleted successfully.");
                    $("div.loading").hide();
                }
                else {
                    alert("Some error occured, please refresh the page and try again");
                    $("div.loading").hide();
                }
            }
        });
    }
}
function cancelAddProfile() {
    lastTab = "#viewButton";
    $.ajax({
        type: "post",
        url: "view_configuration_template.py",
        success: function (result) {
            $("#viewDiv").html(result);
        }
    });
    chosseDeviceForAdd = 0;
    $("#addButton, #editButton").removeClass("tab-active").addClass("tab-button");
    $("#viewButton").removeClass("tab-button").addClass("tab-active");
    $("#addDiv").hide();
    $("#viewDiv").show();
    $("#addDiv").html("");
}
function cancelEditProfile() {
    lastTab = "#viewButton";
    $.ajax({
        type: "post",
        url: "view_configuration_template.py",
        success: function (result) {
            $("#viewDiv").html(result);
        }
    });
    chosseDeviceForAdd = 0;
    $("#addButton, #editButton").removeClass("tab-active").addClass("tab-button");
    $("#viewButton").removeClass("tab-button").addClass("tab-active");
    $("#editDiv, #editButton").hide();
    $("#viewDiv").show();
    $("#editDiv").html("");
}
function validateCreateTemplate(formObj) {
    $(formObj).validate({
        rules: {
            deviceName: "required",
            templateName: "required",
            AP_HOSTNAME: "required",
            AP_NETMASK: "required",
            IPGW: "required",
            AMPDUFRAMES: {
                required: "#chk_AMPDU_Enable:checked"
            },
            AMPDULIMIT: {
                required: "#chk_AMPDU_Enable:checked"
            },
            AMPDUMIN: {
                required: "#chk_AMPDU_Enable:checked"
            },
            AP_SYSLOG_IP: {
                required: "#syslog_enable:checked"
            },
            SYSLOG_PORT: {
                required: "#syslog_enable:checked"
            },
            SNMP_Comm: {
                required: "#snmp_enable:checked"
            },
            SNMP_Location: {
                required: "#snmp_enable:checked"
            },
            SNMP_Contact: {
                required: "#snmp_enable:checked"
            },
            DHCP_SIP: {
                required: "#DHCP_SER_EN:checked"
            },
            DHCP_EIP: {
                required: "#DHCP_SER_EN:checked"
            },
            DHCP_NM: {
                required: "#DHCP_SER_EN:checked"
            },
            DHCP_LEASE: {
                required: "#DHCP_SER_EN:checked"
            },
            txt_date: {
                required: "#NTP_Enable option:eq(0):selected"
            },
            txt_hour: {
                required: "#NTP_Enable option:eq(0):selected"
            },
            txt_minute: {
                required: "#NTP_Enable option:eq(0):selected"
            },
            txt_second: {
                required: "#NTP_Enable option:eq(0):selected"
            },
            NTPSERVERIP: {
                required: "#NTP_Enable option:eq(1):selected"
            }
        },
        messages: {
            deviceName: " *",
            templateName: " *",
            AP_HOSTNAME: " *",
            AP_NETMASK: " *",
            IPGW: " *",
            AMPDUFRAMES: {
                required: " *"
            },
            AMPDULIMIT: {
                required: " *"
            },
            AMPDUMIN: {
                required: " *"
            },
            AP_SYSLOG_IP: {
                required: " *"
            },
            SYSLOG_PORT: {
                required: " *"
            },
            SNMP_Comm: {
                required: " *"
            },
            SNMP_Location: {
                required: " *"
            },
            SNMP_Contact: {
                required: " *"
            },
            DHCP_SIP: {
                required: " *"
            },
            DHCP_EIP: {
                required: " *"
            },
            DHCP_NM: {
                required: " *"
            },
            DHCP_LEASE: {
                required: " *"
            },
            txt_date: {
                required: " *"
            },
            txt_hour: {
                required: " *"
            },
            txt_minute: {
                required: " *"
            },
            txt_second: {
                required: " *"
            },
            NTPSERVERIP: {
                required: " *"
            }
        }
    });
}
// ============================ AP Configuration Function ==================================
// network
var dhcpState = function (state) {
    if (!state) {
        $('#DHCP_SIP').attr("readonly", true);
        $('#DHCP_EIP').attr("readonly", true);
        $('#DHCP_NM').attr("readonly", true);
        $('#DHCP_LEASE').attr("readonly", true);
        //document.getElementById('DHCP_ClientList').disabled=true;
    }
    else {
        $('#DHCP_SIP').attr("readonly", false);
        $('#DHCP_EIP').attr("readonly", false);
        $('#DHCP_NM').attr("readonly", false);
        $('#DHCP_LEASE').attr("readonly", false);
        //document.getElementById('DHCP_ClientList').disabled=false;
    }
};
// radio
var ManageVlanPrompt = function (status) {
    if (status)
        alert("The First VAP will be used for management");
};
var ToggleMVlan = function (status) {
    var row = document.getElementById("ManageVlan_tr");
    if (status) {
        if ((document.getElementById('startup_multi').checked == true) || (document.getElementById('startup_multivlan').checked == true)) {
            var noofvaps = '4';
            document.getElementById('NoofVaps').value = noofvaps;
            document.getElementById('HID_AP_MAX_VAP').value = noofvaps;
            document.getElementById('NoofVaps').disabled = false;
            manageVapDropDown(noofvaps);
        }

        if ("1" == "1" && ("standard" == "multivlan"))
            document.getElementById('Enbl_mngmtvlan').checked = true;
        else
            document.getElementById('Dsbl_mngmtvlan').checked = true;
        row.style.display = 'block';
    }
    else {
        row.style.display = 'none';
        document.getElementById('Dsbl_mngmtvlan').checked = true;
        if ((document.getElementById('startup_client').checked == true) || (document.getElementById('startup_standard').checked == true) || (document.getElementById('startup_rootap').checked == true)) {
            document.getElementById('NoofVaps').value = 1;
            document.getElementById('HID_AP_MAX_VAP').value = 1;
            manageVapDropDown(1)
            document.getElementById('NoofVaps').disabled = true;
        }
        else if (document.getElementById('startup_repeater').checked == true) {
            document.getElementById('NoofVaps').value = 2;
            document.getElementById('HID_AP_MAX_VAP').value = 2;
            manageVapDropDown(2);
            document.getElementById('NoofVaps').disabled = true;
        }
        if ((document.getElementById('startup_multi').checked == true) || (document.getElementById('startup_multivlan').checked == true)) {
            var noofvaps = '4';
            document.getElementById('NoofVaps').value = noofvaps;
            document.getElementById('HID_AP_MAX_VAP').value = noofvaps;
            manageVapDropDown(noofvaps);
            document.getElementById('NoofVaps').disabled = false;
        }
        if ((document.getElementById('startup_client').checked == true) || (document.getElementById('startup_repeater').checked == true))//Disable the Channel selection in Client Mode
        {
            document.getElementById('AP_Channel').disabled = true;
        }
        else//Enable the Channel selection
        {
            document.getElementById('AP_Channel').disabled = false;
        }
    }
};
var SwapAggregation = function (status) {
    $('#AMPDUFRAMES').attr("readonly", !status);
    $('#AMPDULIMIT').attr("readonly", !status);
    $('#AMPDUMIN').attr("readonly", !status);
};

//Distance
var SwapDistance = function (type) {
    var manual = document.getElementById('Distance_manual');
    var auto = document.getElementById('Distance_auto');
    if (type == 0) {
        manual.style.display = 'none';
        auto.style.display = 'none';
    }
    if (type == 1) {
        manual.style.display = 'none';
        auto.style.display = 'block';
    }
    if (type == 2) {
        manual.style.display = 'block';
        auto.style.display = 'none';
    }
};

// vap config
var Toggle_ssid = function (val) {
    var hidechk = document.getElementById('HIDE_SSID_' + val);
    var hdnvar = document.getElementById('hdn_ssid_' + val);
    if (hidechk.checked) {
        hidechk.value = 1;
        hdnvar.value = 1;
    }
    else {
        hidechk.value = 0;
        hdnvar.value = 0;
    }
};
var Toggle_Dynvlan = function () {
    if (document.getElementById('chk_dyn_vlan').checked) {
        displayData(3, currentVap);
        default_fillEnt(currentVap);
        document.getElementById('secwpa2_' + currentVap).checked = true;
        document.getElementById('sec_802_' + currentVap).disabled = true;
        document.getElementById('sec_open_' + currentVap).disabled = true;
        document.getElementById('chk_PersonalKey_' + currentVap).disabled = true;
        document.getElementById('sec_wep_' + currentVap).disabled = true;
        document.getElementById('sec_wpa_' + currentVap).checked = true;
        document.getElementById('dyn_vlan').value = 1;
        document.getElementById('chk_EnterpriseKey_' + currentVap).checked = true;
    }
    else {
        document.getElementById('sec_802_' + currentVap).disabled = false;
        document.getElementById('sec_open_' + currentVap).disabled = false;
        document.getElementById('chk_PersonalKey_' + currentVap).disabled = true;
        document.getElementById('sec_wep_' + currentVap).disabled = false;
        document.getElementById('chk_PersonalKey_' + currentVap).disabled = false;
        document.getElementById('dyn_vlan').value = 0;
    }
};
var displayData = function (id, val) {
    var obj1 = document.getElementById('open_div_' + val);
    if (parseInt(val) == 1 || parseInt(val) == 2)
        var obj2 = document.getElementById('WEP_div_' + val);
    var obj3 = document.getElementById('WPA_div_' + val);
    //var obj4=document.getElementById('802_div');
    switch (id) {
        case 1:
        {
            obj1.style.display = 'block';
            if (parseInt(val) == 1 || parseInt(val) == 2)
                obj2.style.display = 'none';
            obj3.style.display = 'none';
            // obj4.style.display='none';
            break;
        }
        case 2:
        {
            obj1.style.display = 'none';
            if (parseInt(val) == 1 || parseInt(val) == 2)
                obj2.style.display = 'block';
            obj3.style.display = 'none';
            // obj4.style.display='none';
            defaultwep(val);
            break;
        }
        case 3:
        {
            obj1.style.display = 'none';
            if (parseInt(val) == 1 || parseInt(val) == 2)
                obj2.style.display = 'none';
            obj3.style.display = 'block';
            // obj4.style.display='none';
            securitydef(val);
            break;
        }
        case 4:
        {
            obj1.style.display = 'none';
            if (parseInt(val) == 1 || parseInt(val) == 2)
                obj2.style.display = 'none';
            obj3.style.display = 'none';
            obj4.style.display = 'block';
            break;
        }
        default:
        {
            break;
        }
    }
};
var defaultwep = function () {
    if (!(document.getElementById('wepmode1').checked || document.getElementById('wepmode2').checked || document.getElementById('wepmode4').checked)) {
        document.getElementById('wepmode1').checked = true;
        document.getElementById('Wepkey1_chk').checked = true;
    }
};
var securitydef = function (val) {
    var sec802 = document.getElementById('sec_802_' + val);
    var secwpa = document.getElementById('secwpa_' + val);
    var secwpa2 = document.getElementById('secwpa2_' + val);
    var secauto = document.getElementById('secauto_' + val);
    if (!(sec802.checked || secwpa.checked || secwpa2.checked || secauto.checked)) {
        secwpa2.checked = true;
        document.getElementById('cypher_CCMP_' + val).checked = true;
        document.getElementById('chk_PersonalKey_' + val).checked = true;
        document.getElementById("AP_WPA_GROUP_REKEY_" + val).value = '600';
        document.getElementById("AP_WPA_GMK_REKEY_" + val).value = '86400';
    }
};
var default_fillEnt = function (val) {
    var dsbl = document.getElementById('interface_dis_' + val);
    var enbl = document.getElementById('interface_enb_' + val);
    var reauth = document.getElementById('AP_EAP_REAUTH_PER_' + val);
    var port = document.getElementById('AP_AUTH_PORT_' + val);
    var server = document.getElementById('AP_AUTH_SERVER_' + val);
    var sec = document.getElementById('AP_AUTH_SECRET_' + val);
    var Interfc = document.getElementById('AP_WPA_PREAUTH_IF_' + val);
    if (!(dsbl.checked || enbl.checked)) {
        dsbl.checked = true;
    }
    if (reauth.value == '') {
        reauth.value = '3600';
    }
    if (port.value == '') {
        port.value = '1812';
    }
    dsbl.disabled = false;
    enbl.disabled = false;
    reauth.disabled = false;
    port.disabled = false;
    server.disabled = false;
    sec.disabled = false;
    Interfc.disabled = false;
    document.getElementById('PSK_KEY_' + val).disabled = true;
};
var wepkeycheck = function (keyid) {
    var flag = 0;
    var key = document.getElementById('WEPKEY_' + keyid).value;
    if ((key.length == 0) || (key.length == 5) || (key.length == 13) || (key.length == 16)) {
        flag = 1;
    }
    else {
        if ((key.length == 10) || (key.length == 26) || (key.length == 32)) {
            var valid = (/[^A-Fa-f0-9]/.test(key) == false );
            if (!valid) {
                alert('Not a valid HEX Key. Key contains non-Hex characters');
                document.getElementById('WEPKEY_' + keyid).value = '';
                return 0;
            }
            else {
                flag = 1;
            }
        }
    }
    if (flag == 0) {
        alert("Invalid WEP key length. Length can be 5,13,16 for ASCII and 10,26,32 for HEX");
        document.getElementById('WEPKEY_' + keyid).value = '';
        return 0;
    }
    return 1;
};
var EnableEnterprise = function (val) {
    document.getElementById('chk_PersonalKey_' + val).checked = false;
    document.getElementById('chk_EnterpriseKey_' + val).checked = true;
    document.getElementById('chk_PersonalKey_' + val).disabled = true;
    document.getElementById('PSK_KEY_' + val).disabled = true;
    document.getElementById('AP_WEP_REKEY_' + val).value = '600';
    //Default values for Enterprise
    default_fillEnt(val);
};
var AlterEnterprise = function (val) {
    if (!document.getElementById('chk_dyn_vlan').checked) {
        document.getElementById('chk_PersonalKey_' + val).disabled = false;
    }
    if (document.getElementById('chk_PersonalKey_' + val).checked) {
        document.getElementById('PSK_KEY_' + val).disabled = false;
    }
    document.getElementById('AP_WEP_REKEY_' + val).value = '';
};
var default_clearEnt = function (val) {
    var dsbl = document.getElementById('interface_dis_' + val);
    var enbl = document.getElementById('interface_enb_' + val);
    var reauth = document.getElementById('AP_EAP_REAUTH_PER_' + val);
    var port = document.getElementById('AP_AUTH_PORT_' + val);
    var server = document.getElementById('AP_AUTH_SERVER_' + val);
    var sec = document.getElementById('AP_AUTH_SECRET_' + val);
    var Interfc = document.getElementById('AP_WPA_PREAUTH_IF_' + val);
    dsbl.checked = false;
    enbl.checked = false;
    //Don't remove the existing values
    //reauth.value='';
    //port.value='';
    //server.value='';
    //sec.value='';
    //Interfc.value='';
    dsbl.disabled = true;
    enbl.disabled = true;
    reauth.disabled = true;
    port.disabled = true;
    server.disabled = true;
    sec.disabled = true;
    Interfc.disabled = true;
    document.getElementById('PSK_KEY_' + val).disabled = false;
};
var keylen_check = function (val) {
    var psk = document.getElementById('chk_PersonalKey_' + val);
    var wpa = document.getElementById('sec_wpa_' + val);
    if (!(wpa.checked && psk.checked)) {
        return true;
    }
    var key = document.getElementById('PSK_KEY_' + val).value;
    if (key.length < 8) {
        alert('Key length should be greater than 8');
        document.getElementById('PSK_KEY_' + val).value = '';
        return false;
    }
    return true;
};
var modeChange = function (type, numb) {
    var m = '#' + type + '_mode' + numb;
    var t = '#txt_' + type + '_thr' + numb;
    var h = '#hdn_' + type + '_thr' + numb;
    //alert(t);
    var mode = $(m);
    var thr = $(t);
    var hdn = $(h);
    if (parseInt(mode.val()) == 0) {
        thr.hide();
        hdn.val('off');
    }
    /*if(mode.value==1)
     {
     thr.style.visibility='hidden'
     thr.value=1;
     }*/
    if (parseInt(mode.val()) == 2) {
        thr.show();
        if (hdn.val() == 'off') {
            if (parseInt(thr.val()) < 256 || parseInt(thr.val()) > 2346)
                thr.val('');
            else if ($.trim(thr.val()) != "")
                hdn.val(thr.val())
        }
        else if (parseInt(hdn.val()) > 255)
            thr.val(hdn.val());
    }
};
var checkThr = function (type, numb) {
    var m = '#' + type + '_mode' + numb;
    var t = '#txt_' + type + '_thr' + numb;
    var h = '#hdn_' + type + '_thr' + numb;
    var mode = $(m);
    var thr = $(t);
    var hdn = $(h);
    if (parseInt(mode.val()) == 2) {
        if (parseInt(thr.val()) < 256 || parseInt(thr.val()) > 2346) {
            alert('Threshold should be between 256 - 2346');
            hdn.val('off');
            return false;
        }
        if ($.trim(thr.val()) != "")
            hdn.val(thr.val());
        else
            hdn.val("off");
    }
    return true;
};

// ACL
var ToggleACL = function (val, vap) {
    var acltable = $('#acl_vap' + vap + '_tr');
    if (val) {
        acltable.show();
    }
    else {
        acltable.hide();
    }
};
// Services
var ServiceState = function (type, state) {
    if (type == 'Snmp') {
        $('#snmp_comm').attr("readonly", !state);
        $('#snmp_location').attr("readonly", !state);
        $('#snmp_contact').attr("readonly", !state);
    }
    else {
        $('#syslog_ip').attr("readonly", !state);
        $('#syslog_port').attr("readonly", !state);
    }
};
var TimeFlag = 0;
var checktime = function (type) {
    if (type == 'hour') {
        var hour = document.getElementById('txt_hour');
        if (parseInt(hour.value, 10) > 24) {
            alert('Invalid Time');
            hour.value = '0';
        }
    }

    if (type == 'minute' || type == 'second') {
        var minute = document.getElementById('txt_minute');
        if (parseInt(minute.value, 10) > 60) {
            alert('Invalid Time');
            minute.value = '0';
        }
        var sec = document.getElementById('txt_second');
        if (parseInt(sec.value, 10) > 60) {
            alert('Invalid Time');
            sec.value = '0';
        }
    }
};
var GetSystemTime = function (trigger) {

    if (trigger == 1 && TimeFlag == 0) {
        TimeFlag = 1;
        document.getElementById('btn_getTime').value = "Set Date&Time Manually";
    }
    else {
        if (trigger == 1 && TimeFlag == 1) {
            TimeFlag = 0;
            document.getElementById('btn_getTime').value = "Copy Computer Date&Time";
        }
    }

    if (TimeFlag == 1) {
        var currentTime = new Date();
        var day = 1;
        var month = 1;
        var year = 2010;
        var hour = 0;
        var minute = 0;
        var seconds = 0;
        var gmtHours = -currentTime.getTimezoneOffset() / 60;
        day = currentTime.getDate();
        if (parseInt(day, 10) < 10) {
            day = '0' + day;
        }
        month = currentTime.getMonth() + 1;
        if (parseInt(month, 10) < 10) {
            month = '0' + month;
        }

        year = currentTime.getFullYear();
        hour = currentTime.getHours();
        if (parseInt(hour, 10) < 10) {
            hour = '0' + hour;
        }
        minute = currentTime.getMinutes();
        if (parseInt(minute, 10) < 10) {
            minute = '0' + minute;
        }
        seconds = currentTime.getSeconds();
        if (parseInt(seconds, 10) < 10) {
            seconds = '0' + seconds;
        }
        var zone = document.getElementById('DropDownTimezone');
        //Time Zone Setting
        if (parseInt(gmtHours, 10) > 0) {
            gmtHours = '+' + gmtHours;
        }
        gmtHours = gmtHours.replace(".5", ":30");
        gmtHours = gmtHours.replace(".75", ":45");
        var flag = 0;
        for (var i = 0; i < gmtHours.length; i++) {
            if (gmtHours[i] == ':')
                flag = 1;
        }
        if (flag == 0) {
            gmtHours = gmtHours + ":00";
        }

        for (i = 0; i < zone.options.length; i++) {
            var txt = zone.options[i].text.substring(10, gmtHours.length);
            if (txt == gmtHours) {
                zone.options[i].selected = true;
            }
        }

        //End of TimeZone set


        var cur_date = month + '/' + day + '/' + year;
        document.getElementById('txt_date').value = cur_date;
        document.getElementById('txt_hour').value = hour;
        document.getElementById('txt_minute').value = minute;
        document.getElementById('txt_second').value = seconds;
    }
};
var AlterTimeSettings = function () {
    var type = $('#NTP_Enable').val();
    if (type == "Disable") {
        $('#Time_NTP').hide();
        $('#Time_Manual').show();
    }
    if (type == "Enable") {
        $('#Time_NTP').show();
        $('#Time_Manual').hide();
    }
};
var change_Ntpserver = function () {
    var serverlist = document.getElementById('NTPServer_list');
    document.getElementById('NTPServer_txt').value = serverlist.value;
    serverlist.selectedIndex = 0;
};
// function created by yogesh kumar (ccpl)
function selectNoOfVap() {
    $("input[name='HID_AP_MAX_VAP']").val($("#NoofVaps").val());
    manageVapDropDown($("#NoofVaps").val());
}
function aclVap() {
    $("table.acl-table").hide();
    $("#acl_vap" + $("#acl_vap").val() + "_table").show();
}
function vapVap() {
    currentVap = $("#vap_vap").val();
    $("table.vap-table").hide();
    $("#vap_vap" + $("#vap_vap").val() + "_table1").show();
    $("#vap_vap" + $("#vap_vap").val() + "_table2").show();

    var stmod = $("input[name='AP_STARTMODE']:checked").val();
    $("#vapMsg").html("Configuration/Settings for VAP " + $("#vap_vap").val());
    if (stmod == "standard") {
        $("#WEP_div_1").html(wep);
        $("#WEP_div_2").html("");
        $("#wepdiv_1").show();
    }
    else if (stmod == "rootap") {
        $("#WEP_div_1").html(wep);
        $("#WEP_div_2").html("");
        $("#wepdiv_1").show();
    }
    else if (stmod == "repeater") {
        $("#WEP_div_1").html("");
        $("#WEP_div_2").html(wep);

        if ($("#vap_vap").val() == "1") {
            // for vap 1
            $("#wepdiv_1").hide();
            $("#vapMsg").html($("#vapMsg").html() + " : Repeater AP");
        }
        else {
            //for vap 2
            $("#wepdiv_2").show();
            $("#vapMsg").html($("#vapMsg").html() + " : Repeater Client");
        }
    }
    else if (stmod == "client") {
        $("#WEP_div_1").html(wep);
        $("#WEP_div_2").html("");
        $("#wepdiv_1").show();
    }
    else if (stmod == "multi") {
        $("#WEP_div_1").html(wep);
        $("#WEP_div_2").html("");
        $("#wepdiv_1").show();
        $("#wepdiv_2").hide();
    }
    else if (stmod == "multivlan") {
        $("#WEP_div_1").html(wep);
        $("#WEP_div_2").html("");
        $("#wepdiv_1").show();
        $("#wepdiv_2").hide();
    }
}
function manageVapDropDown(num) {
    for (i = 1; i <= 8; i++) {
        if (i > num) {
            $("#acl_vap option[value='" + i + "']").hide();
            $("#vap_vap option[value='" + i + "']").hide();
        }
        else {
            $("#acl_vap option[value='" + i + "']").show();
            $("#vap_vap option[value='" + i + "']").show();
        }
    }
    $("#acl_vap option[value='1']").attr("selected", true);
    $("#vap_vap option[value='1']").attr("selected", true);
    aclVap();
    vapVap();
}
function callAfterCreateTemplateForm() {
//======================== Services Tab ===========================//
    // upnp
    if ($("input[name='upnpHidden']").val() == "Enable")
        $("input[id='upnp_enable']").attr("checked", true);
    else
        $("input[id='upnp_disable']").attr("checked", true);

    // syslog
    if ($("input[name='sysLogHidden']").val() == "Enable") {
        $("input[id='syslog_enable']").attr("checked", true);
        ServiceState('Syslog', true);
    }
    else {
        $("input[id='syslog_disable']").attr("checked", true);
        ServiceState('Syslog', false);
    }

    // snmp
    if ($("input[name='snmpHidden']").val() == "Enable") {
        $("input[id='snmp_enable']").attr("checked", true);
        ServiceState('Snmp', true);
    }
    else {
        $("input[id='snmp_disable']").attr("checked", true);
        ServiceState('Snmp', false);
    }

    // dhcp
    if ($("input[name='dhcpHidden']").val() == "Enable") {
        $("input[id='DHCP_SER_EN']").attr("checked", true);
        dhcpState(true);
    }
    else {
        $("input[id='DHCP_SER_DS']").attr("checked", true);
        dhcpState(false);
    }

    // timezone
    $("#DropDownTimezone option[value='" + $("input[name='timeZoneHidden']").val() + "']").attr('selected', 'selected');

    // ntp
    $("#NTP_Enable option[value='" + $("input[name='ntpHidden']").val() + "']").attr('selected', 'selected');
    AlterTimeSettings();
//======================== Services Tab End ===========================//
//========================== ACl Tab ==================================//
    for (i = 1; i <= 8; i++) {
        // vap i
        if ($("input[id='acl_vap" + i + "_hd']").val() == "1") {
            $("input[id='acl_vap" + i + "_enabled']").attr("checked", true);
            ToggleACL(true, i);
        }
        else {
            $("input[id='acl_vap" + i + "_disabled']").attr("checked", true);
            ToggleACL(false, i)
        }
        if ($("input[id='acltype_vap" + i + "_hd']").val() == "0")
            $("input[id='acltype_vap" + i + "_deny']").attr("checked", true);
        else
            $("input[id='acltype_vap" + i + "_allow']").attr("checked", true);
    }
//======================== ACl Tab End ================================//
//========================== Radio Tab ==================================//
    // startup mode
    if ($("input[id='startmode_hd']").val() == "standard") {
        $("input[id='startup_standard']").attr("checked", true);
        ToggleMVlan(false);
    }
    else if ($("input[id='startmode_hd']").val() == "rootap") {
        $("input[id='startup_rootap']").attr("checked", true);
        ToggleMVlan(false);
    }
    else if ($("input[id='startmode_hd']").val() == "repeater") {
        $("input[id='startup_repeater']").attr("checked", true);
        ToggleMVlan(false);
    }
    else if ($("input[id='startmode_hd']").val() == "client") {
        $("input[id='startup_client']").attr("checked", true);
        ToggleMVlan(false);
    }
    else if ($("input[id='startmode_hd']").val() == "multi") {
        $("input[id='startup_multi']").attr("checked", true);
        ToggleMVlan(false);
    }
    else if ($("input[id='startmode_hd']").val() == "multivlan") {
        $("input[id='startup_multivlan']").attr("checked", true);
        ToggleMVlan(true);
        if (!document.getElementById('Enbl_mngmtvlan').checked)
            document.getElementById('Dsbl_mngmtvlan').checked = true;
        document.getElementById('NoofVaps').disabled = true;
    }

    // MANAGEMENT VLAN
    if ($("input[id='mngmtvlan_hd']").val() == "1")
        $("input[id='Enbl_mngmtvlan']").attr("checked", true);
    else
        $("input[id='Dsbl_mngmtvlan']").attr("checked", true);

    // ATH_countrycode
    $("#ATH_countrycode option[value='" + $("input[id='countrycode_hd']").val() + "']").attr('selected', 'selected');

    //AP_MAX_VAP
    $("#NoofVaps option[value='" + $("input[id='HID_AP_MAX_VAP']").val() + "']").attr('selected', 'selected');
    manageVapDropDown($("input[id='HID_AP_MAX_VAP']").val());

    //AP_PRIMARY_CH
    $("#AP_Channel option[value='" + $("input[id='HID_AP_Channel']").val() + "']").attr('selected', 'selected');

    //AP_CHMODE
    $("#AP_CHMODE option[value='" + $("input[id='HID_AP_CHMODE']").val() + "']").attr('selected', 'selected');

    //AP_TXPOWER
    $("#AP_TXPOWER option[value='" + $("input[id='HID_AP_TXPOWER']").val() + "']").attr('selected', 'selected');

    // SHORTGI
    if ($("input[id='HID_SHORTGI']").val() == "1")
        $("input[id='SHORTGI_1']").attr("checked", true);
    else
        $("input[id='SHORTGI_0']").attr("checked", true);

    // AMPDUENABLE
    if ($("input[id='HID_AMPDUENABLE']").val() == "1") {
        $("input[id='chk_AMPDU_Enable']").attr("checked", true);
        SwapAggregation(true);
    }
    else {
        $("input[id='chk_AMPDU_Disable']").attr("checked", true);
        SwapAggregation(false);
    }

    // CWMMODE
    if ($("input[id='HID_CWMMODE']").val() == "1")
        $("input[id='CWMMODE_1']").attr("checked", true);
    else
        $("input[id='CWMMODE_0']").attr("checked", true);

    // TX_CHAINMASK
    if ($("input[id='HID_TX_CHAINMASK']").val() == "1")
        $("input[id='TX_CHAINMASK_1']").attr("checked", true);
    else if ($("input[id='HID_TX_CHAINMASK']").val() == "3")
        $("input[id='TX_CHAINMASK_3']").attr("checked", true);
    else
        $("input[id='TX_CHAINMASK_0']").attr("checked", true);

    // RX_CHAINMASK
    if ($("input[id='HID_RX_CHAINMASK']").val() == "1")
        $("input[id='RX_CHAINMASK_1']").attr("checked", true);
    else if ($("input[id='HID_RX_CHAINMASK']").val() == "3")
        $("input[id='RX_CHAINMASK_3']").attr("checked", true);
    else
        $("input[id='RX_CHAINMASK_0']").attr("checked", true);

    // code form config file
    SwapDistance(0);
//======================== Radio Tab End ================================//

//========================== VAP Tab ==================================//
    // AP_DYN_VLAN
    if ($("#dyn_vlan").val() == "1")
        $("#chk_dyn_vlan").attr("checked", true);
    else
        $("#chk_dyn_vlan").attr("checked", false);
    Toggle_Dynvlan();


    for (i = 1; i <= 8; i++) {
        // HIDE_SSID
        if ($("#hdn_ssid_" + i).val() == "1") {
            $("#HIDE_SSID_" + i).attr("checked", true);
        }
        else {
            $("#HIDE_SSID_" + i).attr("checked", false);
        }

        // HID_AP_MODE
        if ($("#HID_AP_MODE_" + i).val() == "ap") {
            $("#ap_mode_ap_" + i).attr("checked", true);
        }
        else {
            $("#ap_mode_wds_ap_" + i).attr("checked", true);
        }

        // AP_SECMODE
        if ($("#HID_AP_SECMODE_" + i).val() == "WEP") {
            $("#sec_wep_" + i).attr("checked", true);
            displayData(2, i);
        }
        else if ($("#HID_AP_SECMODE_" + i).val() == "WPA") {
            $("#sec_wpa_" + i).attr("checked", true);
            displayData(3, i);
        }
        else {
            $("#sec_open_" + i).attr("checked", true);
            displayData(1, i);
        }

        // AP_CYPHER
        if ($("#HID_AP_CYPHER_" + i).val() == "TKIP")
            $("#cypher_tkip_" + i).attr("checked", true);
        else if ($("#HID_AP_CYPHER_" + i).val() == "TKIP CCMP")
            $("#cypher_tkip_ccmp_" + i).attr("checked", true);
        else
            $("#cypher_CCMP_" + i).attr("checked", true);

        // AP_SECFILE
        if ($("#HID_AP_SECFILE_" + i).val() == "EAP") {
            $("#chk_EnterpriseKey_" + i).attr("checked", true);
            default_fillEnt(i);
        }
        else {
            $("#chk_PersonalKey_" + i).attr("checked", true);
            default_clearEnt(i);
        }

        // AP_RSN_ENA_PREAUTH
        if ($("#HID_AP_RSN_ENA_PREAUTH_" + i).val() == "1") {
            $("#interface_enb_" + i).attr("checked", true);
        }
        else if ($("#HID_AP_RSN_ENA_PREAUTH_" + i).val() == "0") {
            $("#interface_dis_" + i).attr("checked", true);
        }

        // AP_WPA
        if ($("#HID_AP_WPA_" + i).val() == "0") {
            $("#sec_802_" + i).attr("checked", true);
            EnableEnterprise(i);
        }
        else if ($("#HID_AP_WPA_" + i).val() == "1") {
            $("#secwpa_" + i).attr("checked", true);
            AlterEnterprise(i);
        }
        else if ($("#HID_AP_WPA_" + i).val() == "3") {
            $("#secauto_" + i).attr("checked", true);
            AlterEnterprise(i);
        }
        else {
            $("#secwpa2_" + i).attr("checked", true);
            AlterEnterprise(i);
        }
        // AP_RTS_THR
        if ($("input[id='hdn_rts_thr" + i + "']").val() == "off") {
            $("#rts_mode" + i + " option[value='0']").attr('selected', 'selected');
            $("#txt_rts_thr" + i).hide()
        }
        else {
            $("#rts_mode" + i + " option[value='2']").attr('selected', 'selected');
            $("#txt_rts_thr" + i).show().val($("input[id='hdn_rts_thr" + i + "']").val())
        }

        // AP_FRAG_THR
        if ($("input[id='hdn_frag_thr" + i + "']").val() == "off") {
            $("#frag_mode" + i + " option[value='0']").attr('selected', 'selected');
            $("#txt_rts_thr" + i).hide()
        }
        else {
            $("#frag_mode" + i + " option[value='2']").attr('selected', 'selected');
            $("#txt_frag_thr" + i).show().val($("input[id='hdn_frag_thr" + i + "']").val())
        }
    }
    vapLoad();
//======================== VAP Tab End ================================//
}
function vapLoad() {
    if ($("select[name='AP_CHMODE']").val() == '11G') {
        for (i = 1; i <= 8; i++)
            $('#span_cypher_' + i).show()
    }
    else {
        for (i = 1; i <= 8; i++) {
            $('#span_cypher_' + i).hide()
            $('#cypher_CCMP_' + i).attr("checked", true);
        }
    }


    var stmod = $("input[name='AP_STARTMODE']:checked").val();
    if (stmod == "standard") {
        $('#MultiVapmod_opt_1').hide();
        $('#MultiVlan_opt_1').hide();
        $('#Mac_opt').hide();
        $('#Mac_opt2').hide();
        $('#hidessid_div_1').show();
        $('#chk_dyn_vlan').attr("disabled", false);
        $("#beacon_row").show();
    }
    else if (stmod == "rootap") {
        $('#MultiVapmod_opt_1').hide();
        $('#MultiVlan_opt_1').hide();
        $('#Mac_opt').hide();
        $('#Mac_opt2').hide();
        $('#hidessid_div_1').show();
        $('#chk_dyn_vlan').attr("disabled", false);
        $("#beacon_row").show();
    }
    else if (stmod == "repeater") {
        // for vap 1
        $('#MultiVapmod_opt_1').hide();
        $('#MultiVlan_opt_1').hide();
        $('#Mac_opt').show();
        $('#MultiVapmod_opt_2').hide();
        $('#MultiVlan_opt_2').hide();
        $('#hidessid_div_2').hide();
        $('#hidessid_div_1').show();
        $('#chk_dyn_vlan').attr("disabled", true);
        if (repeaterToClient == 0) {
            repeaterToClient = 1;
            $("#Mac_opt2").html($("#Mac_opt").html()).show();
            $("#Mac_opt").html("").hide();
        }
        if ($("input[name='AP_SECMODE']:checked").val() == "WEP") {
            $("#sec_open_1").attr("checked", true);
            $("#sec_wep_1").attr("checked", false);
            displayData(1, '1');
        }
        $("#beacon_row").show();
    }
    else if (stmod == "client") {
        $('#MultiVapmod_opt_1').hide();
        $('#MultiVlan_opt_1').hide();
        $('#Mac_opt').show();
        $('#hidessid_div_1').hide();
        $('#chk_dyn_vlan').attr("disabled", true);
        if (repeaterToClient == 1) {
            repeaterToClient = 0;
            $("#Mac_opt").html($("#Mac_opt2").html()).show();
            $("#Mac_opt2").html("").hide();
        }
        $("#beacon_row").hide();
    }
    else if (stmod == "multi") {
        $('#MultiVapmod_opt_1').show();
        $('#MultiVapmod_opt_2').show();
        $('#MultiVlan_opt_1').hide();
        $('#MultiVlan_opt_2').hide();
        $('#MultiVlan_opt_3').hide();
        $('#MultiVlan_opt_4').hide();
        $('#MultiVlan_opt_5').hide();
        $('#MultiVlan_opt_6').hide();
        $('#MultiVlan_opt_7').hide();
        $('#MultiVlan_opt_8').hide();
        $('#Mac_opt').hide();
        $('#Mac_opt2').hide();
        $('#hidessid_div_1').show();
        $('#hidessid_div_2').show();
        $('#chk_dyn_vlan').attr("disabled", true);
        if ($("input[name='AP_SECMODE_2']:checked").val() == "WEP") {
            $("#sec_open_2").attr("checked", true);
            $("#sec_wep_2").attr("checked", false);
            displayData(1, '2');
        }
        $("#beacon_row").hide();
    }
    else if (stmod == "multivlan") {
        $('#MultiVapmod_opt_1').show();
        $('#MultiVapmod_opt_2').show();
        $('#MultiVlan_opt_1').show();
        $('#MultiVlan_opt_2').show();
        $('#MultiVlan_opt_3').show();
        $('#MultiVlan_opt_4').show();
        $('#MultiVlan_opt_5').show();
        $('#MultiVlan_opt_6').show();
        $('#MultiVlan_opt_7').show();
        $('#MultiVlan_opt_8').show();
        $('#Mac_opt').hide();
        $('#Mac_opt2').hide();
        $('#hidessid_div_1').show();
        $('#hidessid_div_2').show();
        $('#chk_dyn_vlan').attr("disabled", true);
        if ($("input[name='AP_SECMODE_2']:checked").val() == "WEP") {
            $("#sec_open_2").attr("checked", true);
            $("#sec_wep_2").attr("checked", false);
            displayData(1, '2');
        }
        $("#beacon_row").hide();
    }
}
var vapValidation = function () {
    var errorMsg = "";
    var tempMsg = "";
    for (i = 1; i <= parseInt($("#HID_AP_MAX_VAP").val()); i++) {
        tempMsg = "";

        // ESSID Validation
        if ($.trim($("#AP_SSID_" + i).val()) == "") {
            tempMsg += "\tESSID cannot be empty.\n";
        }

        // Vlan Id and Vlan Priority Validation
        if ($("input[name='AP_STARTMODE']:checked").val() == "multivlan") {
            if (!(parseInt($("#AP_VLAN_" + i).val()) > 0 && parseInt($("#AP_VLAN_" + i).val()) < 4096)) {
                tempMsg += "\tInvalid Vlan Id.\n";
            }
            if (!(parseInt($("#VLAN_PRI_" + i).val()) >= 0 && parseInt($("#VLAN_PRI_" + i).val()) < 8)) {
                tempMsg += "\tInvalid Vlan Priority.\n";
            }
        }

        // Checking the min-key length
        var secmode = "None";
        var secfile = "PSK";
        if (i == 1) {
            secmode = $("input[name='AP_SECMODE']:checked").val();
            secfile = $("input[name='AP_SECFILE']:checked").val();
        }
        else {
            secmode = $("input[name='AP_SECMODE_" + i + "']:checked").val();
            secfile = $("input[name='AP_SECFILE_" + i + "']:checked").val();
        }
        if (secmode == "WPA" && secfile == "PSK") {
            if ($("#PSK_KEY_" + i).val().length < 8) {
                tempMsg += "\tKey length should be greater than 8.\n";
            }
        }
        if (secmode == "WPA" && secfile == "EAP") {
            if ($.trim($("#AP_AUTH_SERVER_" + i).val()) == "") {
                tempMsg += "\tAuth Server IP cannot be empty.\n";
            }
            if ($.trim($("#AP_AUTH_SECRET_" + i).val()) == "") {
                tempMsg += "\tShared Secret cannot be null.\n";
            }
        }
        if (secmode == "WEP") {
            var flag = 0, prikey = 0;
            for (var j = 1; j < 5; j++) {
                if ($("#Wepkey" + i + "_chk").attr("checked")) {
                    prikey = j;
                }

            }
            if (prikey > 0) {
                if ($.trim($('#WEPKEY_' + prikey).val()) == '') {
                    for (var j = 1; j < 5; j++) {
                        if ($.trim($('#WEPKEY_' + j).val()) != '') {
                            flag = 1;
                            $('#Wepkey' + j + '_chk').attr("checked", true);
                        }
                    }
                    if (flag == 0) {
                        tempMsg += "\tWEP Primary key cannot be empty\n";
                    }

                }
            }
            else {
                tempMsg += "\tPrimary key not selected\n";
            }
        }
        if (tempMsg != "") {
            errorMsg += "VAP " + i + ":\n" + tempMsg + "\n";
        }
    }
    if (errorMsg != "") {
        alert(errorMsg);
        return false;
    }
    else {
        return true;
    }
}
function setValuesInWep() {
    // HID_AP_WEP_MODE_0
    if ($("#HID_AP_WEP_MODE_0").val() == "2")
        $("#wepmode2").attr("checked", true);
    else if ($("#HID_AP_WEP_MODE_0").val() == "4")
        $("#wepmode4").attr("checked", true);
    else
        $("#wepmode1").attr("checked", true);

    // HID_AP_PRIMARY_KEY_0
    if ($("#HID_AP_PRIMARY_KEY_0").val() == "2")
        $("#Wepkey2_chk").attr("checked", true);
    else if ($("#HID_AP_PRIMARY_KEY_0").val() == "3")
        $("#Wepkey3_chk").attr("checked", true);
    else if ($("#HID_AP_PRIMARY_KEY_0").val() == "4")
        $("#Wepkey4_chk").attr("checked", true);
    else
        $("#Wepkey1_chk").attr("checked", true);

    // WEPKEY_1
    $("#WEPKEY_1").val($("#HID_WEPKEY_1").val());

    // WEPKEY_2
    $("#WEPKEY_2").val($("#HID_WEPKEY_2").val());

    // WEPKEY_3
    $("#WEPKEY_3").val($("#HID_WEPKEY_3").val());

    // WEPKEY_4
    $("#WEPKEY_4").val($("#HID_WEPKEY_4").val());
}
// ========================== End AP Configuration Function ===============================
