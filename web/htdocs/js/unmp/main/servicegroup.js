var SERVICEGROUPNAME = "";
$(document).ready(function () {
    $("#formDiv").hide();
    formForServiceGroup("add", "");
    $("#addservicetable").click(function () {
        $(this).slideUp(1000);
        $("#formDiv").slideDown(1000, function () {
            $("#serviceGroupName").focus();
        });
    })
    jQuery.validator.addMethod("noSpace", function (value, element) {
        return value.indexOf(" ") < 0 && value != "";
    }, "No space please and don't leave it empty");
});
function formForServiceGroup(action, serviceGroupName) {
    $.ajax({
        type: "get",
        url: "form_for_servicegroup.py?action=" + action + "&serviceGroupName=" + serviceGroupName,
        success: function (result) {
            $("#formDiv").html(result);
            if (action == "edit") {
                actionForServiceGroup("edit");
                $("#addservicetable").slideUp(1000);
                $("#formDiv").slideDown(1000, function () {
                    $("#serviceGroupName").focus();
                });
            }
            else {
                actionForServiceGroup("add");
            }
        }
    });
}
function actionForServiceGroup(act) {
    action = act
    validateServiceGroup("addServiceGroupForm");
    $("#addServiceGroupForm").submit(function () {
        formAction = $(this).attr("action") + "?" + $(this).serialize();
        if ($("#addServiceGroupForm").valid()) {
            loadingServiceGroup();
            $.ajax({
                type: "post",
                url: formAction,
                success: function (result) {
                    //alert(result)
                    if ($.trim(result) == "0") {
                        loadingHideServiceGroup(false);
                        alert("Service Group Name already exist.");
                    }
                    else if ($.trim(result) == "1") {
                        resetAddServiceGroup();
                        setTimeout("loadingHideServiceGroup(true);", 3000);
                        if (action == "edit") {
                            alert("Service Group Updated Successfully.");
                            $("#formDiv").slideUp(1000);
                            $("#addservicetable").slideDown(1000);
                            setTimeout("formForServiceGroup('add','');", 3000);
                        }
                        else {
                            alert("Service Group Added Successfully.");
                        }
                    }
                    else {
                        loadingHideServiceGroup(false);
                        alert("Service Group Name and Alias both are require fields.");
                    }
                },
                error: function () {
                    loadingHideServiceGroup(false);
                    alert("Some Error Occur");
                }
            });
        }
        return false;
    });
}
function validateServiceGroup(formid) {
    $("#" + formid).validate({
        rules: {
            serviceGroupName: {
                required: true,
                noSpace: true
            },
            alias: "required"
        },
        messages: {
            serviceGroupName: {
                required: " *",
                noSpace: " Space not allow"
            },
            alias: " *"
        }
    });
}
function editServiceGroup(servicename) {
    formForServiceGroup("edit", servicename);
}
function deleteServiceGroup(serviceGroupName) {
    if (parseInt($("input[id='totalServiceGroup']").val()) < 2) {
        alert("You Could not Delete this service group, because atleast one service group must be in NMS.");
    }
    else {
        SERVICEGROUPNAME = serviceGroupName
        $("div#DeleteServiceGroupMsg").show();
        loadingServiceGroup();
        $("input[id='command1']").attr("checked", "checked");
    }
}
function resetAddServiceGroup() {
    $("label.error").hide();
    $("#serviceGroupName").val("").focus();
    $("#alias").val("");
}
function cancelEditServiceGroup() {
    $("#formDiv").slideUp(1000);
    $("#addservicetable").slideDown(1000);
    formForServiceGroup("add", "");
}
function cancelAddServiceGroup() {
    $("label.error").hide();
    $("#formDiv").slideUp(1000);
    $("#addservicetable").slideDown(1000);
}
function gridViewServiceGroup() {
    $.ajax({
        type: "get",
        url: "grid_view_servicegroup.py",
        success: function (result) {
            $("#gridviewDiv").html(result);
        }
    });
}
function loadingServiceGroup() {
    $("div.loading").show();
}
function loadingHideServiceGroup(load) {
    $("div.loading").hide();
    if (load) {
        parent.side.location = 'side.py';
        gridViewServiceGroup();
    }
}
function cancelDelete() {
    $("div#DeleteServiceGroupMsg").hide();
    loadingHideServiceGroup(false);
}
function okDelete() {
    loadingServiceGroup();
    $("div#DeleteServiceGroupMsg").hide();
    $.ajax({
        type: "get",
        url: "ajaxcall_delete_servicegroup.py?serviceGroupName=" + SERVICEGROUPNAME + "&command=" + $('input:radio[name=command]:checked').val(),
        success: function (result) {
            //alert(result)
            if ($.trim(result) == "0") {
                loadingHideServiceGroup(false);
                alert("Service Group Name could not delete, Please try again later.");
            }
            else if ($.trim(result) == "1") {
                resetAddServiceGroup();
                setTimeout("loadingHideServiceGroup(true);", 3000);
                alert("Service Group Deleted Successfully.");
            }
            else {
                loadingHideServiceGroup(false);
                alert("Some Error Occur" + result);
            }
        },
        error: function () {
            loadingHideServiceGroup(false);
            alert("Some Error Occur");
        }
    });
}
