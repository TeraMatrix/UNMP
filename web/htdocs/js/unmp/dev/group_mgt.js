var $spinLoading = null;
var $spinMainLoading = null;

// Data Table Object
var oTable = null;

// Default Selected Link
var defaultSelectedLink = null;

// selected row
var aSelected = [];

var userArray = [];

var unameArray = [];

var boxuserArray = [];

var boxunameArray = [];

var hgArray = [];
var hgNameArray = [];

var boxHgArray = [];
var boxHgNameArray = [];

var selectedGroupId = "";

var selectedGroupName = "";

var boxGroupId = "";

var hg_data = [];

var userData = [];

var userDataInGp = [];

var $tooltip = null;

function groupDataTable(obj) {
    spinStart($spinLoading, $spinMainLoading);

    $.ajax({
        type: "get",
        url: "group_table.py",
        cache: false,
        success: function (result) {
            $("div#group_name_div").html(result);
            group_info();
            if (!obj) {
                obj = $("p.gp-name").eq(0);
            }
            spinStop($spinLoading, $spinMainLoading);
            obj.click();

        }
    });
}

function group_info() {
    $("p.gp-name").click(function () {
        spinStart($spinLoading, $spinMainLoading);
        selectedGroupId = "";
        selectedGroupName = "";
        var id = $(this).attr("id");
        selectedGroupName = $(this).text();
        selectedGroupId = id;
        $("p.gp-name").css({"background-color": "", "height": "18px", "border-bottom": "1px solid #DDD", "border-top": "1px solid #DDD", "border-right": "2px solid #AAA", "cursor": "pointer"});
        $(this).css({"background-color": "#ccc", "height": "20px", "border-bottom": "2px solid #AAA", "border-top": "2px solid #AAA", "border-left": "2px solid #AAA", "border-right": "0px solid #DDD"});
        $.ajax({
            type: "get",
            url: "group_info.py?&group_id=" + id,
            cache: false,
            success: function (result) {
                $("div#group_info").html(result);
                spinStop($spinLoading, $spinMainLoading);
            }
        });
        if ($("div.group-links").attr("id") == 'group_users') {
            showUser();
            searchEventUser();
        }
        else {
            showHgInGp();
            searchEventHgInGp();
        }
    });
}

function searchEventHgInGp() {
    $("input#search_hg_gp").keyup(function () {
        hgSearchInGp($.trim($(this).val()));
    });
}


function showHgInGp() {
    searchHgInGp = "";
    HgDataInGp = [];
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "show_hostgroups.py?group_id=" + selectedGroupId,
        cache: false,
        success: function (result1) {
            try {
                HgDataInGp = eval(result1);
            }
            catch (err) {
                HgDataInGp = [];
            }
            spinStop($spinLoading, $spinMainLoading);
            hgSearchInGp();

        }
    });
}

function hgSearchInGp(searchHgInGp) {
    if (!searchHgInGp) {
        searchHgInGp = "";
    }

    var $hg_table = $("<table width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" class=\"tt-table-new\" style=\"margin-bottom:0;\" />");

    var $hg_tr = null;
    var j = 0;
    for (i in HgDataInGp) {
        if (String(HgDataInGp[i][1]).toLowerCase().indexOf(searchHgInGp.toLowerCase()) >= 0 || String(HgDataInGp[i][1]).toLowerCase().indexOf(searchHgInGp.toLowerCase()) >= 0) {
            if (j == 0) {
                var $hg_tr = $("<tr/>");
            }
            if (j < 3) {
                var $hg_td = $("<td class=\"cell-info1\" />");
                var $hg_input = $("<input type='checkbox' name='hostgroup_check' value=" + "'" + String(HgDataInGp[i][0]) + "'" + " />");
                $hg_input.appendTo($hg_td);
                $hg_td.append("<span style=\"line-height:1.8em;\">" + (String(HgDataInGp[i][1]) + " (" + String(HgDataInGp[i][2]) + ")") + "</span>");
                $hg_td.appendTo($hg_tr);
                j = j + 1;

            }
            if (j == 3) {
                $hg_tr.appendTo($hg_table);
                j = 0;
            }
        }

    } // end of outer for
    if (j != 0) {
        j = 3 - j;
        while (j != 0) {
            var $hg_td = $("<td class=\"cell-info1\" />");
            $hg_td.appendTo($hg_tr);
            j = j - 1
        }
        $hg_tr.appendTo($hg_table);
    }
    //alert($hg_table.html());
    $("div#hg_ingp").html($hg_table);
}

