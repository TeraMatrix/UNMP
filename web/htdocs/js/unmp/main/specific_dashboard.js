var $spinLoading = null;
var $spinMainLoading = null;
var spIpAddress = '';
var spMainObj = null;
var deviceTypeId = '';
var graph_type = 1;
var limitFlag = 1;
var spRecursionVar = null;
var refresh_time = 10;// default time for refreshing the hidden datatime value.
var spE1MainObj = null;
var linkObj = null;
var spEndDate = '';
var spEndTime = '';
var totalSelectedGraph = "";
var mozilBrowser = false;

$(function () {
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire

    $("input[id='current_rept_div']").attr("checked", "checked");
    refresh_time = $("#sp_refresh_time").val();
    deviceTypeId = $("select[id='device_type']").val();
    if (deviceTypeId != 'ap25')
        $("#client_rsl_table").parent().parent().css('display', 'none');

    $("#device_type").change(function () {
        $("#filter_ip").val("");
        $("#filter_mac").val("");
    });
    $('#sp_start_date, #sp_start_time, #sp_end_date,  #sp_end_time').calendricalDateTimeRange({
        isoTime: true
    });
    $("input[id='filter_ip']").keypress(function () {
        $("input[id='filter_mac']").val("");

    })
    $("input[id='btnSearch']").click(function () {
        deviceList();
    })

    $("input[id='filter_ip']").ccplAutoComplete("common_ip_mac_search.py?device_type=" + deviceTypeId + "&ip_mac_search=" + 1, {
        dataType: 'json',
        max: 30,
        selectedItem: $("input[id='filter_ip']").val(),
        callAfterSelect: function (obj) {
            ipSelectMacDeviceType(obj, 1);
        }
    });

    $("input[id='filter_mac']").ccplAutoComplete("common_ip_mac_search.py?device_type=" + deviceTypeId + "&ip_mac_search=" + 0, {
        dataType: 'json',
        max: 30,
        selectedItem: $("input[id='filter_mac']").val(),
        callAfterSelect: function (obj) {
            ipSelectMacDeviceType(obj, 0);
        }
    });

    $("input[id='filter_ip']").val($("input[id='filter_ip']").val());
    $("select[id='device_type']").val($("input[id='device_type']").val());
    $("select[id='device_type']").val(deviceTypeId);


    $("#up_down_search").toggle(function () {
            //var $span = $(this);
            //var $span = $this.find("span").eq(0);
            $("#up_down_search").removeClass("dwn");
            $("#up_down_search").addClass("up");
            $("#filterOptions").show();
            $("#hide_search").css({
                'background-color': "#F1F1F1",
                'display': "block",
                'height': '20px',
                'position': 'static',
                'overflow': 'hidden',
                'width': "100%"});
        },
        function () {
            //var $this = $(this);
            //var $span = $this.find("span").eq(0);
            $("#up_down_search").removeClass("up");
            $("#up_down_search").addClass("dwn");
            $("#filterOptions").hide();
            $("#hide_search").css({
                'background-color': "#F1F1F1",
                'display': "block",
                'height': '20px',
                'overflow': 'hidden',
                'position': 'static',
                'right': 1,
                'top': 1,
                'width': "100%",
                'z-index': 1000});

        });
    spIpAddress = $("input#filter_ip").val();
//	$("#page_tip").colorbox(
//	{
//	href:"page_tip_sp_monitor_dashboard.py",
//	title: "Dashboard",
//	opacity: 0.4,
//	maxWidth: "80%",
//	width:"650px",
//	height:"500px",
//	onComplte:function(){}
//	})

    $('#sp_host_info_div').slideUp('fast');
    // Slide up and slide down functionality starthere
    $("#tab_yo").slideUp('fast');
    $("#sp_show_graph_list").toggle(
        function () {
            $('#tab_yo').slideDown('slow', function () {
                $("#sp_show_graph_list").val('Dashboard Configuration')
            });
        },
        function () {
            $('#tab_yo').slideUp('slow', function () {
                $("#sp_show_graph_list").val('Dashboard Configuration')
            });
        });
    $("#sp_ad_graph").click(function () {
        parent.main.location = "get_ap_advanced_graph_value.py?ip_address='" + String(spIpAddress) + "'&device_type_id=" + deviceTypeId;
    });
    specificGenericGraphJson();
});


