/*var errorMessages = {
 'noHost':'No Host Exist',
 'missingDeviceType':'Please shut down the UNMP and reconcile the device',
 'missingNodeType' : 'Node Type missing.Please reconcile the device',
 'masterSlave' : 'Master not exist For this Device',
 'networkUnreachable' : 'Netwrok is Unreachable.Please Try after some time.',
 'exception' : 'System Error Occured.Contact Your Administrator.',
 'noProfile' :"No Profiling Exist",
 'noSite' : 'There is no site for this device',
 'notPingMaster': 'The device is not responsive'
 };

 var json = {};
 var link_tunnel_status = 0
 function deviceList()
 {
 $spinLoading = $("div#spin_loading");		// create object that hold loading circle
 $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
 var device_type = "ap25";
 // this retreive the value of ipaddress textbox
 var ip_address = $("input[id='filter_ip']").val();
 // this retreive the value of macaddress textbox
 var mac_address = $("input[id='filter_mac']").val();
 // this retreive the value of selectdevicetype from select menu
 var selected_device_type = $("select[id='device_type']").val();
 spinStart($spinLoading,$spinMainLoading);
 // this ajax return the call to function get_device_data_table which is in odu_view and pass the ipaddress,macaddress,devicetype with url
 $.ajax({
 type:"get",
 url:"firmware_master_slave_list.py?ip_address=" + ip_address + "&mac_address=" + mac_address + "&selected_device_type=" + selected_device_type,
 success:function(result){
 result = eval('('+ result +')')
 if (result.success == 0)
 {
 if(result.msg == 'noProfile')
 {
 $("#firmware_div").html("No Host Exist");
 }
 else if(result.msg == 'moreProfile')
 {
 parent.main.location = "odu_listing.py?ip_address=" + ip_address + "&mac_address=" + mac_address +
 "&selected_device_type=" + selected_device_type;
 }
 else
 {
 $("#firmware_div").html("");
 alert(result.site);
 var htmlText = "";

 for(var i=0; i<result.site.length;i++)
 {
 alert(result.site[i]["node_type"]);
 // htmlText+="<p>" + String(result.site[i]["node_type"]) + ":" + String(result.site[i]["ip_address"]) + "</p>";
 if(result.site[i]["link_status"]!=2 || result.site[i]["tunnel_status"]!=1)
 {
 link_tunnel_status = link_tunnel_status + 1;
 }

 }

 /*  $("#firmware_div").append(htmlText);
 $("#firmware_table_div").hide();
 if(result.msg!=1)
 {
 $().toastmessage('showErrorToast',errorMessages[result.msg]);
 }
 $("#select_file").toggle(function () {
 selectFirmwareTable();
 },function(){
 $("#firmware_table_div").slideUp();
 });
 $("input[name='upload_new_file']").click(function(){
 uploadFile();
 });
 }
 }
 spinStop($spinLoading,$spinMainLoading);
 }
 });
 }



 function optionSelected(obj)
 {
 var $obj = $(obj);
 if($obj.attr("checked"))
 {
 $("#selected_firmware").val($obj.attr("id"));
 }
 }

 function selectFirmwareTable()
 {
 var device_type = $("input[name='selected_device']").val();
 $.ajax({
 type:"get",
 url:"select_firmware_table.py?device_type=" + device_type,
 success:function(result){
 $("#firmware_table_div").html(result);
 $("#firmware_table_div").slideDown();
 $("input[name='firmware_file']").click(function(){
 optionSelected(this);
 });
 }
 });
 }


 function uploadFile()
 {
 var device_type = $("input[name='selected_device']").val();
 var host_id = $("input[name='host_id']").val();
 $.colorbox(
 {
 href:"update_firmware_view.py?host_id="+host_id+"&device_type="+device_type,
 iframe:true,
 title : "Upload File",
 opacity: 0.4,
 maxWidth: "80%",
 width:"700px",
 height:"700px",
 onClosed:function(){var device_type = $("input[name='selected_device']").val();
 $.ajax({
 type:"get",
 url:"select_firmware_table.py?device_type=" + device_type,
 success:function(result){
 $("#firmware_table_div").html(result);
 }
 });
 },
 overlayClose:false
 });
 }

 $(function(){
 $("input[id='btnSearch']").click(function(){
 //call the device list function on click of search button
 deviceList();
 });
 $("input[id='filter_ip']").keypress(function(){
 $("input[id='filter_mac']").val("");
 })
 deviceList();

 });					*/


