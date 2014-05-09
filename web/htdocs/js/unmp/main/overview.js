/* ================================================= global variable ================================================ */
var minRefreshTime = 10000;	// refresh time in ms for refresh the discovery details.
var maxRefreshTime = 15000;	// refresh time in ms for refresh the discovery details.
var defaultOpenTab = "";
var pingView = 0;		// 0 for displaying discovered host details and 1 for displaying discovery details.
var snmpView = 0;		// 0 for displaying discovered host details and 1 for displaying discovery details.
var upnpView = 0;		// 0 for displaying discovered host details and 1 for displaying discovery details.
var sdmcView = 0;		// 0 for displaying discovered host details and 1 for displaying discovery details.
/* ================================================= global variable ================================================ */

/*================================================= Right Click Menu ==================================================*/
/*
 1 = Left   Mousebutton
 2 = Centre Mousebutton
 3 = Right  Mousebutton
 */

$(function () {
    //document.oncontextmenu = function() {return false;};
    $(document).mousedown(function (e) {
        if (e.which === 1) {
            resetMenu();
        }
        if (e.which === 3) {
            e.preventDefault();
            $("#vakata-contextmenu").show().css("left", e.pageX).css("top", e.pageY);
        }
        return true;
    });

    $("div#vakata-contextmenu").find("a").hover(function (event) {
        $(this).parent().parent().find("ul").hide();
        $(this).next().show();
    }, function (event) {
        //$(this).next().hide();
    });
    $("div#vakata-contextmenu").find("a").mousedown(function (e) {
        e.stopPropagation();
        alert($(this).html());
        resetMenu();
    });
});
function resetMenu() {
    $("#vakata-contextmenu").hide();
    $("#vakata-contextmenu").find("ul").find("li").find("ul").hide();
}
/*================================================= Right Click Menu ==================================================*/

