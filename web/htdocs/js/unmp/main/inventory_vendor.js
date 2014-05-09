var aSelected = [];
/* Datatable selected rows Array */
var formStatus = 0;
/* { 0:form for add and upadate not present, 1:form for add and upadate not present } */
var $gridViewDiv = null;
var $formDiv = null;
var $spinLoading = null;
var $spinMainLoading = null;
var $form = null;
var $formTitle = null;
var $formInput = null;
var $formTextarea = null;
var $formAddButton = null;
var $formEditButton = null;
var $tooltip = null;

var messages = {
    "add": "Vendor Added Successfully",
    "edit": "Vendor Details Edit Successfully",
    "del": "Selected Vendor(s) Deleted Successfully",
    "delConfirm": "Are You Sure, You want to Delete Selected Vendor(s)?",
    "duplicateError": "Please Enter Different Vendor Name, This is Already Exist.",
    "noneSelectedError": "Select Atleast one Vendor.",
    "multiSelectedError": "Select only single Vendor.",
    "validationError": "Some Fields are Missing or Incorrect.",
    "dbError": "Some Database Error occurred, Please Contact Your Administrator.",
    "noRecordError": "No Record Exist, May be vendor already deleted, Please reload this page.",
    "sysError": "UNMP Server has encountered an error. Please retry after some time.",
    "unknownError": "UNMP Server has encountered an error. Please retry after some time."
};
var actionName = null;

$(function () {
    // spin loading object
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire

    /* create object of divs */
    $gridViewDiv = $("div#grid_view_div");
    $formDiv = $("div#form_div");

    /* show grid view only hide other */
    $gridViewDiv.show();
    $formDiv.hide();

    /* page tip [for page tip write this code on each page please dont forget to change "href" value because this link create your help tip page] */
//	$("#page_tip").colorbox(
//	{
//		href:"help_inventory_vendor.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"450px",
//		height:"350px",
//		onComplte:function(){}
//	});

    /* create grid view */
    gridViewVendor();

    /* Click event handler for grid view */
    $('#grid_view tbody tr').live('click', function () {
        var id = this.id;
        var index = jQuery.inArray(id, aSelected);

        if (index === -1) {
            aSelected.push(id);
        } else {
            aSelected.splice(index, 1);
        }

        $(this).toggleClass('row_selected');
    });
});

function gridViewVendor() {
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "post",
        url: "grid_view_vendor.py",
        cache: false,
        success: function (result) {
            try {
                result = eval(result);
            }
            catch (err) {
                result = [];
            }
            //	create data table object
            oTable = $('#grid_view').dataTable({
                "bDestroy": true,
                "bJQueryUI": true,
                "bProcessing": true,
                "sPaginationType": "full_numbers",
                "bPaginate": true,
                "bStateSave": false,
                "aaData": result,
                "oLanguage": {
                    "sInfo": "_START_ - _END_ of _TOTAL_",
                    "sInfoEmpty": "0 - 0 of 0",
                    "sInfoFiltered": "(of _MAX_)"
                },
                "fnRowCallback": function (nRow, aData, iDisplayIndex) {
                    if (jQuery.inArray(aData.DT_RowId, aSelected) !== -1) {
                        $(nRow).addClass('row_selected');
                    }
                    return nRow;
                },
                "aoColumns": [
                    { "bSearchable": false, "bVisible": false, "aTargets": [ 0 ] },
                    { "sTitle": "S.No.", "sWidth": "5%" },
                    { "sTitle": "Vendor Name", "sClass": "center", "sWidth": "35%"},
                    { "sTitle": "Description", "sClass": "center", "sWidth": "60%"}//,
                ]
            });
            oTable.fnDraw();
            spinStop($spinLoading, $spinMainLoading);
        }
    });
}

