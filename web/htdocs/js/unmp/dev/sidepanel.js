var circles_array = new Array();
//flag variable that used to when new discovered drag handle functionality work or not
var dragHandleFlag = false;
//flag variable that used to rule the connection of new discovered host with other host
var newHostConFlag = false;
//variable to hold json data of new discovered host
var newHostJson = null;
var result = new Array(); // This global variable used for store the all host name from json for particular NMS .
//flag variable that show new host drag happen or not 
var dragHappenFlag = false;
//array used to hold host of site that moved
var lastHostMoved = [];
//array used to hold sites that moved
var movedSiteLocations = new Array();
var labelArr = new Array();
var labelDict = {};
var labelFlag = 0;

$(document).ready(function () {

    $("#ctr").click(function () {
        $(this).parent().toggleClass("hide");
        if ($(this).hasClass("h")) {
            $(this).removeClass('h').addClass('s');
        }
        else {
            $(this).removeClass('s').addClass('h');
        }

    });
    $("#cnt li").click(function () {
        var val = $(this).attr('id');
    });
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
                //newHostJson=result.output;
                newDiscoverDevice(result.output, "tfbc");
                newDiscoverDevice(result.disable_hosts, "dfbc");
                //bindDragHandlerToNewHost();

            }
        }

    });
    //setTimeout(function(){$("#ctr").click();},3000);
    return false;


});


/*
 * This function display the NMS name in sidepanel. 
 * 
 * Related With:
 * 				None
 * 
 * Parameter:
 * 				Data	: 	data contain the json format
 * 				item	:   this contain the div id name 
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				This function return a html un-order list of name in input json format .
 * 
 * How to Use: pass json format and div id for display the result .
 *              <ul><li id=json.name>json.name<li>
 * 		    <li id=json.name>json.name<li></ul>		
 * 				
 */


function nmsDevices(data, item) {
    var html = "";
    var l = data.length;
    html += "<ul>";
    if (l > 0) {
        for (var i = 0; i < l; i++) {
            var dddd = data[i];
            html += "<li id=" + dddd.name + "><a href=# style=\"text-decoration: none\" onClick=\"nmsHostDetails('" + dddd.name + "')\">" + dddd.name + "</a></li>";
        }
    }
    else {
        html += "<li> No NMS exists.</li>";
    }
    html += "</ul>";
    $('div#' + item).html(html);

};


/*
 * This function display the host in the NMS and its also show the output in sidepanel.
 * 
 * Related With:
 * 				None
 * 
 * Parameter:
 * 				Data	: 	data contain the json format
 * 				item	:   this contain the div id name 
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				This function return a html un-order list of name in input json format .
 * 
 * How to Use: pass json format and div id for display the result .
 *              <ul><li id=json.name>json.name<li>
 * 		    <li id=json.name>json.name<li></ul>		
 * 				
 */

function nmsHostDevices(data, item) {
    $("div#s input[id='searchHost']").val("");
    var html = "";
    result = [];
    var host_result = getHost(data)
    html += "<ul>";
    if (host_result.length > 0) {
        for (var i = 0; i < host_result.length; i++) {
            html += "<li id=" + host_result[i] + "><a href=# style=\"text-decoration: none\" onClick=\"hostDetails('" + host_result[i] + "')\">" + host_result[i] + "</a></li>";
        }
    }
    else {
        html += "<li> No Hosts exists.</li>";
    }
    html += "</ul>";
    $('#' + item).html(html);
};


/*
 * This function display the new discover device.
 * 
 * Related With:
 * 				None
 * 
 * Parameter:
 * 				Data	: 	data contain the json format
 * 				item	:   this contain the div id name 
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				This function return a html un-order list of name in input json format .
 * 
 * How to Use: pass json format and div id for display the result .
 *              <ul><li id=json.name>json.name<li>
 * 		    <li id=json.name>json.name<li></ul>		
 * 				
 */

function newDiscoverDevice(data, item) {
    var html = "";
    var l = data.length;
    html += "<ul>";
    if (l > 0) {
        for (var i = 0; i < l; i++) {
            var aaaa = data[i];
            html += "<li id=" + aaaa["name"] + " latitude=" + aaaa["latitude"] + " longitude=" + aaaa["longitude"] + "><a href=# style=\"text-decoration: none\">" + aaaa["name"] + "</a></li>";
        }
    }
    else {
        html += "<li>No hosts exists.</li>";
    }
    html += "</ul>";
    $('#' + item).html(html);
};


/*
 * This function display the NMS on google map by sidepanel click event on NMS.
 * 
 * Related With:
 * 				ccpl_map.js
 * 
 * Parameter:
 * 				nmsName	: 	This store the nmsName 
 * 
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				its show the clickable NMS hosts and hide the previous hosts on google map. 
 * 
 * How to Use: pass NMS name.
 *              and Its call the google.maps.event.trigger() function correspondence NMS.
 * 		   		
 */
