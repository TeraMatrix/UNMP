$(function () {
    userGridView();
    formForUser("add", "");
    jQuery.validator.addMethod("noSpace", function (value, element) {
        return value.indexOf(" ") < 0 && value != "";
    }, "No space please and don't leave it empty");

})
function userGridView() {
    $.ajax({
        type: "get",
        url: "user_grid_view.py",
        success: function (result) {
            $("div#userListDiv").html(result);
        }
    });
}
function formForUser(action, userName) {
    $.ajax({
        type: "get",
        url: "form_for_user.py?action=" + action + "&user=" + userName,
        success: function (result) {
            $("div#formDiv").html(result);
            if (action == "edit") {
                actionForUserForm("edit");
            }
            else {
                actionForUserForm("add");
            }
        }
    });
}
function actionForUserForm(act) {
    action = act
    validateUserForm("userForm", action);
    $("#userForm").submit(function () {
        formAction = $(this).attr("action") + "?" + $(this).serialize();
        if ($("#userForm").valid()) {
            loadingUserForm();
            $.ajax({
                type: "post",
                url: formAction,
                success: function (result) {
                    //alert(result)
                    if ($.trim(result) == "0") {
                        loadingHideUserForm(false);
                        alert("User Name already exist.");
                    }
                    else if ($.trim(result) == "1") {
                        if (action == "edit") {
                            alert("User Updated Successfully.");
                            cancelEditUser();
                        }
                        else {
                            alert("User Added Successfully.");
                            resetAddUser();
                        }
                        loadingHideUserForm(true);
                    }
                    else if ($.trim(result) == "2") {
                        loadingHideUserForm(false);
                        alert("You can not Edit your own User ID and role");
                    }
                    else {
                        loadingHideUserForm(false);
                        alert("Please fill require fields.");
                    }
                },
                error: function () {
                    loadingHideUserForm(false);
                    alert("Some Error Occur");
                }
            });
        }
        return false;
    });
}
function validateUserForm(formid, action) {
    if (action == "edit") {
        $("#" + formid).validate({
            rules: {
                userName: {
                    required: true,
                    noSpace: true
                },
                userRole: "required",
                password: {
                    minlength: 8
                },
                cpassword: {
                    minlength: 8,
                    equalTo: "#password"
                }//,
            },
            messages: {
                userName: {
                    required: "*",
                    noSpace: " Space not allow"
                },
                userRole: "*",
                password: {
                    minlength: " Your password must be at least 8 characters long"
                },
                cpassword: {
                    minlength: " Your password must be at least 8 characters long",
                    equalTo: " Please enter the same password as above"
                }//,
            }
        });
    }
    else {
        $("#" + formid).validate({
            rules: {
                userName: {
                    required: true,
                    noSpace: true
                },
                password: {
                    required: true,
                    minlength: 8
                },
                cpassword: {
                    required: true,
                    minlength: 8,
                    equalTo: "#password"
                },
                userRole: "required"
            },
            messages: {
                userName: {
                    required: "*",
                    noSpace: " Space not allow"
                },
                password: {
                    required: "*",
                    minlength: " Your password must be at least 8 characters long"
                },
                cpassword: {
                    required: "*",
                    minilength: " Your password must be at least 8 characters long",
                    equalTo: " Please enter the same password as above"
                },
                userRole: "*"
            }
        });
    }
}
function addUser() {
    $("div#addUserDivButton").fadeOut(1000);
    $("div#formDiv").slideDown(1000, function () {
        $("input[name='userName']").focus();
    });
}
function editUser(userName) {
    $("div#addUserDivButton").fadeOut(1000);
    formForUser("edit", userName);
    $("div#formDiv").slideDown(1000, function () {
        $("input[name='password']").focus();
    });
}
function deleteUser(userName) {
    if (confirm("Are you sure you want to delete this user?")) {
        loadingUserForm();
        $.ajax({
            type: "get",
            url: "delete_user.py?userName=" + userName,
            success: function (result) {
                //alert(result)
                if ($.trim(result) == "0") {
                    loadingHideUserForm(false);
                    alert("User could not delete, Please try again later.");
                }
                else if ($.trim(result) == "1") {
                    alert("Host Deleted Successfully.");
                    cancelEditUser();
                    loadingHideUserForm(true);
                }
                else if ($.trim(result) == "2") {
                    loadingHideUserForm(false);
                    alert("You can not delete your own User ID");
                }
                else if ($.trim(result) == "3") {
                    loadingHideUserForm(false);
                    alert("User Does not Exist.");
                }
                else {
                    loadingHideUserForm(false);
                    alert("Some Error Occur");
                }
            },
            error: function () {
                loadingHideUserForm(false);
                alert("Some Error Occur");
            }
        });
    }
}
function cancelAddUser() {
    $("div#addUserDivButton").fadeIn(1000);
    $("div#formDiv").slideUp(1000);
}
function resetAddUser() {
    $("input[name='userName'], input[name='password'], input[name='cpassword'], select[name='userRole']").val("");
}
function cancelEditUser() {
    cancelAddUser();
    formForUser("add", "");
}
function loadingUserForm() {
    $("div.loading").show();
}
function loadingHideUserForm(load) {
    $("div.loading").hide();
    if (load) {
        userGridView();
    }
}
