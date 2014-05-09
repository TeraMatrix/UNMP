var $spinLoading = null;
var $spinMainLoading = null;
// Data Table Object
var oTable = null;

// Default Selected Link
var defaultSelectedLink = null;

// selected row
var aSelected = [];

var $tooltip = null;

function userDataTable() {
    aSelected = [];
    $.ajax({
        type: "get",
        url: "user_detail_table.py",
        cache: false,
        success: function (result) {
            oTable = $('#user_table').dataTable({
                "bDestroy": true,
                "bJQueryUI": true,
                "bProcessing": true,
                "sPaginationType": "full_numbers",
                "bStateSave": true,
                "aaData": eval(result),
                "fnRowCallback": function (nRow, aData, iDisplayIndex) {
                    if (jQuery.inArray(aData.DT_RowId, aSelected) !== -1) {
                        $(nRow).addClass('row_selected');
                    }
                    return nRow;
                },
                "aoColumns": [
                    { "bSearchable": false, "bVisible": false, "aTargets": [ 0 ] },
                    { "sTitle": "User Name", "sClass": "center", "sWidth": "12%" },
                    { "sTitle": "Usergroup", "sClass": "center", "sWidth": "10%"},
                    { "sTitle": "First Name", "sClass": "center", "sWidth": "12%"},
                    { "sTitle": "Last Name", "sClass": "center", "sWidth": "12%" },
                    { "sTitle": "Designation", "sClass": "center", "sWidth": "12%" },
                    { "sTitle": "Mobile No", "sClass": "center", "sWidth": "12%"  },
                    { "sTitle": "E-Mail ID", "sClass": "center", "sWidth": "20%"  }
                ]
            });
            oTable.fnDraw();

        }
    });
}

function fnGetSelected(oTableLocal) {
    var aReturn = new Array();
    var aTrs = oTableLocal.fnGetNodes();
    for (var i = 0; i < aTrs.length; i++) {
        if ($(aTrs[i]).hasClass('row_selected')) {
            aReturn.push(aTrs[i]);
        }
    }
    return aReturn;
}