function nmsHostDetails(nmsName) {
    newHostConFlag = false;
    $("#newHostSaver").css("display", "none");
    $("div ul li#" + nmsName).addClass("selected");
    for (i in markers_array) {
        for (j in markers_array[i].plines)
            markers_array[i].plines[j].setMap(null);
        markers_array[i].setMap(null);
    }
    markers_array = [];
    for (i in nmsArr) {
        if (nmsArr[i].getTitle() == nmsName) {
            //$("div#"+nmsName).
            google.maps.event.trigger(nmsArr[i], 'click');
        }
    }
    for (i in circles_array) {
        circles_array[i].centermarker.setMap(null);
        circles_array[i].setMap(null);
    }
    circles_array = [];
}


/*
 * This function display the Hosts on google map by sidepanel click event on NMS.
 * 
 * Related With:
 * 				ccpl_map.js
 * 
 * Parameter:
 * 				hostName	: 	This store the nmsName 
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				its show the clickable host  than show the services and information of hosts 
 * 
 * How to Use: pass NMS name.
 *              and Its call the google.maps.event.trigger() function correspondence NMS.
 * 		   		
 */

function hostDetails(hostName) {

    for (i in markers_array) {
        if (markers_array[i].getTitle() == hostName)
            google.maps.event.trigger(markers_array[i], 'click');
    }
}

/*
 * This function return the array of host name from json .
 * 
 * Related With:
 * 				None
 * 
 * Parameter:
 * 				hs	: 	it contain the json 
 * 
 * Return:
 * 				Its return the host name of array.
 * 
 * Output:
 * 				None 
 * 
 * How to Use: pass josn Format.
 * 				josn=[{name:'lcoalhost',id='64-fds-232'
 * 									child:{name:'172.22.0.110',id:'fdkls-456'}}]
 *               its return result=[localhost,172.22.0.110]
 * 		   		
 */

function getHost(hs) {
    for (var j = 0; j < hs.length; j++) {
        var nHost = hs[j];
        if (nHost.child) {
            getHost(nHost.child);
        }
        result.push(nHost.name);
    }
    return result;
}


/*
 * This function display the Serching result for NMS.
 * 
 * Related With:
 * 				None
 * 
 * Parameter:
 * 				event	:   This contain the keyup event object.
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				This function return a searching result in  html un-order list  format and display the output on side panel .
 * 
 * How to Use: pass json format and div id for display the result .
 *              <ul><li id=json.name>json.name<li>

 * 		    <li id=json.name>json.name<li></ul>		
 * 				
 */
function searchNMSResult(event) {
    var flag = 0;
    var html = "";
    html += "<ul>";
    for (i in nmsData) {
        if (((nmsData[i].name).toLowerCase().indexOf($("#searchNMS").val().toLowerCase())) >= 0) {
            html += "<li id=" + nmsData[i].name + "><a href=# style=\"text-decoration: none\" onClick=\"nmsHostDetails('" + nmsData[i].name + "')\">" + nmsData[i].name + "</a></li>";
            flag = 1;
        }
    }
    if (flag != 1)
        html += "<li> No NMS exists.</li>";
    html += "</ul>";
    $('#ffbc').html(html);
}


/*
 * This function display the Serching result for hosts.
 * 
 * Related With:
 * 				None
 * 
 * Parameter:
 * 				event	:   This contain the keyup event object.
 * 
 * Return:
 * 				None
 * 
 * Output:
 * 				This function return a searching result in  html un-order list  format and display the output on side panel .
 * 
 * How to Use: pass json format and div id for display the result .
 *              <ul><li id=json.name>json.name<li>
 * 		    <li id=json.name>json.name<li></ul>		
 * 				
 */
function searchHostResult(event) {
    result = [];
    var hostResult = getHost(nmsresult);
    var flag = 0;
    var html = "";
    html += "<ul>";
    //var chCode = ('charCode' in event) ? event.charCode : event.keyCode;
    srchStr = $("#searchHost").val().toLowerCase().toString();
    for (i in hostResult) {
        if ((hostResult[i].toLowerCase().search(srchStr)) >= 0) {
            html += "<li id=" + hostResult[i] + "><a href=# style=\"text-decoration: none\" onClick=\"hostDetails('" + hostResult[i] + "')\">" + hostResult[i] + "</a></li>";
            flag = 1;
        }
    }
    if (flag != 1)
        html += "<li> No host exists.</li>";
    html += "</ul>";
    $('#sfbc').html(html);
}


/*==============code started by pawan=========*/
/*
 * DragHandle is prototype that handle dragging functionality of new host
 */
