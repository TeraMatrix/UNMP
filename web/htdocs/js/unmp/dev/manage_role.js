var $spinLoading = null;
var $spinMainLoading = null;
var flag_addrole = 1
var $addRoleForm = null;

var selectedRoleId = "";
var $jq = "";
function roleDataTable(obj) {
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "role_table.py",
        cache: false,
        success: function (result) {
            $("div#role_name_div").html(result);
            role_info();
            if (!obj) {
                obj = $("p.role-name").eq(0);
            }
            obj.click();
            spinStop($spinLoading, $spinMainLoading);
        }
    });
}

function role_info() {
    $("p.role-name").click(function () {
        selectedRoleId = "";
        var id = $(this).attr("id");
        selectedRoleId = id;
        $("p.role-name").css({"background-color": "", "height": "18px", "border-bottom": "1px solid #DDD", "border-top": "1px solid #DDD"});
        $(this).css({"background-color": "#ccc", "height": "20px", "border-bottom": "2px solid #AAA", "border-top": "2px solid #AAA"});
        $.ajax({
            type: "get",
            url: "role_info.py?&role_id=" + id,
            cache: false,
            success: function (result) {
                $("div#role_info").html(result);
            }
        });
        /*		if ($("div.group-links").attr("id") == 'group_users')
         {
         showUser();
         searchEventUser();
         }
         else
         {
         showHgInGp();
         searchEventHgInGp();
         }
         */
    });
}


function addGrpInRole() {
    $().toastmessage('showNoticeToast', " add groups to Role ");
}

function delGrpFrmRole() {
    $().toastmessage('showNoticeToast', " delete groups from role ");
}

function moveGrpToRole() {
    $().toastmessage('showNoticeToast', " Move groups from Role ");
}


$(document).ready(function () {

    // spin loading object
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
    roleDataTable();
    //$jq = jQuery.noConflict();
    // page tip [for page tip write this code on each page please dont forget to change "href" value because this link create your help tip page]
    /*	$("#page_tip").colorbox(
     {
     href:"help_format.py",
     title: " Have to be Done",
     opacity: 0.4,
     maxWidth: "80%",
     width:"350px",
     height:"250px"
     });

     */


});


function name_chk() {
    /*	if($("form").attr('id') == "add_role_form")
     {
     val_ = $("input#role_name").val();
     type_ = "get";
     func_type = "role";
     }
     */
    val_ = $("input#role_name").val();
    type_ = "get";
    func_type = "role";
    /* */
    if (val_.length > 4) {

        $.ajax({
            type: type_,
            url: "check_rolename.py?&name=" + val_ + "&type=" + func_type,
            cache: false,
            success: function (result) {
                result = eval("(" + result + ")");

                if (result.success == 0) {
                    $("span#check_result").css("color", "green");
                    $("span#check_result").html("Name is Available ");

                }
                else {
                    $("span#check_result").css("color", "red");
                    $("span#check_result").html("**Name is NOT Available ");

                }

            }
        });
    }
    else {
        $("span#check_result").html("");
    }
}


function addRole() {
    //spinStart($spinLoading,$spinMainLoading);
    if (flag_addrole == 0 && addRoleForm != null) {
        $("div#add_role").html(addRoleForm);
        $("div#container_body").hide();
        closeRole();
        $("div#add_role").show();
        //checkbox_role();
        //roleformValidate();
        //spinStop($spinLoading,$spinMainLoading);
    }
    else {
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "get",
            url: "add_roleview.py",
            cache: false,
            success: function (result) {

                addRoleForm = result;
                $("div#add_role").html(addRoleForm);
                $("div#container_body").hide();
                closeRole();
                //roleformValidate();
                $("div#add_role").show();
                //checkbox_role();
                flag_addrole = 0;
                //roleformValidate();
                spinStop($spinLoading, $spinMainLoading);
            }
        });
        return false;
    }

}


function closeRole() {
    $("#close_role").click(function () {
        $("div#add_role").hide();
        $("div#edit_role").hide();
        $("div#container_body").show();
    });

}
/*
 function checkbox_role()
 {
 //$jq = jQuery.noConflict();
 $jq('#treeList :checkbox').change(function (){
 $jq(this).siblings('ul').find(':checkbox').prop('checked', this.checked);
 if (this.checked) {
 $jq(this).parentsUntil('#treeList', 'ul').siblings(':checkbox').prop('checked', true);
 }
 else {
 $jq(this).parentsUntil('#treeList', 'ul').each(function(){
 var $this = $(this);
 var childSelected = $this.find(':checkbox:checked').length;
 if (!childSelected) {
 $this.prev(':checkbox').prop('checked', false);
 }
 });
 }
 });
 }*/
