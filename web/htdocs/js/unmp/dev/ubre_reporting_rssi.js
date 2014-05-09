var aSelectedAvg = [];
var oTableAvg = null;
var aSelectedTotal = [];
var oTableTotal = null;
var $spinLoading = null;
var $spinMainLoading = null;
var submitClicked = false;

$(document).ready(function () {
    hostGroupSearch();
    HostSearch();
    //del_groupOnSpanClick();
    deleteGpAction();
    deleteHostAction();
    selectGroup();
    $spinLoading = $("div#spin_loading");        // create object that hold loading circle
    $spinMainLoading = $("div#main_loading");    // create object that hold loading squire
    $("#average_report_table").hide();
    $("#total_report_table").hide();
    $("#avg_header").hide();
    $("#total_header").hide();
    var cur_date = new Date();
    var d = cur_date.getDate();
    var y = cur_date.getFullYear();
    var m = cur_date.getMonth();
    var cdate = new Date(y, m, d);
    $("#get_reporting_data").submit(function () {
        $("#error_msg").hide();
        var str1 = $("#start_date").val();
        var str2 = $("#end_date").val();
        str1 = str1.split("/");
        str2 = str2.split("/");
        var date1 = new Date(str1[2], parseInt(str1[1], 10) - 1, str1[0]);
        var date2 = new Date(str2[2], parseInt(str2[1], 10) - 1, str2[0]);
        if (date2 < date1) {
            $().toastmessage('showErrorToast', "End Date can't be greater than Start Date");
            return false;
        }
        else if (cdate < date1 || cdate < date2) {
            $().toastmessage('showErrorToast', "Dates can't be greater than current Date");
            return false;
        }
        var $fromObj = $(this);
        var url = $fromObj.attr("action");
        var method = $fromObj.attr("method");
        var data = $fromObj.serialize();
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: method,
            url: url + '?all_host=' + filterHoststring() + '&all_group=' + filterGroupstring(),
            data: data,
            cache: false,
            success: function (result) {
                try {
                    result = eval("(" + result + ")");
                }
                catch (err) {
                    result = [];
                }
                //average_data(result.avg);
                //total_data(result.all);
                ////////
                crcAverage = result.avg;
                crcTotal = result.all;
                if (crcAverage.success == 0) {
                    average_data(crcAverage.result);
                }
                else {
                    $().toastmessage('showErrorToast', "Some error occurred while fetching Average Data ");
                    average_data([]);
                }

                if (crcTotal.success == 0) {
                    total_data(crcTotal.result);
                }
                else {
                    $().toastmessage('showErrorToast', "Some error occurred while fetching Total Data ");
                    total_data([]);
                }
                //////
                submitClicked = true;
                spinStop($spinLoading, $spinMainLoading);

            }
        });
        return false;
    });

    /* Click event handler*/
    $('#average_report_table tbody tr').live('click', function () {
        var id = this.id;
        var index = jQuery.inArray(id, aSelectedAvg);

        if (index === -1) {
            aSelectedAvg.push(id);
        } else {
            aSelectedAvg.splice(index, 1);
        }

        $(this).toggleClass('row_selected');
    });
    $('#total_report_table tbody tr').live('click', function () {
        var id = this.id;
        var index = jQuery.inArray(id, aSelectedTotal);

        if (index === -1) {
            aSelectedTotal.push(id);
        } else {
            aSelectedTotal.splice(index, 1);
        }

        $(this).toggleClass('row_selected');
    });
    $('#start_date, #start_time, #end_date,  #end_time').calendricalDateTimeRange({
        isoTime: true
    });