$.blueJSON = new Object();
Raphael.fn.drawGrid = function (x, y, w, h, wv, hv, color) {
    color = color || "#000";
    var path = ["M", Math.round(x) + .5, Math.round(y) + .5, "L", Math.round(x + w) + .5, Math.round(y) + .5, Math.round(x + w) + .5, Math.round(y + h) + .5, Math.round(x) + .5, Math.round(y + h) + .5, Math.round(x) + .5, Math.round(y) + .5],
        rowHeight = h / hv,
        columnWidth = w / wv;
    for (var i = 1; i < hv; i++) {
        path = path.concat(["M", Math.round(x) + .5, Math.round(y + i * rowHeight) + .5, "H", Math.round(x + w) + .5]);
    }
    for (i = 1; i < wv; i++) {
        path = path.concat(["M", Math.round(x + i * columnWidth) + .5, Math.round(y) + .5, "V", Math.round(y + h) + .5]);
    }
    return this.path(path.join(",")).attr({stroke: color});
};
$.blueJSON.firmwareFunctions = {
    line: function (obj, pathString, style) {
        obj.path(pathString).attr(style);
    },
    dashLine: function (obj, startX, startY, endX, endY, style, dash) {
        var dashSpace = 2;
        if (startX == endX) {
            for (var i = startY; i <= endY; i += dashSpace) {
                var path = "M" + String(startX) + " " + String(i) + "L" + String(endX) + " " + String(i + dash);
                if (endY < i + dash)
                    path = "M" + String(startX) + " " + String(i) + "L" + String(endX) + " " + String(endY);
                i += dash;
                $.blueJSON.firmwareFunctions.line(obj, path, style);
            }
        }
        else if (startY == endY) {
            for (var i = startX; i <= endX; i += dashSpace) {
                var path = path = "M" + String(i) + " " + String(startY) + "L" + String(i + dash) + " " + String(endY);
                if (endX < i + dash)
                    path = path = "M" + String(i) + " " + String(startY) + "L" + String(endX) + " " + String(endY);
                i += dash;
                $.blueJSON.firmwareFunctions.line(obj, path, style);
            }
        }

    },
    newLine: function (obj, startX, startY, endX, endY, style, lineType) {
        //default line
        var defaultLine = 100;
        var path = path = "M" + String(startX) + " " + String(startY) + "L" + String(startX + 40) + " " + String(startY);
        $.blueJSON.firmwareFunctions.line(obj, path, style);

        var path = path = "M" + String(startX + 60) + " " + String(startY) + "L" + String(startX + defaultLine) + " " + String(startY);
        $.blueJSON.firmwareFunctions.line(obj, path, style);

        startX += defaultLine;
        if (lineType == "solid") {
            var path = path = "M" + String(startX) + " " + String(startY) + "L" + String(startX) + " " + String(endY);
            $.blueJSON.firmwareFunctions.line(obj, path, style);

            path = path = "M" + String(startX) + " " + String(endY) + "L" + String(endX - 110) + " " + String(endY);
            $.blueJSON.firmwareFunctions.line(obj, path, style);

            path = path = "M" + String(endX - 90) + " " + String(endY) + "L" + String(endX) + " " + String(endY);
            $.blueJSON.firmwareFunctions.line(obj, path, style);
        }
        else {
            var dash = 5;
            if (lineType == "dot")
                dash = 5;
            var path = path = "M" + String(startX) + " " + String(startY) + "L" + String(startX) + " " + String(endY);
            $.blueJSON.firmwareFunctions.line(obj, path, style);

            $.blueJSON.firmwareFunctions.dashLine(obj, startX, endY, endX, endY, style, dash);
        }
    },
    reloadAxis: 1,
    reloadObj: null,
    reload: function () {
        $.blueJSON.firmwareFunctions.reloadObj.stop().animate({transform: "r" + String($.blueJSON.firmwareFunctions.reloadAxis * 360)}, 500, $.blueJSON.firmwareFunctions.reload);
        $.blueJSON.firmwareFunctions.reloadAxis++;
    },
    reloadStop: function () {
        $.blueJSON.firmwareFunctions.reloadObj.stop()
        $.blueJSON.firmwareFunctions.reloadAxis = 1;
    }
};
$.blueJSON.firmware = function (options) {
    var options = $.extend({
        ajax: {
            url: "firmware_site.py",
            type: "get",
            data: {}
        },
        chooseFirmwareAjax: {
            url: "firmware_file_list.py",
            type: "get",
            data: {}
        },
        actionFirmwareAjax: {
            url: "start_firmware.py",
            type: "get",
            data: {}
        },
        resetFirmwareAjax: {
            url: "reset_firmware.py",
            type: "get",
            data: {}
        },
        getFirmwareStatus: {
            url: "get_firmware_status.py",
            type: "get",
            data: {}
        },
        otherFunction: {
            uploadNewFirmware: function () {
                alert("Uploading new firmware...");
            }
        },
        containerId: "id",
        footerId: "footer_id",
        selectedFirmware: null,
        selectedFirmwareType: null,
        firmwareStatus: 0,
        frmAjax: null,
        ajaxMainCallObj: null,
        getFirmwareStatusCallObj: null,
        getFirmwareStatusCallTime: 15000,
        ajaxMainCallTime: 15000,
        selectedTab: null,
        font: {
            size: "10px",
            family: "FranklinGothicFSCondensed-1, FranklinGothicFSCondensed-2"
            //family:"'Lucida Grande',Lucida,Arial,sans-serif"
        },
        master: {
            x: 30,
            y: 60,
            oldX: null,
            oldY: null,
            width: 170,
            height: 35,
            radius: 0,
            nextX: 0,
            nextY: 0,
            textX: 70,
            textY: 17,
            normal: {
                backgroundColor: "none",
                border: {
                    width: "0px",
                    color: "",
                    type: "solid"
                },
                text: {
                    color: "#000"
                },
                style: {
                    "fill": "90-#EAEAEA:5-#FAFAFA:95",
                    "fill-opacity": 0.8
                }
            },
            hover: {
                backgroundColor: "none",
                border: {
                    width: "0px",
                    color: "",
                    type: "solid"
                },
                text: {
                    color: "#000"
                },
                style: {
                    "fill": "90-#EAEAEA:5-#FAFAFA:95",
                    "fill-opacity": 1.0
                }
            },
            linkState: {
                connt: {
                    normal: {
                        backgroundColor: "none",
                        border: {
                            width: "1px",
                            color: "",
                            type: "solid"
                        },
                        text: {
                            color: "#000"
                        },
                        style: {
                            "fill": "90-#2CA654:5-#45C56F:95",
                            "fill-opacity": 1.0
                        }
                    },
                    hover: {
                        backgroundColor: "none",
                        border: {
                            width: "1px",
                            color: "",
                            type: "solid"
                        },
                        text: {
                            color: "#000"
                        },
                        style: {
                            "fill": "90-#2CA654:5-#45C56F:95",
                            "fill-opacity": 1.0
                        }
                    }
                },
                partConnt: {
                    normal: {
                        backgroundColor: "none",
                        border: {
                            width: "1px",
                            color: "",
                            type: "solid"
                        },
                        text: {
                            color: "#000"
                        },
                        style: {
                            "fill": "90-#FBB412:5-#FFCB0D:95",
                            "fill-opacity": 1.0
                        }
                    },
                    hover: {
                        backgroundColor: "none",
                        border: {
                            width: "1px",
                            color: "",
                            type: "solid"
                        },
                        text: {
                            color: "#000"
                        },
                        style: {
                            "fill": "90-#FBB412:5-#FFCB0D:95",
                            "fill-opacity": 1.0
                        }
                    }
                },
                disConnt: {
                    normal: {
                        backgroundColor: "none",
                        border: {
                            width: "1px",
                            color: "",
                            type: "solid"
                        },
                        text: {
                            color: "#000"
                        },
                        style: {
                            "fill": "90-#E2261C:5-#E75148:95",
                            "fill-opacity": 1.0
                        }
                    },
                    hover: {
                        backgroundColor: "none",
                        border: {
                            width: "1px",
                            color: "",
                            type: "solid"
                        },
                        text: {
                            color: "#000"
                        },
                        style: {
                            "fill": "90-#E2261C:5-#E75148:95",
                            "fill-opacity": 1.0
                        }
                    }
                }
            }
        },
        slave: {
            x: 500,
            y: 60,
            oldX: null,
            oldY: null,
            width: 170,
            height: 35,
            radius: 0,
            nextX: 0,
            nextY: 70,
            textX: 70,
            textY: 17,
            normal: {
                backgroundColor: "none",
                border: {
                    width: "0px",
                    color: "",
                    type: "solid"
                },
                text: {
                    color: "#000"
                },
                style: {
                    "fill": "90-#EAEAEA:5-#FAFAFA:95",
                    "fill-opacity": 1.0
                }
            },
            hover: {
                backgroundColor: "none",
                border: {
                    width: "0px",
                    color: "",
                    type: "solid"
                },
                text: {
                    color: "#000"
                },
                style: {
                    "fill": "90-#EAEAEA:5-#FAFAFA:95",
                    "fill-opacity": 1.0
                }
            },
            linkState: {
                connt: {
                    normal: {
                        backgroundColor: "none",
                        border: {
                            width: "1px",
                            color: "",
                            type: "solid"
                        },
                        text: {
                            color: "#000"
                        },
                        style: {
                            "fill": "90-#2CA654:5-#45C56F:95",
                            "fill-opacity": 1.0
                        }
                    },
                    hover: {
                        backgroundColor: "none",
                        border: {
                            width: "1px",
                            color: "",
                            type: "solid"
                        },
                        text: {
                            color: "#000"
                        },
                        style: {
                            "fill": "90-#2CA654:5-#45C56F:95",
                            "fill-opacity": 1.0
                        }
                    }
                },
                partConnt: {
                    normal: {
                        backgroundColor: "none",
                        border: {
                            width: "1px",
                            color: "",
                            type: "solid"
                        },
                        text: {
                            color: "#000"
                        },
                        style: {
                            "fill": "90-#FBB412:5-#FFCB0D:95",
                            "fill-opacity": 1.0
                        }
                    },
                    hover: {
                        backgroundColor: "none",
                        border: {
                            width: "1px",
                            color: "",
                            type: "solid"
                        },
                        text: {
                            color: "#000"
                        },
                        style: {
                            "fill": "90-#FBB412:5-#FFCB0D:95",
                            "fill-opacity": 1.0
                        }
                    }
                },
                disConnt: {
                    normal: {
                        backgroundColor: "none",
                        border: {
                            width: "1px",
                            color: "",
                            type: "solid"
                        },
                        text: {
                            color: "#000"
                        },
                        style: {
                            "fill": "90-#E2261C:5-#E75148:95",
                            "fill-opacity": 1.0
                        }
                    },
                    hover: {
                        backgroundColor: "none",
                        border: {
                            width: "1px",
                            color: "",
                            type: "solid"
                        },
                        text: {
                            color: "#000"
                        },
                        style: {
                            "fill": "90-#E2261C:5-#E75148:95",
                            "fill-opacity": 1.0
                        }
                    }
                }
            }
        },
        messageText: {
            type: {
                error: {
                    size: "15px",
                    color: "#BC3123",
                    x: 240,
                    y: 27
                },
                success: {
                    size: "10px",
                    color: "#1E9125",
                    x: 440,
                    y: 27
                },
                warning: {
                    size: "10px",
                    color: "#D6B327",
                    x: 440,
                    y: 27
                },
                notice: {
                    size: "10px",
                    color: "#888888",
                    x: 440,
                    y: 27
                }
            }
        },
        data: {
            site: [],
            device_type: "UBR",
            success: 1,
            msg: "Sorry, Site Not Exist."
        },
        msg: {
            "0": ["Site links are connected.\nYou can update firmware using FTP or CGI.", "#158226"],
            "1": ["Site links are not properly connected.\nYou can't update firware using FTP.", "#CD3133"],

            "2": ["Firmware download done successfully.\n Now you can activate it.", "#158226"],
            "3": ["Firmware download failed.\nPlease try again.", "#CD3133"],
            "4": ["Firmware download failed due to timeout.\nPlease try again.", "#CD3133"],
            "5": ["Firmware download failed due to SNMP failed.\nPlease try again.", "#CD3133"],
            "6": ["Firmware download failed. Device not responding.\nPlease try again.", "#CD3133"],
            "7": ["Firmware downloading....", "#158226"],

            "8": ["Firmware activation done successfully.", "#158226"],
            "9": ["Firmware activation failed.\nPlease try again.", "#CD3133"],
            "10": ["Firmware activation failed due to timeout.\nPlease try again.", "#CD3133"],
            "11": ["Firmware activation failed due to SNMP failed.\nPlease try again.", "#CD3133"],
            "12": ["Firmware activation failed. Device not responding.\nPlease try again.", "#CD3133"],
            "13": ["Firmware activating....", "#158226"],

            "14": ["Please choose firmware.", "#CD3133"],
            "15": ["Before activating you have to download the firmware.", "#CD3133"]
        }
    }, options);


    options.drawSite = function () {
        var $chooseFrDiv = null;
        var $deviceDiv = null;

        var $footerContainer = $("#" + options.footerId).css({"padding-left": "0", "overflow": "hidden"}).html("");

        if (options.master.oldX == null || options.master.oldY == null || options.slave.oldX == null || options.slave.oldY == null) {
            options.master.oldX = options.master.x;
            options.master.oldY = options.master.y;
            options.slave.oldX = options.slave.x;
            options.slave.oldY = options.slave.y;
            $deviceDiv = $("<div/>").addClass("firmware-device-div").hide();
            $deviceDiv.insertBefore($footerContainer);
            $chooseFrDiv = $("<div/>").addClass("firmware-choose-div").hide();
            $chooseFrDiv.insertBefore($footerContainer);
        }
        else {
            options.master.x = options.master.oldX;
            options.master.y = options.master.oldY;
            options.slave.x = options.slave.oldX;
            options.slave.y = options.slave.oldY;
            $chooseFrDiv = $footerContainer.prev();//.slideUp();
            $deviceDiv = $footerContainer.prev().prev();
        }
        // did minus 1 becuase one is master and others are slave
        var gPnlHgt = ((options.data.site.length - 2) * options.slave.height) + ((options.data.site.length - 3) * options.slave.nextY) + options.slave.y;
        var gPnlHgt = gPnlHgt > 360 && gPnlHgt || 360;
        // position X
        var gPnlX = 0;//(options.master.x < options.slave.x && options.master.x || options.slave.x) - 10;
        // position Y
        var gPnlY = 0;//(options.master.y < options.slave.y && options.master.y || options.slave.y) - 10;
        // Spacing B/W Grids
        var gPnlSpc = 5;
        // panal header height
        var gPnlHdrHgt = 35;

        // panal header width
        $("#" + options.containerId).html("").css({"height": gPnlHgt + gPnlHdrHgt});
        r = new Raphael(options.containerId);
        //r.canvas.style.overflow = "scroll";
        r.setSize(r.width, r.height);
        options.rSet = r.set();

        var gPnlWdth = r.width;
        var gPnlHdrWdth = gPnlWdth;

        // creating Grid Panel
        // panal header
        var gPnlHdrR = r.rect(gPnlX, gPnlY, gPnlHdrWdth, gPnlHdrHgt);
        gPnlHdrR.attr({fill: "90-#DADADA-#DDDDDD", "fill-opacity": 0.3});
        gPnlHdrR.attr({stroke: "#808080", 'stroke-width': 1});


        // panal header icon
        for (var cn = 1; cn < 4; cn++) {
            var gPnlHdrIcn = r.rect(gPnlX + 10, gPnlY + 6 + 5 * cn, 17, 3, 2);
            gPnlHdrIcn.attr({"fill": "#555", stroke: "#FFF", 'stroke-width': 1});
        }


        // panal header text
        var gPnlHdrT = r.text(gPnlX + 33, gPnlY + 17, options.data.device_type + " SITE");
        gPnlHdrT.attr({fill: "#555", 'font-weight': 'bold', 'text-anchor': 'start'});

        //panal refresh image
        var gPnlHdrRf = r.image("images/new/refresh2.png", r.width - 30, gPnlY + 7, 20, 20);
        gPnlHdrRf.attr({"fill-opacity": 0.5});
        var gPnlHdrRfR = r.rect(r.width - 30, gPnlY + 7, 20, 20, 10);
        gPnlHdrRfR.attr({fill: "#EEE", "fill-opacity": 0.3, "cursor": "pointer", stroke: "", 'stroke-width': "0px", title: "Reload Site"});
        //gPnlHdrRfR.glowing = gPnlHdrRfR.glow({width:1,color:"#555"});
        gPnlHdrRfR.hover(function () {
            this.attr({'stroke-width': "1px", stroke: "#AAA"});
        },function () {
            this.attr({'stroke-width': "0px", stroke: ""});
        }).click(function () {
                $.blueJSON.firmwareFunctions.reloadAxis = 1;
                $.blueJSON.firmwareFunctions.reloadObj = gPnlHdrRf;
                $.blueJSON.firmwareFunctions.reload();
                options.ajaxMainCall();
            });


        // panel body
        var gPnlHdrR = r.rect(gPnlX, gPnlY + gPnlHdrHgt, gPnlWdth, gPnlHgt);
        gPnlHdrR.attr({"fill": "90-#FFF:5-#FAFAFA:95", "fill-opacity": 1.0});
        gPnlHdrR.attr({stroke: "#808080", 'stroke-width': 1});
        gPnlHdrR.glowing = gPnlHdrR.glow({width: 5});


        r.drawGrid(gPnlX, gPnlY + gPnlHdrHgt, gPnlWdth, gPnlHgt, 20, gPnlHdrHgt / 2, "#EEE");

        // create help tip
        var ht = r.rect(options.master.x, options.master.y + 80, options.master.width + 30, 95, options.master.radius);
        ht.attr({"fill": "90-#FFF:5-#FAFAFA:95", "fill-opacity": 1.0});
        ht.attr({stroke: "", 'stroke-width': 0});
        ht.glowing = ht.glow({width: 7});

        // connected
        var cir = r.circle((options.master.x + 20), (options.master.y + 100), 5);
        cir.attr({fill: options.slave.linkState.connt.normal.backgroundColor, stroke: options.slave.linkState.connt.normal.border.color, 'stroke-width': options.slave.linkState.connt.normal.border.width});
        cir.attr(options.slave.linkState.connt.normal.style);
        cir.glowing = cir.glow({width: 1});
        var t = r.text((options.master.x + 97), (options.master.y + 100), "Assignned and Connected");

        // partially connected
        var cir = r.circle((options.master.x + 20), (options.master.y + 125), 5);
        cir.attr({fill: options.slave.linkState.partConnt.normal.backgroundColor, stroke: options.slave.linkState.partConnt.normal.border.color, 'stroke-width': options.slave.linkState.partConnt.normal.border.width});
        cir.attr(options.slave.linkState.partConnt.normal.style);
        cir.glowing = cir.glow({width: 1});
        var t = r.text((options.master.x + 104), (options.master.y + 125), "Assignned but not Connected");

        // disconnected
        var cir = r.circle((options.master.x + 20), (options.master.y + 150), 5);
        cir.attr({fill: options.slave.linkState.disConnt.normal.backgroundColor, stroke: options.slave.linkState.disConnt.normal.border.color, 'stroke-width': options.slave.linkState.disConnt.normal.border.width});
        cir.attr(options.slave.linkState.disConnt.normal.style);
        cir.glowing = cir.glow({width: 1});
        var t = r.text((options.master.x + 65), (options.master.y + 150), "Disconnected");

        // end - create help tip

        var ftpDisStatus = false;
        var cgiDisStatus = false;

        for (var i = 0; i < options.data.site.length; i++) {
            if (options.data.site[i]["node_type"] == 0) {
                var c = r.rect(options.master.x, options.master.y, options.master.width, options.master.height, options.master.radius);
                var t = r.text(options.master.x + options.master.textX, options.master.y + options.master.textY, options.data.site[i]["ip_address"]);
                var cir = r.circle((options.master.x + options.master.width + 50), (options.master.y + options.master.height / 2), 5);
                var dt = r.rect(options.master.x, options.master.y, 22, options.master.height, options.master.radius);
                dt.attr({fill: "90-#999:5-#AAA:95", stroke: "", 'stroke-width': 0 });

                var dtt = r.text(options.master.x + 11, (options.master.y + options.master.height / 2), "M");
                dtt.attr({fill: "#FAFAFA"});
                dtt.attr({'font-size': "11px", 'font-weight': "bold"});
                //dtt.transform("r270");

                t.attr({'font-size': options.font.size, 'font-family': options.font.family});

                t.host = c.host = options.data.site[i];
                t.host.x = c.host.x = options.master.x;
                t.host.y = c.host.y = options.master.y;
                c.glowing = c.glow({width: 2});
                cir.glowing = cir.glow({width: 2});

                c.attr({fill: options.master.normal.backgroundColor, stroke: options.master.normal.border.color, 'stroke-width': options.master.normal.border.width});
                c.attr(options.master.normal.style);
                if (c.host["link_status"] == 0)	// disconnected
                {
                    var tempDisConn = options.master.linkState.disConnt;
                    cir.attr({fill: tempDisConn.normal.backgroundColor, stroke: tempDisConn.normal.border.color, 'stroke-width': tempDisConn.normal.border.width});
                    cir.attr(tempDisConn.normal.style);
                    t.attr({fill: tempDisConn.normal.text.color});
                    ftpDisStatus = true;
                }
                else if (c.host["link_status"] == 1)	// partially connected
                {
                    var tempPartConn = options.master.linkState.partConnt;
                    cir.attr({fill: tempPartConn.normal.backgroundColor, stroke: tempPartConn.normal.border.color, 'stroke-width': tempPartConn.normal.border.width});
                    cir.attr(tempPartConn.normal.style);
                    t.attr({fill: tempPartConn.normal.text.color});
                    ftpDisStatus = true;
                }
                else if (c.host["link_status"] == 2)	// connected
                {
                    var tempConn = options.master.linkState.connt;
                    cir.attr({fill: tempConn.normal.backgroundColor, stroke: tempConn.normal.border.color, 'stroke-width': tempConn.normal.border.width});
                    cir.attr(tempConn.normal.style);
                    t.attr({fill: tempConn.normal.text.color});
                }
                c.click(function () {
                    deviceDetails(this.host);
                    //this.attr("fill", "#9cc");
                });
                c.node.onmouseover = function () {
                    this.style.cursor = 'pointer';
                    //console.log(String(options));
                };
                t.node.onmouseover = function () {
                    this.style.cursor = 'pointer';
                };
                t.click(function () {
                    deviceDetails(this.host);
                });
                options.master.x = options.master.x + options.master.nextX;
                options.master.y = options.master.y + options.master.nextY;
                options.firmwareStatus = options.data.site[i]["firmware_status"];
                if (options.data.site[i]["firmware_status"] != 0 && options.selectedFirmware == null && options.selectedFirmwareType == null) {
                    options.selectedFirmware = options.data.site[i]["firmware_file_name"]
                    options.selectedFirmwareType = options.data.site[i]["firmware_type"]
                }
            }
            else {
                var c = r.rect(options.slave.x, options.slave.y, options.slave.width, options.slave.height, options.slave.radius);
                var t = r.text(options.slave.x + options.slave.textX, options.slave.y + options.slave.textY, options.data.site[i]["ip_address"]);
                var cir = r.circle((options.slave.x - 100), (options.slave.y + options.slave.height / 2), 5);

                var dt = r.rect(options.slave.x, options.slave.y, 22, options.slave.height, options.slave.radius);
                dt.attr({fill: "90-#999:5-#AAA:95", 'stroke-width': 0, stroke: ""});

                var dtt = r.text(options.slave.x + 11, (options.slave.y + options.slave.height / 2), "S");
                dtt.attr({fill: "#FAFAFA"});
                dtt.attr({'font-size': "11px", 'font-weight': "bold"});
                //dtt.transform("r270");

                t.attr({'font-size': options.font.size, 'font-family': options.font.family});

                t.host = c.host = options.data.site[i];

                c.glowing = c.glow({width: 2});
                cir.glowing = cir.glow({width: 2});

                c.attr({fill: options.slave.normal.backgroundColor, stroke: options.slave.normal.border.color, 'stroke-width': options.slave.normal.border.width});
                c.attr(options.slave.normal.style);

                // create line
                startX = options.master.x + options.master.width;
                startY = options.master.y + options.master.height / 2;
                endX = options.slave.x;
                endY = options.slave.y + options.slave.height / 2;
                var lineStyle = {stroke: "#111", fill: null, "stroke-width": 2};

                if (c.host["link_status"] == 0)	// disconnected
                {
                    var tempDisConn = options.slave.linkState.disConnt;
                    cir.attr({fill: tempDisConn.normal.backgroundColor, stroke: tempDisConn.normal.border.color, 'stroke-width': tempDisConn.normal.border.width});
                    cir.attr(tempDisConn.normal.style);
                    t.attr({fill: tempDisConn.normal.text.color});
                    $.blueJSON.firmwareFunctions.newLine(r, startX, startY, endX, endY, lineStyle, "solid");	//dot
                    ftpDisStatus = true;
                }
                else if (c.host["link_status"] == 1)	// partially connected
                {
                    var tempPartConn = options.slave.linkState.partConnt;
                    cir.attr({fill: tempPartConn.normal.backgroundColor, stroke: tempPartConn.normal.border.color, 'stroke-width': tempPartConn.normal.border.width});
                    cir.attr(tempPartConn.normal.style);
                    t.attr({fill: tempPartConn.normal.text.color});
                    $.blueJSON.firmwareFunctions.newLine(r, startX, startY, endX, endY, lineStyle, "solid");	//dash
                    ftpDisStatus = true;
                }
                else if (c.host["link_status"] == 2)	// connected
                {
                    var tempConn = options.slave.linkState.connt;
                    cir.attr({fill: tempConn.normal.backgroundColor, stroke: tempConn.normal.border.color, 'stroke-width': tempConn.normal.border.width});
                    cir.attr(tempConn.normal.style);
                    t.attr({fill: tempConn.normal.text.color});
                    $.blueJSON.firmwareFunctions.newLine(r, startX, startY, endX, endY, lineStyle, "solid");
                }
                c.click(function () {
                    deviceDetails(this.host);
                    //this.attr("fill", "#9cc");
                });
                c.node.onmouseover = function () {
                    this.style.cursor = 'pointer';
                };
                t.node.onmouseover = function () {
                    this.style.cursor = 'pointer';
                };
                t.click(function () {
                    deviceDetails(this.host);
                })
                options.slave.x = options.slave.x + options.slave.nextX;
                options.slave.y = options.slave.y + options.slave.nextY;
            }
        }

        // normal HTML Starts from here
        // creating option button

        var $ftpDiv = $("<div/>").html("FTP").addClass("firmware-btn");
        var $cgiDiv = $("<div/>").html("CGI").addClass("firmware-btn");
        var $ftpMainDiv = $("<div/>").addClass("firmware-div").hide();
        var $cgiMainDiv = $("<div/>").addClass("firmware-div").hide();
        var $otherMainDiv = $("<div/>").addClass("firmware-other-div");

        if (ftpDisStatus) {
            $ftpDiv.addClass("firmware-btn-disable").removeClass("firmware-btn");
        }
        if (cgiDisStatus) {
            $cgiDiv.addClass("firmware-btn-disable").removeClass("firmware-btn");
            ;
        }

        $ftpDiv.click(function () {
            if (!$ftpDiv.hasClass("firmware-btn-disable")) {
                $cgiDiv.removeClass("firmware-btn-active");
                $ftpDiv.addClass("firmware-btn-active");
                $ftpMainDiv.show();
                $cgiMainDiv.hide();
                options.selectedTab = "FTP";
            }
        });
        $cgiDiv.click(function () {
            if (!$cgiDiv.hasClass("firmware-btn-disable")) {
                $ftpDiv.removeClass("firmware-btn-active");
                $cgiDiv.addClass("firmware-btn-active");
                $ftpMainDiv.hide();
                $cgiMainDiv.show();
                options.selectedTab = "CGI";
            }
        });
        if (options.selectedTab == null) {
            if (!ftpDisStatus) {
                $ftpDiv.click();
            }
            else if (!cgiDisStatus) {
                $cgiDiv.click();
            }
        }
        else {
            if (options.selectedTab == "FTP") {
                $ftpDiv.click();
            }
            else {
                $cgiDiv.click();
            }

        }


        var $chooseFrFtpBtn = $("<button/>").addClass("yo-button").addClass("yo-small").text("Choose Firmware");
        var $chooseFrCgiBtn = $("<button/>").addClass("yo-button").addClass("yo-small").text("Choose Firmware");
        var $frCgiBtn = $("<button/>").addClass("yo-button").addClass("yo-small").text("Update Firmware");
        var $dwnFrFtpBtn = $("<button/>").addClass("yo-button").addClass("yo-small").text("Download Firmware");
        var $actFrFtpBtn = $("<button/>").addClass("yo-button").addClass("yo-small").text("Active Firmware");
        var $uploadFrBtn = $("<button/>").addClass("yo-button").addClass("yo-small").text("Upload New Firmware");

        var abortFirmwareRequest = function () {
            if (options.frmAjax != null) {
                options.frmAjax.abort()
            }
            options.getFirmwareStatusCall();
            //spinStop($spinLoading,$spinMainLoading);
        };
        var firmwareRequest = function (req, dt) {
            clearTimeout(options.ajaxMainCallObj);
            options.frmAjax = $.ajax({
                type: options.actionFirmwareAjax.type,
                url: options.actionFirmwareAjax.url,
                data: $.extend(dt, options.actionFirmwareAjax.data),
                success: function (result) {
                    if (req == "ftpDwn") {
                        var msg = "";
                        if (result.success == 0) {
                            for (var resI = 0; resI < result.result.length; resI++) {
                                msg += result.result[resI]["msg"] + " for " + result.result[resI]["ip_address"] + "";
                            }
                        }
                        else {
                            msg += String(result.result);
                        }
                        if (msg != "") {
                            $.prompt(String(msg), {prefix: 'jqismooth'});
                            options.mainMsg.attr({'text': options.msg["3"][0], 'fill': options.msg["3"][1]});
                            $chooseFrFtpBtn.attr("disabled", false).removeClass("disabled");
                            $chooseFrCgiBtn.attr("disabled", false).removeClass("disabled");
                            $frCgiBtn.attr("disabled", false).removeClass("disabled");
                            $dwnFrFtpBtn.attr("disabled", false).removeClass("disabled");
                            $actFrFtpBtn.attr("disabled", true).addClass("disabled");
                            $uploadFrBtn.attr("disabled", false).removeClass("disabled");
                        }
                    }
                    else if (req == "ftpAct") {
                        options.mainMsg.attr({'text': options.msg["13"][0], 'fill': options.msg["13"][1]});
                    }
                    else {
                        options.mainMsg.attr({'text': options.msg["3"][0], 'fill': options.msg["3"][1]});
                    }
                    options.frmAjax = null;
                }
            });
            setTimeout(function () {
                abortFirmwareRequest()
            }, 10000);
        };

        var fetchFirmwareList = function (conObj) {
            $.ajax({
                type: options.chooseFirmwareAjax.type,
                url: options.chooseFirmwareAjax.url,
                data: options.chooseFirmwareAjax.data,
                success: function (result) {
                    conObj.html("");
                    if (result.success == 0) {
                        var $table = $("<table/>").addClass("yo-table").attr({"cellspacing": 0, "cellpadding": 0, "width": "100%"});
                        var $tr = $("<tr/>").addClass("yo-table-head");
                        $("<th/>").addClass("vertline").html("&nbsp;").appendTo($tr);
                        $("<th/>").addClass("vertline").html("Firmware Name").appendTo($tr);
                        $("<th/>").addClass("vertline").html("Firmware Path").appendTo($tr);
                        $tr.appendTo($table);
                        for (var d in result.firmware) {
                            if (result.firmware[d].length == 2) {
                                var $tr = $("<tr/>")
                                $("<input/>").attr({"type": "radio", "name": "frm_name", "value": result.firmware[d][0]})
                                    .appendTo($("<td/>").css("width", "10%").addClass("vertline").appendTo($tr)).click(function () {
                                        var $this = $(this);
                                        if ($this.attr("checked")) {
                                            options.selectedFirmware = $this.val();
                                            options.selectedFirmwareType = $ftpDiv.hasClass("firmware-btn-active") && "FTP" || "CGI"
                                            updateFirmwareMsg();
                                            $chooseFrFtpBtn.click();
                                        }
                                    }).attr("checked", options.selectedFirmware == result.firmware[d][0] && true || false);
                                $("<td/>").css("width", "30%").addClass("vertline").html(result.firmware[d][0]).appendTo($tr);
                                $("<td/>").css("width", "60%").addClass("vertline").html(result.firmware[d][1]).appendTo($tr);
                                $tr.appendTo($table);
                            }
                        }
                        $table.appendTo(conObj);
                    }
                    else {
                        conObj.html("<div class='firmware-error'>" + result.msg + "</div>")
                    }
                }
            });
        };

        var resetFirmwareSite = function () {
            var dd = {};
            dd.status = "done";
            dd.host_ids = [];
            dd.host_ips = [];
            dd.node_types = [];
            for (var siteI = 0; siteI < options.data.site.length; siteI++) {
                dd.host_ids[dd.host_ids.length] = options.data.site[siteI]["host_id"];
                dd.host_ips[dd.host_ips.length] = options.data.site[siteI]["ip_address"];
                dd.node_types[dd.node_types.length] = options.data.site[siteI]["node_type"];
            }
            dd.device_type = options.device_type;
            dd.firmware_file = options.selectedFirmware;
            clearTimeout(options.ajaxMainCallObj);
            $.ajax({
                type: options.resetFirmwareAjax.type,
                url: options.resetFirmwareAjax.url,
                data: $.extend(dd, options.resetFirmwareAjax.data),
                success: function (result) {
                    if (result.success != 0) {
                        $.prompt(String("Site reloading has a problem. Please try again later."), {prefix: 'jqismooth'});
                    }
                    else {
                        options.selectedFirmware = null;
                        options.selectedFirmwareType = null;
                        options.selectedFirmwareRObj = null;
                        //options.ajaxMainCall();
                    }
                },
                complete: function () {
                    options.getFirmwareStatusCallObj = setTimeout(function () {
                        options.getFirmwareStatusCall()
                    }, options.getFirmwareStatusCallTime);
                }
            });
        };

        $uploadFrBtn.click(function () {
            options.otherFunction.uploadNewFirmware();
        });
        $chooseFrFtpBtn.click(function () {
            if ($chooseFrDiv.css("display") == 'none') {
                fetchFirmwareList($chooseFrDiv);
                $chooseFrDiv.slideDown();
            }
            else {
                $chooseFrDiv.slideUp();
            }
        });
        $chooseFrCgiBtn.toggle(function () {
            $chooseFrFtpBtn.click();
        }, function () {
            $chooseFrFtpBtn.click();
        });
        $chooseFrCgiBtn.appendTo($cgiMainDiv);
        $chooseFrFtpBtn.appendTo($ftpMainDiv);

        $dwnFrFtpBtn.click(function () {
            if (options.selectedFirmware == null) {
                $.prompt(String(options.msg["14"][0]), {prefix: 'jqismooth'});
            }
            else {
                options.selectedFirmwareType = options.selectedTab;
                var dd = {};
                dd.type = "ftpdownload";
                dd.host_ids = [];
                dd.host_ips = [];
                dd.node_types = [];
                for (var siteI = 0; siteI < options.data.site.length; siteI++) {
                    dd.host_ids[dd.host_ids.length] = options.data.site[siteI]["host_id"];
                    dd.host_ips[dd.host_ips.length] = options.data.site[siteI]["ip_address"];
                    dd.node_types[dd.node_types.length] = options.data.site[siteI]["node_type"];
                }
                dd.host_ids = String(dd.host_ids);
                dd.host_ips = String(dd.host_ips);
                dd.node_types = String(dd.node_types);
                dd.device_type = options.data.device_type;
                dd.firmware_file = options.selectedFirmware;
                options.mainMsg.attr({'text': options.msg["7"][0], 'fill': options.msg["7"][1]});
                $chooseFrFtpBtn.attr("disabled", true).addClass("disabled");
                $chooseFrCgiBtn.attr("disabled", true).addClass("disabled");
                $frCgiBtn.attr("disabled", true).addClass("disabled");
                $dwnFrFtpBtn.attr("disabled", true).addClass("disabled");
                $actFrFtpBtn.attr("disabled", true).addClass("disabled");
                $uploadFrBtn.attr("disabled", true).addClass("disabled");
                updateFirmwareMsg();
                firmwareRequest("ftpDwn", dd);
            }
        });
        $frCgiBtn.click(function () {
            if (options.selectedFirmware == null) {
                $.prompt(String(options.msg["14"][0]), {prefix: 'jqismooth'});
            }
            else {
                options.selectedFirmwareType = options.selectedTab;
                var dd = {};
                dd.type = "cgi";
                dd.host_ids = [];
                dd.host_ips = [];
                dd.node_types = [];
                for (var siteI = 0; siteI < options.data.site.length; siteI++) {
                    dd.host_ids[dd.host_ids.length] = options.data.site[siteI]["host_id"];
                    dd.host_ips[dd.host_ips.length] = options.data.site[siteI]["ip_address"];
                    dd.node_types[dd.node_types.length] = options.data.site[siteI]["node_type"];
                }
                dd.host_ids = String(dd.host_ids);
                dd.host_ips = String(dd.host_ips);
                dd.node_types = String(dd.node_types);
                dd.device_type = options.data.device_type;
                dd.firmware_file = options.selectedFirmware;
                options.mainMsg.attr({'text': options.msg["7"][0], 'fill': options.msg["7"][1]});
                $chooseFrFtpBtn.attr("disabled", true).addClass("disabled");
                $chooseFrCgiBtn.attr("disabled", true).addClass("disabled");
                $frCgiBtn.attr("disabled", true).addClass("disabled");
                $dwnFrFtpBtn.attr("disabled", true).addClass("disabled");
                $actFrFtpBtn.attr("disabled", true).addClass("disabled");
                $uploadFrBtn.attr("disabled", true).addClass("disabled");
                updateFirmwareMsg();
                firmwareRequest("cgiDwn", dd);
            }
        });
        $actFrFtpBtn.click(function () {
            if (options.selectedFirmware == null) {
                $.prompt(String(options.msg["14"][0]), {prefix: 'jqismooth'});
            }
            else {
                if (options.firmwareStatus == 1 || options.firmwareStatus == 9 || options.firmwareStatus == 10 || options.firmwareStatus == 11 || options.firmwareStatus == 12 || options.firmwareStatus == 13) {
                    var dd = {};
                    dd.type = "ftpactivate";
                    dd.host_ids = [];
                    dd.host_ips = [];
                    dd.node_types = [];
                    for (var siteI = 0; siteI < options.data.site.length; siteI++) {
                        dd.host_ids[dd.host_ids.length] = options.data.site[siteI]["host_id"];
                        dd.host_ips[dd.host_ips.length] = options.data.site[siteI]["ip_address"];
                        dd.node_types[dd.node_types.length] = options.data.site[siteI]["node_type"];
                    }
                    dd.host_ids = String(dd.host_ids);
                    dd.host_ips = String(dd.host_ips);
                    dd.node_types = String(dd.node_types);
                    dd.device_type = options.data.device_type;
                    dd.firmware_file = options.selectedFirmware;
                    options.mainMsg.attr({'text': options.msg["13"][0], 'fill': options.msg["13"][1]});
                    $chooseFrFtpBtn.attr("disabled", true).addClass("disabled");
                    $chooseFrCgiBtn.attr("disabled", true).addClass("disabled");
                    $frCgiBtn.attr("disabled", true).addClass("disabled");
                    $dwnFrFtpBtn.attr("disabled", true).addClass("disabled");
                    $actFrFtpBtn.attr("disabled", true).addClass("disabled");
                    $uploadFrBtn.attr("disabled", true).addClass("disabled");
                    firmwareRequest("ftpAct", dd);
                }
                else {
                    $.prompt(String(options.msg["15"][0]), {prefix: 'jqismooth'});
                }
            }
        });

        $frCgiBtn.appendTo($cgiMainDiv);
        $dwnFrFtpBtn.appendTo($ftpMainDiv);
        $actFrFtpBtn.appendTo($ftpMainDiv);
        $uploadFrBtn.appendTo($otherMainDiv);

        $ftpDiv.appendTo($footerContainer);
        $ftpMainDiv.appendTo($footerContainer);
        $cgiMainDiv.appendTo($footerContainer);
        $cgiDiv.appendTo($footerContainer);
        $otherMainDiv.appendTo($footerContainer);

        // msg
        if (options.firmwareStatus == 0) {
            if (ftpDisStatus) {
                options.mainMsg = r.text(options.master.x, options.master.y + 200, options.msg["1"][0]);
                options.mainMsg.attr({fill: options.msg["1"][1], 'text-anchor': 'start'});
            }
            else {
                options.mainMsg = r.text(options.master.x, options.master.y + 200, options.msg["0"][0]);
                options.mainMsg.attr({fill: options.msg["0"][1], 'text-anchor': 'start'});
            }
            //.attr("disabled",false).removeClass("disabled");
            //.attr("disabled",true).addClass("disabled");
            $chooseFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $chooseFrCgiBtn.attr("disabled", false).removeClass("disabled");
            $frCgiBtn.attr("disabled", false).removeClass("disabled");
            $dwnFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $actFrFtpBtn.attr("disabled", true).addClass("disabled");
            $uploadFrBtn.attr("disabled", false).removeClass("disabled");
        }
        else if (options.firmwareStatus == 1) {
            options.mainMsg = r.text(options.master.x, options.master.y + 200, options.msg["2"][0]);
            options.mainMsg.attr({fill: options.msg["2"][1], 'text-anchor': 'start'});
            $chooseFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $chooseFrCgiBtn.attr("disabled", false).removeClass("disabled");
            $frCgiBtn.attr("disabled", false).removeClass("disabled");
            $dwnFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $actFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $uploadFrBtn.attr("disabled", false).removeClass("disabled");
        }
        else if (options.firmwareStatus == 2) {
            options.mainMsg = r.text(options.master.x, options.master.y + 200, options.msg["3"][0]);
            options.mainMsg.attr({fill: options.msg["3"][1], 'text-anchor': 'start'});
            $chooseFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $chooseFrCgiBtn.attr("disabled", false).removeClass("disabled");
            $frCgiBtn.attr("disabled", false).removeClass("disabled");
            $dwnFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $actFrFtpBtn.attr("disabled", true).addClass("disabled");
            $uploadFrBtn.attr("disabled", false).removeClass("disabled");
        }
        else if (options.firmwareStatus == 3) {
            options.mainMsg = r.text(options.master.x, options.master.y + 200, options.msg["4"][0]);
            options.mainMsg.attr({fill: options.msg["4"][1], 'text-anchor': 'start'});
            $chooseFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $chooseFrCgiBtn.attr("disabled", false).removeClass("disabled");
            $frCgiBtn.attr("disabled", false).removeClass("disabled");
            $dwnFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $actFrFtpBtn.attr("disabled", true).addClass("disabled");
            $uploadFrBtn.attr("disabled", false).removeClass("disabled");
        }
        else if (options.firmwareStatus == 4) {
            options.mainMsg = r.text(options.master.x, options.master.y + 200, options.msg["5"][0]);
            options.mainMsg.attr({fill: options.msg["5"][1], 'text-anchor': 'start'});
            $chooseFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $chooseFrCgiBtn.attr("disabled", false).removeClass("disabled");
            $frCgiBtn.attr("disabled", false).removeClass("disabled");
            $dwnFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $actFrFtpBtn.attr("disabled", true).addClass("disabled");
            $uploadFrBtn.attr("disabled", false).removeClass("disabled");
        }
        else if (options.firmwareStatus == 5) {
            options.mainMsg = r.text(options.master.x, options.master.y + 200, options.msg["6"][0]);
            options.mainMsg.attr({fill: options.msg["6"][1], 'text-anchor': 'start'});
            $chooseFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $chooseFrCgiBtn.attr("disabled", false).removeClass("disabled");
            $frCgiBtn.attr("disabled", false).removeClass("disabled");
            $dwnFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $actFrFtpBtn.attr("disabled", true).addClass("disabled");
            $uploadFrBtn.attr("disabled", false).removeClass("disabled");
        }
        else if (options.firmwareStatus == 6) {
            options.mainMsg = r.text(options.master.x, options.master.y + 200, options.msg["7"][0]);
            options.mainMsg.attr({fill: options.msg["7"][1], 'text-anchor': 'start'});
            $chooseFrFtpBtn.attr("disabled", true).addClass("disabled");
            $chooseFrCgiBtn.attr("disabled", true).addClass("disabled");
            $frCgiBtn.attr("disabled", true).addClass("disabled");
            $dwnFrFtpBtn.attr("disabled", true).addClass("disabled");
            $actFrFtpBtn.attr("disabled", true).addClass("disabled");
            $uploadFrBtn.attr("disabled", true).addClass("disabled");
        }
        else if (options.firmwareStatus == 11) {
            options.mainMsg = r.text(options.master.x, options.master.y + 200, options.msg["8"][0]);
            options.mainMsg.attr({fill: options.msg["8"][1], 'text-anchor': 'start'});
            $chooseFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $chooseFrCgiBtn.attr("disabled", false).removeClass("disabled");
            $frCgiBtn.attr("disabled", false).removeClass("disabled");
            $dwnFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $actFrFtpBtn.attr("disabled", true).addClass("disabled");
            $uploadFrBtn.attr("disabled", false).removeClass("disabled");
            //if(options.getFirmwareStatusCallObj !=null)
            //setTimeout(function(){clearTimeout(options.getFirmwareStatusCallObj);},5000);
            //setTimeout(function(){
            /*$.prompt("Firmware updated successfully for this site.",
             {
             buttons:{OK:true},
             prefix:'jqismooth',
             callback:function(v,m) {
             if(v != undefined && v==true)
             {
             resetFirmwareSite();
             }
             else
             {
             resetFirmwareSite();
             }
             }
             });*/
            //},5000);
        }
        else if (options.firmwareStatus == 12) {
            options.mainMsg = r.text(options.master.x, options.master.y + 200, options.msg["9"][0]);
            options.mainMsg.attr({fill: options.msg["9"][1], 'text-anchor': 'start'});
            $chooseFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $chooseFrCgiBtn.attr("disabled", false).removeClass("disabled");
            $frCgiBtn.attr("disabled", false).removeClass("disabled");
            $dwnFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $actFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $uploadFrBtn.attr("disabled", false).removeClass("disabled");
        }
        else if (options.firmwareStatus == 13) {
            options.mainMsg = r.text(options.master.x, options.master.y + 200, options.msg["10"][0]);
            options.mainMsg.attr({fill: options.msg["10"][1], 'text-anchor': 'start'});
            $chooseFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $chooseFrCgiBtn.attr("disabled", false).removeClass("disabled");
            $frCgiBtn.attr("disabled", false).removeClass("disabled");
            $dwnFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $actFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $uploadFrBtn.attr("disabled", false).removeClass("disabled");
        }
        else if (options.firmwareStatus == 14) {
            options.mainMsg = r.text(options.master.x, options.master.y + 200, options.msg["11"][0]);
            options.mainMsg.attr({fill: options.msg["11"][1], 'text-anchor': 'start'});
            $chooseFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $chooseFrCgiBtn.attr("disabled", false).removeClass("disabled");
            $frCgiBtn.attr("disabled", false).removeClass("disabled");
            $dwnFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $actFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $uploadFrBtn.attr("disabled", false).removeClass("disabled");
        }
        else if (options.firmwareStatus == 15) {
            options.mainMsg = r.text(options.master.x, options.master.y + 200, options.msg["12"][0]);
            options.mainMsg.attr({fill: options.msg["12"][1], 'text-anchor': 'start'});
            $chooseFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $chooseFrCgiBtn.attr("disabled", false).removeClass("disabled");
            $frCgiBtn.attr("disabled", false).removeClass("disabled");
            $dwnFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $actFrFtpBtn.attr("disabled", false).removeClass("disabled");
            $uploadFrBtn.attr("disabled", false).removeClass("disabled");
        }
        else if (options.firmwareStatus == 16) {
            options.mainMsg = r.text(options.master.x, options.master.y + 200, options.msg["13"][0]);
            options.mainMsg.attr({fill: options.msg["13"][1], 'text-anchor': 'start'});
            $chooseFrFtpBtn.attr("disabled", true).addClass("disabled");
            $chooseFrCgiBtn.attr("disabled", true).addClass("disabled");
            $frCgiBtn.attr("disabled", true).addClass("disabled");
            $dwnFrFtpBtn.attr("disabled", true).addClass("disabled");
            $actFrFtpBtn.attr("disabled", true).addClass("disabled");
            $uploadFrBtn.attr("disabled", true).addClass("disabled");
        }

        if (options.selectedFirmware != null) {
            options.selectedFirmwareRObj = r.text(options.master.x, options.master.y + 250, "Selected Firmware: " + options.selectedFirmware + "\nFirmware Type: " + options.selectedFirmwareType);
            options.selectedFirmwareRObj.attr({fill: "#111", 'text-anchor': 'start'});
        }

        var updateFirmwareMsg = function () {
            if (options.selectedFirmwareRObj == undefined) {
                options.selectedFirmwareRObj = r.text(options.master.x, options.master.y + 250, "Selected Firmware: " + options.selectedFirmware + "\nFirmware Type: " + options.selectedFirmwareType);
                options.selectedFirmwareRObj.attr({fill: "#111", 'text-anchor': 'start'});
            }
            else {
                options.selectedFirmwareRObj.attr({text: "Selected Firmware: " + options.selectedFirmware + "\nFirmware Type: " + options.selectedFirmwareType})
            }
        }

        var deviceDetails = function (hostObj) {
            var $table = $("<table/>").addClass("tt-table").attr({'cellspacing': "0", 'cellpadding': "0", 'width': "100%"});
            var $tr = $("<tr/>");
            $("<img/>").addClass("img-link").attr("src", "images/new/close.png").css({"float": "right", "margin-right": "10px"}).appendTo($("<th/>").addClass("cell-title").attr("colspan", "2").html("Host Details").appendTo($tr)).click(function () {
                $deviceDiv.slideUp();
            });
            $tr.appendTo($table);

            $tr = $("<tr/>");
            $("<td/>").addClass("cell-label").css("width", "100px").html("IP Address").appendTo($tr);
            $("<td/>").addClass("cell-info").html(hostObj["ip_address"]).appendTo($tr);
            $tr.appendTo($table);

            $tr = $("<tr/>");
            $("<td/>").addClass("cell-label").css("width", "100px").html("MAC Address").appendTo($tr);
            $("<td/>").addClass("cell-info").html(hostObj["mac_address"]).appendTo($tr);
            $tr.appendTo($table);

            $tr = $("<tr/>");
            $("<td/>").addClass("cell-label").css("width", "100px").html("Node Type").appendTo($tr);
            $("<td/>").addClass("cell-info").html(hostObj["node_type"] == 0 && "Master" || "Slave").appendTo($tr);
            $tr.appendTo($table);

            $tr = $("<tr/>");
            $("<td/>").addClass("cell-label").css("width", "100px").html("Link Status").appendTo($tr);
            $("<td/>").addClass("cell-info").html(hostObj["link_status"] == 2 && "Connected" || "Disconnected").appendTo($tr);
            $tr.appendTo($table);

            $tr = $("<tr/>");
            $("<td/>").addClass("cell-label").css("width", "100px").html("Firmware Status").appendTo($tr);
            if (hostObj["firmware_status"] == 0) {
                $("<td/>").addClass("cell-info").html(" - ").appendTo($tr);
            }
            else if (hostObj["firmware_status"] == 1) {
                $("<td/>").addClass("cell-info").html("Download Successfully").appendTo($tr);
            }
            else if (hostObj["firmware_status"] == 2) {
                $("<td/>").addClass("cell-info").html("Download Failed").appendTo($tr);
            }
            else if (hostObj["firmware_status"] == 3) {
                $("<td/>").addClass("cell-info").html("Device Timeout").appendTo($tr);
            }
            else if (hostObj["firmware_status"] == 4) {
                $("<td/>").addClass("cell-info").html("SNMP Failed").appendTo($tr);
            }
            else if (hostObj["firmware_status"] == 5) {
                $("<td/>").addClass("cell-info").html("Device Not Responding").appendTo($tr);
            }
            else if (hostObj["firmware_status"] == 6) {
                $("<td/>").addClass("cell-info").html("Downloading...").appendTo($tr);
            }
            else if (hostObj["firmware_status"] == 11) {
                $("<td/>").addClass("cell-info").html("Activation Successfully").appendTo($tr);
            }
            else if (hostObj["firmware_status"] == 12) {
                $("<td/>").addClass("cell-info").html("Activation Failed").appendTo($tr);
            }
            else if (hostObj["firmware_status"] == 13) {
                $("<td/>").addClass("cell-info").html("Device Timeout").appendTo($tr);
            }
            else if (hostObj["firmware_status"] == 14) {
                $("<td/>").addClass("cell-info").html("SNMP Failed").appendTo($tr);
            }
            else if (hostObj["firmware_status"] == 15) {
                $("<td/>").addClass("cell-info").html("Device Not Responding").appendTo($tr);
            }
            else if (hostObj["firmware_status"] == 16) {
                $("<td/>").addClass("cell-info").html("Activating...").appendTo($tr);
            }
            $tr.appendTo($table);

            $tr = $("<tr/>");
            $("<td/>").addClass("cell-label").css("width", "100px").html("Firmware File Name").appendTo($tr);
            $("<td/>").addClass("cell-info").html(hostObj["firmware_file_name"]).appendTo($tr);
            $tr.appendTo($table);

            $tr = $("<tr/>");
            $("<td/>").addClass("cell-label").css("width", "100px").html("Firmware Type").appendTo($tr);
            $("<td/>").addClass("cell-info").html(String(hostObj["firmware_type"]).toUpperCase()).appendTo($tr);
            $tr.appendTo($table);

            $tr = $("<tr/>");
            $("<td/>").addClass("cell-label").css("width", "100px").html("Update Time").appendTo($tr);
            $("<td/>").addClass("cell-info").html(hostObj["firmware_time"]).appendTo($tr);
            $tr.appendTo($table);

            $tr = $("<tr/>");
            $("<td/>").addClass("cell-label").css("width", "100px").html("Message").appendTo($tr);
            $("<td/>").addClass("cell-info").html(hostObj["firmware_msg"]).appendTo($tr);
            $tr.appendTo($table);

            $deviceDiv.html("");
            $table.appendTo($deviceDiv);
            $deviceDiv.slideDown();
        };
        /*options.ftpbtn =
         options.ftpbtn.appendTo($("#" + options.containerId));


         options.ftpbtn = $("<button/>").addClass("yo-button").addClass("yo-small").css({"position":"absolute","top":"241px","left":"30px"}).text("Activate Software(FTP)").attr("disabled",ftpDisStatus).addClass(ftpDisStatus && "disabled" || "").hide();
         options.ftpbtn.appendTo($("#" + options.containerId));

         options.cgibtn = $("<button/>").addClass("yo-button").addClass("yo-small").css({"position":"absolute","top":"241px","left":"175px","min-width":"40px"}).text("CGI").attr("disabled",cgiDisStatus).addClass(cgiDisStatus && "disabled" || "");;
         options.cgibtn.appendTo($("#" + options.containerId));
         */

        // device details box
        /*
         options.deviceDetails = {}
         options.deviceDetails.x = options.master.x +300
         options.deviceDetails.y = options.master.y+80
         options.deviceDetails.width = options.master.width+140;
         options.deviceDetails.height = 150
         options.deviceDetails.radius = 2

         // main box

         options.deviceDetails.main = r.rect(options.deviceDetails.x,options.deviceDetails.y,options.deviceDetails.width,options.deviceDetails.height,6);

         /*r.path(
         "M" + String(options.deviceDetails.x) + "," + String(options.deviceDetails.y) +
         "L" + String(options.deviceDetails.x + options.deviceDetails.width) + "," + String(options.deviceDetails.y) +
         "L" + String(options.deviceDetails.x + options.deviceDetails.width) + "," + String(options.deviceDetails.y + options.deviceDetails.height) +
         "L" + String(options.deviceDetails.x) + "," + String(options.deviceDetails.y + options.deviceDetails.height) +
         "L" + String(options.deviceDetails.x) + "," + String(options.deviceDetails.y + 22) +
         "L" + String(options.deviceDetails.x - 20) + "," + String(options.deviceDetails.y + 17) +
         "L" + String(options.deviceDetails.x) + "," + String(options.deviceDetails.y + 12) +
         "L" + String(options.deviceDetails.x) + "," + String(options.deviceDetails.y)
         );*/

        /*
         options.deviceDetails.main.attr({"fill":"90-#FFF:5-#FFF:95","fill-opacity": 0.9,stroke:"#666",'stroke-width':"1px","overflow":"hidden"});
         options.deviceDetails.main.glowing = options.deviceDetails.main.glow({width:5,color:"#AAA",fill:true});
         options.rSet.push(options.deviceDetails.main);

         // main box design
         options.deviceDetails.bd = r.rect(options.deviceDetails.x + 1, options.deviceDetails.y + 1, 22, 32);
         options.deviceDetails.bd.attr({fill: "90-#FFF:5-#EEE:95","fill-opacity": 0.8, 'stroke-width': 0});
         //options.deviceDetails.bd.glowing = options.deviceDetails.bd.glow({color:"#EEE",width:2});
         options.rSet.push(options.deviceDetails.bd);

         // device state
         /*
         options.deviceDetails.ds = r.circle(options.deviceDetails.x + 15, options.deviceDetails.y + 16, 5);
         options.deviceDetails.ds.attr({fill: options.master.linkState.disConnt.normal.backgroundColor, stroke:options.master.linkState.disConnt.normal.border.color, 'stroke-width': options.master.linkState.disConnt.normal.border.width});
         options.deviceDetails.ds.attr(options.master.linkState.disConnt.normal.style);
         options.rSet.push(options.deviceDetails.ds);
         */

        // head design
        /*options.deviceDetails.hd = r.rect(options.deviceDetails.x+1,options.deviceDetails.y + 1,options.deviceDetails.width-1,32);
         options.deviceDetails.hd.attr({"fill":"90-#FFF:5-#EEE:95","fill-opacity": 0.8, 'stroke-width': 0});
         options.deviceDetails.hd.glowing = options.deviceDetails.hd.glow({color:"#EEE",width:2});
         options.rSet.push(options.deviceDetails.hd);
         */
        /*
         // head text
         options.deviceDetails.headText = t = r.text(options.deviceDetails.x + 12 , options.deviceDetails.y + 15, "Host Details:");
         options.deviceDetails.headText.attr({"font-weight":"bold","color":"#AAA",'text-anchor': 'start'});
         options.rSet.push(options.deviceDetails.headText);


         */

        // end - device details box
    };
    options.ajaxMainCall = function () {
        spinStart($spinLoading, $spinMainLoading);
        if (options.getFirmwareStatusCallObj != null)
            clearTimeout(options.getFirmwareStatusCallObj);
        if (options.ajaxMainCallObj != null)
            clearTimeout(options.ajaxMainCallObj);
        $.ajax({
            type: options.ajax.type,
            url: options.ajax.url,
            data: options.ajax.data,
            success: function (result) {
                options.data = result;
                if (options.data.success == 0) {
                    options.drawSite();
                }
                else {
                    $("#" + options.containerId).html("").css({"height": "100%"});
                    r = new Raphael(options.containerId);
                    var t = r.text(options.messageText.type.error.x, options.messageText.type.error.y, options.data.msg);
                    t.attr({'font-size': options.messageText.type.error.size, 'font-family': options.font.family});
                    t.attr("fill", options.messageText.type.error.color);
                }
            },
            complete: function () {
                //options.ajaxMainCallObj = setTimeout(function(){options.ajaxMainCall()},options.ajaxMainCallTime);
                options.getFirmwareStatusCallObj = setTimeout(function () {
                    options.getFirmwareStatusCall()
                }, options.getFirmwareStatusCallTime);
                spinStop($spinLoading, $spinMainLoading);
            }
        });
    };
    options.getFirmwareStatusCall = function () {
        if (options.getFirmwareStatusCallObj != null)
            clearTimeout(options.getFirmwareStatusCallObj);
        if (options.ajaxMainCallObj != null)
            clearTimeout(options.ajaxMainCallObj);
        var host_ids = [];
        for (var i = 0; i < options.data.site.length; i++) {
            host_ids[host_ids.length] = options.data.site[i]["host_id"];
        }
        $.ajax({
            type: options.getFirmwareStatus.type,
            url: options.getFirmwareStatus.url,
            data: $.extend(options.getFirmwareStatus.data, {"host_ids": String(host_ids)}),
            success: function (result) {
                //{"result": {"72": ["1", " Software download completed confirm by snmp "], "71": ["1", " Software download completed confirm by snmp "]}, "success": 0}
                for (var i = 0; i < options.data.site.length; i++) {
                    if (result.result[options.data.site[i]["host_id"]] != undefined)
                        options.data.site[i]["firmware_status"] = result.result[options.data.site[i]["host_id"]][0];
                    options.data.site[i]["firmware_msg"] = result.result[options.data.site[i]["host_id"]][1];
                }
                if (options.data.success == 0) {
                    options.drawSite();
                }
                else {
                    $("#" + options.containerId).html("").css({"height": "100%"});
                    r = new Raphael(options.containerId);
                    var t = r.text(options.messageText.type.error.x, options.messageText.type.error.y, options.data.msg);
                    t.attr({'font-size': options.messageText.type.error.size, 'font-family': options.font.family});
                    t.attr("fill", options.messageText.type.error.color);
                }
            },
            complete: function () {
                options.getFirmwareStatusCallObj = setTimeout(function () {
                    options.getFirmwareStatusCall()
                }, options.getFirmwareStatusCallTime);
            }
        });
    };
    options.ajaxMainCall();

    //r.circle(330, 300, 600).animate({fill: "#EEEEEE", stroke: "#000", "stroke-width": 60, "stroke-opacity": 0.5}, 2000);
    /*
     var c = r.rect(200,10,80,35,3);
     c.attr({fill: '#9cf', stroke:'#ddd','stroke-width': 3});
     c.click(function(){
     c.attr("fill", "green");
     });
     c.node.onmouseover = function(){
     this.style.cursor = 'pointer';
     };
     var t = r.text(240,27,"UBRe");
     t.attr({'font-size': 15, 'font-family': 'FranklinGothicFSCondensed-1, FranklinGothicFSCondensed-2'});
     t.attr("fill", "#f1f1f1");
     //t.translate((35 - text.getBBox().width)/2, (45 - text.getBBox().height)/2);
     //t.translate(r.width/2, r.height/2);
     t.node.onmouseover = function(){
     this.style.cursor = 'pointer';
     };*/
};

