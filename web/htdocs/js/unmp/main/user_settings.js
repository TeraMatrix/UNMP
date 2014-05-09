/*
 * 
 * Author			:	Mahipal Choudhary

 * Version			:	0.1
 * Modify Date			:	12-September-2011
 * Purpose			:	Define All Required Javascript Functions
 * Require Library		:	jquery 1.4 or higher version and jquery.validate
 * Browser			:	Mozila FireFox [3.x or higher] and Chrome [all versions]
 * 
 * Copyright (c) 2011 Codescape Consultant Private Limited
 * 
 */

$(document).ready(function () {
    $("div.yo-tabs").yoTabs();

    // spin loading object [write this code on each page]
    var spinLoading = $("div#spin_loading");		// create object that hold loading circle
    var spinMainLoading = $("div#main_loading");	// create object that hold loading squire
    $("#edit_user_form").show();
    $("#edit_password_form").hide();

    //var page_tip_href;
    $("a#personal_information_tab").click(function (e) {
        e.preventDefault();
        currentTab = "active";
        $("#edit_user_form").show();
        $("#edit_password_form").hide();
        //page_tip_href = "help_change_user_setting.py";
    });

    /* Disable Host Tab*/
    $("a#change_password_tab").click(function (e) {
        e.preventDefault();
        currentTab = "active";
        $("#edit_user_form").hide();
        $("#edit_password_form").show();
        //page_tip_href = "help_change_password.py";
    });

    $("div#grid_view_div").find('.active').click();

    if (($("div#is_first_login").length != 0)) {
        $().toastmessage('showNoticeToast', "You have logged in for first time, kindly change your password!");
        //page_tip_href = "help_change_password.py";
    }
    if (($("div#is_password_expired").length != 0)) {
        $().toastmessage('showNoticeToast', "Your password has been expired, kindly change your password!");
        //page_tip_href = "help_change_password.py";
    }

    $("#edit_user_form").validate({
        rules: {
            first_name: {
                alpha: true,
                maxlength: 25
            },
            last_name: {
                maxlength: 25,
                alpha: true
            },
            mobile: {
                minlength: 10,
                maxlength: 10,
                positiveNumber: true
            },
            email_id: {
                email: true
            }

        },

        messages: {

        }
    });


    // Edit start Title: "User Management Password Complexity"
    // Redmine Issue: Features
    // 687: "User Management Password Complexity"
    // Added code to implement: Password 2 num, 2 alpha, 2 special,
    // and min 8 characters
    // By: Grijesh Chauhan, Date: 8, Feb 2013


    $.validator.addMethod("passwd",
        function (value, element, regexp) {
            var re = new RegExp(/((?=(.*\d.*){2,})(?=(.*[a-zA-Z].*){2,})(?=(.*[\\\@\#\$\(\)\{\;\_\&\}\[\]\!\~\,\.\!\*\^\?\/\|\<\:\>\+\=\-\_\%\"\'].*){2,}).{8,20})/);
            return this.optional(element) || re.test(value);
        },
        "Invalid input"
    );

    $.validator.addMethod(
        "equalToOld",
        function (value, element) {
            var is_valid_passwd = false;
            $.ajax({
                type: 'GET',
                url: "check_password.py?&pwd=" + value,
                cache: false,
                async: false,
                success: function (result) {
                    if (result.success == 0) {
                        is_valid_passwd = true;
                    }
                    else {
                        is_valid_passwd = false;
                    }
                }
            });
            return is_valid_passwd;
        },
        ' Invalid Password'
    );


    jQuery.validator.addMethod("notEqualTo",
        function (value, element, param) {
            return this.optional(element) || value != $(param).val();
        },
        "Please specify a different (non-default) value"
    );

    $("#edit_password_form").validate({
        rules: {
            password: {
                required: true,
                passwd: ".*"
            },
            confirm_password_1: {
                required: true,
                minlength: 8,
                notEqualTo: "#password",
                passwd: ".*"
            },
            confirm_password_2: {
                required: true,
                minlength: 8,
                equalTo: "#confirm_password_1"
            }
        },
        messages: {
            password: {
                required: "*",
                minlength: "Your password must be at least 8 characters long. Please try",
                passwd: " Password should consist of 2 Numeric, 2 alpha, 2 special"
            },

            confirm_password_1: {
                required: "*",
                minlength: "Your password must be at least 8 characters long. Please try",
                notEqualTo: "New Password can't be same as Old password",
                passwd: " Password should consist of 2 Numeric, 2 alpha, 2 special"
            },
            confirm_password_2: {
                required: "*",
                minlength: "Your password must be at least 8 characters long. Please try",
                equalTo: " Passwords doesn't match"
            }

        }
    });
    // Edit end


    $("#edit_user_form").submit(function () {
        if ($(this).valid()) {

            var form = $(this);
            var method = form.attr("method");
            var action = form.attr("action");
            var data = form.serialize();
            //alert(data);
            $.ajax({
                type: method,
                url: action,
                data: data,
                cache: false,
                success: function (result) {
                    if (result == 0) {
                        $().toastmessage('showSuccessToast', "User Details Saved Successfully.");
                        //$("#close_edit_user").click();

                    }
                    else if (result.success == 1) {
                        $().toastmessage('showErrorToast', String(result));

                    }
                }
            });
        }
        else {
            $().toastmessage('showErrorToast', "Some Fileds are Missing or Incorrect.");
        }
        return false;
    });


    $("#edit_password_form").submit(function () {
        if ($(this).valid()) {

            var form = $(this);
            var method = form.attr("method");
            var action = form.attr("action");
            var data = form.serialize();
            //alert(data);
            $.ajax({
                type: method,
                url: action,
                data: data,
                cache: false,
                success: function (result) {
                    if (result.success == 0) {
                        $().toastmessage('showSuccessToast', "Password Saved Successfully.");
                        //$("#close_edit_password").click();
                        form[0].reset();
                    }
                    else if (result.success == 1) {

                        $().toastmessage('showErrorToast', result.msg);
                    }
                }
            });
        }
        else {
            $().toastmessage('showErrorToast', "Some Fileds are Missing or Incorrect.");
        }
        return false;
    });

    $("#close_edit_user").click(function () {
        window.history.go(-1);
    });


    /* Removed due to Redmine Issue #1065: UNMP CRASH ON LOGIN for new user
     // Removing this function Causes to an non-uniform behaviour of cancel
     // button in UNMP system

     $("#close_edit_password").click(function(){
     window.history.go(-1);
     });
     */


    // add tool tip
    $tooltipEditPassword = $("form#edit_password_form input[type='password']").tooltip({
        // place tooltip on the right edge
        position: "center right",
        // a little tweaking of the position
        offset: [-2, 10],
        // use the built-in fadeIn/fadeOut effect
        effect: "fade",
        // custom opacity setting
        opacity: 0.7
    });
    // add tool tip
    $tooltipEditUserDetails = $("form#edit_user_form input[type='text'],form#edit_user_form textarea").tooltip({
        // place tooltip on the right edge
        position: "center right",
        // a little tweaking of the position
        offset: [-2, 10],
        // use the built-in fadeIn/fadeOut effect
        effect: "fade",
        // custom opacity setting
        opacity: 0.7
    });

//	$("#page_tip").colorbox(
//	{
//        href: page_tip_href,
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"600px",
//		height:"500px"
//	});
});

