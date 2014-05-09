$(function () {
    $("#select_devices").change(function () {
        $.ajax({
            type: "post",
            url: "get_device_by_type.py?device_type=" + $(this).val(),
            success: function (result) {
                result = $(result);
                result.find("table").find("input[name='check_all']").click(function () {
                    if (this.checked) {
                        $(this).parent().parent().parent().find("input[name='host']").attr("checked", true);
                    }
                    else {
                        $(this).parent().parent().parent().find("input[name='host']").attr("checked", false);
                    }
                });
                result.find("table").find("input[name='host']").click(function () {
                    if (this.checked) {
                        if ($(this).parent().parent().parent().find("input[name='host']:checked").size() == $(this).parent().parent().parent().find("input[name='host']").size()) {
                            $(this).parent().parent().parent().find("input[name='check_all']").attr("checked", true);
                        }
                    }
                    else {
                        $(this).parent().parent().parent().find("input[name='check_all']").attr("checked", false);
                    }
                });
                result.find("table").find("#update_btn").click(function () {
                    if ($("input[name='host']:checked").size() == 0) {
                        alert("Please Select at least one site.");
                    }
                    else {
                        if ($("#firmware").val() == "") {
                            $("label.file-error").show();
                        }
                        else {
                            $("label.file-error").hide();
                            $("#image_load").loading_div(10000, "File Uploading...", 0, null);
                            setTimeout(function () {
                                $("#update_btn").hide();
                                $("#active_btn").show();
                            }, 10000);
                        }
                    }
                });
                result.find("table").find("#active_btn").click(function () {
                    if ($("input[name='host']:checked").size() == 0) {
                        alert("Please Select at least one site.");
                    }
                    else {
                        if ($("#firmware").val() == "") {
                            $("label.file-error").show();
                        }
                        else {
                            $("label.file-error").hide();
                            $("input[name='host']:checked").each(function (i, btn_obj) {
                                $("#loading_" + $(btn_obj).attr("id")).loading_div(5000, "Updating..", 0, "red");
                                setTimeout(function () {
                                    $("#loading_" + $(btn_obj).attr("id")).loading_div(3000, "Activating..", 0, "green");
                                }, 5500);
                            });
                            setTimeout(function () {
                                $("#active_btn").hide();
                                $("#update_btn").show();
                                $("#firmware").val("");
                                $("#image_load").html("");
                            }, (9000));
                        }
                    }
                });
                $("#device_list").html(result);
            }
        });
    });
});
