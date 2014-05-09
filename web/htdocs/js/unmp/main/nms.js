/*
 ===========================================================================
 * jQuery NMS Map using Google Map Javascript API
 * Created by - Deepak Arora
 * Version - jquery-1.2
 * This JQuery File use to display your data over google map simply.
 * Requires jquery-1.6.1.js or jquery-1.6.1.min.js
 * Copyright (c) 2010 Deepak Arora - Code Scape Consultants Pvt. Ltd.
 ===========================================================================
 */




// Global Variable
var nmsData = new Array(); // Its store the NMS information.
var nmsresult = new Array(); // // Its store the host information.
var i = 0
$$ = $.noConflict();
jQuery(function () {
    var mapcanvas = document.getElementById("map_canvas");
    mapcanvas.style.height = '100%';//(screen.height) + 'px';
    mapcanvas.style.width = '100%';//(screen.width) + 'px';	
});
//$$("#page_tip").colorbox(
//	{
//	href:"page_tip_google_map.py",
//	title: "Dashboard",
//	opacity: 0.4,
//	maxWidth: "80%",
//	width:"650px",
//	height:"500px",
//	onComplte:function(){}
//});


/*
 * This function display the google map on page load event.
 * 
 * Parameter:
 * 				None
 * 
 * Related With:
 * 					None
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				This display the google map.
 * 
 */

function loadMap() {
    $.ajax({
        type: "post",
        url: "nms_details.py",
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                alert("Some unknown error occured  so please contact your Administrator");
                return;
            }
            if (result.success == 1 || result.success == '1') {
                alert("Some system error occured  so please contact your Administrator");
                return;
            }
            else if (result.success == 2 || result.success == '2') {
                alert("Some database error occured  so please contact your Administrator");
                return;
            }
            else {
                nmsData = [];
                nmsData = eval(result.output);

                $("#map_canvas").ccplMap({
                    title: "NMS",
                    type: "ROADMAP",
                    zoom: 4,
                    onUpdate: function (changes) {

                        for (i = 0; i < changes.length; i++) {
                            //alert(JSON.stringify(changes[0]));
                            var url = "save_updates.py?host_id=" + changes[i].ele + "&host_log=" + changes[i].lg + "&host_lat=" + changes[i].lt;
                            $.ajax({
                                type: "post",
                                url: url,
                                success: function (result) {
                                    try {
                                        result = eval("(" + result + ")");
                                    } catch (err) {
                                        alert("Some unknown error occured  so please contact your Administrator");
                                        return;
                                    }
                                    if (result.success == 1 || result.success == '1')
                                        alert("Some system error occured  so please contact your Administrator");
                                    else if (result.success == 2 || result.success == '2') {
                                        alert("Some database error occured  so please contact your Administrator");
                                        return;
                                    }

                                }
                            });
                            //console.log("Lati" + changes[i].lt+ "Lag" + changes[i].lg + " Id : " + changes[i].ele);
                        }
                    },
                    onNMSClick: function (id) {
                        // var nmsDetails =  Call your function to get the host and site json.
                        getNMSData(id);
                    },
                    onNMSMove: function (nmsName) {
                        // call to function to get the host and site details under this nms.
                        updateNMSLocation(nmsName);
                    },
                    updateNMSFunction: function (newObj) {
                        saveUpdatedPositions(newObj);
                    },
                    onElementClick: function (element, id) {
                        //console.log(element)

                        var url = "show_details.py?host_id=" + id + "&hostIp=" + element.title;
                        $.ajax({
                            type: "post",
                            url: url,
                            success: function (result) {
                                try {
                                    result = eval("(" + result + ")");
                                } catch (err) {
                                    alert("Some unknown error occured  so please contact your Administrator");
                                }
                                if (result.success == 1 || result.success == '1')
                                    alert("Some system error occured  so please contact your Administrator");
                                else if (result.success == 2 || result.success == '2') {
                                    alert("Some database error occured  so please contact your Administrator");
                                    return;
                                }
                                else {

                                    // var detail = call your function to get host or site details you want to show on device click.
                                    //console.log(result)
                                    showElementDetails(element, result.output);

                                }

                            }

                        });
                    },
                    nmsData: nmsData

                });
                nmsDevices(nmsData, "ffbc");

            }


        }
    });
    return false;
}

// get the sites and host under an nms.
function updateNMSLocation(nmsName) {
    // Get the nms detail in the specificed format and pass in ths function updateNMSPositions of ccpl_map
    // Get object of connected device in the form  [id: deviceid, lt: latitude, lg: longitude ]]
    $("#map_canvas").updateNMSPositions(nmsArr);
}

// This function updates the devices position in the database.
function saveUpdatedPositions(newObj) {
    console.dir(newObj);
    // Call your function here to update the updated positions in database.
}

/*
 * This function display the NMS name in sidepanel.
 * 
 * Parameter:
 * 				nmsName	: 	this take nmsName.
 * 
 * Related With:
 * 					nmsHostDevices
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				This dispalyy the all NMS name  in side panel.
 * 
 */