function roleformValidate() {
    /* add role validate
     */
    $("div#add_role_form").validate({
        rules: {
            role_name: {
                required: true,
                minlength: 5
            }

        },
        messages: {
            role_name: {
                required: "*",
                minlength: " at least 5 characters"
            }
        }
    });
    /* add role validate */
}

function roleformSubmit() {
    var form = $('div#add_role_form');
    if (true)//if(form.valid())
    {
        //var method = form.attr("method");
        //	var action = form.attr("action");
        //	alert(method);
        //	alert(action);
        var role_name = $("input#role_name").val();
        var descp = $("textarea#description").val();
        var prole_id = $("select#role").val();
        //plinkArray = [];
        //$.each($("input[name='plink_id']:checked"), function(i,obj){
        //	plinkArray.push($(obj).val());
        //});
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "get",
            url: "add_role.py?role_name=" + role_name + "&descp=" + descp + "&prole_id=" + prole_id,//+"&plink_ids="+String(plinkArray),
            cache: false,
            //data:"role_name="+role_name+"&descp="+descp,//+"&plink_ids="+plinkArray,
            success: function (result) {
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    //alert("Role Added Successfully");
                    $().toastmessage('showSuccessToast', "Role Added Successfully.");
                    roleDataTable();
                    $("#close_role").click();

                }
                else if (result.success == 1) {
                    //alert(String(result["result"]));
                    $().toastmessage('showErrorToast', String(result["result"]));
                }
                else {
                    var dt = result.result;
                    for (key in dt) {
                        resultStr += key + ": " + dt[key] + "<br/>"
                    }
                    //$().toastmessage('showErrorToast', "Some Fileds are Missing or Incorrect.");
                }
                spinStop($spinLoading, $spinMainLoading);
            }

        });
        return false;
    }
    else {
        $().toastmessage('showErrorToast', "Some Fileds are Missing or Incorrect.");
    }

}


function editformSubmit() {
    var form = $('div#edit_role_form');
    if (true)//if(form.valid())
    {
        //	var method = form.attr("method");
        //	var action = form.attr("action");
        //	alert(method);
        //	alert(action);
        var role_id = $("input#role_id").val();
        var descp = $("textarea#description").val();
        var prole_id = $("select#role").val();
        //alert(prole_id);
        //plinkArray = [];
        //$.each($("input[name='plink_id']:checked"), function(i,obj){
        //	plinkArray.push($(obj).val());
        //});
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "get",
            url: "edit_role.py?role_id=" + role_id + "&descp=" + descp + "&prole_id=" + prole_id,//+"&plink_ids="+String(plinkArray),
            cache: false,
            //data:"role_name="+role_name+"&descp="+descp,//+"&plink_ids="+plinkArray,
            success: function (result) {
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    //alert("Role Updated Successfully.");
                    $().toastmessage('showSuccessToast', "Role Updated Successfully.");
                    roleDataTable();
                    $("#close_role").click();

                }
                else if (result.success == 1) {
                    //alert(result["result"]);
                    $().toastmessage('showErrorToast', String(result["result"]));
                }
                else {
                    var dt = result.result;
                    for (key in dt) {
                        resultStr += key + ": " + dt[key] + "<br/>"
                    }
                    $().toastmessage('showErrorToast', "Some Fileds are Missing or Incorrect.");
                }
                spinStop($spinLoading, $spinMainLoading);
            }

        });
        return false;
    }
    else {
        $().toastmessage('showErrorToast', "Some Fileds are Missing or Incorrect.");
    }

}


function editRole() {
    //spinStart($spinLoading,$spinMainLoading);
    $.ajax({
        type: "get",
        url: "edit_roleview.py?role_id=" + selectedRoleId,
        cache: false,
        success: function (result) {
            $("div#edit_role").html(result);
            closeRole();
            $("div#container_body").hide();
            $("div#edit_role").show();
            //checkbox_role();
            //spinStop($spinLoading,$spinMainLoading);

        }
    });
}


function deleteRoleCallback(v, m) {
    if (v != undefined && v == true) {
        var action = "del_role.py";
        var data = "role_id=" + selectedRoleId;
        var method = "get";
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            url: action,
            type: method,
            data: data,
            cache: false,
            success: function (result) {
                result = eval("(" + result + ")");
                if (result.success == 0) {
                    // do paragraph modifications
                    $().toastmessage('showSuccessToast', "Role Deleted Successfully.");
                    roleDataTable();
                }
                else {
                    //alert(result.result);
                    $().toastmessage('showWarningToast', result.result);
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }
    else {
        $().toastmessage('showNoticeToast', "Remain Unchanged.");
    }
}

function delRole() {
    //alert(selectedGroupId);
    $.prompt('Are you sure, you want to delete this Role?', { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: deleteRoleCallback });
}