var DragHandler = {
    _oElem: null,

    // public method. Attach drag handler to an element.
    attach: function (oElem) {
        oElem.onmousedown = DragHandler._dragBegin;
        oElem.dragEnd = new Function();
        return oElem;
    },
    // private method. Begin drag process.
    _dragBegin: function (e) {
        var oElem = DragHandler._oElem = this;


        if (isNaN(parseInt(oElem.style.left))) {
            oElem.style.left = '0px';
        }
        if (isNaN(parseInt(oElem.style.top))) {
            oElem.style.top = '0px';
        }

        var x = startx = parseInt(oElem.style.left);
        var y = starty = parseInt(oElem.style.top);

        e = e ? e : window.event;
        oElem.mouseX = e.clientX;
        oElem.mouseY = e.clientY;
        document.onmousemove = DragHandler._drag;
        document.onmouseup = DragHandler._dragEnd;
        return false;
    },
    // private method. Drag (move) element.
    _drag: function (e) {
        var oElem = DragHandler._oElem;
        dragHappenFlag = true;
        var x = parseInt(oElem.style.left);
        var y = parseInt(oElem.style.top);

        e = e ? e : window.event;
        oElem.style.left = x + (e.clientX - oElem.mouseX) + 'px';
        oElem.style.top = y + (e.clientY - oElem.mouseY) + 'px';

        oElem.mouseX = e.clientX;
        oElem.mouseY = e.clientY;

        return false;
    },


    // private method. Stop drag process.
    _dragEnd: function () {
        var oElem = DragHandler._oElem;
        var x = parseInt(oElem.style.left);
        var y = parseInt(oElem.style.top);
        oElem.style.left = startx + 'px';
        oElem.style.top = starty + 'px';
        document.onmousemove = null;
        document.onmouseup = null;
        DragHandler._oElem = null;
        oElem.dragEnd(oElem, x, y);

    }

}//End of DragHandler prototyping

//This function is used to bind dragging functionality to new host
function bindDragHandlerToNewHost() {
    //array that hold DragHandler object that bind to new host
    var hostDragHandler = new Array();
    //Iterating the received json data of new discovered host
    for (i in newHostJson) {
        //binding drag handler to new discovered host
        var dh = DragHandler.attach(document.getElementById(newHostJson[i].name));
        //binding drag end handler function
        dh.dragEnd = findandmark;
        hostDragHandler.push(dh);
    }
}

/*
 * The function executed when the drag event is over
 * and this one calls the respective function to generate the marker
 */
function findandmark(element, x, y) {
    //checking whether drag happen allow or not
    if (dragHandleFlag) {
        var latlng;
        //checking whether drag happen or not
        if (dragHappenFlag) {
            dragHappenFlag = false;
            var bounds = new google.maps.LatLngBounds();
            var width = parseInt(document.getElementById("map_canvas").style.width);
            var height = parseInt(document.getElementById("map_canvas").style.height);


            //if (x > -width && x < 0 && y > 0 && y < height) {
            x = x + 1200;
            abc1 = dummy1.getProjection();
            //Dynamically seting the maps width
            var map_div = document.getElementById("map_canvas").style;
            var elements_div = document.getElementById("cnt").style;

            //var horizontal_adjustment = parseInt(map_div.borderWidth) + parseInt(elements_div.borderWidth) + parseInt(elements_div.marginLeft);
            y += 415;
            var title;
            var content;
            var point = new google.maps.Point(x, y);
            latlng = abc1.fromContainerPixelToLatLng(point);
        }
        else {
            var lat1 = parseFloat($("#tfbc li[id='" + element.id + "']").attr('latitude'));
            var lng1 = parseFloat($("#tfbc li[id='" + element.id + "']").attr('longitude'));
            latlng = new google.maps.LatLng(lat1, lng1);
            map.setCenter(latlng);
        }
        icon = "images/host_e.png";
        var isDrag = true;

        //creating instance of google.maps.Marker class to add new discovered host to google map
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(latlng.lat(), latlng.lng()),
            map: map,
            draggable: true,
            icon: icon,
            title: element.id
        });

        marker.setMap(map);
        marker.set('cm', new Array());
        marker.set('id', element.id);
        marker.plines = [];
        //map.setCenter(latlng);
        //bounds.extend( new google.maps.LatLng(latlng.lat(),latlng.lng()));
        //map.fitBounds(bounds);
        markers_array.push(marker);
        nmsDetailsArr.push(marker);
        //bindFunctinality(marker); this function work for new discover device.
        newHostConFlag = true;
        newHostParent = [];
        dragHandleFlag = false;
        $("#tfbc li[id='" + marker.id + "']").css('display', 'none');
        $("#newHostSaver").css('display', 'block');
        //newHostUpdate(marker.id,marker.getPosition().lat(),marker.getPosition().lng());
    }
    //return;
}
/* 
 * This function is used to bind events to new discovered host
 */


