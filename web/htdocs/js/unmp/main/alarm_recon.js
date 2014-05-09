var host_id
var upVar
var tbl_alarm
var img_status
$("div#outer_div").ready(function () {

    // spin loading object
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
    tbl_alarm = $("table#alarm_details");
    img_status = $("img#img-status");
    host_id = $('div#details').attr('name');
    $("button#start_recon_alarm").click(function () {
        var alarm_count = $('select#recon_items').val();
        if (host_id != undefined) {
            spinStart($spinLoading, $spinMainLoading);
            var action = "start_alarm.py";
            var data = "host_id=" + host_id + "&recon_items=" + alarm_count;
            var method = "get";

            $.ajax({
                url: action,
                type: method,
                data: data,
                cache: false,
                success: function (result) {
                    spinStop($spinLoading, $spinMainLoading);
                    //alert(result);
                    result = eval("(" + result + ")");
                    if (result.success == 0) {
                        $().toastmessage('showSuccessToast', String(result.result));
                        tbl_alarm.find("td#result").text(String(result.result));
                        tbl_alarm.find("td#time").text(result.time);
                    }
                    else {
                        //alert(result.result);
                        $().toastmessage('showWarningToast', String(result.result));
                    }
                    //spinStop($spinLoading,$spinMainLoading);
                }
            });
        }
        else {
            $().toastmessage('showWarningToast', ' Request did not dispatch: Host information not found on page');
        }
    });

    //setTimeout(startUpdate(), 3000);
    //startUpdate();

    upVar = setInterval(updateCallback, 5000);


});

function updateCallback() {
    var action = "update_alarmview.py";
    var data = "host_id=" + host_id;
    var method = "get";
    $.ajax({
        url: action,
        type: method,
        data: data,
        cache: false,
        success: function (result) {
            if (result.success == 0) {
                img_status.attr("src", "images/host_status" + String(result.status) + ".png");
                img_status.attr("title", result.status_msg);
                img_status.attr("original-title", result.status_msg);
                tbl_alarm.find("td#result").text(result.msg);
                tbl_alarm.find("td#time").text(result.time);
                tbl_alarm.find("td#state").html(result.state);
                tbl_alarm.find("td#output").text(String(result.output));
            }
            else {
                $().toastmessage('showSuccessToast', String(result.result));
            }
        }
    });
}


function stopUpdate() {
    clearInterval(upVar);
}

function startUpdate() {
    upVar = setInterval(updateCallback, 5000);
}