/*================================================= Tree ==================================================*/
$(function () {
    $("ins").toggle(function () {
        if ($(this).parent().hasClass("jstree-open")) {
            $(this).parent().removeClass("jstree-open").addClass("jstree-closed")
            $(this).next().next().slideUp();
            if ($(this).next().next().find("a").hasClass("jstree-clicked"))
                $(this).next().click();
        }
    }, function () {
        if ($(this).parent().hasClass("jstree-closed")) {
            $(this).parent().removeClass("jstree-closed").addClass("jstree-open")
            $(this).next().next().slideDown();
            if ($(this).next().next().find("a").hasClass("jstree-clicked"))
                $(this).next().click();
        }
    });
    $("div.jstree").find("a").click(function () {
        $("div.jstree").find("a").removeClass("jstree-clicked");
        $(this).addClass("jstree-clicked").removeClass("jstree-hovered");
    });
    $("div.jstree").find("a").find("ins").click(function () {
        $(this).parent().click();
    })
    $("div.jstree").find("a").hover(function () {
        $("div.jstree").find("a").removeClass("jstree-hovered");
        if ($(this).hasClass("jstree-clicked")) {
        }
        else
            $(this).addClass("jstree-hovered");
    }, function () {
        $(this).removeClass("jstree-hovered");
    });
});
/*================================================= Tree ==================================================*/
$(function () {
    $("a#optionMenuButton").click(function (e) {
        e.preventDefault();
        e.stopPropagation();
        if (defaultOpenTab != "") {
            var pos = $(this).offset();
            var objWidth = $(this).width();
            var objHeight = $(this).height();
            $(this).removeClass("tab-button").addClass("tab-active");
            $("#optionMenu").css({"left": (pos.left - $("#optionMenu").width() + objWidth), "top": (pos.top + objHeight)}).slideDown();
        }
    });
    $(document).click(function () {
        $("#optionMenu").slideUp();
        $("a#optionMenuButton").removeClass("tab-active").addClass("tab-button");
    });
    $("#optionMenu").find("a").click(function (e) {
        e.preventDefault();
        e.stopPropagation();
        if ($(this).hasClass("disable")) {
            //do nothing...
        }
        else {
            if ($(this).attr("rel") == "start") {
                startStopDiscovery("start", defaultOpenTab);
                $(document).click();
            }
            else if ($(this).attr("rel") == "stop") {
                startStopDiscovery("stop", defaultOpenTab);
                $(document).click();
            }
            else if ($(this).attr("rel") == "viewDetails") {
                if (defaultOpenTab == "ping") {
                    pingView = 1;
                    viewDiscoveryDetails(defaultOpenTab);
                }
                else if (defaultOpenTab == "snmp") {
                    snmpView = 1;
                    viewDiscoveryDetails(defaultOpenTab);
                }
                else if (defaultOpenTab == "upnp") {
                    upnpView = 1;
                    viewDiscoveryDetails(defaultOpenTab);
                }
                else if (defaultOpenTab == "sdmc") {
                    sdmcView = 1;
                    viewDiscoveryDetails(defaultOpenTab);
                }
                $(document).click();
            }
            else if ($(this).attr("rel") == "hideDetails") {
                $("div.tab-head").find("a.tab-active").removeClass("tab-active").addClass("tab-button");
                $("div#pingDiv, div#snmpDiv, div#upnpDiv, div#sdmcDiv").hide();
                defaultOpenTab = "";
                $(document).click();
            }
            else if ($(this).attr("rel") == "discoveredHostDetails") {
                if (defaultOpenTab == "ping") {
                    pingView = 0;
                    viewDiscoveredHostDetails(defaultOpenTab);
                }
                else if (defaultOpenTab == "snmp") {
                    snmpView = 0;
                    viewDiscoveredHostDetails(defaultOpenTab);
                }
                else if (defaultOpenTab == "upnp") {
                    upnpView = 0;
                    viewDiscoveredHostDetails(defaultOpenTab);
                }
                else if (defaultOpenTab == "sdmc") {
                    sdmcView = 0;
                    viewDiscoveredHostDetails(defaultOpenTab);
                }
                $(document).click();
            }
        }
    })
    $("a#pingButton").click(function (e) {
        e.preventDefault();
        defaultOpenTab = "ping";
        pingButtonClick();
    });
    $("a#snmpButton").click(function (e) {
        e.preventDefault();
        defaultOpenTab = "snmp";
        snmpButtonClick();
    });
    $("a#upnpButton").click(function (e) {
        e.preventDefault();
        defaultOpenTab = "upnp";
        upnpButtonClick();
    });
    $("a#sdmcButton").click(function (e) {
        e.preventDefault();
        defaultOpenTab = "sdmc";
        sdmcButtonClick();
    });
    checkStatusAndSetImages("all");
    $("input[name='allChecked']").click(function () {
        if (this.checked) {
            $(this).parent().parent().parent().find("input[name='host']").attr("checked", true);
        }
        else {
            $(this).parent().parent().parent().find("input[name='host']").attr("checked", false);
        }
    });
    $("table.host-table").find("input[name='host']").click(function () {
        if (this.checked) {
            if ($(this).parent().parent().parent().find("input[name='host']:checked").size() == parseInt($(this).parent().parent().parent().find("input[name='totalHost']").val())) {
                $(this).parent().parent().parent().find("input[name='allChecked']").attr("checked", true);
            }
        }
        else {
            $(this).parent().parent().parent().find("input[name='allChecked']").attr("checked", false);
        }
    });
    setTimeout("reloadPingDiv();", 500);
    setTimeout("reloadSnmpDiv();", 1500);
    setTimeout("reloadUpnpDiv();", 2200);
    setTimeout("reloadSdmcDiv();", 3000);
    setTimeout("reloadAllDiv();", 3500);
    if (defaultOpenTab == "")
        $("a#pingButton").click();
})
function pingButtonClick() {
    $("a#pingButton").parent().find("a.tab-active").removeClass("tab-active").addClass("tab-button");
    $("a#pingButton").removeClass("tab-button").addClass("tab-active");
    $("div.discoveryDetailsBody").hide();
    $($("a#pingButton").attr("href")).show();
    if ($("input[id='pingStatus']").val() == "1") {
        $("a[rel='start']").addClass("disable");
        $("a[rel='stop']").removeClass("disable");
    }
    else if ($("input[id='pingStatus']").val() == "0") {
        $("a[rel='start']").removeClass("disable");
        $("a[rel='stop']").addClass("disable");
    }
    else {
        $("a[rel='start']").addClass("disable");
        $("a[rel='stop']").addClass("disable");
    }
}
function snmpButtonClick() {
    $("a#snmpButton").parent().find("a.tab-active").removeClass("tab-active").addClass("tab-button");
    $("a#snmpButton").removeClass("tab-button").addClass("tab-active");
    $("div.discoveryDetailsBody").hide();
    $($("a#snmpButton").attr("href")).show();
    if ($("input[id='snmpStatus']").val() == "1") {
        $("a[rel='start']").addClass("disable");
        $("a[rel='stop']").removeClass("disable");
    }
    else if ($("input[id='snmpStatus']").val() == "0") {
        $("a[rel='start']").removeClass("disable");
        $("a[rel='stop']").addClass("disable");
    }
    else {
        $("a[rel='start']").addClass("disable");
        $("a[rel='stop']").addClass("disable");
    }
}
function upnpButtonClick() {
    $("a#upnpButton").parent().find("a.tab-active").removeClass("tab-active").addClass("tab-button");
    $("a#upnpButton").removeClass("tab-button").addClass("tab-active");
    $("div.discoveryDetailsBody").hide();
    $($("a#upnpButton").attr("href")).show();
    if ($("input[id='upnpStatus']").val() == "1") {
        $("a[rel='start']").addClass("disable");
        $("a[rel='stop']").removeClass("disable");
    }
    else if ($("input[id='upnpStatus']").val() == "0") {
        $("a[rel='start']").removeClass("disable");
        $("a[rel='stop']").addClass("disable");
    }
    else {
        $("a[rel='start']").addClass("disable");
        $("a[rel='stop']").addClass("disable");
    }
}
function sdmcButtonClick() {
    $("a#sdmcButton").parent().find("a.tab-active").removeClass("tab-active").addClass("tab-button");
    $("a#sdmcButton").removeClass("tab-button").addClass("tab-active");
    $("div.discoveryDetailsBody").hide();
    $($("a#sdmcButton").attr("href")).show();
    if ($("input[id='sdmcStatus']").val() == "1") {
        $("a[rel='start']").addClass("disable");
        $("a[rel='stop']").addClass("disable");
    }
    else if ($("input[id='upnpStatus']").val() == "0") {
        $("a[rel='start']").addClass("disable");
        $("a[rel='stop']").addClass("disable");
    }
    else {
        $("a[rel='start']").addClass("disable");
        $("a[rel='stop']").addClass("disable");
    }
}
function checkStatusAndSetImages(isClicked) {
    if ($("input[id='sdmcStatus']").val() == "1") {
        $("a#sdmcButton").find("span").removeClass("tab-img-stopped").removeClass("tab-img-done").addClass("tab-img-started");
        if (isClicked == "all")
            $("a#sdmcButton").click();
    }
    else if ($("input[id='sdmcStatus']").val() == "0") {
        $("a#sdmcButton").find("span").removeClass("tab-img-done").removeClass("tab-img-started").addClass("tab-img-stopped");
    }
    else if ($("input[id='sdmcStatus']").val() == "100") {
        $("a#sdmcButton").find("span").removeClass("tab-img-started").removeClass("tab-img-stopped").addClass("tab-img-done");
    }
    if ($("input[id='upnpStatus']").val() == "1") {
        $("a#upnpButton").find("span").removeClass("tab-img-stopped").removeClass("tab-img-done").addClass("tab-img-started");
        if (isClicked == "all")
            $("a#upnpButton").click();
    }
    else if ($("input[id='upnpStatus']").val() == "0") {
        $("a#upnpButton").find("span").removeClass("tab-img-done").removeClass("tab-img-started").addClass("tab-img-stopped");
    }
    else if ($("input[id='upnpStatus']").val() == "100") {
        $("a#upnpButton").find("span").removeClass("tab-img-started").removeClass("tab-img-stopped").addClass("tab-img-done");
    }
    if ($("input[id='snmpStatus']").val() == "1") {
        $("a#snmpButton").find("span").removeClass("tab-img-stopped").removeClass("tab-img-done").addClass("tab-img-started");
        if (isClicked == "all")
            $("a#snmpButton").click();
    }
    else if ($("input[id='snmpStatus']").val() == "0") {
        $("a#snmpButton").find("span").removeClass("tab-img-done").removeClass("tab-img-started").addClass("tab-img-stopped");
    }
    else if ($("input[id='snmpStatus']").val() == "100") {
        $("a#snmpButton").find("span").removeClass("tab-img-started").removeClass("tab-img-stopped").addClass("tab-img-done");
    }
    if ($("input[id='pingStatus']").val() == "1") {
        $("a#pingButton").find("span").removeClass("tab-img-stopped").removeClass("tab-img-done").addClass("tab-img-started");
        if (isClicked == "all")
            $("a#pingButton").click();
    }
    else if ($("input[id='pingStatus']").val() == "0") {
        $("a#pingButton").find("span").removeClass("tab-img-done").removeClass("tab-img-started").addClass("tab-img-stopped");
    }
    else if ($("input[id='pingStatus']").val() == "100") {
        $("a#pingButton").find("span").removeClass("tab-img-stopped").removeClass("tab-img-done").addClass("tab-img-done");
    }
    if (isClicked == "sdmc") {
        sdmcButtonClick();
    }
    else if (isClicked == "upnp") {
        upnpButtonClick();
    }
    else if (isClicked == "snmp") {
        snmpButtonClick();
    }
    else if (isClicked == "ping") {
        pingButtonClick();
    }
}
function startStopDiscovery(action, type) {
    $.ajax({
        type: "post",
        url: "stopStartDiscovery.py?action=" + action + "&type=" + type,
        success: function (result) {
            if (type == "ping") {
                if (pingView == 0)
                    viewDiscoveredHostDetails(type)
                else
                    viewDiscoveryDetails(type);
            }
            else if (type == "snmp") {
                if (snmpView == 0)
                    viewDiscoveredHostDetails(type)
                else
                    viewDiscoveryDetails(type);

            }
            else if (type == "upnp") {
                if (snmpView == 0)
                    viewDiscoveredHostDetails(type)
                else
                    viewDiscoveryDetails(type);

            }
            if (action == "start") {
                $.ajax({
                    type: "post",
                    url: "startDiscovery.py?type=" + type,
                    success: function (result) {
                    }
                })
            }
            discoveredHostDetailsForAll();
        }
    });
}
function discoveredHostDetailsForAll() {
    $.ajax({
        type: "get",
        url: "discoveredHostDetailsForAll.py",
        success: function (result) {
            result = $(result);
//================ Add Jquery events Again ===========================
            $(result).find("table").find("input[name='allChecked']").click(function () {
                if (this.checked) {
                    $(this).parent().parent().parent().find("input[name='host']").attr("checked", true);
                }
                else {
                    $(this).parent().parent().parent().find("input[name='host']").attr("checked", false);
                }
            });
            $(result).find("table").find("input[name='host']").click(function () {
                if (this.checked) {
                    if ($(this).parent().parent().parent().find("input[name='host']:checked").size() == parseInt($(this).parent().parent().parent().find("input[name='totalHost']").val())) {
                        $(this).parent().parent().parent().find("input[name='allChecked']").attr("checked", true);
                    }
                }
                else {
                    $(this).parent().parent().parent().find("input[name='allChecked']").attr("checked", false);
                }
            });
//================ End Add Jquery events Again ===========================

            $("#allDiv").html(result);
        }
    });
}
function viewDiscoveredHostDetails(type) {
    url = "";
    resultDiv = "";
    if (type == "ping") {
        url = "dicoveredHostDetailsForPing.py";
        resultDiv = "#pingDiv";
    }
    else if (type == "snmp") {
        url = "dicoveredHostDetailsForSnmp.py";
        resultDiv = "#snmpDiv";
    }
    else if (type == "upnp") {
        url = "dicoveredHostDetailsForUpnp.py";
        resultDiv = "#upnpDiv";
    }
    else if (type == "sdmc") {
        url = "dicoveredHostDetailsForSdmc.py";
        resultDiv = "#sdmcDiv";
    }
    $.ajax({
        type: "post",
        url: url,
        success: function (result) {
            result = $(result);
//================ Add Jquery events Again ===========================
            $(result).find("table").find("input[name='allChecked']").click(function () {
                if (this.checked) {
                    $(this).parent().parent().parent().find("input[name='host']").attr("checked", true);
                }
                else {
                    $(this).parent().parent().parent().find("input[name='host']").attr("checked", false);
                }
            });
            $(result).find("table").find("input[name='host']").click(function () {
                if (this.checked) {
                    if ($(this).parent().parent().parent().find("input[name='host']:checked").size() == parseInt($(this).parent().parent().parent().find("input[name='totalHost']").val())) {
                        $(this).parent().parent().parent().find("input[name='allChecked']").attr("checked", true);
                    }
                }
                else {
                    $(this).parent().parent().parent().find("input[name='allChecked']").attr("checked", false);
                }
            });
//================ End Add Jquery events Again ===========================
            $(resultDiv).html(result);
            if (defaultOpenTab == type)
                checkStatusAndSetImages(type);
        }
    });
}
function viewDiscoveryDetails(type) {
    url = "";
    resultDiv = "";
    if (type == "ping") {
        url = "discoveryDetailsForPing.py";
        resultDiv = "#pingDiv";
    }
    else if (type == "snmp") {
        url = "discoveryDetailsForSnmp.py";
        resultDiv = "#snmpDiv";
    }
    else if (type == "upnp") {
        url = "discoveryDetailsForUpnp.py";
        resultDiv = "#upnpDiv";
    }
    else if (type == "sdmc") {
        url = "discoveryDetailsForSdmc.py";
        resultDiv = "#sdmcDiv";
    }
    $.ajax({
        type: "post",
        url: url,
        success: function (result) {
            $(resultDiv).html(result);
            if (defaultOpenTab == type)
                checkStatusAndSetImages(type);
        }
    });
}
function reloadPingDiv() {
    if ($("input[id='pingStatus']").val() == "1") {
        if (pingView == 0)
            viewDiscoveredHostDetails("ping")
        else
            viewDiscoveryDetails("ping");
        setTimeout("reloadPingDiv();", minRefreshTime);
    }
    else {
        getStatusOfDiscovery("ping");
        setTimeout("reloadPingDiv();", maxRefreshTime);
    }
}
function reloadSnmpDiv() {
    if ($("input[id='snmpStatus']").val() == "1") {
        if (snmpView == 0)
            viewDiscoveredHostDetails("snmp")
        else
            viewDiscoveryDetails("snmp");
        setTimeout("reloadSnmpDiv();", (minRefreshTime + 1000));
    }
    else {
        getStatusOfDiscovery("snmp");
        setTimeout("reloadSnmpDiv();", (maxRefreshTime + 1000));
    }
}
function reloadUpnpDiv() {
    if ($("input[id='upnpStatus']").val() == "1") {
        if (upnpView == 0)
            viewDiscoveredHostDetails("upnp")
        else
            viewDiscoveryDetails("upnp");
        setTimeout("reloadUpnpDiv();", (minRefreshTime + 1500));
    }
    else {
        getStatusOfDiscovery("upnp");
        setTimeout("reloadUpnpDiv();", (maxRefreshTime + 1500));
    }
}
function reloadSdmcDiv() {
    if ($("input[id='sdmcStatus']").val() == "1") {
        if (sdmcView == 0)
            viewDiscoveredHostDetails("sdmc")
        else
            viewDiscoveryDetails("sdmc");
        setTimeout("reloadSdmcDiv();", (minRefreshTime + 2000));
    }
    else {
        getStatusOfDiscovery("sdmc");
        setTimeout("reloadSdmcDiv();", (maxRefreshTime + 2000));
    }
}
function reloadAllDiv() {
    discoveredHostDetailsForAll();
    if ($("input[id='sdmcStatus']").val() == "1" || $("input[id='snmpStatus']").val() == "1" || $("input[id='upnpStatus']").val() == "1" || $("input[id='pingStatus']").val() == "1") {
        setTimeout("reloadAllDiv();", (minRefreshTime + 2000));
    }
    else {
        setTimeout("reloadAllDiv();", (maxRefreshTime + 2000));
    }
}
function getStatusOfDiscovery(type) {
    $.ajax({
        type: "post",
        url: "discoveryStatus.py?type=" + type,
        success: function (result) {
            if (type == "ping") {
                $("input[id='pingStatus']").val(result);
            }
            else if (type == "snmp") {
                $("input[id='snmpStatus']").val(result);
            }
            else if (type == "upnp") {
                $("input[id='upnpStatus']").val(result);
            }
            else if (type == "sdmc") {
                $("input[id='sdmcStatus']").val(result);
            }
            checkStatusAndSetImages("no");
        }
    });
}
function allSubmit() {
    if ($("#allSubmit").parent().parent().parent().find("input[name='host']:checked").size() == 0) {
        alert("Please select atleast one host");
    }
    else {
        var sdmSelectedHost = [];
        var sdmSelectedDeviceType = [];
        var snmpSelectedHost = [];
        var snmpSelectedDeviceType = [];
        var upnpSelectedHost = [];
        var upnpSelectedDeviceType = [];
        var pingSelectedHost = [];
        var pingSelectedDeviceType = [];
        $("#allSubmit").parent().parent().parent().find("input[name='host']:checked").each(function () {
            if ($(this).attr("class") == "sdm") {
                sdmSelectedHost.push($(this).val());
                sdmSelectedDeviceType.push($(this).parent().parent().find("select[name='deviceType']").val());
            }
            else if ($(this).attr("class") == "snmp") {
                snmpSelectedHost.push($(this).val());
                snmpSelectedDeviceType.push($(this).parent().parent().find("select[name='deviceType']").val());
            }
            else if ($(this).attr("class") == "upnp") {
                upnpSelectedHost.push($(this).val());
                upnpSelectedDeviceType.push($(this).parent().parent().find("select[name='deviceType']").val());
            }
            else if ($(this).attr("class") == "ping") {
                pingSelectedHost.push($(this).val());
                pingSelectedDeviceType.push($(this).parent().parent().find("select[name='deviceType']").val());
            }
        });
        if (sdmSelectedHost.length > 0) {
            createHost("sdmc", sdmSelectedHost, sdmSelectedDeviceType);
        }
        if (snmpSelectedHost.length > 0) {
            createHost("snmp", snmpSelectedHost, snmpSelectedDeviceType);
        }
        if (upnpSelectedHost.length > 0) {
            createHost("upnp", upnpSelectedHost, upnpSelectedDeviceType);
        }
        if (pingSelectedHost.length > 0) {
            createHost("ping", pingSelectedHost, pingSelectedDeviceType);
        }
        alert("Selected host(s) added successfully.");
    }
}
function pingSubmit() {
    if ($("#pingSubmit").parent().parent().parent().find("input[name='host']:checked").size() == 0) {
        alert("Please select atleast one host");
    }
    else {
        var selectedHost = [];
        var selectedDeviceType = [];
        $("#pingSubmit").parent().parent().parent().find("input[name='host']:checked").each(function () {
            selectedHost.push($(this).val());
            selectedDeviceType.push($(this).parent().parent().find("select[name='deviceType']").val());
        });
        createHost("ping", selectedHost, selectedDeviceType);
    }
}