function showUser() {
    //alert(selectedGroupId);
    searchUser = "";
    userData = [];
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "group_users.py?&group_id=" + selectedGroupId,
        cache: false,
        success: function (result1) {
            try {
                userData = eval(result1);
            }
            catch (err) {
                userData = [];
            }
            userSearch();
            spinStop($spinLoading, $spinMainLoading);
        }
    });
}

function searchEventUser() {
    $("input#search_User").keyup(function () {
        userSearch($.trim($(this).val()));
    });
}

function userSearch(searchUser) {
    if (!searchUser) {
        searchUser = "";
    }
    var $userTable = $("<table width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" class=\"tt-table-new\" style=\"margin-bottom:0;\" />");
    var $userTr = null;
    var j = 0;
    var flag_search = 0;
    if (userData.length < 1) {
        var $userTr = $("<tr/>");
        var $userTd = $("<td class=\"cell-info1\" > No User(s) Assinged to this Group </td>");
        $userTd.appendTo($userTr);
        $userTr.appendTo($userTable);
        flag_search = 1
        $('div#status-header').find('button').attr("disabled", 'true').addClass("disabled");
        $('div#status-header').find('button#add_user_to_group').removeAttr("disabled").removeClass("disabled");
    }
    for (i in userData) {
        if (String(userData[i][1]).toLowerCase().indexOf(searchUser.toLowerCase()) >= 0 || String(userData[i][3]).toLowerCase().indexOf(searchUser.toLowerCase()) >= 0) {
            flag_search = 2;
            if (j == 0) {
                var $userTr = $("<tr/>");
            }
            if (j < 3) {
                var $userTd = $("<td class=\"cell-info1\" />");
                var $userInput = $("<input type='checkbox' name='user_check' value=" + "'" + String(userData[i][0]) + "'" + " />");
                $userInput.appendTo($userTd);
                $userTd.append("<span style=\"line-height:1.8em;\">" + (String(userData[i][1]) + " (" + String(userData[i][2]) + " " + String(userData[i][3]) + ")") + "</span>");
                $userTd.appendTo($userTr);
                j = j + 1;

            }
            if (j == 3) {
                $userTr.appendTo($userTable);
                j = 0;
            }
        }

    } // end of outer for

    if (j != 0) {
        j = 3 - j;
        while (j != 0) {
            var $userTd = $("<td class=\"cell-info1\" />");
            $userTd.appendTo($userTr);
            j = j - 1;
        }
        $userTr.appendTo($userTable);
    }

    if (flag_search == 0) {
        var $userTr = $("<tr/>");
        var $userTd = $("<td class=\"cell-info1\" > No matching records found</td>");
        $userTd.appendTo($userTr);
        $userTr.appendTo($userTable);
        $('div#status-header').find('button').attr("disabled", 'true').addClass("disabled");
        $('div#status-header').find('button#add_user_to_group').removeAttr("disabled").removeClass("disabled");

    }
    if (flag_search == 2) {
        $('div#status-header').find('button').removeAttr("disabled").removeClass("disabled");
    }
    //alert($userTable.html());

    $("div#users_ingrp").html($userTable);
}


//================================================= Hostgroup in group ===============================================

function addHgToGrp() {
    $("#add_hg_to_group").colorbox(
        {
            href: "add_hgingp_view.py",
            onComplete: function () {
                var selectAll = $("button#selectAll");
                showHg();
                searchEvent();
                selectAll.click(function () {
                    $("input[class='box-hg-check']").attr('checked', 'checked');
                });
            },
            title: "Assign/Add Hostgroups To Group",
            opacity: 0.4,
            maxWidth: "80%",
            width: "550px",
            height: "450px"
        });

}

