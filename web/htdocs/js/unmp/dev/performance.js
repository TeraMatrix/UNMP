// disable all keys and right click
var start_date_val = ""
var end_date_val = ""
$.fn.DisableKeyAndRightClick =
    function () {
        return this.each(function () {
            $(this).bind("contextmenu", function (e) {
                e.preventDefault();
            });
            $(this).keydown(function (e) {
                return false;
            })
        })
    };
function host_start() {
    $("#submit_date").click(function () {
        start_date_val = $("input#start_date").val();
        end_date_val = $("input#end_date").val();
        $.ajax({
            type: 'post',
            url: 'host_history.py?start_date=' + start_date_val + "&end_date=" + end_date_val,
            success: function (result) {
                $("#service_list").hide();
                $("#host_list").html(result);
                click_info()
            }
        });
    });
}

function click_info() {
    $("td.hostname").hover(function () {
            $(this).css("font-weight", "bold");
        },
        function () {
            $(this).css("font-weight", "normal")
        });
    $("td.hostname").click(function () {

        start_date_val = $("input#start_date").val();
        end_date_val = $("input#end_date").val();
        $.ajax({

            type: "post",
            url: "get_service_by_host.py?host_name=" + $(this).html() + "&start_date=" + start_date_val + "&end_date=" + end_date_val,
            success: function (result) {
                $("#service_list").html(result).show();
            }
        });
    });

}

$(function () {
    host_start();
    click_info();
    $('#start_date, #end_date').calendricalDateRange({
        isoTime: true
    });
    $('#start_date,  #end_date').DisableKeyAndRightClick();
});