function bindFunctinality(marker) {
    //adding drag start event to marker
    google.maps.event.addListener(marker, 'dragstart', function (event) {
        lastMovedPos = event.latLng;
    });
    //adding drag event to marker
    google.maps.event.addListener(marker, 'drag', function (event) {
        for (var p = 0; p < marker.plines.length; p++)
            marker.plines[p].setPath([event.latLng, marker.cm[p].getPosition()]);
        if (lockMode == "on") {
            $('#customtooltip').hide();
            lockMode = "off";
            lockNode = null;
        }
    });
    //adding dragend event to marker
    google.maps.event.addListener(marker, 'dragend', function (event) {
        $('.map3saveloc').show();
        movedLocations.push(new Array(marker, lastMovedPos));
    });
    //adding click event to marker
    google.maps.event.addListener(marker, 'click', function (event) {
        //deviceClickHandler(marker,marker.id);
    });

    var center;
    //adding right click to marker
    google.maps.event.addListener(marker, 'rightclick', function (event) {
        //alert(marker.getDraggable());
        if (lockMode == "off" || marker != lockNode) {
            center = event.latLng;
            abc = dummy1.getProjection();
            var centerproj = abc.fromLatLngToContainerPixel(new google.maps.LatLng(center.lat(), center.lng()));
            $('#customtooltip').css({'top': centerproj.y, 'left': centerproj.x, 'display': 'block'});
            lockMode = 'on';
            lockPos = center;
            lockNode = marker;

            if (marker.getDraggable())
                $('#chkLock').attr('checked', false);
            else
                $('#chkLock').attr('checked', true);
        }
    });
    //adding bounds_changed event to map
    google.maps.event.addListener(map, 'bounds_changed', function (event) {
        if (lockMode == 'on') {
            abc = dummy1.getProjection();
            var centerproj = abc.fromLatLngToContainerPixel(new google.maps.LatLng(lockPos.lat(), lockPos.lng()));
            $('#customtooltip').css({'top': centerproj.y, 'left': centerproj.x, 'display': 'block'});
        }
    });
}

//Function implement the click handler to new discovered host
function deviceClickHandler(marker, id) {// alert(element);alert(id);

    //console.log(element)
    var url = "show_details.py?host_id=" + id;
    $.ajax({
        type: "post",
        url: url,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                alert("Some unknown error occered so please contact your Administrator");
            }
            if (result.success == 1 || result.success == '1')
                alert("Some system error occured  so please contact your Administrator");
            else if (result.success == 2 || result.success == '2') {
                alert("Some database error occured  so please contact your Administrator");
                return;
            }
            else {

                if (newHostConFlag) {
                    newHostConFlag = false;
                    var newMarker = markers_array[markers_array.length - 1];
                    if (marker.id != newMarker.id) {
                        var polyline = new google.maps.Polyline({
                            path: [marker.getPosition(), newMarker.getPosition()]
                        });
                        polyline.setMap(map);

                        newMarker.plines.push(polyline);
                        newMarker.cm.push(marker);

                        //marker.plines.push(polyline);
                        //marker.cm.push(newMarker);
                        //updateNewHostConnInfo(marker.id,newMarker.id);
                        $("#newHostSaver").css("display", "block");

                    }
                }
                else
                    showElementDetails(marker, result.output);

            }

        }

    });
}

/*new discovered host functioality stop here.  */

//Function used to save new added host 						
function saveAdd() {
    var marker = markers_array[markers_array.length - 1];
    if (marker.cm.length == 0) {
        alert("please connect to parent.");
    }
    else {
        marker.cm[0].cm[marker];
        marker.cm[0].plines.push(marker.plines[0]);
        dragHandleFlag = true;
        $("#newHostSaver").css('display', 'none');
        $("#tfbc li[id='" + marker.id + "']").remove();
        newHostUpdate(marker.id, marker.cm[0].title, marker.getPosition().lat(), marker.getPosition().lng());
    }
}

//Function used to undo the action happen to new discovered host
function undoAdd() {
    var marker = markers_array[markers_array.length - 1];
    if (marker.plines.length == 0) {
        marker.setMap(null);
        var newmarkArray = new Array();
        for (i = 0; i < markers_array.length - 1; i++)
            newmarkArray.push(markers_array[i]);
        markers_array = newmarkArray;
        $("#tfbc li[id='" + marker.id + "']").css('display', '');
        dragHandleFlag = true;
        $("#newHostSaver").css('display', 'none');
    }
    else {
        marker.plines[0].setMap(null);
        marker.plines = [];
        marker.cm = [];
        newHostConFlag = true;

    }
}

