/*
 *
 * Author			:	Mahipal Choudhary
 * Version			:	0.1
 * Modify Date			:	07-Dec-2011
 * Purpose			:	Define All Required Javascript Functions for report of log viewing
 * Require Library		:	jquery 1.4 or higher version and jquery.validate
 * Browser			:	Mozila FireFox [3.x or higher] and Chrome [all versions]
 *
 * Copyright (c) 2011 Codescape Consultant Private Limited
 *
 */

var aSelectedLog = [];				// initialize parameters for table
var oTableLogh = null;
var $spinLoading = null;
var $spinMainLoading = null;
var delUserName = null;

$(document).ready(function () {
    $spinLoading = $("div#spin_loading");        // create object that hold loading circle
    $spinMainLoading = $("div#main_loading");    // create object that hold loading square
    get_log();

    $('#login_user_table tbody tr').live('click', function () {
        var id = this.id;
        var index = jQuery.inArray(id, aSelectedLog);

        if (index === -1) {
            aSelectedLog.push(id);
        } else {
            aSelectedLog.splice(index, 1);
        }

        $(this).toggleClass('row_selected');
    });
//	$("#page_tip").colorbox(  			//page tip
//	    {
//		href:"view_page_tip_manage_login.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"600px",
//		height:"400px"
//	    });
});


function log_data(tabledata) {
//	create data table object
    oTableLog = $('#login_user_table').dataTable({
        "bDestroy": true,
        "bJQueryUI": true,
        "bProcessing": true,
        "sPaginationType": "full_numbers",
        "bPaginate": true,
        "bStateSave": false,
        "aaData": tabledata,
        "aLengthMenu": [
            [20, 40, 60, -1],
            [20, 40, 60, "All"]
        ],
        "bLengthChange": true,
        "iDisplayLength": 20,
        "sScrollY": String($("div#container_body").height() - 153),
        "aaSorting": [],
        "oLanguage": {
            "sInfo": "_START_ - _END_ of _TOTAL_",
            "sInfoEmpty": "0 - 0 of 0",
            "sInfoFiltered": "(of _MAX_)"
        },
        "fnRowCallback": function (nRow, aData, iDisplayIndex) {
            if (jQuery.inArray(aData.DT_RowId, aSelectedLog) !== -1) {
                $(nRow).addClass('row_selected');
            }
            return nRow;
        },
        "aoColumnDefs": [
            { "aTargets": [0], "sTitle": "User Id", "sClass": "center", "sWidth": "15%" },
            { "aTargets": [1], "sTitle": "User Name", "sClass": "center", "sWidth": "20%" },
            { "aTargets": [2], "sTitle": "Usergroup", "sClass": "center", "sWidth": "12%" },
            { "aTargets": [3], "sTitle": "Last Login", "sClass": "center", "sWidth": "15%"},
            { "aTargets": [4], "sTitle": "Is Logged in", "sClass": "center", "sWidth": "10%" },
            { "aTargets": [5], "sTitle": "Last Activity", "sClass": "center", "sWidth": "15%" },
            { "aTargets": [6], "sTitle": "Destroy Session", "sClass": "center", "sWidth": "15%" },
        ]
        // "aoColumns": [
        // 	{ "sTitle": "User Id","sClass": "center","sWidth": "15%" },
        // 	{ "sTitle": "User Name" , "sClass": "center","sWidth": "20%"},
        // 	{ "sTitle": "Usergroup" , "sClass": "center","sWidth": "12%"},
        // 	{ "sTitle": "Last Activity" , "sClass": "center","sWidth": "15%"},
        // 	{ "sTitle": "Last Login", "sClass": "center","sWidth": "15%" },
        // 	{ "sTitle": "Is Logged in", "sClass": "center","sWidth": "10%" },
        // 	{ "sTitle": "Destroy Session", "sClass": "center","sWidth": "15%" }
        // ]
    });
    //oTableAvg.fnDraw();
};

function get_log() {							// create table for logs
    var result2 = [];
    var url = "get_login_data.py";
    var method = "get";
    var data = {};
    $.ajax({
        type: method,
        url: url,
        data: data,
        cache: false,
        success: function (result) {
            try {
                result2 = eval("(" + result + ")");
                //result2=result.data;
                //last_execution_time=result.last_execution_time;
            }
            catch (err) {
                result2 = [];
                $().toastmessage('showErrorToast', err);
            }
            log_data(result2);
        }

    });
}
function fnGetSelected(oTableLog) {
    var aReturn = new Array();
    var aTrs = oTableLog.fnGetNodes();
    for (var i = 0; i < aTrs.length; i++) {
        if ($(aTrs[i]).hasClass('row_selected')) {
            aReturn.push(aTrs[i]);
        }
    }
    return aReturn;
}

function delUser(id) {
    delUserName = id;
    $.prompt('Are you sure, you want to end session of this user?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: deleteUserCallback });
    /*		$.ajax({
     type:"get",
     url:"delete_login_user.py?&user_id="+id,
     cache:false,
     success:function(result)
     {
     try
     {
     result2 = eval("(" + result + ")");
     $().toastmessage('showSuccessToast',"Session of User Destroyed successfully");
     $("#del_user_"+id).hide();
     }
     catch(err)
     {
     result2=[];
     $().toastmessage('showErrorToast', err);
     }
     }
     });*/
}


function deleteUserCallback(v, m) {
    if (v != undefined && v == true && delUserName) {
        $.ajax({
            type: "get",
            url: "delete_login_data.py?&user_id=" + delUserName,
            cache: false,
            success: function (result) {
                try {
                    //result2 = eval("(" + result + ")");
                    if (result == '0') {
                        $().toastmessage('showSuccessToast', "User Session Destroy Successfully");//"Session of User Destroyed successfully");
                        $("#del_user_" + delUserName).hide();
                        get_log();

                    }
                    else {
                        $().toastmessage('showErrorToast', "Some Error Occurred");
                    }
                }
                catch (err) {
                    $().toastmessage('showErrorToast', err);
                }
            }
        });
    }
    else {
        $().toastmessage('showNoticeToast', "Remain Unchanged.");
    }
}