function boxAddHg() {
    boxHgArray = [];
    boxHgNameArray = [];
    $.each($("input[class='box-hg-check']:checked"), function (i, obj) {
        boxHgArray.push($(obj).val());
        boxHgNameArray.push($(obj).parent().text());
    });

    if (boxHgArray.length == 0) {
        $.prompt("Select at least one Hostgroups", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to Add Hostgroup(s)?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: boxAddHgCallback });
    }

}

function boxAddHgCallback(v, m) {
    if (v != undefined && v == true) {
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "get",
            url: "add_hostgroup_togroup.py?&group_id=" + selectedGroupId + "&hg_ids=" + String(boxHgArray) + "&grp_name=" + selectedGroupName + "&hg_names=" + String(boxHgNameArray),
            cache: false,
            success: function (result) {
                //alert(result);
                result = eval("(" + result + ")");
                if (result.success == 0) {

                    $().toastmessage('showSuccessToast', "Hostgroups Added Successfully.");
                    $("p[id='" + selectedGroupId + "']").click();
                    showHg();
                }
                else {
                    $().toastmessage('showWarningToast', String(result.result));
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }

}

function delHgFrmGrp() {
    hgArray = [];
    hgNameArray = [];
    $.each($("input[name='hostgroup_check']:checked"), function (i, obj) {
        hgArray.push($(obj).val());
        hgNameArray.push($(obj).parent().text());
    });

    if (hgArray.length == 0) {
        $.prompt("Select at least one Hostgroup", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to delete Hostgroup(s)?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: delHgCallback });
    }
}

function delHgCallback(v, m) {
    if (v != undefined && v == true) {
        var action = "del_hostgroup_fromgroup.py";
        var data = "hg_ids=" + String(hgArray) + "&group_id=" + selectedGroupId + "&hg_names=" + String(hgNameArray) + "&grp_name=" + selectedGroupName;
        var method = "get";
        //alert(String(hgArray)+" .. "+String(selectedGroupId));
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            url: action,
            type: method,
            data: data,
            cache: false,
            success: function (result) {
                //alert(result);
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    $().toastmessage('showSuccessToast', "Hostgroup(s) Deleted Successfully.");
                    $("p[id='" + selectedGroupId + "']").click();
                }
                else {
                    //alert(result.result);
                    $().toastmessage('showWarningToast', String(result.result));
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }

}

function moveHgToGrp() {
    hgArray = [];
    hgNameArray = [];
    $.each($("input[name='hostgroup_check']:checked"), function (i, obj) {
        hgArray.push($(obj).val());
        hgNameArray.push($(obj).parent().text());
    });
    if (hgArray.length == 0) {
        $.prompt("Select at least one Hostgroup", {prefix: 'jqismooth'});
    }
    else {
        boxGroupId = "";
        $.colorbox(
            {
                href: "move_hgtogp_view.py?gp_id=" + selectedGroupId,
                onComplete: function () {
                    $('select#groups').change(function () {
                        boxGroupId = "";
                        var $this = $(this);
                        boxGroupId = $this.val();
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


function boxMoveHg() {
    if (boxGroupId == "" || boxGroupId == null) {
        $.prompt("Select at least one Group", {prefix: 'jqismooth'});
    }
    else if (hgArray.length == 0) {
        $.prompt("Select at least one Hostgroup", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to Move Hostgroup(s)?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: boxMoveHgCallback });
    }

}

function boxMoveHgCallback(v, m) {
    if (v != undefined && v == true) {
        //alert(boxGroupId+" "+String(hgArray)+" "+String(selectedGroupId));
        spinStart($spinLoading, $spinMainLoading);
        var group_name = "";
        group_name = $("div#selectGroupDiv").find("select#groups option:selected").text();
        $.ajax({
            type: "get",
            url: "move_hostgroup_togroup.py?&group_id=" + boxGroupId + "&hg_ids=" + String(hgArray) + "&old_group_id=" + String(selectedGroupId) + "&hg_names=" + String(hgNameArray) + "&grp_name=" + group_name + "&sel_group=" + selectedGroupName,
            cache: false,
            success: function (result) {
                result = eval("(" + result + ")");
                if (result.success == 0) {

                    $().toastmessage('showSuccessToast', "Hostgroup(s) Moved Successfully.");
                    $("p[id='" + selectedGroupId + "']").click();
                    $("div#cboxClose").click();
                    boxGroupId = null;
                }
                else {
                    //alert(result.result);
                    $().toastmessage('showWarningToast', String(result.result));
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }
}

function showHg1() {
    $.ajax({
        type: "get",
        url: "group_hostgroups.py?group_id=" + selectedGroupId + "&all=0" + "&light_box=" + 1,
        cache: false,
        success: function (result1) {
            $("div#hostgroups_in_grp").html(result1);
            $("div#hostgroups_in_grp").find("input[type='checkbox']").addClass("box-hg-check");
        }
    });

}

function searchEvent() {
    $("input#search_hg").keyup(function () {
        hgSearch($.trim($(this).val()));
    });
}


function showHg(searchHg) {
    spinStart($spinLoading, $spinMainLoading);
    searchHg = "";
    hg_data = [];
    $.ajax({
        type: "get",
        url: "show_hostgroups.py?group_id=" + selectedGroupId + "&all=0" + "&light_box=" + 1,
        cache: false,
        success: function (result1) {
            try {
                hg_data = eval(result1);
            }
            catch (err) {
                hg_data = [];
            }
            hgSearch();
            //var searchHg = $.trim($("div#hg_ingrp_head").find("input#search_hg")).val());
            spinStop($spinLoading, $spinMainLoading);

        }
    });

}

function hgSearch(searchHg) {
    if (!searchHg) {
        searchHg = "";
    }

    var $hg_table = $("<table width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" class=\"tt-table-new\" />");

    var $hg_tr = null;
    var j = 0;
    for (i in hg_data) {
        if (String(hg_data[i][1]).toLowerCase().indexOf(searchHg.toLowerCase()) >= 0 || String(hg_data[i][1]).toLowerCase().indexOf(searchHg.toLowerCase()) >= 0) {
            if (j == 0) {
                var $hg_tr = $("<tr/>");
            }
            if (j < 3) {
                var $hg_td = $("<td class=\"cell-info1\" />");
                var $hg_input = $("<input type='checkbox' class='box-hg-check' name='hostgroup_check' value=" + "'" + String(hg_data[i][0]) + "'" + " />");
                $hg_input.appendTo($hg_td);
                $hg_td.append("<span style=\"line-height:1.8em;\">" + (String(hg_data[i][1]) + " (" + String(hg_data[i][2]) + ")") + "</span>");
                $hg_td.appendTo($hg_tr);
                j = j + 1;

            }
            if (j == 3) {
                $hg_tr.appendTo($hg_table);
                j = 0;
            }
        }

    } // end of outer for
    if (j != 0) {
        j = 3 - j;
        while (j != 0) {
            var $hg_td = $("<td class=\"cell-info1\" />");
            $hg_td.appendTo($hg_tr);
            j = j - 1
        }
        $hg_tr.appendTo($hg_table);
    }
    //alert($hg_table.html());
    $("div#hostgroups_in_grp").html($hg_table);
}

//================================================= END hostgroup in group ===============================================

//================================================= user in group ===============================================

function showUserInGp() {

    //alert(selectedGroupId);
    spinStart($spinLoading, $spinMainLoading);
    searchUserInGp = "";
    userDataInGp = [];
    $.ajax({
        type: "get",
        url: "group_users.py?&group_id=" + boxGrpId,
        cache: false,
        success: function (result1) {
            try {
                userDataInGp = eval(result1);
            }
            catch (err) {
                userDataInGp = [];
            }
            userSearchInGp();
            //var searchUserInGp = $.trim($("div#hg_ingrp_head").find("input#search_hg")).val());
            spinStop($spinLoading, $spinMainLoading);
        }
    });
}

function searchEventUserInGp() {
    $("input#search_user_gp").keyup(function () {
        userSearchInGp($.trim($(this).val()));
    });
}

function userSearchInGp(searchUserInGp) {
    if (!searchUserInGp) {
        searchUserInGp = "";
    }
    var $userTable = $("<table width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" class=\"tt-table-new\" />");
    var $userTr = null;
    var j = 0;
    var flag_search = 0;
    var $div_btn = $('div#users_in_grp').next().find('button');
    if (userDataInGp.length < 1) {
        var $userTr = $("<tr/>");
        var $userTd = $("<td class=\"cell-info1\" ><br> No User(s) Available in this Group for addition <br><br> Select another Group from Select Group list <br></td>");
        $userTd.appendTo($userTr);
        $userTr.appendTo($userTable);
        $div_btn.attr('disabled', true).addClass("disabled");
        if ($("button#selectAll").find("span").text() == 'uncheck all') {
            $("button#selectAll").click();
        }
        flag_search = 1

    }
    for (i in userDataInGp) {
        if (String(userDataInGp[i][1]).toLowerCase().indexOf(searchUserInGp.toLowerCase()) >= 0 || String(userDataInGp[i][3]).toLowerCase().indexOf(searchUserInGp.toLowerCase()) >= 0) {
            flag_search = 2;
            if (j == 0) {
                var $userTr = $("<tr/>");
            }
            if (j < 3) {
                var $userTd = $("<td class=\"cell-info1\" />");
                var $userInput = $("<input type='checkbox' class='box-user-check' name='user_check' value=" + "'" + String(userDataInGp[i][0]) + "'" + " />");
                $userInput.appendTo($userTd);
                $userTd.append("<span style=\"line-height:1.8em;\">" + (String(userDataInGp[i][1]) + " (" + String(userDataInGp[i][2]) + " " + String(userDataInGp[i][3]) + ")") + "</span>");
                $userTd.appendTo($userTr);
                j = j + 1;

            }
            if (j == 3) {
                $userTr.appendTo($userTable);
                j = 0;
            }
        }

    } // end of outer for

    if (j != 0) {
        j = 3 - j;
        while (j != 0) {
            var $userTd = $("<td class=\"cell-info1\" />");
            $userTd.appendTo($userTr);
            j = j - 1;
        }
        $userTr.appendTo($userTable);
    }

    if (flag_search == 0) {
        var $userTr = $("<tr/>");
        var $userTd = $("<td class=\"cell-info1\" > No matching records found</td>");
        $userTd.appendTo($userTr);
        $userTr.appendTo($userTable);
        if ($("button#selectAll").find("span").text() == 'uncheck all') {
            $("button#selectAll").click();
        }

        $div_btn.attr('disabled', true).addClass("disabled");
    }
    if (flag_search == 2) {
        if ($("button#selectAll").find("span").text() == 'uncheck all') {
            $("button#selectAll").click();
        }
        $div_btn.removeAttr('disabled').removeClass("disabled");
    }

    //alert($userTable.html());
    $("div#users_in_grp").html($userTable);
}


function addUsrToGrp() {
    $("#add_user_to_group").colorbox(
        {
            href: "add_useringp_view.py?gp_id=" + selectedGroupId,
            onComplete: function () {
                var $groupSelect = $('select#groups');
                var selectAll = $("button#selectAll");
                $groupSelect.change(function () {
                    var $selectThis = $(this);
                    boxGrpId = $selectThis.val();
                    showUserInGp();
                    searchEventUserInGp();
                });
                $groupSelect.change();
                selectAll.toggle(function () {
                    $('div#users_in_grp').find('input:checkbox').attr('checked', 'checked');
                    $(this).find("span").text('uncheck all');
                }, function () {
                    $('div#users_in_grp').find('input:checkbox').removeAttr('checked');
                    $(this).find("span").text('check all');
                });
            },
            title: "Add User To Group",
            opacity: 0.4,
            maxWidth: "80%",
            width: "550px",
            height: "450px"
        });
}


function boxAddUsers() {
    boxuserArray = [];
    boxunameArray = [];
    $.each($("input[class='box-user-check']:checked"), function (i, obj) {
        boxuserArray.push($(obj).val());
        boxunameArray.push($(obj).parent().text());
    });
    if (boxuserArray.length == 0) {
        $.prompt("Select at least one User", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to Add User(s)?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: boxAddUsersCallback });
    }

}

function boxAddUsersCallback(v, m) {
    if (v != undefined && v == true) {
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "get",
            url: "add_users_togroup.py?&group_id=" + selectedGroupId + "&user_ids=" + String(boxuserArray) + "&users=" + String(boxunameArray) + "&grp_name=" + selectedGroupName,
            cache: false,
            success: function (result) {
                result = eval("(" + result + ")");
                if (result.success == 0) {

                    $().toastmessage('showSuccessToast', "Users Added Successfully.");
                    $("p[id='" + selectedGroupId + "']").click();
                    showUserInGp();
                }
                else {
                    //alert(result.result);
                    $().toastmessage('showWarningToast', String(result.result));
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }

}

function delUsrFrmGrp() {
    userArray = [];
    unameArray = [];
    $.each($("input[name='user_check']:checked"), function (i, obj) {
        userArray.push($(obj).val());
        unameArray.push($(obj).parent().text());
    });

    if (userArray.length == 0) {
        $.prompt("Select at least one User", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to delete User(s)?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: delUsersCallback });
    }
}

function delUsersCallback(v, m) {
    if (v != undefined && v == true) {
        //alert(unameArray);
        spinStart($spinLoading, $spinMainLoading);
        var action = "del_users_fromgroup.py";
        var data = "user_ids=" + String(userArray) + "&users=" + String(unameArray) + "&grp_name=" + selectedGroupName;
        var method = "get";
        $.ajax({
            url: action,
            type: method,
            data: data,
            cache: false,
            success: function (result) {
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    $().toastmessage('showSuccessToast', "User(s) Deleted Successfully.\n User(s) Now Assigned to Default System Group");
                    $("p[id='" + selectedGroupId + "']").click();
                }
                else {
                    //alert(result.result);
                    $().toastmessage('showWarningToast', String(result.result));
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }


}


function moveUsrToGrp() {
    userArray = [];
    unameArray = [];
    $.each($("input[name='user_check']:checked"), function (i, obj) {
        userArray.push($(obj).val());
        unameArray.push($(obj).parent().text());
    });
    if (userArray.length == 0) {
        $.prompt("Select at least one User", {prefix: 'jqismooth'});
    }
    else {
        boxGroupId = "";
        $.colorbox(
            {
                href: "move_usertogp_view.py?gp_id=" + selectedGroupId,
                onComplete: function () {
                    $('select#groups').change(function () {
                        boxGroupId = "";
                        var $this = $(this);
                        boxGroupId = $this.val();
                    });

                },
                title: "Move User To Group",
                opacity: 0.4,
                maxWidth: "80%",
                width: "400px",
                height: "150px"
            });
    }
}


function boxMoveUsers() {
    if (boxGroupId == "" || boxGroupId == null) {
        $.prompt("Select at least one Group", {prefix: 'jqismooth'});
    }
    else if (userArray.length == 0) {
        $.prompt("Select at least one User", {prefix: 'jqismooth'});
    }
    else {
        $.prompt('Are you sure, you want to Move User(s)?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: boxMoveUsersCallback });
    }

}

function boxMoveUsersCallback(v, m) {
    if (v != undefined && v == true) {
        //alert(boxGroupId);
        spinStart($spinLoading, $spinMainLoading);
        var group_name = "";
        group_name = $("div#selectGroupDiv").find("select#groups option:selected").text();
        $.ajax({
            type: "get",
            url: "add_users_togroup.py?&group_id=" + boxGroupId + "&user_ids=" + String(userArray) + "&users=" + String(unameArray) + "&grp_name=" + group_name + "&sel_group=" + selectedGroupName,
            cache: false,
            success: function (result) {
                result = eval("(" + result + ")");
                if (result.success == 0) {

                    $().toastmessage('showSuccessToast', "Users Moved Successfully.");
                    $("p[id='" + selectedGroupId + "']").click();
                    $("div#cboxClose").click();
                    boxGroupId = null;
                }
                else {
                    //alert(result.result);
                    $().toastmessage('showWarningToast', String(result.result));
                    $("p[id='" + selectedGroupId + "']").click();
                    $("div#cboxClose").click();
                    boxGroupId = null;
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }

}
//================================================= END user in group ===============================================


//============================================= document.ready======================================================
$(document).ready(function () {

    // spin loading object
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire

    groupDataTable();
    // page tip [for page tip write this code on each page please dont forget to change "href" value because this link create your help tip page]

    // add tool tip
    $tooltip = $("#add_group_form input[type='text'],#add_group_form textarea,#add_group_form select").tooltip({
        // place tooltip on the right edge
        position: "center right",
        // a little tweaking of the position
        offset: [-2, 10],
        // use the built-in fadeIn/fadeOut effect
        effect: "fade",
        // custom opacity setting
        opacity: 0.7
    });
    $("#add_group_form").validate({
        rules: {
            group_name: {
                required: true,
                minlength: 4
            },

            role: "required"

        },
        messages: {
            group_name: {
                required: "*",
                minlength: " at least 4 characters"
            },


            role: {
                required: "*"
            }
        }
    });
    $("#add_group_form").submit(function () {
        if ($(this).valid()) {
            spinStart($spinLoading, $spinMainLoading);

            var form = $(this);
            var role_name = form.find("select#role option:selected").text();
            var method = form.attr("method");
            var action = form.attr("action");
            //alert(action);
            var data = form.serialize();
            //alert(data);
            $.ajax({
                type: method,
                url: action,
                data: data + "&role_name=" + role_name,
                cache: false,
                success: function (result) {
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        $().toastmessage('showSuccessToast', "Group Added Successfully.");
                        groupDataTable();
                        $("#close_add_group").click();

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
    $("#close_add_group").click(function () {
        $("div#group_form").hide();
        $("div#edit_grp_form").hide();
        if ($tooltip)
            $tooltip.tooltip().hide();
        $("table#group_datatable").show();
        $("div#groups_detail_div").show();
    });

//	$("#page_tip").colorbox(
//	    {
//		href:"help_users_group.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"600px",
//		height:"400px"
//	    });


});


function addGroup() {
    $("table#group_datatable").hide();
    //$("div#groups_detail_div").hide();
    $("div#edit_grp_form").hide();
    $("div#group_form").show();
}


function editGroup() {

    //alert(selectedGroupId);
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "edit_group_view.py?&group_id=" + selectedGroupId,
        cache: false,
        success: function (result) {
            if (result.indexOf("NOUSERAVAILABLEWITHTHISID") >= 0) {
                $().toastmessage('showErrorToast', 'No such Group found.');
                groupDataTable();

            }
            else if (result.indexOf("CANNOTEDITSUPERADMIN") >= 0) {
                $().toastmessage('showWarningToast', ' Can\'t edit SuperAdmin group ');
                //groupDataTable();
            }
            else if (result.indexOf("SOMEERROROCCURMAYBEDBERROR") >= 0) {
                $().toastmessage('showErrorToast', ' UNMP server has encounterd an error./n Please REFRESH your page & try again/n Still having problem please contact support team');
                groupDataTable();
            }
            else {

                $("div#edit_grp_form").html(result);
                $("table#group_datatable").hide();
                $("div#groups_detail_div").hide();
                $("div#group_form").hide();
                $("img#edit_group").hide();
                $("div[id='edit_grp_form']").show();

                $("#close_edit_group").click(function () {
                    if ($tooltip)
                        $tooltip.tooltip().hide();
                    $("div#group_form").hide();
                    $("div#edit_grp_form").hide();
                    $("img#edit_group").show();
                    $("table#group_datatable").show();
                    $("div#groups_detail_div").show();
                });

                $tooltip = $("#edit_grp_form input[type='text'],#edit_grp_form textarea,#edit_grp_form select").tooltip({
                    // place tooltip on the right edge
                    position: "center right",
                    // a little tweaking of the position
                    offset: [-2, 10],
                    // use the built-in fadeIn/fadeOut effect
                    effect: "fade",
                    // custom opacity setting
                    opacity: 0.7
                });


                $("#edit_group_form").validate({
                    rules: {
                        role: "required"
                    },
                    messages: {
                        role: "*"
                    }
                });

                $("#edit_group_form").submit(function () {
                    if ($(this).valid()) {
                        spinStart($spinLoading, $spinMainLoading);
                        var form = $(this);
                        var role_name = form.find("select#role option:selected").text();
                        var method = form.attr("method");
                        var action = form.attr("action");
                        //alert(action);
                        var data = form.serialize();
                        //alert(data);
                        $.ajax({
                            type: method,
                            url: action,
                            data: data + "&role_name=" + role_name,
                            cache: false,
                            success: function (result) {
                                result = eval("(" + result + ")");
                                if (result.success == 0) {
                                    $().toastmessage('showSuccessToast', "Group Updated Successfully.");
                                    groupDataTable();
                                    $("#close_edit_group").click();
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
                    return false;
                });
            }
            spinStop($spinLoading, $spinMainLoading);
        }
    });

}


function name_chk() {
    if ($("form").attr('id') == "add_group_form") {
        val_ = $("input#group_name").val();
        type_ = "get";
        func_type = "group";
    }

    if (val_.length > 3) {

        $.ajax({
            type: type_,
            url: "check_name.py?&name=" + val_ + "&type=" + func_type,
            cache: false,
            success: function (result) {
                result = eval("(" + result + ")");

                if (result.success == 0) {
                    $("input[name='group_name']").removeClass("error").addClass("valid");
                    $("label#check_result").css("color", "green");
                    $("label#check_result").html("Name is Available ");

                }
                else {
                    $("input[name='group_name']").removeClass("valid").addClass("error");
                    $("label#check_result").css("color", "red");
                    $("label#check_result").html("**Name is NOT Available ");
                }

            }
        });
    }
    else {
        $("label#check_result").html("");
    }
}


function deleteGroupCallback(v, m) {
    if (v != undefined && v == true) {
        spinStart($spinLoading, $spinMainLoading);
        var action = "del_group.py";
        var data = "group_id=" + selectedGroupId;
        var method = "get";
        $.ajax({
            url: action,
            type: method,
            data: data,
            cache: false,
            success: function (result) {
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    // do paragraph modifications
                    $().toastmessage('showSuccessToast', "Group Deleted Successfully.");
                    groupDataTable();
                }
                else {
                    //alert(result.result);
                    $().toastmessage('showWarningToast', String(result.result));
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }

}

function delGroup() {
    //alert(selectedGroupId);
    $.prompt('Are you sure, you want to delete this Group? \n This will delete all the users assigned to this group.', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: deleteGroupCallback });
}

function show_gpdetails() {
    var action = "show_group_details.py";
    var data = "group_id=" + group_id;
    var method = "get";

    $.ajax({
        url: action,
        type: method,
        data: data,
        cache: false,
        success: function (result) {
            result = eval("(" + result + ")");
            if (result.success == 0) {
                $().toastmessage('showSuccessToast', "Showing Group Details");
            }
            else {
                //alert(result.result);
                $().toastmessage('showWarningToast', String(result.result));
            }
        }
    });
}


function show_gpusers() {
    var action = "show_group_users.py";
    var data = "group_id=" + group_id;
    var method = "get";
    $.ajax({
        url: action,
        type: method,
        data: data,
        cache: false,
        success: function (result) {
            result = eval("(" + result + ")");
            if (result.success == 0) {
                $().toastmessage('showSuccessToast', "Showing Group Users");
            }
            else {
                //alert(result.result);
                $().toastmessage('showWarningToast', String(result.result));
            }
        }
    });
}