//This funciton used to draw site groups on map
function drawGroups(groupJson) {
//Iterating json data of site groups
    for (i in groupJson) {
        //alert(JSON.stringify(groupJson[i].member));
        //alert(JSON.stringify(groupJson));
        var groupName = groupJson[i].groupName;
        var maxDistance = 0;
        var midPoint;
        var shost_array = new Array();
        var point1 = 0;
        var point2 = 0;
        var distance = 0;
        //Iterating hosts of site group
        for (var s in groupJson[i].member)
            for (var l in markers_array) {
                if (markers_array[l].title == groupJson[i].member[s].id) {
                    if ((markers_array[l].device_type.toLowerCase().indexOf('odu')) >= 0)
                        (groupJson[i].member[s].state == 'e') ? markers_array[l].setIcon("images/device2.png") : markers_array[l].setIcon("images/device6.png");
                    else if ((markers_array[l].device_type.toLowerCase().indexOf('idu')) >= 0)
                        (groupJson[i].member[s].state == 'e') ? markers_array[l].setIcon("images/device2.png") : markers_array[l].setIcon("images/device6.png");
                    else if ((markers_array[l].device_type.toLowerCase().indexOf('ap')) >= 0)
                        (groupJson[i].member[s].state == 'e') ? markers_array[l].setIcon("images/device2.png") : markers_array[l].setIcon("images/device6.png");
                    else if ((markers_array[l].device_type.toLowerCase().indexOf('swt')) >= 0)
                        (groupJson[i].member[s].state == 'e') ? markers_array[l].setIcon("images/device2.png") : markers_array[l].setIcon("images/device6.png");
                    else
                        (groupJson[i].member[s].state == 'e') ? markers_array[l].setIcon("images/device2.png") : markers_array[l].setIcon("images/device6.png");

                    shost_array.push(markers_array[l]);
                }
            }
        var a = 0;
        //alert(groupJson[i].member.length);
        for (j = 0; j < groupJson[i].member.length; j++) {
            for (k = j + 1; k < groupJson[i].member.length; k++) {
                var point1 = new google.maps.LatLng(parseFloat(groupJson[i].member[j].latitude), parseFloat(groupJson[i].member[j].longitude));
                var point2 = new google.maps.LatLng(parseFloat(groupJson[i].member[k].latitude), parseFloat(groupJson[i].member[k].longitude));
                var distance = distanceBetweenPoints(point1, point2);
                if (distance > maxDistance) {
                    maxDistance = distance;
                    var dLon = point2.lng() - point1.lng();
                    var angle = findAngle(point1.lat(), point2.lat(), dLon);
                    midPoint = getPoint({'latitude': point1.lat(), 'longitude': point1.lng(), 'distance': maxDistance / 2, 'angle': angle});
                }
                a++;
            }
            //alert(j);
            if (distance == 0) {
                //alert(a);
                //alert(JSON.stringify(groupJson[i].member[a]));
                maxDistance = .0111111;
                var angle = findAngle(parseFloat(groupJson[i].member[a].latitude), parseFloat(groupJson[i].member[a].longitude), 0.0021111);
                midPoint = getPoint({'latitude': parseFloat(groupJson[i].member[a].latitude), 'longitude': parseFloat(groupJson[i].member[a].longitude), 'distance': maxDistance / 2, 'angle': angle});
                a = 0;
            }

        }
        //creating instance of google.maps.Circle class to add site to google map
        var circle = new google.maps.Circle({
            strokeColor: "#403E51",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: get_random_color(),
            fillOpacity: 0.35,
            map: map,
            center: midPoint,
            radius: (maxDistance * 1000 * 3) / 4
        });
        //setting property hostarray to site that represend members
        circle.set('hostarray', shost_array);
        //creating instance of google.maps.Marker that represent center of site on map
        var centermark = new google.maps.Marker({
            position: midPoint,
            icon: "images/site.png",
            draggable: true,
            title: groupName,
            map: map
        });
        centermark.set('moveOut', false);
        bindDragToHostSite(circle, centermark);
        circle.set("centermarker", centermark);
        circle.set("id", groupName);
        circles_array.push(circle);

    }
}

// function  create by rajendra
function get_random_color() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.round(Math.random() * 15)];
    }
    return color;
}

//function used to handle cheking of moveOut functionality of site groups
function checkMoveOut(element) {
    //Iterating site of map
    for (i in circles_array) {
        if (circles_array[i].centermarker.title == $(element).attr('cstitle'))
            if (element.checked) {
                circles_array[i].centermarker.set('moveOut', true);
                $('#customtooltip1').css('display', 'none');
            }
            else {
                $('#customtooltip1').css('display', 'none');
                circles_array[i].centermarker.set('moveOut', false);
            }
    }


}

