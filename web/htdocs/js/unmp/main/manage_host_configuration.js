var lastTab = null;
var macAddress = "";
var deviceType = "";
$(function () {
    $(document).click(function () {
        $("#addDivHover").hide();
        $("#chooseTemplateHover").hide();
        $("div.tab-head").find("a.tab-active").removeClass("tab-active").addClass("tab-button");
        $(lastTab).removeClass("tab-button").addClass("tab-active");
    });
    /*$("#imageUploadForm").submit(function(){
     if($.trim($("input[name='file']").val()) == "")
     {
     $("#uploadError").show();
     }
     else
     {
     $.ajax({
     type:"post",
     url:$(this).attr("action") + "?" + $(this).serialize(),
     //url: "uploadfile.py",
     success:function(result){
     if(result == "0")
     alert("Image Uploaded successfully. please wait for 5 min device is rebooting.")
     }
     });
     $("#uploadError").hide();
     cancelUpload();
     }
     return false;
     })*/
    $("#chooseTemplateHover").find("a").click(function (e) {
        e.preventDefault();
        e.stopPropagation();
        $("#templateName").val($(this).text());
        $("#templateId").val($(this).attr("name"));
        $("div.device-hover-menu").hide();
        $("div.tab-head").find("a.tab-active").removeClass("tab-active").addClass("tab-button");
        $("div.tab-head").find("a.tab-disable").removeClass("tab-disable").addClass("tab-button");
        $("#settingButton").removeClass("tab-button").addClass("tab-active");
        lastTab = "#settingButton"
    });
    $("#addDivHover").find("a").click(function (e) {
        e.preventDefault();
        e.stopPropagation();
        $("#chooseTemplateHover").hide();
        $("#settingsDiv").html("<div class=\"msg-head\"><img style=\"vertical-align: middle;\" alt=\"\" src=\"images/loading-small.gif\"><span> Loading... </span></div>");
        $.ajax({
            type: "post",
            url: "discoverDevices.py?deviceType=" + $(this).attr("name") + "&sdmcString=" + $(this).attr("sdmc"),
            success: function (result) {
                result = $(result);
//================ Add Jquery events Again ===========================
                $(result).find("input[name='allChecked']").click(function () {
                    if (this.checked) {
                        $(this).parent().parent().parent().find("input[name='host']").attr("checked", true);
                        $(this).parent().parent().parent().find("input[name='address']").attr("readonly", false);
                    }
                    else {
                        $(this).parent().parent().parent().find("input[name='host']").attr("checked", false);
                        $(this).parent().parent().parent().find("input[name='address']").attr("readonly", true);
                    }
                });
                $(result).find("input[name='host']").click(function () {
                    if (this.checked) {
                        if ($(this).parent().parent().parent().find("input[name='host']:checked").size() == parseInt($(this).parent().parent().parent().find("input[name='totalHost']").val())) {
                            $(this).parent().parent().parent().find("input[name='allChecked']").attr("checked", true);
                        }
                        $(this).parent().parent().find("input[name='address']").attr("readonly", false);
                    }
                    else {
                        $(this).parent().parent().parent().find("input[name='allChecked']").attr("checked", false);
                        $(this).parent().parent().find("input[name='address']").attr("readonly", true).val($(this).val());
                    }
                });
                $(result).find("input[name='factoryReset']").click(function () {
                    if (confirm("Are you sure, you want to apply factory reset on this device?")) {
                        $.ajax({
                            type: "post",
                            url: "factory_reset.py?deviceType=" + $(this).attr("devicetype") + "&mac=" + $(this).attr("mac"),
                            success: function (result) {
                                if (result == "0")
                                    alert("Your host reset successfully. please wait for 5 min device is rebooting.");
                            }
                        });
                    }
                });
//================ End Add Jquery events Again ===========================		
                $("#settingsDiv").html(result);
                $("div.tab-body").hide();
                $("#settingsDiv").show();
            }
        });
        $("div.device-hover-menu").hide();
        $("div.tab-head").find("a.tab-active").removeClass("tab-active").addClass("tab-button");
        $("div.tab-head").find("a.tab-disable").removeClass("tab-disable").addClass("tab-button");
        $("#settingButton").removeClass("tab-button").addClass("tab-active");
        lastTab = "#settingButton"
    })
    $("div.tab-head").find("a").click(function (e) {
        e.preventDefault();
        if ($(this).hasClass("tab-disable")) {
            // do nothing
        }
        else {
            if ($(this).attr("href") == "#addDiv") {
                e.stopPropagation();
                $("div.device-hover-menu").hide();
                $(this).parent().find("a.tab-active").removeClass("tab-active").addClass("tab-button");
                $(this).removeClass("tab-button").addClass("tab-active");
                $($(this).attr("href") + "Hover").show();
            }
            else if ($(this).attr("href") == "#chooseTemplate") {
                e.stopPropagation();
                $("div.device-hover-menu").hide();
                $(this).parent().find("a.tab-active").removeClass("tab-active").addClass("tab-button");
                $(this).removeClass("tab-button").addClass("tab-active");
                $($(this).attr("href") + "Hover").show();
            }
            else {
                $(this).parent().find("a.tab-active").removeClass("tab-active").addClass("tab-button");
                $(this).removeClass("tab-button").addClass("tab-active");
                $("div.tab-body").hide();
                $($(this).attr("href")).show();
            }
        }
    });
})
function cancelUpload() {
    macAddress = "";
    deviceType = "";
    $("div.loading").hide();
    $("#imageUploadDiv").hide();
    $("input[name='uploader']").val("");
}
function configSubmit() {
    var templateMsg = " select ";
    var templateCheck = 0;
    var hostCheck = 0;
    if ($("input[name='templateId']").val() == "") {
        templateCheck = 1;
    }
    if ($("#configSubmit").parent().parent().parent().find("input[name='host']:checked").size() == 0) {
        hostCheck = 1;
    }
    else if (templateCheck == 0) {
        var selectedHost = [];
        var newIpAddress = [];
        var macAddress = [];
        var deviceType = [];
        var templateId = $("input[name='templateId']").val();
        $("#configSubmit").parent().parent().parent().find("input[name='host']:checked").each(function () {
            newIpAddress.push($(this).parent().next().find("input[name='address']").val());
            selectedHost.push($(this).val());
            macAddress.push($(this).attr("id"));
            deviceType.push($(this).attr("deviceType"));
        });
        //alert("selected host: " + selectedHost + " chenged " + newIpAddress + "templateId: " + templateId + " mac: " + macAddress);
        $.ajax({
            type: "post",
            url: "apply_config_template.py?ipAddress=" + selectedHost + "&macAddress=" + macAddress + "&deviceType=" + deviceType + "&templateId=" + $("input[name='templateId']").val(),
            success: function (result) {
                if ($.trim(result) == "0") {
                    alert("Configuration Profile Applyed successfully. Selected devices are rebooting please wait for 5 min.")
                }
                else {
                    alert("There is some error occur, refresh the page and try again.")
                }
            }
        });
    }
    if (templateCheck == 1 && hostCheck == 1) {
        alert("Please select configuration profile and at least one host");
    }
    else {
        if (templateCheck == 1) {
            alert("Please select configuration profile");
        }
        else if (hostCheck == 1) {
            alert("Please select at least one host");
        }
    }
}
function setIp() {
    var validation = 0;
    if ($.trim($("input[name='gatewayIp']").val()) == "") {
        validation = 1;
        $("input[name='gatewayIp']").focus();
        $("#gatewayIpError").show();
    }
    else {
        $("#gatewayIpError").hide();
    }
    if ($.trim($("input[name='localNetmask']").val()) == "") {
        validation = 1;
        $("input[name='localNetmask']").focus();
        $("#localNetmaskError").show();
    }
    else {
        $("#localNetmaskError").hide();
    }

    if ($("#configSubmit").parent().parent().parent().find("input[name='host']:checked").size() == 0) {
        alert("Please select at least one host");
    }
    else {
        var selectedHost = [];
        var newIpAddress = [];
        var macAddress = [];
        var deviceType = [];
        var templateId = $("input[name='templateId']").val();
        $("#configSubmit").parent().parent().parent().find("input[name='host']:checked").each(function () {
            newIpAddress.push($(this).parent().next().find("input[name='address']").val());
            selectedHost.push($(this).val());
            macAddress.push($(this).attr("id"));
            deviceType.push($(this).attr("deviceType"));
        });
        if (validation == 0) {
            $.ajax({
                type: "post",
                url: "set_ip.py?oldIpAddress=" + selectedHost + "&newIpAddress=" + newIpAddress + "&macAddress=" + macAddress + "&deviceType=" + deviceType + "&localNetmask=" + $("input[name='localNetmask']").val() + "&gatewayIp=" + $("input[name='gatewayIp']").val(),
                success: function (result) {
                    if (result == "0") {
                        alert("Your host ip changed successfully. please wait for 5 min devices are rebooting.");
                    }
                    else {
                        alert("There is some error occur, refresh the page and try again.");
                    }
                }
            });
        }
    }
}
function imageUploadCheck() {
    if ($("#configSubmit").parent().parent().parent().find("input[name='host']:checked").size() == 0) {
        alert("Please select at least one host");
        return false;
    }
    else {
        var macAddress = [];
        var deviceType = [];
        $("#configSubmit").parent().parent().parent().find("input[name='host']:checked").each(function () {
            macAddress.push($(this).attr("id"));
            deviceType.push($(this).attr("deviceType"));
        });
        $("#deviceTy").val(String(deviceType));
        $("#deviceMac").val(String(macAddress));
        $("div.loading").show();
        $("#imageUploadDiv").show();
        $("#uploadError").hide();
        return true;
    }
}
function uploadImageFileCheck() {
    if ($.trim($("input[name='file']").val()) == "") {
        $("#uploadError").show();
        return false;
    }
    else {
        return true;
    }
}
