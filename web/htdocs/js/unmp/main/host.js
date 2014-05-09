var HOSTNAME = "";
var ADDRESS = "";
$(function () {
    $("#formDiv").hide();
    formForHost("add", "");
    $("#addhosttable").click(function () {
        $(this).fadeOut(1000);
        $("#gridviewDiv").fadeOut(1000, function () {
            $("#formDiv").fadeIn(1000, function () {
                $("#hostName").focus()
            });
        });
    })
    jQuery.validator.addMethod("noSpace", function (value, element) {
        return value.indexOf(" ") < 0 && value != "";
    }, "No space please and don't leave it empty");
});
function formForHost(action, hostName) {
    $.ajax({
        type: "get",
        url: "form_for_host.py?action=" + action + "&hostName=" + hostName,
        success: function (result) {
            $("#formDiv").html(result);
            if (action == "edit") {
                actionForHost("edit");
                $("#addhosttable").fadeOut(1000);
                $("#gridviewDiv").fadeOut(1000, function () {
                    $("#formDiv").fadeIn(1000, function () {
                        $("#alias").focus();
                    });
                });
                $("#deviceType option[value='" + $("input[name='hdDeviceType']").val() + "']").attr("selected", true);
            }
            else {
                actionForHost("add");
            }
            multiSelectHostGroups("HostGroup");
            multiSelectHostParents("HostParent");
            if (action == "edit")
                $("div[id='multiSelectListHostParent']").find("img[id='" + hostName + "']").parent().remove();
        }
    });
}
function actionForHost(act) {
    action = act
    validateHost("addHostForm");
    $("#addHostForm").submit(function () {
        formAction = $(this).attr("action") + "?" + $(this).serialize();
        if ($("#addHostForm").valid()) {
            loadingHost();
            $.ajax({
                type: "post",
                url: formAction,
                success: function (result) {
                    //alert(result)
                    if ($.trim(result) == "0") {
                        loadingHideHost(false);
                        alert("Host Name already exist.");
                    }
                    else if ($.trim(result) == "1") {
                        resetAddHost();
                        setTimeout("loadingHideHost(true);", 3000);
                        if (action == "edit") {
                            alert("Host Updated Successfully.");
                            $("#formDiv").fadeOut(1000);
                            $("#addhosttable").fadeIn(1000);
                            $("#gridviewDiv").fadeIn(1000);
                            setTimeout("formForHost('add','');", 3000);
                        }
                        else {
                            alert("Host Added Successfully.");
                            setTimeout("reloadParentList();", 3000);
                        }
                    }
                    else {	//alert(result);
                        loadingHideHost(false);
                        alert("Host Name and Alias both are require fields.");
                    }
                },
                error: function () {
                    loadingHideHost(false);
                    alert("Some Error Occur");
                }
            });
        }
        return false;
    });
    $("input[id='serviceManagementManual']").click(function () {
        if ($(this).attr("checked")) {
            $("tr.trServiceManagement").hide();
        }
    })
    $("input[id='serviceManagementUsingTemplate']").click(function () {
        if ($(this).attr("checked")) {
            $("tr.trServiceManagement").show();
        }
    })
    serviceManagementOption();
}
function validateHost(formid) {
    $("#" + formid).validate({
        rules: {
            hostName: {
                required: true,
                noSpace: true
            },
            alias: "required",
            ipAddress: "required",
            deviceType: "required"
        },
        messages: {
            hostName: {
                required: " *",
                noSpace: " Space not allow"
            },
            alias: " *",
            ipAddress: " *",
            deviceType: " *"
        }
    });
}
function editHost(hostname) {
    formForHost("edit", hostname);
}
function deleteHost(hostName, address) {
    if (parseInt($("input[id='totalHost']").val()) < 2) {
        alert("You Could not Delete this host, because atleast one host must be in NMS.");
    }
    else {
        HOSTNAME = hostName;
        ADDRESS = address;
        $("div#DeleteHostMsg").show();
        loadingHost();
        $("input[id='command1']").attr("checked", "checked");
    }
}
function resetAddHost() {
    $("label.error").hide();
    $("#hostName").val("").focus();
    $("#alias").val("");
    $("#confPort,#confUsername,#confPassword").val("");
    $("#ipAddress").val("");
    $("div[id='multiSelectListHostGroup']").find("div.selected").find("img").click();
    $("div[id='multiSelectListHostParent']").find("div.selected").find("img").click();
    $("#deviceType option[value='']").attr("selected", true);
}
function cancelEditHost() {
    $("#formDiv").fadeOut(1000, function () {
        $("#addhosttable").fadeIn(1000);
        $("#gridviewDiv").fadeIn(1000);
        formForHost("add", "");
    });
}
function cancelAddHost() {
    $("label.error").hide();
    $("#formDiv").fadeOut(1000, function () {
        $("#addhosttable").fadeIn(1000);
        $("#gridviewDiv").fadeIn(1000);
    });
}
function gridViewHost() {
    $.ajax({
        type: "get",
        url: "grid_view_host.py",
        success: function (result) {
            $("#gridviewDiv").html(result);
        }
    });
}
function loadingHost() {
    $("div.loading").show();
}
function loadingHideHost(load) {
    $("div.loading").hide();
    if (load) {
        parent.side.location = 'side.py';
        gridViewHost();
    }
}
function cancelDelete() {
    $("div#DeleteHostMsg").hide();
    loadingHideHost(false);
}
function okDelete() {
    loadingHost();
    $("div#DeleteHostMsg").hide();
    $.ajax({
        type: "get",
        url: "ajaxcall_delete_host.py?hostName=" + HOSTNAME + "&command=" + $('input:radio[name=command]:checked').val() + "&address=" + ADDRESS,
        success: function (result) {
            if ($.trim(result) == "0") {
                loadingHideHostGroup(false);
                alert("Host could not delete, Please try again later.");
            }
            else if ($.trim(result) == "1") {
                resetAddHost();
                setTimeout("loadingHideHost(true);", 3000);
                alert("Host Deleted Successfully.");
                setTimeout("formForHost('add','');", 3000);
            }
            else {
                loadingHideHost(false);
                alert("Some Error Occur" + result);
            }
        },
        error: function () {
            loadingHideHost(false);
            alert("Some Error Occur");
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
    var hostGroupArray = $("input[name='hdTemp" + hostgroup + "']").val().split(",");
    for (k = 0; k < hostGroupArray.length; k++) {
        $("div[id='multiSelectList" + hostgroup + "']").find("img[id='" + $.trim(hostGroupArray[k]) + "']").click();
    }
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

/*============================= Multiple Selecter For Host Parent =========================*/
function multiSelectHostParents(hostparent) {
    $(".plus" + hostparent).click(function () {
        plusHostParentOption(hostparent, this);
    })
    $(".minus" + hostparent).click(function () {
        minusHostParentOption(hostparent, this);
    })
    var hostParentArray = $("input[name='hdTemp" + hostparent + "']").val().split(",");
    for (k = 0; k < hostParentArray.length; k++) {
        $("div[id='multiSelectList" + hostparent + "']").find("img[id='" + $.trim(hostParentArray[k]) + "']").click();
    }
    $("#rm" + hostparent).click(function (e) {
        e.preventDefault();
        $("div[id='multiSelectList" + hostparent + "']").find("div.selected").find("img").click();
    })
    $("#add" + hostparent).click(function (e) {
        e.preventDefault();
        $("div[id='multiSelectList" + hostparent + "']").find("div.nonSelected").find("img").click();
    })
}
function minusHostParentOption(hostparent, Obj) {
    liObj = $("<li/>");
    imgObj = $("<img/>");
    liObj.append($(Obj).attr("id"));
    imgObj.attr("src", "images/add16.png").attr("class", "plus plus" + hostparent + "").attr("alt", "+").attr("id", $(Obj).attr("id")).click(function () {
        plusHostParentOption(hostparent, this)
    })
    liObj.append(imgObj);
    $(Obj).parent().parent().parent().parent().find("div.nonSelected").find("ul").append(liObj);
    $(Obj).parent().parent().parent().parent().find("input[name='hd" + hostparent + "']").val("");
    j = 0
    for (i = 0; i < $(Obj).parent().parent().find("li").size(); i++) {
        var addedHostParent = $(Obj).parent().parent().find("li").eq(i).find("img").attr("id");
        if (addedHostParent != $(Obj).attr("id")) {
            if (j == 0) {
                $(Obj).parent().parent().parent().parent().find("input[name='hd" + hostparent + "']").val($.trim(addedHostParent));
            }
            else {
                $(Obj).parent().parent().parent().parent().find("input[name='hd" + hostparent + "']").val($(Obj).parent().parent().parent().parent().find("input[name='hd" + hostparent + "']").val() + "," + $.trim(addedHostParent));
            }
            j++;
        }
    }
    $(Obj).parent().parent().parent().parent().find("span#count").html(j)
    $(Obj).parent().remove();
}
function plusHostParentOption(hostparent, Obj) {
    var countParent = 0;
    liObj = $("<li/>");
    imgObj = $("<img/>");
    liObj.append($(Obj).attr("id"));
    imgObj.attr("src", "images/minus16.png").attr("class", "minus minus" + hostparent).attr("alt", "-").attr("id", $(Obj).attr("id")).click(function () {
        minusHostParentOption(hostparent, this)
    })
    liObj.append(imgObj);
    $(Obj).parent().parent().parent().parent().find("div.selected").find("ul").append(liObj);
    hdval = $(Obj).parent().parent().parent().parent().find("input[name='hd" + hostparent + "']").val()
    if ($.trim(hdval) == "") {
        $(Obj).parent().parent().parent().parent().find("input[name='hd" + hostparent + "']").val($(Obj).attr("id"))
    }
    else {
        $(Obj).parent().parent().parent().parent().find("input[name='hd" + hostparent + "']").val(hdval + "," + $(Obj).attr("id"))
    }
    countParent = $(Obj).parent().parent().parent().parent().find("span#count").html();
    $(Obj).parent().parent().parent().parent().find("span#count").html(parseInt(countParent) + 1);
    $(Obj).parent().remove();
}
function reloadParentList() {
    $.ajax({
        type: "get",
        url: "parent_multiple_select_list.py",
        success: function (result) {
            $("#parentList").html(result);
            multiSelectHostParents("HostParent")
        },
        error: function () {
            alert("Problem in loading of new Parent list, please reload page again.");
        }
    });
}
/*============================= End Multiple Selecter For Host Parent =========================*/

/*============================== Service Management Options  =========================== */
function serviceManagementOption() {
    $("input[name='rdServiceTemplate']").click(function () {
        $("div.hostTemplateDiv").hide()
        if ($(this).attr("checked")) {
            $("div#" + $(this).attr("id") + "Div").slideDown();
        }
    })
}
/*============================= End Service Management Options  =========================== */
