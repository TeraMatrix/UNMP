$(function () {
    $.validator.addMethod('SubnetMask', function (value, element) {
        var ip = "^([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/(d|2[4-9]|30)$";
        return value.match(ip);
    }, ' Invalid Subnet Mask');

    $.validator.addMethod('IP4Checker', function (value, element) {
        var ip = "^([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])$";
        return value.match(ip);
    }, ' Invalid IP address');
    $.validator.addMethod('ClassCIPChecker', function (value, element) {
        //var ip = "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){2}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$";
        var ip = "^([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])$";
        return value.match(ip);
    }, ' Invalid Class C IP address');
    $.validator.addMethod('positiveNumber', function (value, element) {
        return Number(value) > 0;
    }, ' Enter a positive number');
    $.validator.addMethod('greaterThan', function (value, element, param) {
        return parseInt($(param).val()) <= parseInt(value);
    }, ' It Show be greater than the value');
    $.validator.addMethod('lessThan', function (value, element, param) {
        return parseInt($(param).val()) >= parseInt(value);
    }, ' It Show be less than the value');
    validateAutoDiscoveryForm();
    multiSelectHostGroups("HostGroup1");
    multiSelectHostGroups("HostGroup2");
    multiSelectHostGroups("HostGroup3");
    multiSelectHostGroups("HostGroup4");
    discovery1();
    discovery2();
    discovery3();
    discovery4();
    $("#version2").change(function () {
        if ($(this).val() == "3") {
            $(".snmpv3Tr").show(100);
        }
        else {
            $(".snmpv3Tr").hide(100);
        }
    });
    $("div.tab-head").find("a").click(function (e) {
        e.preventDefault();
        $(this).parent().find("a.tab-active").removeClass("tab-active").addClass("tab-button");
        $(this).removeClass("tab-button").addClass("tab-active");
        $("div.discoveryDetailsBody").hide();
        $($(this).attr("href")).show();
    });
    var deviceList = $("input[name='deviceList']");
    var allDevices = $("input[name='allDevices']");
    allDevices.click(function () {
        if (this.checked) {
            deviceList.attr("checked", true);
        }
        else {
            deviceList.attr("checked", false);
        }
    });
    deviceList.click(function () {
        if (this.checked) {
            if ($("input[name='deviceList']:checked").size() == parseInt($("input[name='totalShyamDevice']").val())) {
                allDevices.attr("checked", true);
            }
        }
        else {
            allDevices.attr("checked", false);
        }
    });
});

