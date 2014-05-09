var selectedHost = "";
var selectedService = "";
var oldSelectedHost = "";
var oldSelectedService = "";
var actionType = "add";
$(function () {
    $("#formDiv").hide();
    formForService("add", "", "");
    $("#addservicetable").click(function () {
        cancelChooseService();
        $(this).fadeOut(1000);
        $("#gridviewDiv").fadeOut(500, function () {
            $("#formDiv").fadeIn(1000);
        });
    })
    jQuery.validator.addMethod("noSpace", function (value, element) {
        return value.indexOf(" ") < 0 && value != "";
    }, "No space please and don't leave it empty");
});
function formForService(action, checkCommand, host) {
    $.ajax({
        type: "get",
        url: "form_for_service.py?action=" + action + "&checkCommand=" + checkCommand + "&host=" + host,
        success: function (result) {
            $("#formDiv").html(result);
            selectedHost = selectedService = "";
            bindEvents();
            if (action == "edit") {
                actionForService("edit");
                $(".serviceClass,.hostClass,.trBlack").hide();
                $(".trHost,.trWhite,.trService,#serviceForm").show();
                $("#addservicetable").fadeOut(1000);
                $("#gridviewDiv").fadeOut(1000, function () {
                    $("#formDiv").fadeIn(1000);
                });
                selectedService = $("#serviceName").val();
                selectedHost = $("#hostName").val();
                continueChooseService();

                $("li[id='" + selectedHost + "']").css("background", "url('images/selectlist_header.png') repeat-x scroll 50% 50% #CCCCCC");
                $("li[id='" + selectedHost + "']").css("border", "0.5px solid #CCCCCC");
                $("input[id='btnChooseHost']").removeAttr("disabled");


                $("li[id='" + selectedService + "']").css("background", "url('images/selectlist_header.png') repeat-x scroll 50% 50% #CCCCCC");
                $("li[id='" + selectedService + "']").css("border", "0.5px solid #CCCCCC");
                $("input[id='btnChooseService']").removeAttr("disabled");

            }
            else {
                actionForService("add");
                $(".trHost,.trService,.trWhite,.trBlack,.serviceClass,#serviceForm").hide();
            }
            multiSelectServiceGroups("ServiceGroup");
        }
    });
}
function bindEvents() {
    $(".liHost").click(function () {
        selectedHost = $(this).attr("id");
        $(".liHost").css("background", "");
        $(".liHost").css("border", "");
        $(this).css("background", "url('images/selectlist_header.png') repeat-x scroll 50% 50% #CCCCCC");
        $(this).css("border", "0.5px solid #CCCCCC");
        $("input[id='btnChooseHost']").removeAttr("disabled");
    });
    $(".liService").click(function () {
        selectedService = $(this).attr("id");
        $(".liService").css("background", "");
        $(".liService").css("border", "");
        $(this).css("background", "url('images/selectlist_header.png') repeat-x scroll 50% 50% #CCCCCC");
        $(this).css("border", "0.5px solid #CCCCCC");
        $("input[id='btnChooseService']").removeAttr("disabled");
    });
    $("#changeHost").click(function (event) {
        event.preventDefault();
        backToChooseService();
        cancelChooseService();
    })
    $("#changeService").click(function (event) {
        event.preventDefault();
        backToChooseService();
    })
}
function actionForService(act) {
    action = act;
    validateBasicArguments = 0;
    validateService("addServiceForm");
    $("#addServiceForm").submit(function () {
        validateBasicArguments = 0;
        for (i = parseInt($("#basicArgument").val()); i > 0; i--) {
            if ($.trim($("#arg" + i).val()) == "") {
                validateBasicArguments += 1;
                $("label#error_arg" + i).show();
                if ($("#addServiceForm").valid())
                    $("input[id='arg" + i + "']").focus();
            }
            else {
                $("label#error_arg" + i).hide()
            }
        }
        if (parseInt($("#basicArgument").val()) == 0) {
            validateBasicArguments = 0;
        }
        if ($("#addServiceForm").valid() && validateBasicArguments == 0) {
            $("#hdCommand").val($.trim($("#serviceName").val()));
            for (i = 1; i <= parseInt($("#basicArgument").val()); i++) {
                $("#hdCommand").val($("#hdCommand").val() + "!" + $("#arg" + i).val());
            }
            var advanceArgument = "";
            for (i = 1; i <= parseInt($("#advanceArgument").val()); i++) {
                if ($.trim($("#aoarg" + i).val()) != "") {
                    advanceArgument += " " + ($("#aoarg" + i).attr("para") == "-" ? ($("#aoarg" + i).attr("para")) : $("#aoarg" + i).attr("para") + " ") + $("#aoarg" + i).val();
                }
            }
            if (advanceArgument != "") {
                $("#hdCommand").val($("#hdCommand").val() + "!" + advanceArgument);
            }
            formAction = $(this).attr("action") + "?" + $(this).serialize();
            loadingService();
            $.ajax({
                type: "post",
                url: formAction,
                success: function (result) {
                    //alert(result)
                    if ($.trim(result) == "0") {
                        loadingHideService(false);
                        alert("Same Service with same settings already exist for this Host.");
                    }
                    else if ($.trim(result) == "1") {
                        //resetAddService();
                        setTimeout("loadingHideService(true);", 3000);
                        if (action == "edit") {
                            alert("Service Updated Successfully.");
                            cancelAddService();
                            setTimeout("formForService('add','','');", 3000);
                            actionType = "add";
                        }
                        else {
                            alert("Service Added Successfully.");
                            cancelAddService();
                        }
                    }
                    else if ($.trim(result) == "2") {
                        loadingHideService(false);
                        alert("Same Service Description already exist for this Host. Please change your Service Description.");
                    }
                    else {
                        loadingHideService(false);
                        alert("Some Fields are require.");
                    }
                },
                error: function () {
                    loadingHideService(false);
                    alert("Some Error Occur");
                }
            });
        }
        return false;
    });
}
function validateService(formid) {
    $("#" + formid).validate({
        rules: {
            serviceName: {
                required: true,
                noSpace: true
            },
            hostName: {
                required: true,
                noSpace: true
            },
            serviceDescription: "required",
            maxCheckAttempts: {
                number: true
            },
            normalCheckInterval: {
                number: true
            },
            retryCheckInterval: {
                number: true
            },
            notificationInterval: {
                number: true
            }
        },
        messages: {
            serviceName: {
                required: " *",
                noSpace: " Space not allow"
            },
            hostName: {
                required: " *",
                noSpace: " Space not allow"
            },
            serviceDescription: " *",
            maxCheckAttempts: {
                number: " It must be a number"
            },
            normalCheckInterval: {
                number: " It must be a number"
            },
            retryCheckInterval: {
                number: " It must be a number"
            },
            notificationInterval: {
                number: " It must be a number"
            }
        }
    });
}
function editService(checkCommand, host) {
    oldSelectedService = "";
    actionType = "edit"
    formForService("edit", checkCommand, host);
}
function deleteService(serviceName, hostName) {
    if (parseInt($("input[id='totalService']").val()) < 2) {
        alert(" Deleting this service is restricted, because atleast one service must be in NMS.");
    }
    else {
        if (confirm("Are you sure, you want to delete this service?")) {
            loadingService();
            $.ajax({
                type: "get",
                url: "ajaxcall_delete_service.py?checkCommand=" + serviceName + "&hostName=" + hostName,
                success: function (result) {
                    //alert(result)
                    if ($.trim(result) == "0") {
                        loadingHideService(false);
                        alert("Service could not delete, Please try again later.");
                    }
                    else if ($.trim(result) == "1") {
                        //resetAddService();
                        setTimeout("loadingHideService(true);", 3000);
                        alert("Service Deleted Successfully.");
                        setTimeout("formForService('add','','');", 3000);
                        //cancelAddService();
                    }
                    else {
                        loadingHideService(false);
                        alert("Some Error Occur");
                    }
                },
                error: function () {
                    loadingHideService(false);
                    alert("Some Error Occur");
                }
            });
        }
    }
}
/*function resetAddService()
 {
 $("label.error").hide();
 $("#serviceName").val("").focus();
 $("#alias").val("");
 $("#confPort").val("");
 $("#ipAddress").val("");
 $("div[id='multiSelectListServiceGroup']").find("div.selected").find("img").click();
 $("div[id='multiSelectListServiceParent']").find("div.selected").find("img").click();
 }*/