function hostInformation() {
    $('#sp_host_info_div').animate({
            left: '+=50',
            height: 'toggle'
        }, 1000, function () {
            var $hostInfo = $("#host_info");
            if ($hostInfo.attr('src') == "images/new_icons/round_minus.png") {
                $hostInfo.attr('src', "images/new_icons/round_plus.png");
                $hostInfo.attr('original-title', 'Show Status')
//					$("#host_info").html("original-title='Hide Status'");
            }
            else {
                $hostInfo.attr('src', "images/new_icons/round_minus.png");
                $hostInfo.attr('original-title', 'Hide Status')

            }
        }
    );
}


function backListing() {
    if (deviceTypeId == 'odu16' || deviceTypeId == 'odu100')
        redirectPath = 'odu_listing.py';
    else if (deviceTypeId == 'ap25')
        redirectPath = 'ap_listing.py';
    else if (deviceTypeId == 'idu4')
        redirectPath = 'idu_listing.py';
    else if (deviceTypeId == 'ccu')
        redirectPath = 'ccu_listing.py';
    else
        redirectPath = 'odu_listing.py';
    parent.main.location = redirectPath + "?device_type=" + String(deviceTypeId) + "device_list_state=enabled&selected_device_type=";
}


function specificGenericGraphJson() {
    $.ajax({
        type: "post",
        url: "sp_generic_json.py?device_type_id=" + deviceTypeId + "&ip_address=" + spIpAddress,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            if (result.graphs.length == 0)
                $().toastmessage('showErrorToast', 'Graph Information not exists in database for this User.');
            else if (result.success == 0) {
                result.otherData = [
                    {name: 'start_date', value: function () {
                        return $('input#sp_start_date').val();
                    }},
                    {name: 'start_time', value: function () {
                        return $('input#sp_start_time').val();
                    }},
                    {name: 'end_date', value: function () {
                        return $('input#sp_end_date').val();
                    }},
                    {name: 'end_time', value: function () {
                        return $('input#sp_end_time').val();
                    }},
                    {name: 'flag', value: function () {
                        return limitFlag;
                    }},
                    {name: 'ip_address', value: function () {
                        return spIpAddress;
                    }},
                    {name: 'graph_type', value: function () {
                        return graph_type;
                    }}
                ];
                spAddDateTime();
                result.graphColumn = 2;
                spUpdateDateTime();
                $("#sp_main_graph").html("");
                spMainObj = $("#sp_main_graph").yoAllGenericDashboard(result);
                trapAlarmInformation('alarm');
            }
            else {
                $().toastmessage('showErrorToast', result.error_msg);
            }
        }
    });
}


function disbaledReportButton() {
    $("#sp_pdf_report").addClass("disabled");
    $("#sp_pdf_report").attr("disabled", true);
    $("#sp_excel_report").addClass("disabled");
    $("#sp_excel_report").attr("disabled", true);
    $("#sp_csv_report").addClass("disabled");
    $("#sp_csv_report").attr("disabled", true);
    $("#sp_ad_graph").addClass("disabled");
    $("#sp_ad_graph").attr("disabled", true);
    $("#sp_show_graph_list").addClass("disabled");
    $("#sp_show_graph_list").attr("disabled", true);
}

function enabledReportButton() {
    $("#sp_pdf_report").removeClass("disabled");
    $("#sp_pdf_report").attr("disabled", false);
    $("#sp_excel_report").removeClass("disabled");
    $("#sp_excel_report").attr("disabled", false);
    $("#sp_csv_report").removeClass("disabled");
    $("#sp_csv_report").attr("disabled", false);
    $("#sp_ad_graph").removeClass("disabled");
    $("#sp_ad_graph").attr("disabled", false);
    $("#sp_show_graph_list").removeClass("disabled");
    $("#sp_show_graph_list").attr("disabled", false);
    $("#tab_yo").slideUp('fast');

}


