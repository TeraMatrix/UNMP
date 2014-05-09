$(function () {
    jQuery.validator.addMethod("noSpace", function (value, element) {
        return value.indexOf(" ") < 0 && value != "";
    }, "No space please and don't leave it empty");
    formValidation("userForm");
    formFunction("userForm");
});
function formValidation(formId) {
    $("#" + formId).validate({
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
            }
        },
        messages: {
            userName: {
                required: "*",
                noSpace: " Space not allow"
            },
            password: {
                required: "*",
                minlength: " Your password must be at least 8 characters long: ChangedPwd"
            },
            cpassword: {
                required: "*",
                inlength: " Your password must be at least 8 characters long: ChangedPwd",
                equalTo: " Please enter the same password as above"
            }
        }
    });
}
function formFunction(formId) {
    $("#" + formId).submit(function () {
        formAction = $(this).attr("action") + "?" + $(this).serialize();
        if ($(this).valid()) {
            loadingUserForm();
            $.ajax({
                type: "post",
                url: formAction,
                success: function (result) {
                    if ($.trim(result) == "1") {
                        alert("Password Changed Successfully.");
                        loadingHideUserForm(true);
                    }
                    else {
                        alert("Due to some error you could not change your password, contact your administrator.");
                        loadingHideUserForm(false);
                    }
                }
            });
        }
        return false;
    });
}
function loadingUserForm() {
    $("div.loading").show();
}
function loadingHideUserForm(load) {
    $("div.loading").hide();
    if (load) {
        $("input[type='password']").val("");
    }
}