function discovery1() {
    $("#autoDiscovery1").submit(function () {
        formAction = $("#autoDiscovery1").attr("action") + "?" + $("#autoDiscovery1").serialize();
        if ($("#autoDiscovery1").valid()) {
            $.ajax({
                type: "get",
                url: formAction,
                success: function (result) {
                    if ($.trim(result) == "1")	// scheduling deatils does not save
                    {
                        //alert(result);
                        $.ajax({
                            type: "get",
                            url: "start_" + formAction,
                            success: function (result) {
                            }
                        });
                        setTimeout(function () {
                            window.location = "network_overview.py";
                        }, 1000);
                    }
                    else if ($.trim(result) == "2")	// scheduling deatils replace by older
                    {
                        //alert(result)
                        $.ajax({
                            type: "get",
                            url: "start_" + formAction,
                            success: function (result) {
                            }
                        });
                        setTimeout(function () {
                            window.location = "network_overview.py";
                        }, 1000);
                    }
                    else if ($.trim(result) == "3")	// add new scheduling deatils
                    {
                        //alert(result)
                        $.ajax({
                            type: "get",
                            url: "start_" + formAction,
                            success: function (result) {
                            }
                        });
                        setTimeout(function () {
                            window.location = "network_overview.py";
                        }, 1000);
                    }
                    else {
                        alert("Ping discovery already running by " + result + " user");
                    }
                }
            });
        }
        return false;
    });
}
function discovery2() {
    $("#autoDiscovery2").submit(function () {
        formAction = $("#autoDiscovery2").attr("action") + "?" + $("#autoDiscovery2").serialize();
        if ($("#autoDiscovery2").valid()) {
            $.ajax({
                type: "get",
                url: formAction,
                success: function (result) {
                    if ($.trim(result) == "1")	// scheduling deatils does not save
                    {
                        //alert(result);
                        $.ajax({
                            type: "get",
                            url: "start_" + formAction,
                            success: function (result) {
                            }
                        });
                        setTimeout(function () {
                            window.location = "network_overview.py";
                        }, 1000);
                    }
                    else if ($.trim(result) == "2")	// scheduling deatils replace by older
                    {
                        //alert(result)
                        $.ajax({
                            type: "get",
                            url: "start_" + formAction,
                            success: function (result) {
                            }
                        });
                        setTimeout(function () {
                            window.location = "network_overview.py";
                        }, 1000);
                    }
                    else if ($.trim(result) == "3")	// add new scheduling deatils
                    {
                        //alert(result)
                        $.ajax({
                            type: "get",
                            url: "start_" + formAction,
                            success: function (result) {
                            }
                        });
                        setTimeout(function () {
                            window.location = "network_overview.py";
                        }, 1000);
                    }
                    else {
                        alert("SNMP discovery already running by " + result + " user");
                    }
                }
            });
        }
        return false;
    });
}
function discovery3() {
    $("#autoDiscovery3").submit(function () {
        formAction = $("#autoDiscovery3").attr("action") + "?" + $("#autoDiscovery3").serialize();
        if ($("#autoDiscovery3").valid()) {
            $.ajax({
                type: "get",
                url: formAction,
                success: function (result) {
                    if ($.trim(result) == "1")	// scheduling deatils does not save
                    {
                        //alert(result);
                        $.ajax({
                            type: "get",
                            url: "start_" + formAction,
                            success: function (result) {
                            }
                        });
                        setTimeout(function () {
                            window.location = "network_overview.py";
                        }, 1000);
                    }
                    else if ($.trim(result) == "2")	// scheduling deatils replace by older
                    {
                        //alert(result)
                        $.ajax({
                            type: "get",
                            url: "start_" + formAction,
                            success: function (result) {
                            }
                        });
                        setTimeout(function () {
                            window.location = "network_overview.py";
                        }, 1000);
                    }
                    else if ($.trim(result) == "3")	// add new scheduling deatils
                    {
                        //alert(result)
                        $.ajax({
                            type: "get",
                            url: "start_" + formAction,
                            success: function (result) {
                            }
                        });
                        setTimeout(function () {
                            window.location = "network_overview.py";
                        }, 1000);
                    }
                    else {
                        alert("UPnP discovery already running by " + result + " user");
                    }
                }
            });
        }
        return false;
    });
}
function discovery4() {
    $("#autoDiscovery4").submit(function () {
        formAction = $("#autoDiscovery4").attr("action") + "?" + $("#autoDiscovery4").serialize();
        var allDeviceList = [];
        $("input[name='deviceList']:checked").each(function () {
            allDeviceList.push($(this).val());
        });
        if ($("#autoDiscovery4").valid()) {
            $.ajax({
                type: "post",
                url: formAction + "&allDeviceList=" + String(allDeviceList),
                success: function (result) {
                    if ($.trim(result) == "1")	// scheduling deatils does not save
                    {
                        //alert(result);
                        $.ajax({
                            type: "post",
                            url: "start_" + formAction + "&allDeviceList=" + String(allDeviceList),
                            success: function (result) {
                            }
                        });
                        setTimeout(function () {
                            window.location = "network_overview.py";
                        }, 1000);
                    }
                    else if ($.trim(result) == "2")	// scheduling deatils replace by older
                    {
                        //alert(result)
                        $.ajax({
                            type: "post",
                            url: "start_" + formAction + "&allDeviceList=" + String(allDeviceList),
                            success: function (result) {
                            }
                        });
                        setTimeout(function () {
                            window.location = "network_overview.py";
                        }, 1000);
                    }
                    else if ($.trim(result) == "3")	// add new scheduling deatils
                    {
                        //alert(result)
                        $.ajax({
                            type: "post",
                            url: "start_" + formAction + "&allDeviceList=" + String(allDeviceList),
                            success: function (result) {
                            }
                        });
                        setTimeout(function () {
                            window.location = "network_overview.py";
                        }, 1000);
                    }
                    else {
                        alert("SDMC discovery already running by " + result + " user");
                    }
                }
            });
        }
        return false;
    });
}
function validateAutoDiscoveryForm() {
    $("#autoDiscovery").validate({
        rules: {
            range: {
                required: true,
                SubnetMask: true
            },
            timeout: {
                required: true,
                number: true,
                positiveNumber: true
            }
        },
        messages: {
            range: {
                required: " *",
                SubnetMask: " Please enter correct subnet mask"
            },
            timeout: {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater than zero"
            }
        }
    });

    $("#autoDiscovery1").validate({
        rules: {
            ipBase1: {
                required: true,
                ClassCIPChecker: true
            },
            ipRangeStart1: {
                required: true,
                number: true,
                min: 0,
                max: 255
                //lessThan: "#ipRangeEnd1"
            },
            ipRangeEnd1: {
                required: true,
                number: true,
                min: 0,
                max: 255,
                greaterThan: "#ipRangeStart1"
            },
            timeOut1: {
                required: true,
                number: true,
                positiveNumber: true
            }

        },
        messages: {
            ipBase1: {
                required: " *",
                IP4Checker: " Please enter valid class C ip"
            },
            ipRangeStart1: {
                required: " *",
                number: " It must be a number",
                min: " It must be >= 0 and <= 255",
                max: " It must be >= 0 and <= 255"
                //lessThan: " It should be less than IP Range End Value"
            },
            ipRangeEnd1: {
                required: " *",
                number: " It must be a number",
                min: " It must be >= 0 and <= 255",
                max: " It must be >= 0 and <= 255",
                greaterThan: " It should be greater than IP Range Start value"
            },
            timeOut1: {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero"
            }
        }
    });

    $("#autoDiscovery2").validate({
        rules: {
            ipBase2: {
                required: true,
                ClassCIPChecker: true
            },
            ipRangeStart2: {
                required: true,
                number: true,
                min: 0,
                max: 255
                //lessThan: "#ipRangeEnd1"
            },
            ipRangeEnd2: {
                required: true,
                number: true,
                min: 0,
                max: 255,
                greaterThan: "#ipRangeStart2"
            },
            timeOut2: {
                required: true,
                number: true,
                positiveNumber: true
            },
            community2: "required",
            port2: "required",
            userName2: {
                required: '#version2 option:eq(2):selected'
            },
            password2: {
                required: '#version2 option:eq(2):selected'
            },
            authKey2: {
                required: '#version2 option:eq(2):selected'
            },
            authProtocol2: {
                required: '#version2 option:eq(2):selected'
            },
            privPassword2: {
                required: '#version2 option:eq(2):selected'
            },
            privKey2: {
                required: '#version2 option:eq(2):selected'
            },
            privProtocol2: {
                required: '#version2 option:eq(2):selected'
            }
        },
        messages: {
            ipBase2: {
                required: " *",
                IP4Checker: " Please enter valid class C ip"
            },
            ipRangeStart2: {
                required: " *",
                number: " It must be a number",
                min: " It must be >= 0 and <= 255",
                max: " It must be >= 0 and <= 255"
                //lessThan: " It should be less than IP Range End Value"
            },
            ipRangeEnd2: {
                required: " *",
                number: " It must be a number",
                min: " It must be >= 0 and <= 255",
                max: " It must be >= 0 and <= 255",
                greaterThan: " It should be greater than IP Range Start value"
            },
            timeOut2: {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero"
            },
            community2: " *",
            port2: " *",
            userName2: {
                required: " *"
            },
            password2: {
                required: " *"
            },
            authKey2: {
                required: " *"
            },
            authProtocol2: {
                required: " *"
            },
            privPassword2: {
                required: " *"
            },
            privKey2: {
                required: " *"
            },
            privProtocol2: {
                required: " *"
            }
        }
    });
    $("#autoDiscovery3").validate({
        rules: {
            timeOut3: {
                required: true,
                number: true,
                positiveNumber: true
            }

        },
        messages: {
            timeOut3: {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero"
            }
        }
    });
    $("#autoDiscovery4").validate({
        rules: {
            timeOut4: {
                required: true,
                number: true,
                positiveNumber: true
            },
            deviceList: {
                required: true,
                minlength: 1
            }
        },
        messages: {
            timeOut4: {
                required: " *",
                number: " It must be a number",
                positiveNumber: " It must be greater then zero"
            },
            deviceList: {
                required: "Select atleast one device",
                minlength: "Select atleast one device"
            }
        }
    });
}
/*============================= Multiple Selecter For Host Group =========================*/
function multiSelectHostGroups(hostgroup) {
    $(".plus" + hostgroup).click(function () {
        plusHostGroupOption(hostgroup, this);
    })
    $(".minus" + hostgroup).click(function () {
        minusHostGroupOption(hostgroup, this);
    })
    $("#rm" + hostgroup).click(function (e) {
        e.preventDefault();
        $("div[id='multiSelectList" + hostgroup + "']").find("div.selected").find("img").click();
    })
    $("#add" + hostgroup).click(function (e) {
        e.preventDefault();
        $("div[id='multiSelectList" + hostgroup + "']").find("div.nonSelected").find("img").click();
    })
}
function minusHostGroupOption(hostgroup, Obj) {
    liObj = $("<li/>");
    imgObj = $("<img/>");
    liObj.append($(Obj).attr("id"));
    imgObj.attr("src", "images/add16.png").attr("class", "plus plus" + hostgroup + "").attr("alt", "+").attr("id", $(Obj).attr("id")).click(function () {
        plusHostGroupOption(hostgroup, this)
    })
    liObj.append(imgObj);
    $(Obj).parent().parent().parent().parent().find("div.nonSelected").find("ul").append(liObj);
    $(Obj).parent().parent().parent().parent().find("input[name='hd" + hostgroup + "']").val("");
    j = 0
    for (i = 0; i < $(Obj).parent().parent().find("li").size(); i++) {
        var addedHostGroup = $(Obj).parent().parent().find("li").eq(i).find("img").attr("id");
        if (addedHostGroup != $(Obj).attr("id")) {
            if (j == 0) {
                $(Obj).parent().parent().parent().parent().find("input[name='hd" + hostgroup + "']").val($.trim(addedHostGroup));
            }
            else {
                $(Obj).parent().parent().parent().parent().find("input[name='hd" + hostgroup + "']").val($(Obj).parent().parent().parent().parent().find("input[name='hd" + hostgroup + "']").val() + "," + $.trim(addedHostGroup));
            }
            j++;
        }
    }
    $(Obj).parent().parent().parent().parent().find("span#count").html(j)
    $(Obj).parent().remove();
}
function plusHostGroupOption(hostgroup, Obj) {
    var countHost = 0;
    liObj = $("<li/>");
    imgObj = $("<img/>");
    liObj.append($(Obj).attr("id"));
    imgObj.attr("src", "images/minus16.png").attr("class", "minus minus" + hostgroup).attr("alt", "-").attr("id", $(Obj).attr("id")).click(function () {
        minusHostGroupOption(hostgroup, this)
    })
    liObj.append(imgObj);
    $(Obj).parent().parent().parent().parent().find("div.selected").find("ul").append(liObj);
    hdval = $(Obj).parent().parent().parent().parent().find("input[name='hd" + hostgroup + "']").val()
    if ($.trim(hdval) == "") {
        $(Obj).parent().parent().parent().parent().find("input[name='hd" + hostgroup + "']").val($(Obj).attr("id"))
    }
    else {
        $(Obj).parent().parent().parent().parent().find("input[name='hd" + hostgroup + "']").val(hdval + "," + $(Obj).attr("id"))
    }
    countHost = $(Obj).parent().parent().parent().parent().find("span#count").html();
    $(Obj).parent().parent().parent().parent().find("span#count").html(parseInt(countHost) + 1);
    $(Obj).parent().remove();
}
/*============================= End Multiple Selecter For Host Group =========================*/