var $spinLoading = null;
var $spinMainLoading = null;

$(function () {
    // spin loading object
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire
    $("#filterOptions").hide();
    $("#hide_search").hide();
    //alert($("input[name='host_id']").val());
    var firmwareData = {
        ajax: {
            url: "firmware_master_slave_list.py",
            type: "get",
            data: {"host_id": $("input[name='host_id']").val(), "selected_device_type": $("input[name='selected_device']").val()}
        },
        chooseFirmwareAjax: {
            url: "select_firmware_table.py",
            type: "get",
            data: {"device_type": $("input[name='selected_device']").val()}
        },
        getFirmwareStatus: {
            url: "firmware_status_request.py",
            type: "get",
            data: {}
        },
        actionFirmwareAjax: {
            url: "start_firmware.py",
            type: "get",
            data: {}
        },
        resetFirmwareAjax: {
            url: "reset_firmware.py",
            type: "get",
            data: {}
        },
        otherFunction: {
            uploadNewFirmware: function () {
                $.colorbox({
                    href: "update_firmware_view.py",
                    iframe: "true",
                    title: "Upload Firmware File",
                    opacity: 0.4,
                    maxWidth: "80%",
                    width: "400px",
                    height: "250px"
                });
            }
        },
        containerId: "firmware_div",
        footerId: "firmware_footer"
    };
    $.blueJSON.firmware(firmwareData);
    // to stop tactical overview calls
    /*setTimeout(function()
     {
     if(tactical_call != null && tactical_call != null)
     {
     clearTimeout(tactical_call);
     }
     },20000);*/
    //$("#container_body").html("<div id='holder' style=\"background-color:#000;\"></div>");
});

