$(function () {
    // Loading - Spin Object
    var spinLoading = $("div#spin_loading");		// loading circle
    var spinMainLoading = $("div#main_loading");	// loading squire
    var loginBox = $("#login_box");
    var doc = $(document);
    var pageHeight = doc.height();
    var pageWidth = doc.width();
    var loginBoxHeight = loginBox.height();
    var loginBoxWidth = loginBox.width();
    var loginBoxPositionTop = String(((pageHeight / 2) -
        (loginBoxHeight / 2)) * 100 / pageHeight) + "%";
    var loginBoxPositionLeft = String(((pageWidth / 2) -
        (loginBoxWidth / 2)) * 100 / pageWidth) + "%";
    // spin loading object
    //loginBox.css({"top":loginBoxPositionTop,
    //              "left":loginBoxPositionLeft});
    $("input[name='username']").focus();
    $('body').addClass('login_body');
    $("#login_form").submit(function () {
        var formObj = $(this);
        if ($(this).valid()) {
            spinStart(spinLoading, spinMainLoading);
            $.ajax({
                type: formObj.attr("method"),
                url: formObj.attr("action"),
                data: formObj.serialize(),
                cache: false,
                success: function (result) {
                    try {
                        jsonResult = eval("(" + result + ")");
                        switch (+(jsonResult.success)) {
                            case 4:	// password expiry warning
                                $().toastmessage('showNoticeToast', jsonResult.result);
                                setTimeout(function () {
                                    spinStop(spinLoading, spinMainLoading);
                                    window.location.reload();
                                }, 3000);
                                break;
                            case 0:	// successful login!
                                spinStop(spinLoading, spinMainLoading);
                                window.location.reload();
                                break;
                            case 2: // user alteady login from some where else
                                spinStop(spinLoading, spinMainLoading);
                                $.prompt('This account is cuurenlty logged in from other location. You will be logged out from all other sessions. Do you want to continue?',
                                    {
                                        buttons: {Ok: true},
                                        prefix: 'jqismooth',
                                        callback: sessionUser
                                    }
                                );
                                break;
                            case 1:	// username or(/and) password invalid
                            case 3: // entered old-password
                            case 5: // acount lock due to `MaxLoginAttempts`
                            default:
                                spinStop(spinLoading, spinMainLoading);
                                $().toastmessage('showErrorToast', jsonResult.result);
                        }
                    }
                    catch (error) {
                        spinStop(spinLoading, spinMainLoading);
                        $().toastmessage('showErrorToast', "Please Enter Username and Password.");
                        //$().toastmessage('showErrorToast', "Please Enter Valid Username and Password-JS-Bug" + error.message + error.number);
                    }
                }
            });
        }
        else {
            $().toastmessage('showErrorToast', "Please Enter Username and Password.");
        }
        return false;
    });
    $("#login_form").validate({
        rules: {
            username: {
                required: true
            },
            password: {
                required: true
            }
        },
        messages: {
            username: {
                required: " "
            },
            password: {
                required: " "
            }
        }//,	window.location.reload()
        //errorElement:"div"
    });
    // add tool tip
    /*$("#login_form input[type='text'],input[type='password']").tooltip({
     // place tooltip on the right edge
     position: "center right",
     // a little tweaking of the position
     offset: [-2, 10],
     // use the built-in fadeIn/fadeOut effect
     effect: "fade",
     // custom opacity setting
     opacity: 0.7
     });*/
    setTimeout(function () {
        if (tactical_call != null) {
            clearTimeout(tactical_call);
        }
    }, 25000);
});

function sessionUser(v, m) {

    $().toastmessage('showSuccessToast', "Successfully logged in!!");
    //$("#login_form").submit();
    window.location.reload();

}