function deviceList() {
    // this retreive the value of ipaddress textbox
    var ip_address = $("input[id='filter_ip']").val();
    // this retreive the value of macaddress textbox
    var mac_address = $("input[id='filter_mac']").val();
    // this retreive the value of selectdevicetype from select menu
    var selected_device_type = $("select[id='device_type']").val();
    var selectListElem = $("#device_type option:selected").text();
    deviceTypeId = selected_device_type;
    if (selectListElem == "" || selectListElem == undefined)
        selectListElem = ""
    if (selected_device_type == 'odu16' || selected_device_type == 'odu100')
        redirectPath = 'odu_listing.py';
    else if (selected_device_type == 'ap25')
        redirectPath = 'ap_listing.py';
    else if (selected_device_type == 'ccu')
        redirectPath = 'ccu_listing.py';
    else if (selected_device_type == 'idu4')
        redirectPath = 'idu_listing.py';
    else
        redirectPath = 'odu_listing.py';
    apIpAddress = ip_address
    deviceTypeId = $("select[id='device_type']").val();
    $.ajax({
        type: "post",
        url: "get_device_list_ap_for_monitoring.py?&ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type,
        cache: false,
        success: function (result) {
            $("#header3_text").html(selectListElem + " " + apIpAddress + " Dashboard");
            if (result == 0 || result == "0") {
                redirectOnListing(redirectPath);
                $("#adSrhap").hide();
                $("#tab_yo").hide();
                $("#event_table").hide();
                $("#alarm_table").hide();
                $("#main_host_info_div").hide();
                $("#sp_main_graph").html("");
                disbaledReportButton();

            }
            else if (result == 1 || result == "1") {
                parent.main.location = redirectPath + "?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type;

            }
            else if (result == 2 || result == "2") {
                redirectOnListing(redirectPath);
                $("#adSrhap").hide();
                $("#tab_yo").hide();
                $("#event_table").hide();
                $("#alarm_table").hide();
                $("#main_host_info_div").hide();
                $("#sp_main_graph").html("");
                disbaledReportButton();


            }
            else {
                $("#sp_show_msg").html("")
                $("#tab_yo").show();
                $("input#filter_ip").val(result);
                spIpAddress = result;
                $("#event_table").show();
                $("#alarm_table").show();
                $("#main_host_info_div").show();
                $("#sp_main_graph").html("");
                spDeviceDetail();
                specificGenericGraphJson();
                enabledReportButton();
            }
        }
    });

}


function ipSelectMacDeviceType(obj, ipMacVal) {
    selectedVal = $(obj).val();
    $.ajax({
        type: "get",
        url: "get_ip_mac_selected_device.py?selected_val=" + selectedVal + "&ip_mac_val=" + ipMacVal,
        success: function (result) {
            if (parseInt(result.success) == 0) {
                if (ipMacVal == 1) {
                    $("input[id='filter_mac']").val(String(result.mac_address).toUpperCase());
                    $("select[id='device_type']").val(result.selected_device);
                }
                else {
                    $("input[id='filter_ip']").val(result.ip_address);
                    $("select[id='device_type']").val(result.selected_device);
                }
                deviceList();
            }
            else {
                $().toastmessage('showErrorToast', result.error);
            }
        }
    });
}


function redirectOnListing(redirctPath) {
    $().toastmessage('showWarningToast', "Searched Device Doesn't Exist");
    setTimeout(function () {
        parent.main.location = redirectPath + "?ip_address=" + "" + "&mac_address=" + "" + "&selected_device_type=" + "";
    }, 1500);
}


function spDeviceDetail() {
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "post",
        url: "sp_device_details.py?ip_address=" + spIpAddress + "&device_type_id=" + deviceTypeId,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            if (result.success >= 1 || result.success >= "1") {
                $().toastmessage('showErrorToast', result.error_msg);
            }
            else {
                $("#sp_host_info_div").html(result.device_table);
            }
        },
        error: function (req, status, err) {
        }
    });
    spinStop($spinLoading, $spinMainLoading);
}