/*************************************************************
 Raphael.fn.connection = function (obj1, obj2, line, bg) {
    if (obj1.line && obj1.from && obj1.to) {
        line = obj1;
        obj1 = line.from;
        obj2 = line.to;
    }
    var bb1 = obj1.getBBox(),
        bb2 = obj2.getBBox(),
        p = [{x: bb1.x + bb1.width / 2, y: bb1.y - 1},
        {x: bb1.x + bb1.width / 2, y: bb1.y + bb1.height + 1},
        {x: bb1.x - 1, y: bb1.y + bb1.height / 2},
        {x: bb1.x + bb1.width + 1, y: bb1.y + bb1.height / 2},
        {x: bb2.x + bb2.width / 2, y: bb2.y - 1},
        {x: bb2.x + bb2.width / 2, y: bb2.y + bb2.height + 1},
        {x: bb2.x - 1, y: bb2.y + bb2.height / 2},
        {x: bb2.x + bb2.width + 1, y: bb2.y + bb2.height / 2}],
        d = {}, dis = [];
    for (var i = 0; i < 4; i++) {
        for (var j = 4; j < 8; j++) {
            var dx = Math.abs(p[i].x - p[j].x),
                dy = Math.abs(p[i].y - p[j].y);
            if ((i == j - 4) || (((i != 3 && j != 6) || p[i].x < p[j].x) && ((i != 2 && j != 7) || p[i].x > p[j].x) && ((i != 0 && j != 5) || p[i].y > p[j].y) && ((i != 1 && j != 4) || p[i].y < p[j].y))) {
                dis.push(dx + dy);
                d[dis[dis.length - 1]] = [i, j];
            }
        }
    }
    if (dis.length == 0) {
        var res = [0, 4];
    } else {
        res = d[Math.min.apply(Math, dis)];
    }
    var x1 = p[res[0]].x,
        y1 = p[res[0]].y,
        x4 = p[res[1]].x,
        y4 = p[res[1]].y;
    dx = Math.max(Math.abs(x1 - x4) / 2, 10);
    dy = Math.max(Math.abs(y1 - y4) / 2, 10);
    var x2 = [x1, x1, x1 - dx, x1 + dx][res[0]].toFixed(3),
        y2 = [y1 - dy, y1 + dy, y1, y1][res[0]].toFixed(3),
        x3 = [0, 0, 0, 0, x4, x4, x4 - dx, x4 + dx][res[1]].toFixed(3),
        y3 = [0, 0, 0, 0, y1 + dy, y1 - dy, y4, y4][res[1]].toFixed(3);
    var path = ["M", x1.toFixed(3), y1.toFixed(3), "C", x2, y2, x3, y3, x4.toFixed(3), y4.toFixed(3)].join(",");
    if (line && line.line) {
        line.bg && line.bg.attr({path: path});
        line.line.attr({path: path});
    } else {
        var color = typeof line == "string" ? line : "#000";
        return {
            bg: bg && bg.split && this.path(path).attr({stroke: bg.split("|")[0], fill: "none", "stroke-width": bg.split("|")[1] || 3}),
            line: this.path(path).attr({stroke: color, fill: "none"}),
            from: obj1,
            to: obj2
        };
    }
};

 var el;
 window.onload = function () {
    var dragger = function () {
        this.ox = this.type == "rect" ? this.attr("x") : this.attr("cx");
        this.oy = this.type == "rect" ? this.attr("y") : this.attr("cy");
        this.animate({"fill-opacity": .2}, 500);
    },
        move = function (dx, dy) {
            var att = this.type == "rect" ? {x: this.ox + dx, y: this.oy + dy} : {cx: this.ox + dx, cy: this.oy + dy};
            this.attr(att);
            for (var i = connections.length; i--;) {
                r.connection(connections[i]);
            }
            r.safari();
        },
        up = function () {
            this.animate({"fill-opacity": 0}, 500);
        },
        r = Raphael("holder", 640, 480),
        connections = [],
        shapes = [  r.ellipse(190, 100, 30, 20),
                    r.rect(290, 80, 60, 40, 10),
                    r.rect(290, 180, 60, 40, 2),
                    r.ellipse(450, 100, 20, 20)
                ];
    for (var i = 0, ii = shapes.length; i < ii; i++) {
        var color = Raphael.getColor();
        shapes[i].attr({fill: color, stroke: color, "fill-opacity": 0, "stroke-width": 2, cursor: "move"});
        shapes[i].drag(move, dragger, up);
    }
    connections.push(r.connection(shapes[0], shapes[1], "#fff"));
    connections.push(r.connection(shapes[1], shapes[2], "#fff", "#fff|5"));
    connections.push(r.connection(shapes[1], shapes[3], "#000", "#fff"));
};
 /******************************************/

