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
var hostgroup_id_user = null;
$(document).ready(function () {
    $spinLoading = $("div#spin_loading");        // create object that hold loading circle
    $spinMainLoading = $("div#main_loading");    // create object that hold loading square
    get_log();

    $('#lhostgroup_table tbody tr').live('click', function () {
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
//		href:"view_page_tip_hostgroup.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"600px",
//		height:"400px"
//	    });
});


function log_data(tabledata) {
//	create data table object
    oTableLog = $('#hostgroup_table').dataTable({
        "bDestroy": true,
        "bJQueryUI": true,
        "bProcessing": true,
        "sPaginationType": "full_numbers",
        "bPaginate": true,
        "bStateSave": false,
        "aaData": tabledata,
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
        "aoColumns": [
            { "sTitle": "HOSTGROUP NAME", "sClass": "center", "sWidth": "15%" },
            { "sTitle": "USER GROUPS ASSIGNED TO THIS HOSTGROUP", "sClass": "center", "sWidth": "60%"},
            { "sTitle": "MANAGE", "sClass": "center", "sWidth": "25%" }
        ]
    });
    hgroup_info();
    //oTableAvg.fnDraw();
};

function get_log() {							// create table for logs
    var result2 = [];
    var $fromObj = $("#get_hostgroup_data");
    var url = $fromObj.attr("action");
    var method = $fromObj.attr("method");
    var data = $fromObj.serialize();
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


///////////////////////////////////////////


function user_data(user_tabledata) {
//	create data table object
    //alert("sdsds");
    oTableUser = $('#user_details_table').dataTable({
        "bDestroy": true,
        "bJQueryUI": true,
        "bProcessing": true,
        "sPaginationType": "full_numbers",
        "bPaginate": true,
        "bStateSave": false,
        "aaData": user_tabledata,
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
        "aoColumns": [
            { "sTitle": "SELECT", "sClass": "center", "sWidth": "5%" },
            { "sTitle": "GROUP NAME", "sClass": "center", "sWidth": "10%" },
            { "sTitle": "USERS IN THIS GROUP", "sClass": "center", "sWidth": "60%"},
            { "sTitle": "DETAILS", "sClass": "center", "sWidth": "10%"}
            //{ "sTitle": "MANAGE", "sClass": "center","sWidth": "25%" }
        ]
    });
//		hgroup_info();
    //oTableAvg.fnDraw();
};

function user_get_log() {							// create table for logs
    var result2 = [];
    var $fromObj = $("#get_user_data_hostgroup");
    var url = $fromObj.attr("action");
    var method = $fromObj.attr("method");
    var data = $fromObj.serialize();
    $.ajax({
        type: method,
        url: url,
        data: data + "&hostgroup_id=" + selectedHGroupId,
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
            user_data(result2);
        }

    });
}
function fnGetSelected(oTableUser) {
    var aReturn = new Array();
    var aTrs = oTableUser.fnGetNodes();
    for (var i = 0; i < aTrs.length; i++) {
        if ($(aTrs[i]).hasClass('row_selected')) {
            aReturn.push(aTrs[i]);
        }
    }
    return aReturn;
}


///////////////////////////////////////
var oTable = null;
// Data Table Object
// Default Selected Link :@attention: Working 4 jan
var defaultSelectedLink = null;

// selected row 
var aSelected = [];

var userArray = [];

var boxuserArray = [];

var grpArray = [];

var grpNameArray = [];

var selectedHGroupId = "";

var selectedHGName = "";

var boxHGroupId = "";

var boxGrpArray = [];

var boxGrpNameArray = [];

var grpData = [];

var grpDataInHg = [];

var move_box = null;

var $tooltip = null;
var $spinLoading = null;
var $spinMainLoading = null;

function hgroup_info() {
    $("button.yo-button", "#hostgroup_table").click(function () {

        spinStart($spinLoading, $spinMainLoading);
        selectedHGroupId = "";
        selectedHGName = "";
        var id = $(this).attr("id");
        selectedHGName = $(this).attr("name");
        selectedHGroupId = id;
        $.ajax({
            type: "get",
            url: "hostgroup_info.py?&hostgroup_id=" + id,
            cache: false,
            success: function (result) {
                $("div#mahipal").hide();
                $("div#rahul").show();
                $("div#hg_details").text(selectedHGName + " ");
                $("div#hostgroup_info").html(result);
                spinStop($spinLoading, $spinMainLoading);
                user_get_log();
            }
        });

        addHgToGrp();
        showGrpInHg();
        searchEventGpInHg();
    });
}


function searchEventGpInHg() {
    $("input#search_grp_hg").keyup(function () {

        grpSearchInHg($.trim($(this).val()));
    });
}


function showGrpInHg(searchGrpInHg) {
    spinStart($spinLoading, $spinMainLoading);
    searchGrpInHg = "";
    grpDataInHg = [];
    $.ajax({
        type: "get",
        url: "show_groups_user.py?hostgroup_id=" + selectedHGroupId,
        cache: false,
        success: function (result1) {
            //alert(result1);
            try {
                //grpDataInHg = eval(result1);
                grpDataInHg = eval("(" + result1 + ")");
            }
            catch (err) {
                grpDataInHg = [];
            }
            spinStop($spinLoading, $spinMainLoading);
            grpSearchInHg();
            //var searchGrpInHg = $.trim($("div#hg_ingrp_head").find("input#search_hg")).val());
        }
    });
}
function grpSearchInHg(searchGrpInHg) {
    if (!searchGrpInHg) {
        searchGrpInHg = "";
    }
    var $grpTable = $("<table width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" class=\"tt-table\" style=\"margin-bottom:0;\" />");
    var $grpTr = null;
    var j = 0;
    for (i in grpDataInHg) {
        if (String(grpDataInHg[i][0]).toLowerCase().indexOf(searchGrpInHg.toLowerCase()) >= 0) {
            if (j == 0) {
                var $grpTr = $("<tr/>");
            }
            if (j < 1) {
                var $grpTd = $("<td class=\"cell-info1\" />");
                var $grpInput = $("<div id='ck_box'><input type='checkbox' name='group_check' value=" + "'" + String(grpDataInHg[i][0]) + "'" + " />");
                $grpInput.appendTo($grpTd);
                $grpTd.append("<span style=\"line-height:1.8em;\">" + (String(grpDataInHg[i][0])) + "</span></div> ");
                $grpTd.append("<span id='td_user'>" + (String(grpDataInHg[i][1])) + "</span>");
                $grpTd.appendTo($grpTr);
                j = j + 1;

            }
            if (j == 1) {
                $grpTr.appendTo($grpTable);
                j = 0;
            }
        }

    } // end of outer for

    if (j != 0) {
        j = 2 - j;
        while (j != 0) {
            var $grpTd = $("<td class=\"cell-info1\" />");
            $grpTd.appendTo($grpTr);
            j = j - 1
        }
        $grpTr.appendTo($grpTable);
    }

    $("div#grp_in_hg").html($grpTable);
}
//================================================= Hostgroup in group ===============================================

function addHgToGrp() {
    $("#add_group_to_hg").colorbox(
        {
            href: "add_gpinhg_view.py",
            onComplete: function () {
                var selectAll = $("button#selectAll");
                showGrp();
                searchEvent();
                selectAll.click(function () {
                    $("input[class='box-grp-check']").attr('checked', 'checked');
                });
            },
            title: "Assign/Add Groups To Hostgroup",
            opacity: 0.4,
            maxWidth: "80%",
            width: "550px",
            height: "450px"
        });

}


function viewGroupDetails(gid) {
    $.colorbox(
        {
            href: "viewGroupDetails.py?group_id=" + gid,
            onComplete: function () {
            },
            title: "Details of Users Present in this Group",
            opacity: 0.4,
            maxWidth: "80%",
            width: "550px",
            height: "450px"
        });

}
function boxAddGrp() {
    boxGrpArray = [];
    boxGrpNameArray = [];
    $.each($("input[class='box-grp-check']:checked"), function (i, obj) {
        boxGrpArray.push($(obj).val());
        boxGrpNameArray.push($(obj).parent().text());
    });
    //alert(String(boxGrpArray))
    if (boxGrpArray.length == 0) {
        $.prompt("Select at least one Group(s)", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to Add group(s) to this Hostgroup?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: boxAddGrpCallback });
    }

}

function boxAddGrpCallback(v, m) {
    if (v != undefined && v == true) {
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "get",
            url: "add_group_tohostgroup.py?&hostgroup_id=" + selectedHGroupId + "&gp_ids=" + String(boxGrpArray) + "&grp_names=" + String(boxGrpNameArray) + "&hg_name=" + selectedHGName,
            cache: false,
            success: function (result) {
                result = eval("(" + result + ")");
                if (result.success == 0) {

                    $().toastmessage('showSuccessToast', "Groups Added Successfully.");
                    $("button[id='" + selectedHGroupId + "']").click();
                    showGrp();
                }
                else {
                    //alert(result.result);
                    $().toastmessage('showWarningToast', String(result.result));
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }
    else {
        $().toastmessage('showNoticeToast', "Remain Unchanged.");
    }
}

function searchEvent() {
    $("input#search_grp").keyup(function () {
        grpSearch($.trim($(this).val()));
    });
}


function showGrp(searchGrp) {
    spinStart($spinLoading, $spinMainLoading);
    searchGrp = "";
    grpData = [];
    $.ajax({
        type: "get",
        url: "show_groups.py?hostgroup_id=" + selectedHGroupId + "&all=0" + "&light_box=" + 1,
        cache: false,
        success: function (result1) {
            //alert(result1);
            try {
                grpData = eval(result1);
            }
            catch (err) {
                grpData = [];
            }
            grpSearch();
            spinStop($spinLoading, $spinMainLoading);
            //var searchGrp = $.trim($("div#hg_ingrp_head").find("input#search_hg")).val());
        }
    });
}
function grpSearch(searchGrp) {
    if (!searchGrp) {
        searchGrp = "";
    }
    var $grpTable = $("<table width=\"100%\" id=\"grp_table\" cellspacing=\"0\" cellpadding=\"0\" class=\"tt-table\" />");
    var $grpTr = null;
    var j = 0;

    for (i in grpData) {
        if (String(grpData[i][1]).indexOf(searchGrp) >= 0) {
            if (j == 0) {
                var $grpTr = $("<tr/>");
            }
            if (j < 3) {
                var $grpTd = $("<td class=\"cell-info1\" />");
                var $grpInput = $("<input type='checkbox' class='box-grp-check' name='group_check' value=" + "'" + String(grpData[i][0]) + "'" + " />");
                $grpInput.appendTo($grpTd);
                $grpTd.append("<span style=\"line-height:1.8em;\">" + (String(grpData[i][1])) + "</span>");
                $grpTd.appendTo($grpTr);
                j = j + 1;

            }
            if (j == 3) {
                $grpTr.appendTo($grpTable);
                j = 0;
            }
        }

    } // end of outer for

    if (j != 0) {
        j = 3 - j;
        while (j != 0) {
            var $grpTd = $("<td class=\"cell-info1\" />");
            $grpTd.appendTo($grpTr);
            j = j - 1
        }
        $grpTr.appendTo($grpTable);
    }

    $("div#groups_in_hg").html($grpTable);
}

function delGrpFrmHg() {
    grpArray = [];
    grpNameArray = [];
    $.each($("input[name='group_check']:checked"), function (i, obj) {
        grpArray.push($(obj).val());
        grpNameArray.push($(obj).parent().text());
    });

    if (grpArray.length == 0) {
        $.prompt("Select at least one Group", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to delete Group(s) from this Hostgroup?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: delGrpCallback });
    }
}

function delGrpCallback(v, m) {
    if (v != undefined && v == true) {
        spinStart($spinLoading, $spinMainLoading);
        var action = "del_group_fromhostgroup.py";
        var data = "gp_ids=" + String(grpArray) + "&hostgroup_id=" + String(selectedHGroupId) + "&grp_names=" + String(grpNameArray) + "&hg_name=" + selectedHGName;
        var method = "get";
        $.ajax({
            url: action,
            type: method,
            data: data,
            cache: false,
            success: function (result) {
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    $().toastmessage('showSuccessToast', "Hostgroup(s) Deleted Successfully.");
                    $("button[id='" + selectedHGroupId + "']").click();
                }
                else {
                    //alert(result.result);
                    $().toastmessage('showWarningToast', String(result.result));
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }
    else {
        $().toastmessage('showNoticeToast', "Remain Unchanged.");
    }

}

function moveGrpToHg() {
    grpArray = [];
    grpNameArray = [];
    $.each($("input[name='group_check']:checked"), function (i, obj) {
        grpArray.push($(obj).val());
        grpNameArray.push($(obj).parent().text());
    });
    if (grpArray.length == 0) {
        $.prompt("Select at least one Group", {prefix: 'jqismooth'});
    }
    else {
        boxHGroupId = "";
        var move_box = $.colorbox(
            {
                href: "move_gptohg_view.py?hg_id=" + selectedHGroupId,
                onComplete: function () {
                    $('select#groups').change(function () {
                        boxHGroupId = "";
                        var $this = $(this);
                        boxHGroupId = $this.val();
                    });

                },
                title: "Move User Group to Another Hostgroup",
                opacity: 0.4,
                maxWidth: "80%",
                width: "400px",
                height: "150px"
            });
    }

}


function boxMoveGrp() {
    if (boxHGroupId == "" || boxHGroupId == null) {
        $.prompt("Select at least one HostGroup", {prefix: 'jqismooth'});
    }
    else if (grpArray.length == 0) {
        $.prompt("Select at least one Group", {prefix: 'jqismooth'});
    }
    else {

        $.prompt('Are you sure, you want to Move Group(s) from this Hostgroup?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: boxMoveGrpCallback });
    }

}

function boxMoveGrpCallback(v, m) {
    if (v != undefined && v == true) {
        spinStart($spinLoading, $spinMainLoading);
        var hostgroup_name = "";
        hostgroup_name = $("div#selectGroupDiv").find("select#groups option:selected").text();
        //alert(boxHGroupId);
        $.ajax({
            type: "get",
            url: "move_group_tohostgroup.py?&hostgroup_id=" + boxHGroupId + "&gp_ids=" + String(grpArray) + "&old_hostgroup_id=" + selectedHGroupId + "&sel_hg=" + selectedHGName + "&grp_names=" + String(grpNameArray) + "&hg_name=" + hostgroup_name,
            cache: false,
            success: function (result) {
                result = eval("(" + result + ")");
                if (result.success == 0) {

                    $().toastmessage('showSuccessToast', "Group(s) Moved Successfully.");
                    boxHGroupId = "";
                    user_get_log();//$("button[id='" + selectedHGroupId + "']").click();
                    $("div#cboxClose").click();
                }
                else {
                    //alert(result.result);
                    $().toastmessage('showWarningToast', String(result.result));
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }
    else {
        $().toastmessage('showNoticeToast', "Remain Unchanged.");
    }
}
//================================================= END hostgroup in group ===============================================


//===================================================================================================