// Update the date time in text Box
function advancedUpdateDateTime() {
    $.ajax({
        type: "post",
        url: "advanced_update_date_time.py?device_type_id=" + deviceTypeId,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showWarningToast', "Date time not receving in proper format.");
                return;
            }
            else {
                $("#sp_end_date").val(result.end_date);
                $("#sp_end_time'").val(result.end_time);
            }
        }
    });
    return false;
}


// This function update date and time
function spAddDateTime() {
    $.ajax({
        type: "post",
        url: "sp_add_date_time_on_slide.py?device_type_id=" + deviceTypeId + "&ip_address=" + spIpAddress,
        cache: false,
        success: function (result) {
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showWarningToast', "Date time not receving in proper format.");
            }
            else {
                $("#more_graph_columns").html(result.show_graph_table);
                totalSelectedGraph = $("#sp").val();
                $("#sp_start_date").val(result.start_date);
                $("#sp_end_date").val(result.end_date);
                $("#sp_start_time").val(result.start_time);
                $("#sp_end_time").val(result.end_time);
                multiSelectColumns();
            }
        }
    });
    return false;
}


function spUpdateDateTime() {
    if (spRecursionVar != null) {
        clearInterval(spRecursionVar);
    }
    spDeviceDetail();
    if (deviceTypeId == 'ap25') {
        clientInformation()
        $("#client_rsl_table").parent().parent().removeAttr('display');
    }
    spAddDateTime();
    trapAlarmInformation();
    spRecursionVar = setInterval(function () {
        spUpdateDateTime();
    }, refresh_time * 60000);
}


function clientInformation() {
    $.ajax({
        type: "post",
        url: "sp_client_information.py?ip_address=" + spIpAddress + "&device_type_id=" + deviceTypeId,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            if (result.success >= 1 || result.success >= "1") {
                $().toastmessage('showErrorToast', result.error_msg);
            }
            else {
                $("#client_dashboard").html(result.client_table);
            }
        },
        error: function (req, status, err) {
        }
    });
}


function trapAlarmInformation() {
    //console.log(divObj);
    $.ajax({
        type: "post",
        url: "sp_event_alarm_information.py?ip_address=" + spIpAddress,
        data: $(this).serialize(),
        cache: false,
        success: function (result) {
            if (result.success >= 1 || result.success >= "1") {
                $().toastmessage('showErrorToast', result.error_msg);
            }
            else {
                $("#event_dashboard").html(result.event_table);
            }
        },
        error: function (req, status, err) {
        }
    });
}


// This is function create the Excel Report
function spExcelReportGeneration() {
    spCommonReportCreating('sp_excel_report_genrating.py', 'UBR_excel.xls');
}
// This is create the PDF Report.
function spPDFReportGeneration() {
    if ($.browser.mozilla) {
        mozilBrowser = true;
    }
    spCommonReportCreating('sp_pdf_report_genrating.py', 'UBR_PDF_Report.pdf');
}

// This is create the CSV Report.
function spCSVReportGeneration() {
    spCommonReportCreating('sp_csv_report_genrating.py', 'UBR_CSV_Report.csv');
}


