var HOSTGROUPNAME = "";
$(document).ready(function () {
    $("#formDiv").hide();
    formForHostGroup("add", "");
    $("#addhosttable").click(function () {
        $(this).slideUp(1000);
        $("#formDiv").slideDown(1000, function () {
            $("#hostGroupName").focus();
        });
    })
    jQuery.validator.addMethod("noSpace", function (value, element) {
        return value.indexOf(" ") < 0 && value != "";
    }, "No space please and don't leave it empty");
});
function formForHostGroup(action, hostGroupName) {
    $.ajax({
        type: "get",
        url: "form_for_hostgroup.py?action=" + action + "&hostGroupName=" + hostGroupName,
        success: function (result) {
            $("#formDiv").html(result);
            if (action == "edit") {
                actionForHostGroup("edit");
                $("#addhosttable").slideUp(1000);
                $("#formDiv").slideDown(1000, function () {
                    $("#hostGroupName").focus();
                });
            }
            else {
                actionForHostGroup("add");
            }
        }
    });
}
function actionForHostGroup(act) {
    action = act
    validateHostGroup("addHostGroupForm");
    $("#addHostGroupForm").submit(function () {
        formAction = $(this).attr("action") + "?" + $(this).serialize();
        if ($("#addHostGroupForm").valid()) {
            loadingHostGroup();
            $.ajax({
                type: "post",
                url: formAction,
                success: function (result) {
                    //alert(result)
                    if ($.trim(result) == "0") {
                        loadingHideHostGroup(false);
                        alert("Host Group Name already exist.");
                    }
                    else if ($.trim(result) == "1") {
                        resetAddHostGroup();
                        setTimeout("loadingHideHostGroup(true);", 3000);
                        if (action == "edit") {
                            alert("Host Group Updated Successfully.");
                            $("#formDiv").slideUp(1000);
                            $("#addhosttable").slideDown(1000);
                            setTimeout("formForHostGroup('add','');", 3000);
                        }
                        else {
                            alert("Host Group Added Successfully.");
                        }
                    }
                    else {
                        loadingHideHostGroup(false);
                        alert("Host Group Name and Alias both are require fields.");
                    }
                    $("img#del_hostgroup").show();
                    $("img#add_hostgroup").show();
                },
                error: function () {
                    $("img#del_hostgroup").show();
                    $("img#add_hostgroup").show();
                    loadingHideHostGroup(false);
                    alert("Some Error Occur");
                }
            });
        }
        return false;
    });
}
function validateHostGroup(formid) {
    $("#" + formid).validate({
        rules: {
            hostGroupName: {
                required: true,
                noSpace: true
            },
            alias: "required"
        },
        messages: {
            hostGroupName: {
                required: " *",
                noSpace: " Space not allow"
            },
            alias: " *"
        }
    });
}
function editHostGroup(hostname) {
    formForHostGroup("edit", hostname);
}
function deleteHostGroup(hostGroupName) {
    if (parseInt($("input[id='totalHostGroup']").val()) < 2) {
        alert("You Could not Delete this host group, because atleast one host group must be in NMS.");
    }
    else {
        HOSTGROUPNAME = hostGroupName
        $("div#DeleteHostGroupMsg").show();
        loadingHostGroup();
        $("input[id='command1']").attr("checked", "checked");
    }
}
function resetAddHostGroup() {
    $("label.error").hide();
    $("#hostGroupName").val("").focus();
    $("#alias").val("");
}
function cancelEditHostGroup() {
    $("#formDiv").slideUp(1000);
    $("#addhosttable").slideDown(1000);
    formForHostGroup("add", "");
}
function cancelAddHostGroup() {
    $("label.error").hide();
    $("#formDiv").slideUp(1000);
    $("#addhosttable").slideDown(1000);
}
function gridViewHostGroup() {
    $.ajax({
        type: "get",
        url: "grid_view_hostgroup.py",
        success: function (result) {
            $("#gridviewDiv").html(result);
        }
    });
}
function loadingHostGroup() {
    $("div.loading").show();
}
function loadingHideHostGroup(load) {
    $("div.loading").hide();
    if (load) {
        parent.side.location = 'side.py';
        gridViewHostGroup();
    }
}
function cancelDelete() {
    $("div#DeleteHostGroupMsg").hide();
    loadingHideHostGroup(false);
}
function okDelete() {
    loadingHostGroup();
    $("div#DeleteHostGroupMsg").hide();
    $.ajax({
        type: "get",
        url: "ajaxcall_delete_hostgroup.py?hostGroupName=" + HOSTGROUPNAME + "&command=" + $('input:radio[name=command]:checked').val(),
        success: function (result) {
            //alert(result)
            if ($.trim(result) == "0") {
                loadingHideHostGroup(false);
                alert("Host Group Name could not delete, Please try again later.");
            }
            else if ($.trim(result) == "1") {
                resetAddHostGroup();
                setTimeout("loadingHideHostGroup(true);", 3000);
                alert("Host Group Deleted Successfully.");
            }
            else {
                loadingHideHostGroup(false);
                alert("Some Error Occur" + result);
            }
        },
        error: function () {
            loadingHideHostGroup(false);
            alert("Some Error Occur");
        }
    });
}