function getNMSData(nmsName) {
    dragHandleFlag = true;
    for (i in nmsArr) {
        if ($("div ul li#" + nmsArr[i].title).hasClass('nms_selected'))
            $("div ul li#" + nmsArr[i].title).removeClass()
    }
    $("div ul li#" + nmsName).addClass('nms_selected');
    $.ajax({
        type: "post",
        url: " google_host_graph.py?nms_name=" + nmsName,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                alert("Some unknown error occured  so please contact your Administrator");
            }
            if (result.success == 1 || result.success == '1')
                alert("Some system error occured  so please contact your Administrator");
            else if (result.success == 2 || result.success == '2') {
                alert("Some database error occured  so please contact your Administrator");
                return;
            }
            else {
                nmsresult = [];
                nmsresult = eval(result.output);
                //console.dir(result);

                $("#map_canvas").showNMSDetails(nmsresult);
                nmsHostDevices(nmsresult, 'sfbc');
                siteShowManagement()

                // new discover device
                $.ajax({
                    type: "post",
                    url: "new_discover_deviec.py",
                    success: function (result) {
                        try {
                            result = eval("(" + result + ")");
                        } catch (err) {
                            alert("Some unknown error occured  so please contact your Administrator");
                        }
                        if (result.success == 1 || result.success == '1') {
                            alert("Some system error occured  so please contact your Administrator");
                            return;
                        }
                        else if (result.success == 2 || result.success == '2') {
                            $("#tfbc").html("<ul><li>No new discover device exists.</li></ul>")
                            //alert('Please contact your administrator.');
                            return;
                        }
                        else {
                            newHostJson = eval(result.output);
                            newDiscoverDevice(eval(result.output), "tfbc");
                            newDiscoverDevice(result.disable_hosts, "dfbc");
                            //bindDragHandlerToNewHost();
                            updateHostInformation();
                        }
                    }

                });

            }
        }
    });

    return false;
}
function showElementDetails(element, detail) {
    $("#map_canvas").showElementDetails(element, detail);
}


function newHostUpdate(hostIp, parentIp, latitude, langitude) {
    var nmsName = ""
    for (i in nmsArr) {
        if ($("div ul li#" + nmsArr[i].title).hasClass('nms_selected'))
            nmsName = nmsArr[i].title;
    }
    $.ajax({
        type: "post",
        url: " new_host_update.py?hostIp=" + hostIp + "&latitude=" + latitude + "&langitude=" + langitude + "&parentIp=" + parentIp + "&nmsName=" + nmsName,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                alert("Some unknown error occured  so please contact your Administrator");
            }
            if (result.success == 1 || result.success == '1')
                alert("Some system error occured  so please contact your Administrator");
            else if (result.success == 2 || result.success == '2') {
                alert("Some database error occured  so please contact your Administrator");
                return;
            }
            else {
                alert("Host add successfully.");
//					    	if (result.output=="Add")
//								$('#sfbc').find('ul').append("<li id='"+hostIp+"'>"+hostIp+"</li>")
                //console.dir(result);

                $.ajax({
                    type: "post",
                    url: " google_host_graph.py?nms_name=" + nmsName,
                    success: function (result) {
                        try {
                            result = eval("(" + result + ")");
                        } catch (err) {
                            alert("Some unknown error occured  so please contact your Administrator");
                        }
                        if (result.success == 1 || result.success == '1')
                            alert("Some system error occured  so please contact your Administrator");
                        else if (result.success == 2 || result.success == '2') {
                            alert("Some database error occured  so please contact your Administrator");
                            return;
                        }
                        else {
                            nmsresult = [];
                            nmsresult = eval(result.output);
                            //console.dir(result);
                            nmsHostDevices(nmsresult, 'sfbc');

                        }
                    }
                });
                return false;
            }
        }
    });
    return false;

}


function siteShowManagement() {
    nmsName = ""
    for (i in nmsArr) {
        if ($("div ul li#" + nmsArr[i].title).hasClass('nms_selected'))
            nmsName = nmsArr[i].title;
    }
    $.ajax({
        type: "post",
        url: " site_show_management.py?nmsName=" + nmsName,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                alert("Some unknown error occured  so please contact your Administrator");
            }
            if (result.success == 1 || result.success == '1')
                alert("Some system error occured  so please contact your Administrator");
            else if (result.success == 2 || result.success == '2') {
                alert("Some database error occured  so please contact your Administrator");
                return;
            }
            else {
                siteResult = (eval('(' + result.output + ')'));
                drawGroups(siteResult);

            }
        }
    });
    return false;
}


function updateHostInformation() {
    $.ajax({
        type: "post",
        url: "host_status_update_information.py",
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                alert("Some unknown error occured  so please contact your Administrator");
            }
            if (result.success == 1 || result.success == '1')
                alert("Some system error occured  so please contact your Administrator");
            else if (result.success == 2 || result.success == '2') {
                alert("Some database error occured  so please contact your Administrator");
                return;
            }
            else {
                updateStateOfHost(eval(result.hosts_states));
            }
        }
    });
    setTimeout(function () {
        updateHostInformation();
    }, 300000);
    return false;
}