function spCommonReportCreating(redirectPath, file_name) {
    graph_json = {};
    var field = [];
    var cal_type = null;
    var graph = null;
    var tab_option = null;
    var totalGraph = 0;
    var graphQuerySrting = "";
    var ajaxData = {};
    var start_date = $("#sp_start_date").val();
    var start_time = $("#sp_start_time").val();
    var end_date = $("#sp_end_date").val();
    var end_time = $("#sp_end_time").val();
    var calculationType = "";
    var graphType = "";
    var tempFileds = "";
    var chartType1 = null;
    for (node in spMainObj.options.db) {
        // Create chart.
        //svg = convertSVG(spMainObj.options.db[node]["options"]);
        //chartCopy1 = new Highcharts.Chart(spMainObj.options.db[node]["options"]);
        //alert(JSON.stringify(spMainObj.options.db[node]["options"]));
        //svg = spMainObj.options.db[node]["options"].highChart.container.innerHTML;
        if (redirectPath == 'sp_pdf_report_genrating.py') {
            var drawType = "";
            for (var i = 0; i < spMainObj.options.db[node].options.type.length; i++) {
                if (spMainObj.options.db[node].options.type[i].isChecked == 1) {
                    drawType = spMainObj.options.db[node].options.type[i].name;
                }
            }

            plotOptions1 = spMainObj.options.db[node]["options"].highChart.options.plotOptions;
            chartType1 = plotOptions1[drawType];
            try {
                chartType1.animation = false;
                chartType1.showCheckbox = false;
                chartType1.visible = true;
            } catch (err) {
            }

            chartCopy1 = new Highcharts.Chart(spMainObj.options.db[node]["options"].highChart.options);
            svg = chartCopy1.container.innerHTML;

            //svg = spMainObj.options.db[node]["options"].highChart.container.innerHTML;
            svg = convertSVG(svg);
            $.ajax({
                type: "post",
                //url:"../../images/download.php",
                url: "download.php",
                data: {
                    "type": "image/png",
                    "svg1": svg,
                    "filename": spMainObj.options.db[node]["options"].name,
                    "download": "Download"
                },
                success: function (result) {
                    //$().toastmessage('showErrorToast', result);
                },
                error: function (req, status, err) {
                    $().toastmessage('showErrorToast', "Image creator not present on desired location.");
                }
            })
        }
        // End chart.

        totalGraph += 1;
        field = [];
        var tempFileds = spMainObj.options.db[node]["options"].fields;
        for (var i = 0; i < tempFileds.length; i++) {
            if (tempFileds[i].isChecked == 1) {
                field[field.length] = tempFileds[i].name;
            }
        }

        calculationType = spMainObj.options.db[node]["options"].calType;
        for (var j = 0; j < calculationType.length; j++) {
            if (calculationType[j].isChecked == 1) {
                cal_type = calculationType[j].name;
            }
        }
        graphType = spMainObj.options.db[node]["options"].type;
        for (var j = 0; j < graphType.length; j++) {
            if (graphType[j].isChecked == 1) {
                graph = graphType[j].value;
            }
        }

        tab_option = spMainObj.options.db[node]["options"].tabList.selected;
        ajaxData = spMainObj.options.db[node]["options"].ajax.data['table_name'];

        graphQuerySrting += "&start" + String(totalGraph) + "=" + spMainObj.options.db[node]["options"].startFrom;
        graphQuerySrting += "&limit" + String(totalGraph) + "=" + spMainObj.options.db[node]["options"].itemLimit;

        graphQuerySrting += "&table_name" + String(totalGraph) + "=" + ajaxData;
        graphQuerySrting += "&type" + String(totalGraph) + "=" + graph;

        graphQuerySrting += "&field" + String(totalGraph) + "=" + field;
        graphQuerySrting += "&cal" + String(totalGraph) + "=" + cal_type;
        graphQuerySrting += "&graph_id" + String(totalGraph) + "=" + spMainObj.options.db[node]["options"].name;
        graphQuerySrting += "&tab" + String(totalGraph) + "=" + tab_option;
        graphQuerySrting += "&graph_name" + String(totalGraph) + "=" + spMainObj.options.db[node]["options"].displayName;
    }
    graphQuerySrting += "&total_graph=" + String(totalGraph)
    var select_option = $("input[name='option']:checked").val();
    if (select_option == 0) {
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "post",
            url: "advanced_update_date_time.py?device_type_id=" + deviceTypeId,
            data: $(this).serialize(),
            cache: false,
            success: function (result) {
                if (result.success == 1 || result.success == "1") {
                    $().toastmessage('showWarningToast', "Date time not receving in proper format.");
                    return;
                }
                else {
                    $.ajax({
                        type: "post",
                        url: redirectPath + "?ip_address=" + spIpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + result.end_date + "&end_time=" + result.end_time + "&device_type_id=" + deviceTypeId + "&select_option=" + select_option + "&limitFlag=" + limitFlag + graphQuerySrting,
                        data: $(this).serialize(),
                        cache: false,
                        success: function (result) {
                            if (result.success >= 1 || result.success >= "1") {
                                $().toastmessage('showErrorToast', result.error_msg);
                            }
                            else {
                                $().toastmessage('showSuccessToast', 'Report Generated Successfully');
                                window.location = "download/" + result.file_name;

                            }
                            spinStop($spinLoading, $spinMainLoading);

                        }
                    });
                }
            }
        });
    }
    else {
        spinStart($spinLoading, $spinMainLoading);
        $.ajax({
            type: "post",
            url: redirectPath + "?ip_address=" + spIpAddress + "&start_date=" + start_date + "&start_time=" + start_time + "&end_date=" + end_date + "&end_time=" + end_time + "&device_type_id=" + deviceTypeId + "&select_option=" + select_option + "&limitFlag=" + limitFlag + graphQuerySrting,
            data: $(this).serialize(),
            cache: false,
            success: function (result) {
                if (result.success >= 1 || result.success >= "1") {
                    $().toastmessage('showErrorToast', result.error_msg);
                }
                else {
                    $().toastmessage('showSuccessToast', 'Report Generated Successfully');
                    window.location = "download/" + result.file_name;

                }
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    }
}


/* Create chart code start here.
 */
function convertSVG(svgTxt) {
    var svg = svgTxt;
    // sanitize

    // sanitize
    svg = svg
        .replace(/zIndex="[^"]+"/g, '')
        .replace(/isShadow="[^"]+"/g, '')
        .replace(/symbolName="[^"]+"/g, '')
        .replace(/jQuery[0-9]+="[^"]+"/g, '')
        .replace(/isTracker="[^"]+"/g, '')
        .replace(/url\([^#]+#/g, 'url(#')
        .replace(/<svg /, '<svg xmlns:xlink="http://www.w3.org/1999/xlink" ')
        .replace(/ href=/g, " transform=\"translate(-15,-15)\" height=\"16\" width=\"16\" xlink:href=")
        .replace(/\n/, ' ')
        .replace(/<\/svg>.*?$/, '</svg>') // any HTML added to the container after the SVG (#894)
        /* This fails in IE < 8
         .replace(/([0-9]+)\.([0-9]+)/g, function(s1, s2, s3) { // round off to save weight
         return s2 +'.'+ s3[0];
         })*/

        // Replace HTML entities, issue #347
        .replace(/&nbsp;/g, '\u00A0') // no-break space
        .replace(/&shy;/g, '\u00AD') // soft hyphen

        // IE specific
        .replace(/<IMG /g, '<image ')
        .replace(/height=([^" ]+)/g, 'height="$1"')
        .replace(/width=([^" ]+)/g, 'width="$1"')
        .replace(/hc-svg-href="([^"]+)">/g, 'xlink:href="$1"/>')
        .replace(/id=([^" >]+)/g, 'id="$1"')
        .replace(/class=([^" ]+)/g, 'class="$1"')
        .replace(/ transform /g, ' ')
        .replace(/:(path|rect)/g, '$1')
        .replace(/style="([^"]+)"/g, function (s) {
            return s.toLowerCase();
        });

    // IE9 beta bugs with innerHTML. Test again with final IE9.
    svg = svg.replace(/(url\(#highcharts-[0-9]+)&quot;/g, '$1')
        .replace(/&quot;/g, "'");
    if (svg.match(/ xmlns="/g).length === 2) {
        svg = svg.replace(/xmlns="[^"]+"/, '');
    }

    //console.log(svg)
    if (mozilBrowser = true) {
        svg = svg.replace(/<image ([^>]*)([^\/])>/gi, '<image $1$2 />');
    }

    return svg;

}


//  Chart code end.


// Selectded list function start here
function multiSelectColumns() {
    $(".plus").click(function () {
        plusHostParentOption(this);
    })
    $(".minus").click(function () {
        minusHostParentOption(this);
    })
    var hostParentArray = [];
    var tempHostParent = $("input[name='spTemp']").val();
    if (tempHostParent != undefined) {
        hostParentArray = tempHostParent.split(",");
    }
    for (k = 0; k < hostParentArray.length; k++) {
        $("div[id='multiSelectList']").find("img[id='" + $.trim(hostParentArray[k]) + "']").click();
    }
    $("#rm").click(function (e) {
        e.preventDefault();
        $("div[id='multiSelectList']").find("div.selected").find("img").click();
    })
    $("#add").click(function (e) {
        e.preventDefault();
        $("div[id='multiSelectList']").find("div.nonSelected").find("img").click();
    })
}
function minusHostParentOption(Obj) {
    liObj = $("<li/>");
    imgObj = $("<img/>");
    liObj.append($(Obj).attr("name"));
    imgObj.attr("src", "images/add16.png").attr("class", "plus plus").attr("alt", "+").attr("id", $(Obj).attr("id")).attr("name", $(Obj).attr("name")).click(function () {
        plusHostParentOption(this)
    })
    liObj.append(imgObj);
    $(Obj).parent().parent().parent().parent().find("div.nonSelected").find("ul").append(liObj);
    $(Obj).parent().parent().parent().parent().find("input[name='sp']").val("");
    j = 0
    for (i = 0; i < $(Obj).parent().parent().find("li").size(); i++) {
        var addedHostParent = $(Obj).parent().parent().find("li").eq(i).find("img").attr("id");
        if (addedHostParent != $(Obj).attr("id")) {
            if (j == 0) {
                $(Obj).parent().parent().parent().parent().find("input[name='sp']").val($.trim(addedHostParent));
            }
            else {
                $(Obj).parent().parent().parent().parent().find("input[name='sp']").val($(Obj).parent().parent().parent().parent().find("input[name='sp']").val() + "," + $.trim(addedHostParent));
            }
            j++;
        }
    }
    $(Obj).parent().parent().parent().parent().find("span#count").html(j)
    $(Obj).parent().remove();
}

function plusHostParentOption(Obj) {
    var countParent = 0;
    liObj = $("<li/>");
    imgObj = $("<img/>");
    liObj.append($(Obj).attr("name"));
    imgObj.attr("src", "images/minus16.png").attr("class", "minus").attr("alt", "-").attr("id", $(Obj).attr("id")).attr("name", $(Obj).attr("name")).click(function () {
        minusHostParentOption(this)
    })
    liObj.append(imgObj);
    $(Obj).parent().parent().parent().parent().find("div.selected").find("ul").append(liObj);
    hdval = $(Obj).parent().parent().parent().parent().find("input[name='sp']").val()
    if ($.trim(hdval) == "") {
        $(Obj).parent().parent().parent().parent().find("input[name='sp']").val($(Obj).attr("id"))
    }
    else {
        $(Obj).parent().parent().parent().parent().find("input[name='sp']").val(hdval + "," + $(Obj).attr("id"))
    }
    countParent = $(Obj).parent().parent().parent().parent().find("span#count").html();
    $(Obj).parent().parent().parent().parent().find("span#count").html(parseInt(countParent) + 1);
    $(Obj).parent().remove();
}


function show_graph_click() {
    totalSelectedGraph = $("#sp").val();
    if (totalSelectedGraph == "") {
        $().toastmessage('showWarningToast', "Please select atleast one graph from dashboard configuration.");
        return false;
    }
    $.ajax({
        type: "post",
        url: "update_show_graph.py?device_type_id=" + deviceTypeId + "&selected_graph=" + $("#sp").val(),
//		data:$(this).serisalize(), // $(this).text?
        cache: false,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                $().toastmessage('showWarningToast', "UNMP Server has encountered an error. Please retry after some time.");
                return;
            }
            if (result.success == 1 || result.success == "1") {
                $().toastmessage('showWarningToast', messages[result.msg]);
                return;
            }
            else {
                specificGenericGraphJson();
            }
        }
    });
}