function snmpSubmit() {
    if ($("#snmpSubmit").parent().parent().parent().find("input[name='host']:checked").size() == 0) {
        alert("Please select atleast one host");
    }
    else {
        var selectedHost = [];
        var selectedDeviceType = [];
        $("#snmpSubmit").parent().parent().parent().find("input[name='host']:checked").each(function () {
            selectedHost.push($(this).val());
            selectedDeviceType.push($(this).parent().parent().find("select[name='deviceType']").val());
        });
        createHost("snmp", selectedHost, selectedDeviceType);
    }
}

function upnpSubmit() {
    if ($("#upnpSubmit").parent().parent().parent().find("input[name='host']:checked").size() == 0) {
        alert("Please select atleast one host");
    }
    else {
        var selectedHost = [];
        var selectedDeviceType = [];
        $("#upnpSubmit").parent().parent().parent().find("input[name='host']:checked").each(function () {
            selectedHost.push($(this).val());
            selectedDeviceType.push($(this).parent().parent().find("select[name='deviceType']").val());
        });
        createHost("upnp", selectedHost, selectedDeviceType);
    }
}

function sdmcSubmit() {
    if ($("#sdmcSubmit").parent().parent().parent().find("input[name='host']:checked").size() == 0) {
        alert("Please select atleast one host");
    }
    else {
        var selectedHost = [];
        var selectedDeviceType = [];
        $("#sdmcSubmit").parent().parent().parent().find("input[name='host']:checked").each(function () {
            selectedHost.push($(this).val());
            selectedDeviceType.push($(this).parent().parent().find("select[name='deviceType']").val());
        });
        createHost("sdmc", selectedHost, selectedDeviceType);
    }
}
function createHost(discoveryType, hostList, devType) {
    $("div.loading").show();
    $.ajax({
        type: "post",
        url: "createHostConfiguration.py?type=" + discoveryType + "&hostList=" + String(hostList) + "&deviceType=" + String(devType),
        async: false,
        success: function (result) {
            setTimeout(function () {
                createService(discoveryType, hostList, result)
            }, 3000);
        }
    })
}
function createService(discoveryType, hostList, service) {
    if (parseInt(service) == 2) {
        $.ajax({
            type: "post",
            url: "createSeviceConfiguration.py?type=" + discoveryType + "&hostList=" + hostList + "&service=" + service,
            success: function (result) {
                if (discoveryType == "ping") {
                    setTimeout(function () {
                        viewDiscoveredHostDetails("ping");
                    }, 3000);
                }
                else if (discoveryType == "snmp") {
                    setTimeout(function () {
                        viewDiscoveredHostDetails("snmp");
                    }, 3000);
                }
                else if (discoveryType == "upnp") {
                    setTimeout(function () {
                        viewDiscoveredHostDetails("upnp");
                    }, 3000);
                }
                else if (discoveryType == "sdmc") {
                    setTimeout(function () {
                        viewDiscoveredHostDetails("sdmc");
                    }, 3000);
                }
                discoveredHostDetailsForAll();
                $("div.loading").hide();
                //reload nms tree
            }
        });
    }
    else if (parseInt(service) == 1) {
        if (discoveryType == "ping") {
            setTimeout(function () {
                viewDiscoveredHostDetails("ping");
            }, 3000);
        }
        else if (discoveryType == "snmp") {
            setTimeout(function () {
                viewDiscoveredHostDetails("snmp");
            }, 3000);
        }
        else if (discoveryType == "upnp") {
            setTimeout(function () {
                viewDiscoveredHostDetails("upnp");
            }, 3000);
        }
        else if (discoveryType == "sdmc") {
            setTimeout(function () {
                viewDiscoveredHostDetails("sdmc");
            }, 3000);
        }
        discoveredHostDetailsForAll();
        $("div.loading").hide();
        $.ajax({
            type: "post",
            url: "createSeviceConfiguration.py?type=" + discoveryType + "&hostList=" + hostList + "&service=" + service,
            success: function (result) {
                //alert(result);
                //reload nms tree
            }
        });
    }
    else {
        if (discoveryType == "ping") {
            setTimeout(function () {
                viewDiscoveredHostDetails("ping");
            }, 3000);
        }
        else if (discoveryType == "snmp") {
            setTimeout(function () {
                viewDiscoveredHostDetails("snmp");
            }, 3000);
        }
        else if (discoveryType == "upnp") {
            setTimeout(function () {
                viewDiscoveredHostDetails("upnp");
            }, 3000);
        }
        else if (discoveryType == "sdmc") {
            setTimeout(function () {
                viewDiscoveredHostDetails("sdmc");
            }, 3000);
        }
        discoveredHostDetailsForAll();
        $("div.loading").hide();
        // reload nms tree
    }
}