//Function used to implement dragging functionality of site groups
function bindDragToHostSite(circle, centermark) {
    google.maps.event.addListener(centermark, 'rightclick', function (event) {

        var center = event.latLng;
        var abc = dummy1.getProjection();
        var centerproj = abc.fromLatLngToContainerPixel(new google.maps.LatLng(center.lat(), center.lng()));
        $('#customtooltip1').css({'top': centerproj.y, 'left': centerproj.x, 'display': 'block'});
        $('#chkMoveOut').attr("cstitle", centermark.title);
        if (centermark.moveOut)
            $('#chkMoveOut').attr('checked', true);
        else
            $('#chkMoveOut').attr('checked', false);

    });
    google.maps.event.addListener(centermark, 'dragend', function (e) {
        for (m in circle.hostarray) {
            var ppos = circle.hostarray[m].getPosition();
            var distance = distanceBetweenPoints(circle.getCenter(), ppos);
            var angle = findAngle(circle.getCenter().lat(), ppos.lat(), (ppos.lng() - circle.getCenter().lng()));
            var newpos = getPoint({latitude: e.latLng.lat(), longitude: e.latLng.lng(), distance: distance, angle: angle});
            circle.hostarray[m].setPosition(newpos);
            for (var p = 0; p < circle.hostarray[m].plines.length; p++)
                circle.hostarray[m].plines[p].setPath([circle.hostarray[m].getPosition(), circle.hostarray[m].cm[p].getPosition()]);

            if (lockMode == "on") {
                $('#customtooltip').hide();
                lockMode = "off";
                lockNode = null;
            }

            movedSiteLocations.push(new Array(circle.hostarray[m], ppos));
        }
        lastHostMoved.push(new Array(centermark, circle.getCenter()));
        $('.map5saveloc').show();
        circle.setCenter(e.latLng);

    });
}

//Function used to calculate distance between points
function distanceBetweenPoints(p1, p2) {
    var R = 6371; // earth's mean radius in km
    var dLat = (p2.lat() - p1.lat()) * Math.PI / 180;
    var dLong = (p2.lng() - p1.lng()) * Math.PI / 180;
    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos((p1.lat()) * Math.PI / 180) * Math.cos((p2.lat()) * Math.PI / 180) * Math.sin(dLong / 2) * Math.sin(dLong / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var d = R * c;
    return d;
}

//Function used to find point in latlong if a point, distance from point and angle from point is given
function getPoint(pointOptions) {
    var lat1 = pointOptions.latitude * Math.PI / 180;
    var lon1 = pointOptions.longitude * Math.PI / 180;
    var R = 6371;
    var d = pointOptions.distance;
    var lat = Math.asin(Math.sin(lat1) * Math.cos(d / R) + Math.cos(lat1) * Math.sin(d / R) * Math.cos(pointOptions.angle * Math.PI / 180));

    var lon = lon1 + Math.atan2(Math.sin(pointOptions.angle * Math.PI / 180) * Math.sin(d / R) * Math.cos(lat1), Math.cos(d / R) - Math.sin(lat1) * Math.sin(lat));
    lat = lat * 180 / Math.PI;
    lon = lon * 180 / Math.PI;
    return new google.maps.LatLng(lat, lon);
}

//Function used to calculated angle between two points	
function findAngle(lat1, lat2, dLon) {
    lat1 = lat1 * Math.PI / 180;
    lat2 = lat2 * Math.PI / 180;
    dLon = dLon * Math.PI / 180;
    var y = Math.sin(dLon) * Math.cos(lat2);
    var x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLon);
    var brng = Math.atan2(y, x) * 180 / Math.PI;
    return brng;
}

//Function used to save movement of site group
function saveSiteMove() {
    $("#map_canvas").saveSiteMove();
    $('.map5saveloc').hide();
}

//Function used to undo in previous position of site group
function undoSiteMove() {
    if (lastHostMoved.length > 0) {
        var mark = lastHostMoved[lastHostMoved.length - 1][0];
        var pos = lastHostMoved[lastHostMoved.length - 1][1];
        for (i in circles_array) {
            if (mark.title == circles_array[i].id) {
                var circle = circles_array[i];
                for (m in circle.hostarray) {
                    var ppos = circle.hostarray[m].getPosition();
                    var distance = distanceBetweenPoints(circle.getCenter(), ppos);
                    var angle = findAngle(circle.getCenter().lat(), ppos.lat(), (ppos.lng() - circle.getCenter().lng()));
                    var newpos = getPoint({latitude: pos.lat(), longitude: pos.lng(), distance: distance, angle: angle});
                    circle.hostarray[m].setPosition(newpos);
                    for (var p = 0; p < circle.hostarray[m].plines.length; p++)
                        circle.hostarray[m].plines[p].setPath([circle.hostarray[m].getPosition(), circle.hostarray[m].cm[p].getPosition()]);
                    if (lockMode == "on") {
                        $('#customtooltip').hide();
                        markers_arraylockMode = "off";
                        lockNode = null;
                    }

                    movedSiteLocations.push(new Array(circle.hostarray[m], ppos));
                }
                circle.setCenter(pos);
                mark.setPosition(pos);
            }
        }
        lastHostMoved.splice(lastHostMoved.length - 1);
        if (lastHostMoved.length == 0)
            $('.map5saveloc').hide();
    }
}

