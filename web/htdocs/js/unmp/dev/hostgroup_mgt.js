var oTable = null;
// Data Table Object
// Default Selected Link
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

function hgroupDataTable(obj) {
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "hostgroup_table.py",
        cache: false,
        success: function (result) {
            $("div#hostgroup_name_div").html(result);
            hgroup_info();
            if (!obj) {
                obj = $("p.hg-name").eq(0);
            }
            spinStop($spinLoading, $spinMainLoading);
            obj.click();
        }
    });
}

function hgroup_info() {
    $("p.hg-name").click(function () {
        spinStart($spinLoading, $spinMainLoading);
        selectedHGroupId = "";
        selectedHGName = "";
        var id = $(this).attr("id");
        selectedHGName = $(this).text();
        selectedHGroupId = id;
        $("p.hg-name").css({"background-color": "", "height": "18px", "border-bottom": "1px solid #DDD", "border-top": "1px solid #DDD", "border-right": "2px solid #DDD", "cursor": "pointer"});
        $(this).css({"background-color": "#ccc", "height": "20px", "border-bottom": "2px solid #AAA", "border-top": "2px solid #AAA", "border-right": "2px solid #AAA"});
        $.ajax({
            type: "get",
            url: "hostgroup_info.py?&hostgroup_id=" + id,
            cache: false,
            success: function (result) {
                $("div#hostgroup_info").html(result);
                spinStop($spinLoading, $spinMainLoading);
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
        url: "show_groups.py?hostgroup_id=" + selectedHGroupId,
        cache: false,
        success: function (result1) {
            //alert(result1);
            try {
                grpDataInHg = eval(result1);
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
        if (String(grpDataInHg[i][1]).toLowerCase().indexOf(searchGrpInHg.toLowerCase()) >= 0) {
            if (j == 0) {
                var $grpTr = $("<tr/>");
            }
            if (j < 3) {
                var $grpTd = $("<td class=\"cell-info1\" />");
                var $grpInput = $("<input type='checkbox' name='group_check' value=" + "'" + String(grpDataInHg[i][0]) + "'" + " />");
                $grpInput.appendTo($grpTd);
                $grpTd.append("<span style=\"line-height:1.8em;\">" + (String(grpDataInHg[i][1])) + "</span>");
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
        $.prompt('Are you sure, you want to Add group(s)?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: boxAddGrpCallback });
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
                    $("p[id='" + selectedHGroupId + "']").click();
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
    var $grpTable = $("<table width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" class=\"tt-table\" />");
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
        $.prompt('Are you sure, you want to delete Group(s)?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: delGrpCallback });
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
                    $("p[id='" + selectedHGroupId + "']").click();
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
                title: "Move Hostgroup To Group",
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

        $.prompt('Are you sure, you want to Move Group(s)?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: boxMoveGrpCallback });
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
                    $("p[id='" + selectedHGroupId + "']").click();
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
$(document).ready(function () {


    // spin loading object
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire

    hgroupDataTable();

//	$("#page_tip").colorbox(
//	    {
//		href:"help_hostgroup_group.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"600px",
//		height:"400px"
//	    });

});