//	$("#page_tip").colorbox(
//	    {
//		href:"help_rssi.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"650px",
//		height:"450px"
//	    });
// reporting function start
    $("#excel_rpt_rssi").click(function () {
        /*if (submitClicked==false){
         $().toastmessage('showWarningToast', "Please generate report first.");
         return false;
         }*/
        spinStart($spinLoading, $spinMainLoading);
        var cur_date = new Date();
        var d = cur_date.getDate();
        var y = cur_date.getFullYear();
        var m = cur_date.getMonth();
        var cdate = new Date(y, m, d);
        var method = 'post';
        var no_of_devices = $("#no_of_devices").val();
        var start_date = $("#start_date").val();
        var end_date = $("#end_date").val();
        var start_time = $("#start_time").val();
        var end_time = $("#end_time").val();
        var str1 = $("#start_date").val();
        var str2 = $("#end_date").val();
        str1 = str1.split("/");
        str2 = str2.split("/");
        var date1 = new Date(str1[2], parseInt(str1[1], 10) - 1, str1[0]);
        var date2 = new Date(str2[2], parseInt(str2[1], 10) - 1, str2[0]);
        if (date2 < date1) {
            $().toastmessage('showErrorToast', "End Date can't be greater than Start Date");
            spinStop($spinLoading, $spinMainLoading);
            return false;
        }
        else if (cdate < date1 || cdate < date2) {
            $().toastmessage('showErrorToast', "Dates can't be greater than current Date");
            spinStop($spinLoading, $spinMainLoading);
            return false;
        }
        var method = 'post';
        var no_of_devices = $("#no_of_devices").val();
        var start_date = $("#start_date").val();
        var end_date = $("#end_date").val();
        var start_time = $("#start_time").val();
        var end_time = $("#end_time").val();
        var url = "ubre_rssi_excel_reporting.py?no_of_devices=" + no_of_devices + "&start_date=" + start_date + "&end_date=" + end_date + "&start_time=" + start_time + "&end_time=" + end_time + '&all_host=' + filterHoststring() + '&all_group=' + filterGroupstring();
        $.ajax({
            type: method,
            url: url,
            cache: false,
            success: function (result) {
                if (result == 0 || result == '0') {
                    $().toastmessage('showSuccessToast', "Report Generated Successfully.");
                    window.location = "download/rssi_excel.xls";
                }
                else if (result == 1 || result == '1') {
                    $().toastmessage('showWarningToast', 'Data not available for this date. So please choose right date for report download.');
                }
                else {
                    $().toastmessage('showErrorToast', "UNMP Server has encountered an error. Please retry after some time.");
                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    });
// reporting function end

});

function average_data(tabledata) {
//	create data table object
    oTableAvg = $('#average_report_table').dataTable({
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
        "oLanguage": {
            "sInfo": "_START_ - _END_ of _TOTAL_",
            "sInfoEmpty": "0 - 0 of 0",
            "sInfoFiltered": "(of _MAX_)"
        },
        "fnRowCallback": function (nRow, aData, iDisplayIndex) {
            if (jQuery.inArray(aData.DT_RowId, aSelectedAvg) !== -1) {
                $(nRow).addClass('row_selected');
            }
            return nRow;
        },
        "aoColumns": [
            { "sTitle": "TIME", "sWidth": "11%" },
            { "sTitle": "HOST NAME", "sClass": "center", "sWidth": "11%"},
            { "sTitle": "IP ADDRESS", "sClass": "center", "sWidth": "11%" },
            { "sTitle": "PEER 1", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 2", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 3", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 4", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 5", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 6", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 7", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 8", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 9", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 10", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 11", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 12", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 13", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 14", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 15", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 16", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "Group Name", "sClass": "center", "sWidth": "11%" }
        ]
    });
    $("#avg_header").show();
    $("#average_report_table").show();
    //oTableAvg.fnDraw();
};

function total_data(tabledata) {
//	create data table object
    oTableTotal = $('#total_report_table').dataTable({
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
        "oLanguage": {
            "sInfo": "_START_ - _END_ of _TOTAL_",
            "sInfoEmpty": "0 - 0 of 0",
            "sInfoFiltered": "(of _MAX_)"
        },
        "fnRowCallback": function (nRow, aData, iDisplayIndex) {
            if (jQuery.inArray(aData.DT_RowId, aSelectedTotal) !== -1) {
                $(nRow).addClass('row_selected');
            }
            return nRow;
        },
        "aoColumns": [
            { "sTitle": "TIME", "sWidth": "11%" },
            { "sTitle": "HOST NAME", "sClass": "center", "sWidth": "11%"},
            { "sTitle": "IP ADDRESS", "sClass": "center", "sWidth": "11%" },
            { "sTitle": "PEER 1", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 2", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 3", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 4", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 5", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 6", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 7", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 8", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 9", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 10", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 11", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 12", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 13", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 14", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 15", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "PEER 16", "sClass": "center", "sWidth": "6%" },
            { "sTitle": "Group Name", "sClass": "center", "sWidth": "11%" }

        ]
    });
    $("#total_header").show();
    $("#total_report_table").show();
    //oTableTotal.fnDraw();
};


// Excel creating with new functionalty 


// This function is used for searching the text by facebox search box
function hostGroupSearch() {
    $("#group_search").fcbkcomplete({
        isID: 'fb_gp',
        width: '380px',
        json_url: "ubre_show_group_result.py",
        addontab: false,
        maxitems: 10,
        maxshownitems: 10,
        input_min_size: 1,
        height: 10,
        cache: true,
        newel: false,
        input_name: 'Enter Group Name',
        filter_selected: true,
        //select_all_text: "select",
        onselect: function () {
            var selected;
            var selectedText;
            $("#group_search option:selected").each(function () {
                //allGroup.push($(this).val());
                selected = $(this).val();
                selectedText = $(this).text();

            });
            addGroups(selected, selectedText);
            $.ajax({
                type: "post",
                url: "ubre_show_host_data_of_group.py?select_value=" + selected,
                cache: false,
                success: function (result) {
                    for (var h in result) {
                        $("#host_search").trigger("addItem", result[h]);
                    }
                    addHosts(result, selected);
                }
            });

        }
    });
}
// This function is used for searching the host name,ip_address,mac address by facebox search box
function HostSearch() {
    var selected = '';
    var selectedText = '';
    $("#host_search").fcbkcomplete({
        isID: 'fb_host',
        json_url: "ubre_show_host_result.py",
        width: '380px',
        addontab: false,
        maxitems: 10,
        maxshownitems: 10,
        input_min_size: 1,
        height: 10,
        cache: true,
        newel: false,
        filter_selected: true,
        onselect: function () {
            $("#host_search option:selected").each(function () {
                //allHost.push($(this).val());
                selected = $(this).val();
                selectedText = $(this).text();
            });
            addSingleHost(selected, selectedText);
        }

    });
    if (selected != '') {
        addSingleHost(selected, selectedText);
    }
}

//  function to add groups in Container
function addGroups(val, text) {
    var value = val;
    var text = text;
    //var objectString = s;
    var content = '';
    //$.each(objectString.items,function(i,item){
    content += "<li gp_id='" + val + "'>" + text + "<a class='closebutton2'>&times;</a></li>";

    //});
    $('#GroupsList').append(content);
}
function addHosts(s, val) {
    var objectString = s;                //  json string of hosts
    var content = '';
    $.each(objectString, function (i, item) {
        $("div#hostsList").find("li[host_id='" + objectString[i].value + "']").remove();
        content += "<li host_id='" + objectString[i].value + "' rel='" + val + "'>" + objectString[i].title + "<a class='closebutton1'>&times;</a></li>";
    });
    $('#HostsList').append(content);  // append list to conatiner
    var len = filterHoststring();
    if (len.length > 0) {
        $("#no_of_devices").attr('disabled', 'true');
    }
}

function addSingleHost(val, text) {
    //  var objectString = s;                //  json string of hosts
    var content = '';
    //  $.each(objectString,function(i,item){
    content += "<li host_id='" + val + "'>" + text + "<a class='closebutton1'>&times;</a></li>";

    // });
    $('#HostsList').append(content);  // append list to conatiner
    var len = filterHoststring();
    if (len.length > 0) {
        $("#no_of_devices").attr('disabled', 'true');
    }
}

//                       content += "<li host_id='"+ objectString.items[i].value +"'>" + objectString.items[i].title + "<span class='highlight_gp'>["+objectString.items[i].group+"]</span><a class='as-close1'>&times;</a></li>";                                                  

// delete action of host
function deleteGpAction() {
    del_groupOnSpanClick();
}

function del_groupOnSpanClick() {
    $('#GroupsList li a.closebutton2').live('click', function () {
        var target = $(this).parent().attr('gp_id');
//alert(target);
        $(this).parent().remove();
        del_gp_from_fb(target);
        del_hostGroup(target);
    });
}


//function to delete group from facebox list
function del_gp_from_fb(id) {
    $('#fb_gp .bit-box[rel="' + id + '"]').find("a").click();
//	$("ul#fb_gp .bit-box[rel='" + id + "']").find("a").click();
    var len = filterHoststring();
    if (len.length == 0) {
        $("#no_of_devices").attr('disabled', false);
    }
}
function del_hostGroup(id) {
    var target = id;
    $('#HostsList li').each(function () {
        if ($(this).attr('rel') == target) {
            $(this).remove();
            del_host_from_fb($(this).attr('host_id'));
        }
    });
    var len = filterHoststring();
    if (len.length == 0) {
        $("#no_of_devices").attr('disabled', false);
    }
}

//delete action of Host
function deleteHostAction() {
    del_hostOnSpanClick();
}

function del_hostOnSpanClick() {
    $('#HostsList li a.closebutton1').live('click', function () {
        var target = $(this).parent().attr('rel');
        $(this).parent().remove();
        del_host_from_fb($(this).parent().attr('host_id'));
//		del_host_from_fb(target);
        var count = checkHostOfSameGroup(target);
        if (count < 1) {
            del_group(target);
        }
    });
}

//function to delete group from facebox list
function del_host_from_fb(id) {
    $('#fb_host li.bit-box[rel="' + id + '"]').find("a").click();
    var len = filterHoststring();
    if (len.length == 0) {
        $("#no_of_devices").attr('disabled', false);
    }
}
// function to delete group

function del_group(id) {
    $("ul#fb_gp li[rel='" + id + "']").find("a").click();
    $('#GroupsList li[gp_id="' + id + '"]').find("a").click();
    var len = filterHoststring();
    if (len.length == 0) {
        $("#no_of_devices").attr('disabled', false);
    }
}

// function for check host of same group
function checkHostOfSameGroup(rel) {
    var count = 0;
//var flag = 1;
    $('#HostsList li').each(function () {
        if ($(this).attr('rel') == rel) {
            count++;
        }
    });
    return count;
}


function selectGroup() {
    $('#GroupsList li').live('click', function () {
        $('#GroupsList li').removeClass('Highlight');
        $('#hostsList li').removeClass('Highlight');
        var target = $(this);
        var id = target.attr('gp_id');
        if ($(this).hasClass('Highlight')) {
            target.removeClass('Highlight');
            $('#hostsList li[rel="' + id + '"]').removeClass('Highlight');
        }
        else {
            target.addClass('Highlight');
            $('#hostsList li[rel="' + id + '"]').addClass('Highlight');
        }
        //$(this).toggleClass('Highlight');
    });
}
//function returns group string from container 
function filterGroupstring() {
    var groupString = '';
    $('#GroupsList').find('li').each(function () {
        groupString += $(this).attr('gp_id') + ',';

    });
    return groupString;
}
//function returns host string from container 
function filterHoststring() {
    var hostString = '';
    $('#HostsList').find('li').each(function () {
        hostString += $(this).attr('host_id') + ',';

    });
    return hostString;
}


// function for searching group
function searchGroup(gp_id) {
    var id = gp_id;
    var count = 0;
    $('#GroupsList li').each(function () {
        if ($(this).attr('gp_id') == id) {
            count = 1
        }
        else {
            count = 0
        }
    });
    return count;
}

