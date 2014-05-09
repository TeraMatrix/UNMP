var maxAcl = 250;
$(function () {
    loadMacAddressGrid();
    $('a[rel*=facebox]').facebox({
        loadingImage: 'facebox/loading.gif',
        closeImage: 'facebox/closelabel.png'
    })
});
//Allow hex char and : . Used for MAC check 
var macCheck = function (e) {
    var key;
    if (window.event)
        key = window.event.keyCode;
    else key = e.which;
    if ((key >= 48 && key <= 58) || (key == 8) || (key == 0) || (key >= 97 && key <= 102) || (key >= 65 && key <= 70))
        return true;
    else return false;
};
function deleteMacAddress(mac) {
    if (confirm("Are you sure, you want to delete this mac address?")) {
        $.ajax({
            type: "post",
            url: "delete_mac_address.py?mac=" + mac,
            success: function (result) {
                if (result == "0") {
                    alert("Mac Address Deleted Successfully.");
                    loadMacAddressGrid();
                }
                else {
                    alert("There is some error occurred, refresh the page and try again.");
                }
            }
        })
    }
};
function loadMacAddressGrid() {
    $.ajax({
        type: "post",
        url: "list_of_mac_address.py",
        success: function (result) {
            result = $(result);
//================ Add Jquery events ===========================
            $(result).find("table").find("input[name='allMac']").click(function () {
                if (this.checked) {
                    $(this).parent().parent().parent().find("input[name='macAddressValue']").attr("checked", true);
                }
                else {
                    $(this).parent().parent().parent().find("input[name='macAddressValue']").attr("checked", false);
                }
            });
            $(result).find("table").find("input[name='macAddressValue']").click(function () {
                if (this.checked) {
                    if ($(this).parent().parent().parent().find("input[name='macAddressValue']:checked").size() == parseInt($(this).parent().parent().parent().find("input[name='totalMac']").val())) {
                        $(this).parent().parent().parent().find("input[name='allMac']").attr("checked", true);
                    }
                }
                else {
                    $(this).parent().parent().parent().find("input[name='allMac']").attr("checked", false);
                }
            });
//================ End Add Jquery events ===========================
            $("#macGrid").html(result);
        }
    })
};
function addMacAddress() {
    $("input[name='mac']").val($("input[name='mac']").val().toUpperCase());
    var macValue = $("input[name='mac']").val();
    var macArray = macValue.split(":")
    if (macArray.length != 6) {
        alert("Invalid Mac Address");
        return false;
    }
    for (var i = 0; i < 6; i++) {
        if ((macArray[i].length) != 2) {
            alert("Invalid Mac Address");
            return false;
        }
    }
    if ((macValue == "FF:FF:FF:FF:FF:FF") || (macValue == "00:00:00:00:00:00")) {
        alert("Invalid MAC Address.Enter valid MAC Address");
        $("input[name='mac']").val("");
        return false;
    }//add_mac_address
    $.ajax({
        type: "post",
        url: "add_mac_address.py?mac=" + $("input[name='mac']").val(),
        success: function (result) {
            if (result == "0") {
                alert("Mac Address Added Successfully.");
                $("input[name='mac']").val("")
                loadMacAddressGrid();
            }
            else if (result == "1") {
                alert("This Mac Address already exist in the list.");
            }
            else {
                alert("There is some error occured, refresh the page and try again.");
            }
        }
    })
};
function selectApToApply() {
    if ($("input[name='macAddressValue']:checked").size() == 0) {
        alert("Please select at least one mac address");
    }
    else {
        $("div.loading").show();
        $("div#selectApDiv").html("<table width=\"100%\" class=\"addform\"><tr><th> Choose Access Point</th></tr><tr><td><div class=\"msg-head\"><img style=\"vertical-align: middle;\" alt=\"\" src=\"images/loading-small.gif\"><span> Loading... </span></div></td></tr></table>").show();
        $.ajax({
            type: "post",
            url: "select_ap_to_apply_mac.py",
            success: function (result) {
                result = $(result);
//================ Add Jquery events ===========================
                $(result).find("table").find("input[name='allAP']").click(function () {
                    if (this.checked) {
                        $(this).parent().parent().parent().find("input[name='host']").attr("checked", true);
                    }
                    else {
                        $(this).parent().parent().parent().find("input[name='host']").attr("checked", false);
                    }
                });
                $(result).find("table").find("input[name='host']").click(function () {
                    if (this.checked) {
                        if ($(this).parent().parent().parent().find("input[name='host']:checked").size() == parseInt($(this).parent().parent().parent().find("input[name='totalHost']").val())) {
                            $(this).parent().parent().parent().find("input[name='allAP']").attr("checked", true);
                        }
                    }
                    else {
                        $(this).parent().parent().parent().find("input[name='allAP']").attr("checked", false);
                    }
                });
                $(result).find("table").find("input[name='sameUnP']").click(function () {
                    if (this.checked) {
                        $("input[name='hostUsername']").val($("input[name='hostUsername']:eq(0)").val());
                        $("input[name='hostPassword']").val($("input[name='hostPassword']:eq(0)").val());
                    }
                    else {
                        var username = $("input[name='hostUsername']:eq(0)").val();
                        var password = $("input[name='hostPassword']:eq(0)").val()
                        $("input[name='hostUsername']").val("");
                        $("input[name='hostPassword']").val("");
                        $("input[name='hostUsername']:eq(0)").val(username);
                        $("input[name='hostPassword']:eq(0)").val(password);
                    }
                })
//================ End Add Jquery events ===========================
                $("div#selectApDiv").html(result);
            }
        })
    }
}
function applyAP() {
    if ($("input[name='host']:checked").size() == 0) {
        alert("Please select at least one Access Point.");
    }
    else {
        if ($("input[name='vapnum']:checked").size() == 0) {
            alert("Please select at least one VAP.");
        }
        else {
            var totalRequest = 0;
            var successedRequest = 0;
            var displayMsg = "";
            if ($("input[name='actionForMac']:checked").val() == "replace") {
                $("input[name='host']:checked").each(function () {
                    var ip = $(this).attr("ip");
                    $("input[name='vapnum']:checked").each(function () {
                        totalRequest += 1;
                        $.ajax({
                            type: "get",
                            url: "http_request_for_ap.py?username=" + $("input[ip='" + ip + "_user']").val() + "&password=" + $("input[ip='" + ip + "_pass']").val() + "&ap=" + ip + "&url=" + "/cgi-bin/ServerFuncs" + "&para=Method,VAP" + "&arg=RemoveAllMacs," + $(this).val() + "&acltype=-1&restart=0",
                            success: function (result) {
//100,101,200,201,202,203,204,205,206,300,301,302,303,304,305,307,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,500,501,502,503,504,505
                                if (result == "100")
                                    displayMsg += "Access Point " + ip + " has received Request.\n";
                                else if (result == "101")
                                    displayMsg += "Access Point " + ip + " has an Error: Switching Protocols error.\n";
                                else if (result == "200")
                                    successedRequest += 1;
                                else if (result == "201")
                                    successedRequest += 1;
                                else if (result == "202")
                                    successedRequest += 1;
                                else if (result == "203")
                                    displayMsg += "Access Point " + ip + " has an Error: Non-Authoritative Information.\n";
                                else if (result == "204")
                                    displayMsg += "Access Point " + ip + " has an Error: No Content.\n";
                                else if (result == "205")
                                    displayMsg += "Access Point " + ip + " has an Error: Reset Content.\n";
                                else if (result == "206")
                                    displayMsg += "Access Point " + ip + " has an Error: Partial Content.\n";
                                else if (result == "300")
                                    displayMsg += "Access Point " + ip + " has an Error: Multiple Choices.\n";
                                else if (result == "301")
                                    displayMsg += "Access Point " + ip + " has an Error: Object Moved Permanently.\n";
                                else if (result == "302")
                                    displayMsg += "Access Point " + ip + " has an Error: Object Moved Temporarily.\n";
                                else if (result == "303")
                                    displayMsg += "Access Point " + ip + " has an Error: Object Moved.\n";
                                else if (result == "304")
                                    displayMsg += "Access Point " + ip + " has an Error: Not Modified.\n";
                                else if (result == "305")
                                    displayMsg += "Access Point " + ip + " has an Error: Use Proxy.\n";
                                else if (result == "307")
                                    displayMsg += "Access Point " + ip + " has an Error: Temporary Redirected.\n";
                                else if (result == "400")
                                    displayMsg += "Access Point " + ip + " has an Error: Bad Request.\n";
                                else if (result == "401")
                                    displayMsg += "Access Point " + ip + " has an Error: Wrong Username and Password.\n";
                                else if (result == "402")
                                    displayMsg += "Access Point " + ip + " has an Error: No Payment.\n";
                                else if (result == "403")
                                    displayMsg += "Access Point " + ip + " has an Error: Request forbidden.\n";
                                else if (result == "404")
                                    displayMsg += "Access Point " + ip + " has an Error: Not Found.\n";
                                else if (result == "405")
                                    displayMsg += "Access Point " + ip + " has an Error: Method Not Allowed.\n";
                                else if (result == "406")
                                    displayMsg += "Access Point " + ip + " has an Error: Not Acceptable.\n";
                                else if (result == "407")
                                    displayMsg += "Access Point " + ip + " has an Error: Proxy Authentication Required.\n";
                                else if (result == "408")
                                    displayMsg += "Access Point " + ip + " has an Error: Request Timeout.\n";
                                else if (result == "409")
                                    displayMsg += "Access Point " + ip + " has an Error: Request Conflict.\n";
                                else if (result == "410")
                                    displayMsg += "Access Point " + ip + " has an Error: Request no longer exists.\n";
                                else if (result == "411")
                                    displayMsg += "Access Point " + ip + " has an Error: Content-Length Error.\n";
                                else if (result == "412")
                                    displayMsg += "Access Point " + ip + " has an Error: Precondition Failed.\n";
                                else if (result == "413")
                                    displayMsg += "Access Point " + ip + " has an Error: Request Entity too large.\n";
                                else if (result == "414")
                                    displayMsg += "Access Point " + ip + " has an Error: Request-URL too long.\n";
                                else if (result == "415")
                                    displayMsg += "Access Point " + ip + " has an Error: Unsupported Format.\n";
                                else if (result == "416")
                                    displayMsg += "Access Point " + ip + " has an Error: Requested Range not Satisfiable.\n";
                                else if (result == "417")
                                    displayMsg += "Access Point " + ip + " has an Error: Expectation Failed.\n";
                                else if (result == "500")
                                    displayMsg += "Access Point " + ip + " has an Error: Internal Server Error.\n";
                                else if (result == "501")
                                    displayMsg += "Access Point " + ip + " has an Error: Server does not support this operation.\n";
                                else if (result == "502")
                                    displayMsg += "Access Point " + ip + " has an Error: Bad Gateway.\n";
                                else if (result == "503")
                                    displayMsg += "Access Point " + ip + " has an Error: Service Unavailable.\n";
                                else if (result == "504")
                                    displayMsg += "Access Point " + ip + " has an Error: Gateway Timeout.\n";
                                else if (result == "505")
                                    displayMsg += "Access Point " + ip + " has an Error: HTTP Version Not Supported.\n";
                                else if (result == "0")
                                    successedRequest += 1;
                                else
                                    displayMsg += "Access Point " + ip + " has an Error: Network Not Reachable.\n";
                            },
                            error: function (a, s, d) {
                                displayMsg += "Access Point " + ip + " is not connected. please try again.\n";
                            },
                            async: false
                        });
                    });
                });
            }
            if (totalRequest == successedRequest) {
                $("input[name='host']:checked").each(function () {
                    last = 0;
                    lastvap = 0;
                    var ip = $(this).attr("ip");
                    $("input[name='macAddressValue']:checked").each(function () {
                        last += 1;
                        lastvap = 0
                        var mac = $(this).attr("mac");
                        $("input[name='vapnum']:checked").each(function () {
                            lastvap += 1
                            var restart = "&restart=0";
                            totalRequest += 1;
                            if ($("input[name='macAddressValue']:checked").size() == last && $("input[name='vapnum']:checked").size() == lastvap) {
                                restart = "&restart=1"
                            }
                            $.ajax({
                                type: "get",
                                url: "http_request_for_ap.py?username=" + $("input[ip='" + ip + "_user']").val() + "&password=" + $("input[ip='" + ip + "_pass']").val() + "&ap=" + ip + "&url=" + "/cgi-bin/ServerFuncs" + "&para=Method,VAP,MAC" + "&arg=AddACLMac," + $(this).val() + "," + mac + "&acltype=" + $("input[name='ACLTYPE_VAP']:checked").val() + restart,
                                success: function (result) {//alert(result);
//100,101,200,201,202,203,204,205,206,300,301,302,303,304,305,307,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,500,501,502,503,504,505
                                    if (result == "100")
                                        displayMsg += "Access Point " + ip + " has received Request.\n";
                                    else if (result == "101")
                                        displayMsg += "Access Point " + ip + " has an Error: Switching Protocols error.\n";
                                    else if (result == "200")
                                        successedRequest += 1;
                                    else if (result == "201")
                                        successedRequest += 1;
                                    else if (result == "202")
                                        successedRequest += 1;
                                    else if (result == "203")
                                        displayMsg += "Access Point " + ip + " has an Error: Non-Authoritative Information.\n";
                                    else if (result == "204")
                                        displayMsg += "Access Point " + ip + " has an Error: No Content.\n";
                                    else if (result == "205")
                                        displayMsg += "Access Point " + ip + " has an Error: Reset Content.\n";
                                    else if (result == "206")
                                        displayMsg += "Access Point " + ip + " has an Error: Partial Content.\n";
                                    else if (result == "300")
                                        displayMsg += "Access Point " + ip + " has an Error: Multiple Choices.\n";
                                    else if (result == "301")
                                        displayMsg += "Access Point " + ip + " has an Error: Object Moved Permanently.\n";
                                    else if (result == "302")
                                        displayMsg += "Access Point " + ip + " has an Error: Object Moved Temporarily.\n";
                                    else if (result == "303")
                                        displayMsg += "Access Point " + ip + " has an Error: Object Moved.\n";
                                    else if (result == "304")
                                        displayMsg += "Access Point " + ip + " has an Error: Not Modified.\n";
                                    else if (result == "305")
                                        displayMsg += "Access Point " + ip + " has an Error: Use Proxy.\n";
                                    else if (result == "307")
                                        displayMsg += "Access Point " + ip + " has an Error: Temporary Redirected.\n";
                                    else if (result == "400")
                                        displayMsg += "Access Point " + ip + " has an Error: Bad Request.\n";
                                    else if (result == "401")
                                        displayMsg += "Access Point " + ip + " has an Error: Wrong Username and Password.\n";
                                    else if (result == "402")
                                        displayMsg += "Access Point " + ip + " has an Error: No Payment.\n";
                                    else if (result == "403")
                                        displayMsg += "Access Point " + ip + " has an Error: Request forbidden.\n";
                                    else if (result == "404")
                                        displayMsg += "Access Point " + ip + " has an Error: Not Found.\n";
                                    else if (result == "405")
                                        displayMsg += "Access Point " + ip + " has an Error: Method Not Allowed.\n";
                                    else if (result == "406")
                                        displayMsg += "Access Point " + ip + " has an Error: Not Acceptable.\n";
                                    else if (result == "407")
                                        displayMsg += "Access Point " + ip + " has an Error: Proxy Authentication Required.\n";
                                    else if (result == "408")
                                        displayMsg += "Access Point " + ip + " has an Error: Request Timeout.\n";
                                    else if (result == "409")
                                        displayMsg += "Access Point " + ip + " has an Error: Request Conflict.\n";
                                    else if (result == "410")
                                        displayMsg += "Access Point " + ip + " has an Error: Request no longer exists.\n";
                                    else if (result == "411")
                                        displayMsg += "Access Point " + ip + " has an Error: Content-Length Error.\n";
                                    else if (result == "412")
                                        displayMsg += "Access Point " + ip + " has an Error: Precondition Failed.\n";
                                    else if (result == "413")
                                        displayMsg += "Access Point " + ip + " has an Error: Request Entity too large.\n";
                                    else if (result == "414")
                                        displayMsg += "Access Point " + ip + " has an Error: Request-URL too long.\n";
                                    else if (result == "415")
                                        displayMsg += "Access Point " + ip + " has an Error: Unsupported Format.\n";
                                    else if (result == "416")
                                        displayMsg += "Access Point " + ip + " has an Error: Requested Range not Satisfiable.\n";
                                    else if (result == "417")
                                        displayMsg += "Access Point " + ip + " has an Error: Expectation Failed.\n";
                                    else if (result == "500")
                                        displayMsg += "Access Point " + ip + " has an Error: Internal Server Error.\n";
                                    else if (result == "501")
                                        displayMsg += "Access Point " + ip + " has an Error: Server does not support this operation.\n";
                                    else if (result == "502")
                                        displayMsg += "Access Point " + ip + " has an Error: Bad Gateway.\n";
                                    else if (result == "503")
                                        displayMsg += "Access Point " + ip + " has an Error: Service Unavailable.\n";
                                    else if (result == "504")
                                        displayMsg += "Access Point " + ip + " has an Error: Gateway Timeout.\n";
                                    else if (result == "505")
                                        displayMsg += "Access Point " + ip + " has an Error: HTTP Version Not Supported.\n";
                                    else if (result == "0")
                                        successedRequest += 1;
                                    else
                                        displayMsg += "Access Point " + ip + " has an Error: Network Not Reachable.\n";
                                },
                                error: function (a, s, d) {
                                    displayMsg += "Access Point " + ip + " is not connected. please try again.\n";
                                },
                                async: false
                            });//alert($(this).val());
                        });
                    })
                })
                applyCancel();
                if (totalRequest == successedRequest)
                    alert("Mac Address Added Successfully.");
                else
                    alert(displayMsg);

            }
            else {
                alert("Selected Access Point doesn't replaced Mac Addresses:\n" + displayMsg);
                applyCancel();
            }
        }
    }
}
function applyCancel() {
    $("div#selectApDiv").html("").show();
    $("div.loading").hide();
}
function deleteMacFromAP() {
    var macList = [];
    if ($("input[name='host']:checked").size() == 0) {
        alert("Please select at least one Access Point.");
    }
    else {
        if ($("input[name='vapnum']:checked").size() == 0) {
            alert("Please select at least one VAP.");
        }
        else {
            var totalRequest = 0;
            var successedRequest = 0;
            var displayMsg = "";
            $("input[name='host']:checked").each(function () {
                var ip = $(this).attr("ip");
                $("input[name='macAddressValue']:checked").each(function () {
                    macList.push($(this).attr("mac"));
                });
                //ServerFuncs?Method=RemoveSelectedMac&VAP='+vap+'&maclist='+maclist
                $("input[name='vapnum']:checked").each(function () {
                    totalRequest += 1;
                    $.ajax({
                        type: "get",
                        url: "http_request_for_ap.py?username=" + $("input[ip='" + ip + "_user']").val() + "&password=" + $("input[ip='" + ip + "_pass']").val() + "&ap=" + ip + "&url=" + "/cgi-bin/ServerFuncs" + "&para=Method,VAP,maclist" + "&arg=RemoveSelectedMac," + $(this).val() + "," + String(macList),
                        success: function (result) {
//100,101,200,201,202,203,204,205,206,300,301,302,303,304,305,307,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,500,501,502,503,504,505
                            if (result == "100")
                                displayMsg += "Access Point " + ip + " has received Request.\n";
                            else if (result == "101")
                                displayMsg += "Access Point " + ip + " has an Error: Switching Protocols error.\n";
                            else if (result == "200")
                                successedRequest += 1;
                            else if (result == "201")
                                successedRequest += 1;
                            else if (result == "202")
                                successedRequest += 1;
                            else if (result == "203")
                                displayMsg += "Access Point " + ip + " has an Error: Non-Authoritative Information.\n";
                            else if (result == "204")
                                displayMsg += "Access Point " + ip + " has an Error: No Content.\n";
                            else if (result == "205")
                                displayMsg += "Access Point " + ip + " has an Error: Reset Content.\n";
                            else if (result == "206")
                                displayMsg += "Access Point " + ip + " has an Error: Partial Content.\n";
                            else if (result == "300")
                                displayMsg += "Access Point " + ip + " has an Error: Multiple Choices.\n";
                            else if (result == "301")
                                displayMsg += "Access Point " + ip + " has an Error: Object Moved Permanently.\n";
                            else if (result == "302")
                                displayMsg += "Access Point " + ip + " has an Error: Object Moved Temporarily.\n";
                            else if (result == "303")
                                displayMsg += "Access Point " + ip + " has an Error: Object Moved.\n";
                            else if (result == "304")
                                displayMsg += "Access Point " + ip + " has an Error: Not Modified.\n";
                            else if (result == "305")
                                displayMsg += "Access Point " + ip + " has an Error: Use Proxy.\n";
                            else if (result == "307")
                                displayMsg += "Access Point " + ip + " has an Error: Temporary Redirected.\n";
                            else if (result == "400")
                                displayMsg += "Access Point " + ip + " has an Error: Bad Request.\n";
                            else if (result == "401")
                                displayMsg += "Access Point " + ip + " has an Error: Wrong Username and Password.\n";
                            else if (result == "402")
                                displayMsg += "Access Point " + ip + " has an Error: No Payment.\n";
                            else if (result == "403")
                                displayMsg += "Access Point " + ip + " has an Error: Request forbidden.\n";
                            else if (result == "404")
                                displayMsg += "Access Point " + ip + " has an Error: Not Found.\n";
                            else if (result == "405")
                                displayMsg += "Access Point " + ip + " has an Error: Method Not Allowed.\n";
                            else if (result == "406")
                                displayMsg += "Access Point " + ip + " has an Error: Not Acceptable.\n";
                            else if (result == "407")
                                displayMsg += "Access Point " + ip + " has an Error: Proxy Authentication Required.\n";
                            else if (result == "408")
                                displayMsg += "Access Point " + ip + " has an Error: Request Timeout.\n";
                            else if (result == "409")
                                displayMsg += "Access Point " + ip + " has an Error: Request Conflict.\n";
                            else if (result == "410")
                                displayMsg += "Access Point " + ip + " has an Error: Request no longer exists.\n";
                            else if (result == "411")
                                displayMsg += "Access Point " + ip + " has an Error: Content-Length Error.\n";
                            else if (result == "412")
                                displayMsg += "Access Point " + ip + " has an Error: Precondition Failed.\n";
                            else if (result == "413")
                                displayMsg += "Access Point " + ip + " has an Error: Request Entity too large.\n";
                            else if (result == "414")
                                displayMsg += "Access Point " + ip + " has an Error: Request-URL too long.\n";
                            else if (result == "415")
                                displayMsg += "Access Point " + ip + " has an Error: Unsupported Format.\n";
                            else if (result == "416")
                                displayMsg += "Access Point " + ip + " has an Error: Requested Range not Satisfiable.\n";
                            else if (result == "417")
                                displayMsg += "Access Point " + ip + " has an Error: Expectation Failed.\n";
                            else if (result == "500")
                                displayMsg += "Access Point " + ip + " has an Error: Internal Server Error.\n";
                            else if (result == "501")
                                displayMsg += "Access Point " + ip + " has an Error: Server does not support this operation.\n";
                            else if (result == "502")
                                displayMsg += "Access Point " + ip + " has an Error: Bad Gateway.\n";
                            else if (result == "503")
                                displayMsg += "Access Point " + ip + " has an Error: Service Unavailable.\n";
                            else if (result == "504")
                                displayMsg += "Access Point " + ip + " has an Error: Gateway Timeout.\n";
                            else if (result == "505")
                                displayMsg += "Access Point " + ip + " has an Error: HTTP Version Not Supported.\n";
                            else
                                successedRequest += 1;
                        },
                        error: function (a, s, d) {
                            displayMsg += "Access Point " + ip + " is not connected. please try again.\n";
                        },
                        async: false
                    });//alert($(this).val());
                });
            });
            applyCancel();
            if (totalRequest == successedRequest)
                alert("Mac Address Deleted Successfully.");
            else
                alert(displayMsg);
        }
    }
}
// /cgi-bin/AclUpload