function cancelEditService() {
    cancelAddService();
    setTimeout("formForService('add','','');", 1500);
    actionType = "add";
}
function cancelChooseHost() {
    $("#formDiv").fadeOut(1000, function () {
        $("#gridviewDiv").fadeIn(1000);
        $("#addservicetable").fadeIn(1000);
    });
}
function cancelChooseHostForEditService() {
    $(".serviceClass,.hostClass,.trBlack").hide();
    $(".trHost,.trWhite,.trService,#serviceForm").show();
}
function cancelChooseService() {
    $(".trHost,.trService,.trWhite,.trBlack,.serviceClass").hide();
    $(".hostClass").show();
}
function continueChooseHost() {
    $(".trService,.hostClass,#serviceForm").hide();
    $(".trHost,.trBlack,.trWhite,.serviceClass").show();
    if (oldSelectedHost != selectedHost) {
        oldSelectedHost = selectedHost;
        $("input[id='hostName']").val(selectedHost);
    }
}
function continueChooseService() {
    basicI = advinceI = paraI = 0;
    paraArray = new Array();
    $(".serviceClass,.hostClass,.trBlack").hide();
    $(".trHost,.trWhite,.trService").show();
    if (oldSelectedService != selectedService) {
        oldSelectedService = selectedService;
        $("input[id='serviceName']").val(selectedService);
        $.ajax({
            type: "get",
            url: "form_for_service_setting.py?serviceName=" + selectedService + "&action=" + actionType,
            success: function (result) {
                $("#serviceForm").html(result);
                $("#serviceForm").show();
                if ($.trim($("#oldCheckCommand").val()).indexOf(selectedService) == 0 && actionType == "edit") {
                    basicI = parseInt($("#basicArgument").val());
                    advinceI = parseInt($("#advanceArgument").val());
                    paraArray = $.trim($("#oldCheckCommand").val()).split("!");
                    paraI = 1;
                    for (i = 1; i <= basicI; i++) {
                        if (paraArray.length > 1) {
                            $("#arg" + i).val(paraArray[paraI]);
                            paraI++;
                        }
                    }
                    for (i = 1; i <= advinceI; i++) {
                        para = $.trim($("#aoarg" + i).attr("para")) == "-" ? $.trim($("#aoarg" + i).attr("para")) : $.trim($("#aoarg" + i).attr("para")) + " ";
                        tempArray1 = paraArray[paraI].split(para);
                        if (tempArray1.length > 1) {
                            if (para == "-") {
                                if ($.trim(tempArray1[1].split(" -")[0]) == "4" || $.trim(tempArray1[1].split(" -")[0]) == "6") {
                                    $("#aoarg" + i).val($.trim(tempArray1[1].split(" -")[0]));
                                }
                            }
                            else {
                                $("#aoarg" + i).val($.trim(tempArray1[1].split(" -")[0]));
                            }
                        }
                        else {
                            //$("#aoarg" + i).val($.trim(tempArray1[0]));
                        }
                    }
                }
            },
            error: function () {
                alert("Some error occur");
            }
        });
    }
    else {
        $("#serviceForm").show();
    }
}
function cancelAddService() {
    $("label.error").hide();
    $(".trHost,.trService,.trWhite,.trBlack,.serviceClass,.hostClass,#serviceForm").fadeOut(1000);
    $("#formDiv").fadeOut(1000, function () {
        $("#addservicetable,#gridviewDiv").fadeIn(1000)
    });
}
function backToChooseService() {
    $(".trService,.hostClass,#serviceForm").hide();
    $(".trHost,.trBlack,.trWhite,.serviceClass").show();
}
function gridViewService() {
    $.ajax({
        type: "get",
        url: "grid_view_service.py",
        success: function (result) {
            $("#gridviewDiv").html(result);
        }
    });
}
function loadingService() {
    $("div.loading").show();
}
function loadingHideService(load) {
    $("div.loading").hide();
    if (load) {
        parent.side.location = 'side.py';
        gridViewService();
    }
}
/*============================= Multiple Selecter For Service Group =========================*/
function multiSelectServiceGroups(servicegroup) {
    $(".plus" + servicegroup).click(function () {
        plusServiceGroupOption(servicegroup, this);
    })
    $(".minus" + servicegroup).click(function () {
        minusServiceGroupOption(servicegroup, this);
    })
    var hostGroupArray = $("input[name='hdTemp" + servicegroup + "']").val().split(",");
    for (k = 0; k < hostGroupArray.length; k++) {
        $("div[id='multiSelectList" + servicegroup + "']").find("img[id='" + $.trim(hostGroupArray[k]) + "']").click();
    }
    $("#rm" + servicegroup).click(function (e) {
        e.preventDefault();
        $("div[id='multiSelectList" + servicegroup + "']").find("div.selected").find("img").click();
    })
    $("#add" + servicegroup).click(function (e) {
        e.preventDefault();
        $("div[id='multiSelectList" + servicegroup + "']").find("div.nonSelected").find("img").click();
    })
}
function minusServiceGroupOption(servicegroup, Obj) {
    liObj = $("<li/>");
    imgObj = $("<img/>");
    liObj.append($(Obj).attr("id"));
    imgObj.attr("src", "images/add16.png").attr("class", "plus plus" + servicegroup + "").attr("alt", "+").attr("id", $(Obj).attr("id")).click(function () {
        plusServiceGroupOption(servicegroup, this)
    })
    liObj.append(imgObj);
    $(Obj).parent().parent().parent().parent().find("div.nonSelected").find("ul").append(liObj);
    $(Obj).parent().parent().parent().parent().find("input[name='hd" + servicegroup + "']").val("");
    j = 0
    for (i = 0; i < $(Obj).parent().parent().find("li").size(); i++) {
        var addedHostGroup = $(Obj).parent().parent().find("li").eq(i).find("img").attr("id");
        if (addedHostGroup != $(Obj).attr("id")) {
            if (j == 0) {
                $(Obj).parent().parent().parent().parent().find("input[name='hd" + servicegroup + "']").val($.trim(addedHostGroup));
            }
            else {
                $(Obj).parent().parent().parent().parent().find("input[name='hd" + servicegroup + "']").val($(Obj).parent().parent().parent().parent().find("input[name='hd" + servicegroup + "']").val() + "," + $.trim(addedHostGroup));
            }
            j++;
        }
    }
    $(Obj).parent().parent().parent().parent().find("span#count").html(j)
    $(Obj).parent().remove();
}
function plusServiceGroupOption(servicegroup, Obj) {
    var countService = 0;
    liObj = $("<li/>");
    imgObj = $("<img/>");
    liObj.append($(Obj).attr("id"));
    imgObj.attr("src", "images/minus16.png").attr("class", "minus minus" + servicegroup).attr("alt", "-").attr("id", $(Obj).attr("id")).click(function () {
        minusServiceGroupOption(servicegroup, this)
    })
    liObj.append(imgObj);
    $(Obj).parent().parent().parent().parent().find("div.selected").find("ul").append(liObj);
    hdval = $(Obj).parent().parent().parent().parent().find("input[name='hd" + servicegroup + "']").val()
    if ($.trim(hdval) == "") {
        $(Obj).parent().parent().parent().parent().find("input[name='hd" + servicegroup + "']").val($(Obj).attr("id"))
    }
    else {
        $(Obj).parent().parent().parent().parent().find("input[name='hd" + servicegroup + "']").val(hdval + "," + $(Obj).attr("id"))
    }
    countService = $(Obj).parent().parent().parent().parent().find("span#count").html();
    $(Obj).parent().parent().parent().parent().find("span#count").html(parseInt(countService) + 1);
    $(Obj).parent().remove();
}
/*============================= End Multiple Selecter For Service Group =========================*/