// ######################################################### Code by rajendra ###########################
function Label(opt_options) {
    // Initialization
    this.setValues(opt_options);
    // Here go the label styles
    var span = this.span_ = document.createElement('span');
    span.style.cssText = 'position: relative; left: -50%; top: -35px; ' +
        'white-space: nowrap;color:#ffffff;' +
        'padding: 2px;font-family: Arial; font-weight: bold;' +
        'font-size: 12px;';
    var div = this.div_ = document.createElement('div');
    div.appendChild(span);
    div.style.cssText = 'position: absolute; display: none';
};
Label.prototype = new google.maps.OverlayView;
Label.prototype.onAdd = function () {
    var pane = this.getPanes().overlayImage;
    pane.appendChild(this.div_);
    // Ensures the label is redrawn if the text or position is changed.
    var me = this;
    this.listeners_ = [
        google.maps.event.addListener(this, 'position_changed',
            function () {
                me.draw();
            }),
        google.maps.event.addListener(this, 'text_changed',
            function () {
                me.draw();
            }),
        google.maps.event.addListener(this, 'zindex_changed',
            function () {
                me.draw();
            })
    ]
};
// Implement onRemove
Label.prototype.onRemove = function () {
    this.div_.parentNode.removeChild(this.div_);
    // Label is removed from the map, stop updating its position/text.
    for (var i = 0, I = this.listeners_.length; i < I; ++i) {
        google.maps.event.removeListener(this.listeners_[i]);
    }
};
// Implement draw
Label.prototype.draw = function () {
    var projection = this.getProjection();
    var position = projection.fromLatLngToDivPixel(this.get('position'));
    var div = this.div_;
    div.style.left = position.x + 'px';
    div.style.top = position.y + 'px';
    div.style.display = 'block';
    div.style.zIndex = this.get('zIndex'); //ALLOW LABEL TO OVERLAY MARKER
    this.span_.innerHTML = this.get('text').toString();
};
// ###############################################################################