function createForm(act, id) {
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "post",
        url: "form_vendor.py",
        cache: false,
        success: function (result) {
            $formDiv.html(result);
            addFormToolTip();
            cancelForm();
            $form = $("form#form_vendor");
            $formTitle = $("form#form_vendor th#form_title");
            $formInput = $("form#form_vendor input[type='text']");
            $formTextarea = $("form#form_vendor textarea");
            $formAddButton = $("form#form_vendor button[id='add_vendor']");
            $formEditButton = $("form#form_vendor button[id='edit_vendor']");
            submitForm($form);
            if (act == "edit") {
                editForm(id);
            }
            else {
                addForm();
            }
            spinStop($spinLoading, $spinMainLoading);
        }
    });
}
function addFormToolTip() {
    // add tool tip
    $tooltip = $("form#form_vendor input[type='text'],textarea").tooltip({
        // place tooltip on the right edge
        position: "center right",
        // a little tweaking of the position
        offset: [-2, 10],
        // use the built-in fadeIn/fadeOut effect
        effect: "fade",
        // custom opacity setting
        opacity: 0.7
    });
}
function cancelForm() {
    $("button#cancel_vendor").click(function () {
        hideForm();
    });
}
function hideForm() {
    $gridViewDiv.show();
    $formDiv.hide();
    /* this is bcoz when validation unsuccess and you click on cancel button then tooltip visible so this code will hide that. */
    if ($tooltip)
        $tooltip.tooltip().hide();
}
function showForm() {
    $gridViewDiv.hide();
    $formDiv.show();
}
function submitForm($formObj) {
    valiateForm($formObj);
    $formObj.submit(function () {
        var $formThis = $(this);
        if ($formThis.valid()) {
            spinStart($spinLoading, $spinMainLoading);
            var action = $formThis.attr("action");
            var method = $formThis.attr("method");
            var data = $formThis.serialize();
            $.ajax({
                type: method,
                url: action,
                data: data,
                cache: false,
                success: function (result) {
                    try {
                        result = eval("(" + result + ")");
                    }
                    catch (err) {
                        result = {success: 1, msg: "unknownError"};
                    }
                    if (result.success == 0) {
                        hideForm();
                        $().toastmessage('showSuccessToast', messages[actionName]);
                        gridViewVendor();
                    }
                    else {
                        $().toastmessage('showErrorToast', messages[result.msg]);
                    }
                    spinStop($spinLoading, $spinMainLoading);
                }
            });
        }
        else {
            $().toastmessage('showErrorToast', messages["validationError"]);
        }
        return false;
    });
}
function valiateForm($formObj) {
    $formObj.validate({
        rules: {
            vendor_name: {
                required: true,
                alphaNumeric: true
            },
            description: {
                required: true,
                alphaNumeric: true
            }//,
        },
        messages: {
            vendor_name: {
                required: "Vendor Name is Required Field",
                alphaNumeric: "Name should be alpha numeric"
            },
            description: {
                required: "Description is Required Field",
                alphaNumeric: "Description should be alpha numeric"
            }
        }
    });
}
function addForm() {
    $formTitle.html("Add Vendor");
    $form.attr("action", "add_vendor.py");
    $formInput.val("");
    $formTextarea.val("");
    $formAddButton.css({"display": "inline-block"});
    $formEditButton.hide();
    showForm();
}
function editForm(id) {
    $formTitle.html("Edit Vendor");
    $form.attr("action", "edit_vendor.py");
    $formEditButton.css({"display": "inline-block"});
    $formAddButton.hide();
    $.ajax({
        type: "get",
        url: "get_vendor_by_id.py?host_vendor_id=" + id,
        cache: false,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            }
            catch (err) {
                result = {success: 1, msg: "unknownError"};
            }
            if (result.success == 0) {
                $form.find("input#host_vendor_id").val(result.result[0]);
                $formInput.eq(0).val(result.result[1]);
                $formTextarea.eq(0).val(result.result[2]);
                showForm();
            }
            else {
                $().toastmessage('showErrorToast', messages[result.msg]);
            }
        }
    });
}
function addVendor() {
    actionName = "add";
    if (formStatus == 0) {
        createForm(actionName);
        formStatus = 1;
    }
    else {
        addForm();
    }
}

function editVendor() {
    var selectedRow = fnGetSelected(oTable);
    var rLength = selectedRow.length;
    if (rLength == 0) {
        $.prompt(messages["noneSelectedError"], {prefix: 'jqismooth'});
    }
    else if (rLength == 1) {
        var iRow = oTable.fnGetPosition(selectedRow[0]);
        var aData = oTable.fnGetData(iRow);
        var id = aData[0];
        actionName = "edit";
        if (formStatus == 0) {
            createForm(actionName, id);
            formStatus = 1;
        }
        else {
            editForm(id);
        }
    }
    else {
        $.prompt(messages["multiSelectedError"], {prefix: 'jqismooth'});
    }
}

function delVendor() {
    actionName = "delConfirm";
    hideForm();
    var selectedRow = fnGetSelected(oTable);
    var rLength = selectedRow.length;
    if (rLength == 0) {
        $.prompt(messages["noneSelectedError"], {prefix: 'jqismooth'});
    }
    else {
        $.prompt(messages[actionName], { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: delVendorCallback });
    }
}

function delVendorCallback(v, m) {
    actionName = "del"
    if (v != undefined && v == true) {
        var action = "del_vendor.py";
        var method = "get";
        spinStart($spinLoading, $spinMainLoading);
        var selectedRow = fnGetSelected(oTable);
        var rLength = selectedRow.length;
        var hostVendorId = [];
        for (var i = 0; i < selectedRow.length; i++) {
            var iRow = oTable.fnGetPosition(selectedRow[i]);
            var aData = oTable.fnGetData(iRow);
            hostVendorId.push(aData[0]);
        }
        $.ajax({
            type: method,
            url: action + "?host_vendor_ids=" + String(hostVendorId),
            cache: false,
            success: function (result) {
                try {
                    result = eval("(" + result + ")");
                }
                catch (err) {
                    result = {success: 1, msg: "unknownError"};
                }
                if (result.success == 0) {
                    hideForm();
                    $().toastmessage('showSuccessToast', messages[actionName]);
                    for (var i = 0; i < selectedRow.length; i++) {
                        var iRow = oTable.fnGetPosition(selectedRow[i]);
                        oTable.fnDeleteRow(iRow);
                    }
                }
                else {
                    $().toastmessage('showErrorToast', messages[result.msg]);
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }
    else {
        //$().toastmessage('showNoticeToast', "Remain Unchanged.");
    }
}
/*
 * I don't actually use this here, but it is provided as it might be useful and demonstrates
 * getting the TR nodes from DataTables
 */

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