$(document).ready(function () {

    // spin loading object
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire

    /* Click event handler */
    $('#user_table tbody tr').live('click', function () {
        var id = this.id;
        var index = jQuery.inArray(id, aSelected);

        if (index === -1) {
            aSelected.push(id);
        } else {
            aSelected.splice(index, 1);
        }

        $(this).toggleClass('row_selected');
    });
    userDataTable();


    $("#close_add_user").click(function () {
        $("label#check_result").html(" ");
        if ($tooltip)
            $tooltip.tooltip().hide();
        $("div#user_form").hide();
        $("div#edit_usr_form").hide();
        $("div#user_datatable").show();
        $("img#edit_user").show();
        $("img#del_user").show();
        $("img#add_user").show();

    });
    // add tool tip
    $tooltip = $("#add_user_form input[type='text'], \
				 			   #add_user_form input[type='password'], \
				 			   #add_user_form textarea, \
				 			   #add_user_form select"
    ).tooltip({
            // place tooltip on the right edge
            position: "center right",
            // a little tweaking of the position
            offset: [-2, 10],
            // use the built-in fadeIn/fadeOut effect
            effect: "fade",
            // custom opacity setting
            opacity: 0.7
        });

    // Edit start Title: "User Management Password Complexity"
    // Redmine Issue: Features
    // 687: "User Management Password Complexity"
    // Added code to implement: Password 2 num, 2 alpha, 2 special,
    // and min 8 characters
    // By: Grijesh Chauhan, Date: 6, Feb 2013

    $.validator.addMethod(
        "passwd",
        function (value, element, regexp) {
            var re = new RegExp(/((?=(.*\d.*){2,})(?=(.*[a-zA-Z].*){2,})(?=(.*[\\\@\#\$\(\)\{\;\_\&\}\[\]\!\~\,\.\!\*\^\?\/\|\<\:\>\+\=\-\_\%\"\'].*){2,}).{8,20})/);
            return this.optional(element) || re.test(value);
        },
        "Invalid input"
    );

    $("#add_user_form").validate({
        rules: {
            user_name: {
                required: true,
                minlength: 5,
                maxlength: 15,
                noSpace: true
            },
            password: {
                required: true,
                minlength: 8,
                passwd: ".*"
            },
            cpassword: {
                required: true,
                minlength: 8,
                equalTo: "#password"

            },
            groups: "required",

            first_name: {
            		required: true,
                minlength: 1,
                alpha: true,
                maxlength: 25
            },
            last_name: {
                minlength: 1,
                maxlength: 25,
                alpha: true
            },
            mobile: {
                minlength: 10,
                maxlength: 10,
                positiveNumber: true
            },
            email_id: {
            		required: true,
                email: true
            }

        },
        messages: {
            user_name: {
                required: "*",
                minlength: " at least 5 characters",
                maxlenght: " only 15 characters",
                noSpace: " No space Please"
            },

            password: {
                required: "*",
                minlength: "Your password must be at least 8 characters long. Please try",
                passwd: " Password should consist of 2 Numeric, 2 alpha, 2 special"
            },

            cpassword: {
                required: "*",
                minlength: "Your password must be at least 8 characters long. Please try",
                equalTo: " Passwords doesn't match"
            },

						first_name: {
							required: "*"
						},

            groups: {
                required: "*"
            },

            mobile: {
                minlength: "Please enter no more than 10 numbers",
                maxlength: "Please enter no more than 10 numbers"
            },
            
            email_id: {
            		required: "*",
                email: "Please enter a valid email address"
            }
        }
    });


    $("#add_user_form").submit(function () {
        if ($(this).valid()) {
            spinStart($spinLoading, $spinMainLoading);
            var form = $(this);
            var method = form.attr("method");
            var action = form.attr("action");
            var group_name = form.find("select#groups option:selected").text();
            var data = form.serialize();
            //alert(data);
            $.ajax({
                type: method,
                url: action,
                data: data + "&grp_name=" + group_name,
                cache: false,
                success: function (result) {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        $().toastmessage('showSuccessToast', "User Added Successfully.");
                        userDataTable();
                        $("#close_add_user").click();

                    }
                    else if (result.success == 1) {

                        $().toastmessage('showErrorToast', String(result["result"]));
                    }
                    else {
                        var dt = result.result;
                        for (key in dt) {
                            resultStr += key + ": " + dt[key] + "<br/>"
                        }
                        $().toastmessage('showErrorToast', "Please Fill in all the required fields");
                    }

                    spinStop($spinLoading, $spinMainLoading);
                }
            });
        }
        else {
            $().toastmessage('showErrorToast', "Please Fill in all the required fields");
        }
        return false;
    });
//
//	$("#page_tip").colorbox(
//	{
//		href:"help_users_main.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"600px",
//		height:"400px"
//	});
	
});

/*
 * I don't actually use this here, but it is provided as it might be useful and demonstrates
 * getting the TR nodes from DataTables
 */


function name_chk() {
    if ($("form").attr('id') == "add_user_form") {
        val_ = $("input#user_name").val();
        type_ = "get";
        func_type = "user";
    }
    else if ($("form").attr('id') == "add_group_form") {
        val = $("input#group_name");
        type_ = "get";
        func_type = 0;
    }
    if (val_.length > 4) {
        $.ajax({
            type: type_,
            url: "check_name.py?&name=" + val_ + "&type=" + func_type,
            cache: false,
            success: function (result) {
                result = eval("(" + result + ")");

                if (result.success == 0) {
                    $("input[name='user_name']").removeClass("error").addClass("valid");
                    $("label#check_result").css("color", "green");
                    $("label#check_result").html("Name is available ");
                }
                else {
                    $("input[name='user_name']").removeClass("valid").addClass("error");
                    $("label#check_result").css("color", "red");
                    $("label#check_result").html("  Username already exists");
                }

            }
        });
    }
    else {
        $("label#check_result").html("");
    }
}

//function calls from user-edit page to Lock/Unlock a UNMP user
function lock_unlock(){
	statusButton = $("#statusButton");
	statusVal = statusButton.val();
	user_id = $('#user_id').val();
	type_ = "get";
	button = this;
	if(!button.clicked){
		button.clicked = true;
		$.ajax({
			type: type_,
			url: "lock_unlock_usr.py?&status=" + statusVal + '&user_id=' + user_id,
			cache: false,
			success: function(result){
				try{
					jsonResult = eval("(" + result + ")");
					if(jsonResult.success == 0){
						//for managing the Lock / Unlock of the User by Admin
						if (statusVal === "Lock"){
							statusButton.attr("value", "Unlock");
							statusButton.css({"background-color": "green"});
							$().toastmessage('showSuccessToast', jsonResult.result);
						}
						else{
							statusButton.attr("value", "Lock");
							statusButton.css({"background-color": "red"});
							$().toastmessage('showSuccessToast', jsonResult.result);
						}
					}
					else{
						$().toastmessage('showErrorToast', jsonResult.result);
					}
				}
				catch(error){
					$().toastmessage('showErrorToast', "User could not Lock/Unlock, try again!");
				}
			},
			complete: function() {
      	button.clicked = false;
      }
		});						
	}
}

function addUser() {
    $("div#user_datatable").hide();
    $("div#edit_usr_form").hide();
    $("div#user_form").show();
    $("img#edit_user").hide();
    $("img#add_user").hide();
    $("img#del_user").hide();
}

function editUser() {
    var selectedRow = fnGetSelected(oTable);
    var rLength = selectedRow.length;
    if (rLength == 0) {
        $.prompt("Please Select Atleast one user", {prefix: 'jqismooth'});
    }
    else if (rLength == 1) {
        spinStart($spinLoading, $spinMainLoading);
        var iRow = oTable.fnGetPosition(selectedRow[0]);
        var aData = oTable.fnGetData(iRow);
        var id = aData[0];
        var usr = aData[1];

        $.ajax({
            type: "get",
            url: "edit_user_view.py?&user_id=" + id + "&user_name=" + usr,
            cache: false,
            success: function (result) {
                if (result.indexOf("NOUSERAVAILABLEWITHTHISID") >= 0) {
                    $().toastmessage('showErrorToast', 'No such User found');
                    userDataTable();

                }
                else if (result.indexOf("SUPERADMINCANNOTEDIT") >= 0) {
                    $().toastmessage('showWarningToast', ' Editing SuperAdmin type user is not allowed ');
                    userDataTable();
                }
                else if (result.indexOf("SOMEERROROCCURMAYBEDBERROR") >= 0) {
                    $().toastmessage('showErrorToast', ' UNMP server has encounterd an error./n Please REFRESH your page & try again/n Still having problem contact please support team');
                    userDataTable();
                }
                else if (result.indexOf("CANNOTEDITYOURSELF") >= 0) {
                    $().toastmessage('showWarningToast', ' Self updation is restricted ');
                    userDataTable();
                }
                else {
                    $("div#edit_usr_form").html(result);
                    $("div#user_datatable").hide();
                    $("div#user_form").hide();
                    $("div#edit_usr_form").show();
                    $("img#edit_user").hide();
                    $("img#del_user").hide();
                    $("img#add_user").hide();

                    $("#close_edit_user").click(function () {
                        //if($tooltip)
                        //	$tooltip.tooltip().hide();
                        $("div#user_form").hide();
                        $("div#edit_usr_form").hide();
                        $("div#user_datatable").show();
                        $("img#edit_user").show();
                        $("img#del_user").show();
                        $("img#add_user").show();
              
                    });

                    $tooltip = $("#edit_usr_form input[type='text'],#edit_usr_form  textarea,#edit_usr_form  select,#edit_usr_form input[type='password']").tooltip({
                        // place tooltip on the right edge
                        position: "center right",
                        // a little tweaking of the position
                        offset: [-2, 10],
                        // use the built-in fadeIn/fadeOut effect
                        effect: "fade",
                        // custom opacity setting
                        opacity: 0.7
                    });

					
                    $("#edit_user_form").validate({
                        rules: {
                            groups: "required",
                            first_name: {
                            		required: true,
                                minlength: 1,
                                maxlength: 25,
                                alpha: true
                            },
                            last_name: {
                                minlength: 1,
                                maxlength: 25,
                                alpha: true
                            },
                            mobile: {
                                minlength: 10,
                                maxlength: 10,
                                positiveNumber: true
                            },
                            email_id: {
                            		required: true,
                                email: true
                            },
                            new_password: {
                                minlength: 8,
                                passwd: ".*"
                            },
                            cpassword: {
                                minlength: 8,
                                equalTo: "#new_password"
                            }
                        },
                        messages: {
                            groups: "*",
                            new_password: {
                                minlength: " Password must be at least 8 characters long",
                                passwd: " Password should consist of 2 Numeric, 2 alpha, 2 special"
                            },
                            cpassword: {
                                minlength: " Password must be at least 8 characters long",
                                equalTo: " Passwords doesn't match"
                            },
                            first_name: {
                            		required: "*"
                            },
                            email_id: {
                            		required: "*"
                            }                            
                        }
                    });

                    // End edit, Date: `6, Fed 2013`

                    $("#edit_user_form").submit(function () {
                        if ($(this).valid()) {
                            spinStart($spinLoading, $spinMainLoading);
                            var form = $(this);
                            var group_name = form.find("select#groups option:selected").text();
                            var method = form.attr("method");
                            var action = form.attr("action");
                            var data = form.serialize();
//							alert(group_name);
                            $.ajax({
                                type: method,
                                url: action,
                                data: data + "&grp_name=" + group_name,
                                cache: false,
                                success: function (result) {
                                    //alert(result);
                                    result = eval("(" + result + ")");
                                    if (result.success == 0) {
                                        $().toastmessage('showSuccessToast', "User Updated Successfully.");
                                        userDataTable();
                                        $("#close_edit_user").click();
                                    }
                                    else if (result.success == 1) {

                                        $().toastmessage('showErrorToast', String(result["result"]));
                                    }
                                    else {
                                        var dt = result.result;
                                        for (key in dt) {
                                            resultStr += key + ": " + dt[key] + "<br/>"
                                        }
                                        $().toastmessage('showErrorToast', "Please Fill in all the required fields");
                                    }
                                    spinStop($spinLoading, $spinMainLoading);
                                }
                            });
                            return false;
                        }
                        else {
                            $().toastmessage('showErrorToast', "Please Fill in all the required fields");
                        }

                    });

                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
        return false;
        //$.prompt(String(id),{prefix:'jqismooth'});
        //$().toastmessage('showWarningToast', "Edit User Module in progress .");
    }
    else {
        $.prompt("Please Select Only Single user", {prefix: 'jqismooth'});
    }
}

function deleteUserCallback(v, m) {
    if (v != undefined && v == true) {

        spinStart($spinLoading, $spinMainLoading);
        var selectedRow = fnGetSelected(oTable);
        var rLength = selectedRow.length;
        var idStr = "";
        var usrStr = "";
        var selectedDeletedRowArray = [];
        for (var i = 0; i < selectedRow.length; i++) {
            var iRow = oTable.fnGetPosition(selectedRow[i]);
            var aData = oTable.fnGetData(iRow);
            if (i > 0) {
                idStr += ",";
                usrStr += ",";
            }
            idStr += String(aData[0]);
            usrStr += String(aData[1]);
            selectedDeletedRowArray.push(iRow);
            // if delete successfully then call this function

        }
        var action = "del_user.py";
        var data = "user_ids=" + idStr + "&user_names=" + usrStr;
        var method = "get";
        $.ajax({
            url: action,
            type: method,
            data: data,
            cache: false,
            success: function (result) {
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    for (var j = 0; j < selectedDeletedRowArray.length; j++)
                        oTable.fnDeleteRow(selectedDeletedRowArray[j]);
                    //alert("Deleted Successfully");
                    $().toastmessage('showSuccessToast', "User(s) Deleted Successfully.");
                    userDataTable();
                }
                else {
                    $().toastmessage('showWarningToast', result.result);
                    userDataTable();
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
        return false;

    }

}

function delUser() {
    var selectedRow = fnGetSelected(oTable);
    var rLength = selectedRow.length;
    if (rLength == 0) {
        $.prompt("Select Atleast one user", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to delete this user?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: deleteUserCallback });
    }
}