//Function discover the state changed of host
function updateStateOfHost(updateInfo) {
    for (j in updateInfo) {
        for (k in markers_array) {
            //markers_array[k].plines[0].setOptions({'strokeColor':'red'});
            if (markers_array[k].title == updateInfo[j].id) {
                if ((markers_array[k].device_type.toLowerCase().indexOf('odu16')) >= 0) {

                    //markers_array[k].setIcon("images/odu-"+updateInfo[j].state+".png");
                    if (labelFlag == 0) {
                        var label = new Label({
                            map: map
                        });
                        label.set('zIndex', 1234);
                        label.bindTo('position', markers_array[k], 'position');
                        label.set('text', '<div style="text-align:center;margin-top:-24px;font-size:10px;">RM18<br/>' + String(updateInfo[j].signal) + '</div>');
                        markers_array[k].setIcon("images/device" + updateInfo[j].state + ".png");
                        labelDict[markers_array[k].title] = label
                    }
                    else {
                        markers_array[k].setIcon("images/device" + updateInfo[j].state + ".png");
                        labelDict[markers_array[k].title].set('text', '<div style="text-align:center;margin-top:-24px;font-size:10px;">RM18<br/>' + String(updateInfo[j].signal) + '</div>');
                    }

                }
                else if ((markers_array[k].device_type.toLowerCase().indexOf('odu100')) >= 0) {
                    if (labelFlag == 0) {
                        var label = new Label({
                            map: map
                        });
                        label.set('zIndex', 1234);
                        label.bindTo('position', markers_array[k], 'position');
                        label.set('text', '<div style="text-align:center;margin-top:-24px;font-size:10px;">RM<br/>' + String(updateInfo[j].signal) + '</div>');
                        markers_array[k].setIcon("images/device" + updateInfo[j].state + ".png");
                        labelDict[markers_array[k].title] = label
                    }
                    else {
                        markers_array[k].setIcon("images/device" + updateInfo[j].state + ".png");
                        labelDict[markers_array[k].title].set('text', '<div style="text-align:center;margin-top:-24px;font-size:10px;">RM<br/>' + String(updateInfo[j].signal) + '</div>');
                    }

                }
                else if ((markers_array[k].device_type.toLowerCase().indexOf('idu')) >= 0) {
                    //markers_array[k].setIcon("images/idu-"+updateInfo[j].state+".png");
                    if (labelFlag == 0) {
                        var label = new Label({
                            map: map
                        });
                        label.set('zIndex', 1234);
                        label.bindTo('position', markers_array[k], 'position');
                        label.set('text', '<div style="text-align:center;margin-top:-24px;font-size:10px;">IDU</div>');
                        markers_array[k].setIcon("images/device" + updateInfo[j].state + ".png");
                        labelDict[markers_array[k].title] = label
                    }
                    else {
                        markers_array[k].setIcon("images/device" + updateInfo[j].state + ".png");
                        labelDict[markers_array[k].title].set('text', '<div style="text-align:center;margin-top:-24px;font-size:10px;">IDU</div>');
                    }
                }
                else if ((markers_array[k].device_type.toLowerCase().indexOf('ap')) >= 0) {
                    if (labelFlag == 0) {
                        var label = new Label({
                            map: map
                        });
                        label.set('zIndex', 1234);
                        label.bindTo('position', markers_array[k], 'position');
                        label.set('text', '<div style="text-align:center;margin-top:-24px;font-size:10px;">AP<br/>' + String(updateInfo[j].client) + '</div>');
                        markers_array[k].setIcon("images/device" + updateInfo[j].state + ".png");
                        labelDict[markers_array[k].title] = label
                    }
                    else {
                        markers_array[k].setIcon("images/device" + updateInfo[j].state + ".png");
                        labelDict[markers_array[k].title].set('text', '<div style="text-align:center;margin-top:-24px;font-size:10px;">AP<br/>' + String(updateInfo[j].client) + '</div>');
                    }
                }
                else if ((markers_array[k].device_type.toLowerCase().indexOf('ccu')) >= 0) {
                    if (labelFlag == 0) {
                        var label = new Label({
                            map: map
                        });
                        label.set('zIndex', 1234);
                        label.bindTo('position', markers_array[k], 'position');
                        label.set('text', '<div style="text-align:center;margin-top:-24px;font-size:10px;">CCU<br/></div>');
                        markers_array[k].setIcon("images/device" + updateInfo[j].state + ".png");
                        labelDict[markers_array[k].title] = label
                    }
                    else {
                        markers_array[k].setIcon("images/device" + updateInfo[j].state + ".png");
                        labelDict[markers_array[k].title].set('text', '<div style="text-align:center;margin-top:-24px;font-size:10px;">CCU<br/></div>');
                    }
                }
                else if ((markers_array[k].device_type.toLowerCase().indexOf('mou')) >= 0) {
                    if (labelFlag == 0) {
                        var label = new Label({
                            map: map
                        });
                        label.set('zIndex', 1234);
                        label.bindTo('position', markers_array[k], 'position');
                        label.set('text', '<div style="text-align:center;margin-top:-24px;font-size:10px;">MOU<br/></div>');

                        markers_array[k].setIcon("images/device" + updateInfo[j].state + ".png");
                        labelDict[markers_array[k].title] = label
                    }
                    else {
                        markers_array[k].setIcon("images/device" + updateInfo[j].state + ".png");
                        labelDict[markers_array[k].title].set('text', '<div style="text-align:center;margin-top:-24px;font-size:10px;">MOU<br/></div>');
                    }
                }
                else if ((markers_array[k].device_type.toLowerCase().indexOf('rou')) >= 0) {
                    if (labelFlag == 0) {
                        var label = new Label({
                            map: map
                        });
                        label.set('zIndex', 1234);
                        label.bindTo('position', markers_array[k], 'position');
                        label.set('text', '<div style="text-align:center;margin-top:-24px;font-size:10px;">ROU<br/></div>');
                        markers_array[k].setIcon("images/device" + updateInfo[j].state + ".png");
                        labelDict[markers_array[k].title] = label
                    }
                    else {
                        markers_array[k].setIcon("images/device" + updateInfo[j].state + ".png");
                        labelDict[markers_array[k].title].set('text', '<div style="text-align:center;margin-top:-24px;font-size:10px;">ROU<br/></div>');
                    }
                }

                else if ((markers_array[k].device_type.toLowerCase().indexOf('swt')) >= 0) {
                    markers_array[k].setIcon("images/switch-" + updateInfo[j].state + ".png");
                }
                else if ((markers_array[k].title.toLowerCase().indexOf('localhost')) >= 0) {
                    markers_array[k].setIcon("images/localhost-" + updateInfo[j].state + ".png");
                }
                else

                //console.log(markers_array[k].device_type.toLowerCase());
                    markers_array[k].setIcon("images/unknown-" + updateInfo[j].state + ".png");
            }
        }
    }
    labelFlag = 1;
}
/*======================code ended by pawan=======================*/


// change the state of device
function enabledDevice(ip_address) {
    $.ajax({
        type: "post",
        url: "enabled_device_state.py?ip_address=" + ip_address,
        success: function (result) {
            if (result.success == 1 || result.success == '1')
                alert(result.error_msg);
            else
                alert('Host state update successfully.');
        }
    });
}


