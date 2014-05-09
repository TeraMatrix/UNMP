var $spinLoading = null;
var $spinMainLoading = null;
$(document).ready(function () {
    $spinLoading = $("div#spin_loading");        // create object that hold loading circle
    $spinMainLoading = $("div#main_loading");    // create object that hold loading squire
    getStatus();
    $(".start").click(function () {
        var type = $(this).attr("id");
        type = type.substring(0, type.length - 6);
        pid = $("#" + type + "_pid").val();
        var action = "start";
        var info_start = $("#" + type + "_label").html();
        //$("#"+type+"_label").html("starting...");
        label_start = "Trying to start " + $("#" + type + "_name").html() + " daemon...";
        $("#" + type + "_label").html(label_start);
        $.ajax({
            type: "post",
            url: "doAction.py?daemonName=" + type + "&action=" + action,
            cache: false,
            success: function (result) {
                if (result == '0') {
                    $("#" + type + "_on").show();
                    $("#" + type + "_off").hide();
                    $("#" + type + "_restart").show();
                    $("#" + type + "_stop").show();
                    $("#" + type + "_start").hide();
                    error_label_start = $("#" + type + "_name").html() + " daemon started ."
                    setTimeout(function () {
                        $("#" + type + "_label").html(error_label_start);
                    }, 1000);
                    //setTimeout(function() { $("#"+type+"_label").html("started"); }, 1000);
                    setTimeout(function () {
                        $("#" + type + "_label").html(info_start);
                    }, 3000);

                }
                else {
                    error_label_start = $("#" + type + "_name").html() + " daemon can't be started from UNMP interface. Reason insufficient permission error."
                    setTimeout(function () {
                        $("#" + type + "_label").html(error_label_start);
                    }, 1000);
                    setTimeout(function () {
                        $("#" + type + "_label").html(info_start);
                    }, 3000);
                }
            }
        });
    });
    $(".stop").click(function () {
        var type = $(this).attr("id");
        type = type.substring(0, type.length - 5);
        pid = $("#" + type + "_pid").val();
        var info_stop = $("#" + type + "_label").html();
        var action = "stop";
        //alert(type);
        //alert($("#unmp-local_name").html());
        label_stop = "Trying to stop " + $("#" + type + "_name").html() + " daemon...";
        $("#" + type + "_label").html(label_stop);
        $.ajax({
            type: "post",
            url: "doAction.py?daemonName=" + type + "&action=" + action,
            cache: false,
            success: function (result) {
                if (result == '0') {
                    $("#" + type + "_off").show();
                    $("#" + type + "_on").hide();
                    $("#" + type + "_start").show();
                    $("#" + type + "_stop").hide();
                    $("#" + type + "_restart").hide();
                    error_label_stop = $("#" + type + "_name").html() + " daemon stopped ."
                    setTimeout(function () {
                        $("#" + type + "_label").html(error_label_stop);
                    }, 1000);
                    //setTimeout(function() { $("#"+type+"_label").html("Daemon has been stopped..."); }, 1000);
                    setTimeout(function () {
                        $("#" + type + "_label").html(info_stop);
                    }, 3000);
                }
                else if (result == '2') {
                    error_label_stop = $("#" + type + "_name").html() + " daemon can't be stopped from UNMP interface. Reason insufficient permission error."
                    setTimeout(function () {
                        $("#" + type + "_label").html(error_label_stop);
                    }, 1000);
                    //setTimeout(function() { $("#"+type+"_label").html("you cannot stop the daemon from here.."); }, 1000);
                    setTimeout(function () {
                        $("#" + type + "_label").html(info_stop);
                    }, 3000);
                }
                else {
                    error_label_stop = $("#" + type + "_name").html() + " daemon can't be stopped from UNMP interface. Reason insufficient permission error."
                    setTimeout(function () {
                        $("#" + type + "_label").html(error_label_stop);
                    }, 1000);
                    //setTimeout(function() { $("#"+type+"_label").html("Error while stopping the daemon..."); }, 1000);
                    setTimeout(function () {
                        $("#" + type + "_label").html(info_stop);
                    }, 3000);
                }
            }
        });
    });
    $(".restart").click(function () {
        var type = $(this).attr("id");
        type = type.substring(0, type.length - 8);
        pid = $("#" + type + "_pid").val();
        var action = "restart";
        var info_restart = $("#" + type + "_label").html();
        //$("#"+type+"_label").html("restarting...");
        label_restart = "Trying to restart " + $("#" + type + "_name").html() + " daemon...";
        $("#" + type + "_label").html(label_restart);
        $.ajax({
            type: "post",
            url: "doAction.py?daemonName=" + type + "&action=" + action,
            cache: false,
            success: function (result) {
                if (result == '0') {
                    $("#" + type + "_on").show();
                    $("#" + type + "_off").hide();
                    $("#" + type + "_restart").show();
                    $("#" + type + "_stop").show();
                    $("#" + type + "_start").hide();
                    error_label_restart = $("#" + type + "_name").html() + " daemon has been restarted."
                    setTimeout(function () {
                        $("#" + type + "_label").html(error_label_restart);
                    }, 1000);
                    //setTimeout(function() { $("#"+type+"_label").html("Daemon has been Restarted..."); }, 1000);
                    setTimeout(function () {
                        $("#" + type + "_label").html(info_restart);
                    }, 3000);
                }
                else {
                    error_label_restart = $("#" + type + "_name").html() + " daemon can't be restarted from UNMP interface. Reason insufficient permission error."
                    setTimeout(function () {
                        $("#" + type + "_label").html(error_label_restart);
                    }, 1000);
                    //setTimeout(function() { $("#"+type+"_label").html("you cannot restart the daemon from here.."); }, 1000);
                    setTimeout(function () {
                        $("#" + type + "_label").html(info_restart);
                    }, 3000);
                }
            }
        });
    });
    $(".refresh").click(function () {
        var type = $(this).attr("id");
        type = type.substring(0, type.length - 8);
        pid = $("#" + type + "_pid").val();
        var info_refresh = $("#" + type + "_label").html();
        setTimeout(function () {
            $("#" + type + "_label").html("Refreshing");
        }, 1000);
        setTimeout(function () {
            $("#" + type + "_label").html(info_refresh);
        }, 3000);
        $.ajax({
            type: "post",
            url: "get_status.py?&pidfile=" + pid,
            cache: false,
            success: function (result) {
                if (result == '0') {
                    $("#" + type + "_on").show();
                    $("#" + type + "_off").hide();
                    $("#" + type + "_restart").show();
                    $("#" + type + "_stop").show();
                    $("#" + type + "_start").hide();
                }
                else {
                    $("#" + type + "_off").show();
                    $("#" + type + "_on").hide();
                    $("#" + type + "_start").show();
                    $("#" + type + "_stop").hide();
                    $("#" + type + "_restart").hide();
                }
            }
        });
    });

//	$("#page_tip").colorbox(
//	    {
//		href:"help_daemons.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"600px",
//		height:"400px"
//	    });
});

function getStatus() {
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "post",
        url: "load.py",
        cache: false,
        success: function (result) {
            res = result.split(",");
            for (var i = 0; i < res.length - 1; i += 2) {
                if (res[i + 1] == '0') {
                    $("#" + res[i] + "_on").show();
                    $("#" + res[i] + "_off").hide();
                    $("#" + res[i] + "_restart").show();
                    $("#" + res[i] + "_stop").show();
                    $("#" + res[i] + "_start").hide();
                }
                else {
                    $("#" + res[i] + "_off").show();
                    $("#" + res[i] + "_on").hide();
                    $("#" + res[i] + "_start").show();
                    $("#" + res[i] + "_stop").hide();
                    $("#" + res[i] + "_restart").hide();
                }
            }
            spinStop($spinLoading, $spinMainLoading);
        }
    });
}
