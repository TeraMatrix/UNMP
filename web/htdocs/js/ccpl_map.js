/*
===========================================================================
* jQuery CCPL using Google Map Javascript API
* Created by - Deepak Arora
* Version - ccpl_map.js v1.3
* This JQuery File use to display your data over google map simply.
* Requires jquery-1.6.1.js or jquery-1.6.1.min.js
* Copyright (c) 2010 Deepak Arora - Code Scape Consultants Pvt. Ltd. 
===========================================================================
*/
var newHostParent=[];
var markers_array  = [];
var map;
var finalArr = [];
var status = [];
var nmsArr = new Array();
var nmsDetailsArr = new Array();
var Dummy1;
var abc;
var lockMode = 'off';
var lockPos;
var lockNode;
var movedLocations = new Array();
var lastMovedPos;

function Dummy(map) {
    this.setMap(map);
}

Dummy.prototype = new google.maps.OverlayView();
Dummy.prototype.draw = function () {
};
Dummy.prototype.onAdd = function () { };
Dummy.prototype.onRemove = function () { };

(function($) {
 jQuery.fn.extend({
    ccplMap: function (settings) {
        settings = jQuery.extend({
            title: "MyMap", 
            type: "TERRAIN",           
	    option : {},
            centerLat: 26.90,
			centerLng: 75.80,		
			parent: this,
			zoom : 05,
			nmsData : "",
			parentId : this.attr('id'),
			onNMSClick : function(id) { alert('No function is defined to handle NMS click'); },
			onElementClick : function(marker,id) { alert('No function is defined to handle Element click'); },
			onUpdate : function(changes) { alert("No function is defined for update"); },
			onDragStart : function(event) { alert("Drag start"); },
			onDrag : function(event) { alert("Drag drag"); },
			onDragEnd : function(event) { alert("Drag end"); }
        }, settings);
        jQuery.fn.ccplMap.settings = ccplJs.s = settings;

        //to make the div empty
        jQuery(this).html("");
        ccplJs.mapControlFunction.addMap();      
        ccplJs.mapControlFunction.showNMS(); 
	map.setCenter(new google.maps.LatLng(26.76,76.80));
	map.setZoom(4);
        return false;
    }
});
var ccplJs = jQuery.ccplMap = {
    version: "1.3",
	obj: {
        	parent: function () { return jQuery(ccplJs.s.parent); }
	},
    mapControlFunction:
    {
        addMap: function () {	
			var latlng = new google.maps.LatLng(26.90, 75.80);
            var maptype;
            
            if(ccplJs.s.type.toUpperCase() == "ROADMAP")
                maptype = google.maps.MapTypeId.ROADMAP;
            else if(ccplJs.s.type.toUpperCase() == "HYBRID")
                maptype = google.maps.MapTypeId.TERRAIN;

			var myOptions = {
			  zoom: ccplJs.s.zoom,
			  center: new google.maps.LatLng(ccplJs.s.centerLat,ccplJs.s.centerLng),
			  mapTypeId: maptype
			};
			map = new google.maps.Map(document.getElementById(ccplJs.s.parentId), myOptions);			
			
			dummy1 = new Dummy(map);
			abc1 = dummy1.getProjection();		
        },
		showNMS: function() {
			
			$.each(ccplJs.s.nmsData,function(i,dt) {
				var marker = new google.maps.Marker({
					position: new google.maps.LatLng(parseFloat(ccplJs.s.nmsData[i].lt),parseFloat(ccplJs.s.nmsData[i].lg)),
					map:map,
					draggable: true,
					icon: "images/nms.png",
					title:ccplJs.s.nmsData[i].name
				});		
				
				bindHover(marker,map,ccplJs.s.nmsData[i]);
				bindNMSClick(marker,ccplJs.s.nmsData[i],ccplJs);
				nmsArr.push(marker);
			});
			
			map.setCenter(new google.maps.LatLng(ccplJs.s.centerLat,ccplJs.s.centerLng));			
	    },			
		centerTheMap : function () {  
			var bounds = new google.maps.LatLngBounds();	
			for (i in markers_array) {        
				bounds.extend(markers_array[i].getPosition());
				map.fitBounds(bounds);
			}
		},
		getMarkerById : function(id) {	
			for(i in markers_array)							
				if(markers_array[i].id == id)			
					return markers_array[i];
		}		
	}    
};

$.fn.coverAll = function(lat,lng,title) {
	var bounds = new google.maps.LatLngBounds();	
	for (i in markers_array) {        
		bounds.extend(markers_array[i].getPosition());
		map.fitBounds(bounds);
	}
};

$.fn.addNewMarker = function(lat,lng,title) {
	var marker = new google.maps.Marker({
		position: new google.maps.LatLng(lat,lng),
		map:map,
		draggable: true,
		title:title	
	});	
};

$.fn.setMarkersDrag = function(status) {
	for(var i=0;i<markers_array.length;i++) 
		markers_array[i].setDraggable(status);	
};

$.fn.setMarkersVisibility = function(status) {
	for(i in markers_array) {
		markers_array[i].setVisible(status);
	}
};

$.fn.showTopMarkers = function(count) {
	for(i in markers_array) {
		if(i<count)
			markers_array[i].setVisible(true);
		else
			markers_array[i].setVisible(false);
	}
};

$.fn.bindElementClick = function (marker) {		
	google.maps.event.addListener(marker, 'click', function (event) {
		if(newHostConFlag){
			newHostConFlag=false;			
			var newMarker=markers_array[markers_array.length-1];			
			
			
			if(marker.id!=newMarker.id){
			var polyline = new google.maps.Polyline({
				path : [marker.getPosition(),newMarker.getPosition()]
			});
			polyline.setMap(map);			
			
			newMarker.plines.push(polyline);
			newMarker.cm.push(marker);
			
			//marker.plines.push(polyline);
			//marker.cm.push(newMarker);
			
			$("#newHostSaver").css("display","block");
				
			}
			
		}		
		else
		ccplJs.s.onElementClick(marker,marker.id);
	});
};
$.fn.bindDeviceDrag = function (marker) {
		
	google.maps.event.addListener(marker, 'dragstart', function (event) {	
		lastMovedPos = event.latLng;
	});

	google.maps.event.addListener(marker, 'drag', function (event) {
		var siteFlag=false;
		for(i in circles_array){
			for(k in circles_array[i].hostarray)
			if(marker.id==circles_array[i].hostarray[k].id)
			if(!circles_array[i].centermarker.moveOut){
			siteFlag=true;
			var distance=distanceBetweenPoints(circles_array[i].getCenter(),event.latLng)*1000;
			if(distance>=circles_array[i].getRadius()){
			var angle=findAngle(circles_array[i].getCenter().lat(),event.latLng.lat(),(event.latLng.lng()-circles_array[i].getCenter().lng()));
			var newpos=getPoint({latitude:circles_array[i].getCenter().lat(),longitude:circles_array[i].getCenter().lng(),distance:parseFloat(circles_array[i].getRadius())/1000,angle:angle});
			
			marker.setPosition(newpos);
			for(var p = 0;p < marker.plines.length;p++)
			marker.plines[p].setPath([marker.getPosition(),marker.cm[p].getPosition()]);		
			if(lockMode == "on"){
				$('#customtooltip').hide();
				lockMode = "off";
				lockNode = null;
			}
			}
			else{
				for(var p = 0;p < marker.plines.length;p++)
				marker.plines[p].setPath([marker.getPosition(),marker.cm[p].getPosition()]);		
				if(lockMode == "on"){
				$('#customtooltip').hide();
				lockMode = "off";
				lockNode = null;
			}
			}			
			}
			else{
			var distance=distanceBetweenPoints(circles_array[i].getCenter(),event.latLng)*1000;
			if(distance>circles_array[i].getRadius())
			circles_array[i].setRadius(distance);	
			}	
			}
		
		if(!siteFlag){		
		for(var p = 0;p < marker.plines.length;p++)
			marker.plines[p].setPath([event.latLng,marker.cm[p].getPosition()]);		
			if(lockMode == "on"){
				$('#customtooltip').hide();
				lockMode = "off";
				lockNode = null;
			}
			
		}
	});
	google.maps.event.addListener(marker, 'dragend', function (event) {	
		$('.map3saveloc').show();
		movedLocations.push(new Array(marker,lastMovedPos));
	});	
};

$.fn.showElementDetails = function (marker,html) {			
    var info = new google.maps.InfoWindow({
        content: html,
		map:map
    });	
	
	info.open(map, marker);
};
$.fn.undoMove = function () { 
	if(movedLocations.length > 0) {
		var marker = movedLocations[movedLocations.length - 1][0];
		var pos =  movedLocations[movedLocations.length - 1][1];

		
		// Resetting the Marker position to last position.
		marker.setPosition(pos);
		
		// Resetting the Connecting lines of moved device.
		for(var p = 0;p < marker.plines.length;p++)
			marker.plines[p].setPath([pos,marker.cm[p].getPosition()]);
			
		// Removing the last moved positions from array.
		if(movedLocations.length > 0)
			movedLocations.splice(movedLocations.length-1);			
		
		// If no element is left for move hide the undo area.
		if(movedLocations.length == 0){ 
			$('.map3saveloc').hide();
			
		}
	}
};
$.fn.saveSiteMove= function () { 
	var changes = new Array();
	var found = false;

	for(var i=0;i < movedSiteLocations.length;i++) {
		found = false;		
		
		for(var j=0;j < changes.length;j++) {
			if(movedSiteLocations[i][0] == changes[j][0])	{				
				found = true;
				//movedLocations.splice(j);
				break;
			}	
		}
		
		if(found == false) {
			changes.push({ele : movedSiteLocations[i][0].id, lt : movedSiteLocations[i][0].getPosition().lat(), lg : movedSiteLocations[i][0].getPosition().lng() });
		}
		//changes.push({ele : movedLocations[i][0].id, lt : movedLocations[i][0].getPosition().lat(), lg : movedLocations[i][0].getPosition().lng() });
	}

	
	ccplJs.s.onUpdate(changes);
	movedSiteLocations = [];	
	
	
};

$.fn.saveMove = function () { 
	var changes = new Array();
	var found = false;

	for(var i=0;i < movedLocations.length;i++) {
		found = false;		
		
		for(var j=0;j < changes.length;j++) {
			if(movedLocations[i][0] == changes[j][0])	{				
				found = true;
				//movedLocations.splice(j);
				break;
			}	
		}
		
		if(found == false) {
			changes.push({ele : movedLocations[i][0].id, lt : movedLocations[i][0].getPosition().lat(), lg : movedLocations[i][0].getPosition().lng() });
		}
		//changes.push({ele : movedLocations[i][0].id, lt : movedLocations[i][0].getPosition().lat(), lg : movedLocations[i][0].getPosition().lng() });
	}

	
	ccplJs.s.onUpdate(changes);
	movedLocations = [];	
	
	
};

$.fn.bindLockUnclock = function (marker) {
	var center;
	google.maps.event.addListener(marker, 'rightclick', function (event) {
		//alert(marker.getDraggable());
		if(lockMode == "off" || marker != lockNode) {			
			center = event.latLng;
			abc = dummy1.getProjection();					
			var centerproj = abc.fromLatLngToContainerPixel(new google.maps.LatLng(center.lat(), center.lng()));			
			$('#customtooltip').css({'top':centerproj.y,'left':centerproj.x,'display':'block'});
			lockMode = 'on';
			lockPos = center;
			lockNode = marker;
			
			if(marker.getDraggable())
				$('#chkLock').attr('checked', false);
			else
				$('#chkLock').attr('checked', true);
		}	
	});
	
	google.maps.event.addListener(map, 'bounds_changed', function (event) {
		if(lockMode == 'on') {			
			abc = dummy1.getProjection();					
			var centerproj = abc.fromLatLngToContainerPixel(new google.maps.LatLng(lockPos.lat(), lockPos.lng()));			
			$('#customtooltip').css({'top':centerproj.y,'left':centerproj.x,'display':'block'});
		}	
	});
	
};

$.fn.showNMSDetails = function(nmsDetails) {	
	//Clears the NMS devices from MAP.
	for(var i=0;i<nmsArr.length;i++)	
		nmsArr[i].setMap(null);	
	
	var bounds = new google.maps.LatLngBounds();	
	var icon;
	var isDrag;
	for(var i=0;i<nmsDetails.length;i++) {	
		isDrag = true;
		icon = (nmsDetails[i].type == "host") ? ((nmsDetails[i].state == "d") ? "images/Ldown.png" : "images/localhost-0.png" ) : "images/site.png";
		isDrag = (nmsDetails[i].lck && nmsDetails[i].lck == "t") ? false : true;

		
		var marker = new google.maps.Marker({ 
				position: new google.maps.LatLng(parseFloat(nmsDetails[i].lt),parseFloat(nmsDetails[i].lg)),
				map:map,
				draggable: isDrag,
				icon: icon,
				title:nmsDetails[i].name
		});
		marker.setMap(map);	
		marker.set('cm',new Array());
		marker.set('id',nmsDetails[i].id);
		marker.set('device_type',nmsDetails[i].device_type);
		marker.plines = [];
	
		bounds.extend( new google.maps.LatLng(parseFloat(nmsDetails[i].lt),parseFloat(nmsDetails[i].lg)));
		map.fitBounds(bounds);
		markers_array.push(marker);	
		nmsDetailsArr.push(marker);
		
		if(nmsDetails[i].child && nmsDetails[i].child.length > 0) {			
			nmsDetails[i].child.plines = [];			
			this.recurseChild(marker,nmsDetails[i].child,nmsDetails[i].name,nmsDetails[i].lt,nmsDetails[i].lg);		
		       
                }
		else{
                        
			this.bindDeviceDrag(marker);
			this.bindLockUnclock(marker);
			this.bindElementClick(marker);
		}		
	}
	this.coverAll();
};

	$.fn.recurseChild = function(parent,node,name,lt,lg) {		
		var point1 = new google.maps.LatLng(parseFloat(lt),parseFloat(lg));		
		this.bindDeviceDrag(parent);
		this.bindLockUnclock(parent);	
		this.bindElementClick(parent);
			
		var icon;
		var isDrag;
		for(var i=0;i<node.length;i++)	{
			if (node[i].device_type.toLowerCase().indexOf('odu')>=0)
				icon = (node[i].type == "host") ? ((node[i].state == "d") ? "images/Odown.png" : "images/odu-0.png" ) : "images/site.png";
			else if (node[i].device_type.toLowerCase().indexOf('idu')>=0)
				icon = (node[i].type == "host") ? ((node[i].state == "d") ? "images/Idown.png" : "images/idu-0.png" ) : "images/site.png";
			else if (node[i].device_type.toLowerCase().indexOf('swt')>=0)
				icon = (node[i].type == "host") ? ((node[i].state == "d") ? "images/Sdown.png" : "images/switch-0.png" ) : "images/site.png";
			else
				icon = (node[i].type == "host") ? ((node[i].state == "d") ? "images/Udown.png" : "images/unknown-0.png" ) : "images/site.png";
			isDrag = (node[i].lck && node[i].lck == "t") ? false : true; 
			var marker = new google.maps.Marker({
				
				position: new google.maps.LatLng(parseFloat(node[i].lt),parseFloat(node[i].lg)),
				map:map,
				draggable: isDrag,
				icon: icon,
				title:node[i].name
			});

			 //console.log(node[i].name + " ===> " + node[i].lt + "," + node[i].lg);
			marker.setMap(map);
			marker.set('id',node[i].id);
			marker.set('device_type',node[i].device_type);
			marker.set('cm',new Array());
			marker.set('plines',new Array());
			
			var point2 = new google.maps.LatLng(parseFloat(node[i].lt),parseFloat(node[i].lg));
						
			var polyline = new google.maps.Polyline({
				path : [point1, point2]
			});
			polyline.setMap(map);			
			
			marker.plines.push(polyline);
			marker.cm.push(parent);
			
			parent.plines.push(polyline);
			parent.cm.push(marker);
				
			//alert(marker.getPosition().lat());
			markers_array.push(marker);	
			
			if(node[i].child && node[i].child.length > 0) {	
				this.recurseChild(marker,node[i].child,node[i].name,node[i].lt,node[i].lg,true);
			}
			else {				
				this.bindDeviceDrag(marker);
				this.bindLockUnclock(marker);
				this.bindElementClick(marker);
			}
		}	
};
})(jQuery);

	
function bindHover(marker,map,obj) {
	var content = "<div><table style=\"width:300px;font-size:11px;\"><colgroup><col width=\"45%\"/><col width=\"5%\"/><col/></colgroup><tr><th align=\"left\" colspan=\"3\"><img src=\"images/nms.png\" alt=\"\" title=\"nms\" style=\"width:12px;\"/> NMS Details<hr/></th></tr><tr><td>Name </td><td>:</td><td>" + obj.name + "</td><tr><tr><td>Total Devices </td><td>:</td><td>"+ obj.tH +"</td></tr><tr><td>Enable Devices </td><td>:</td><td>"+obj.eH+"</td></tr><tr><td>Disable Devices </td><td>:</td><td>"+(obj.tH - obj.eH)+"</td></tr></table></div>";
	var info = new google.maps.InfoWindow({
		content: content
	});
		
	google.maps.event.addListener(marker, 'mouseover', function (event) {	
		info.open(map,marker);
	});
	
	google.maps.event.addListener(marker, 'mouseout', function (event) {	
		info.close();
	});
}
function bindNMSClick(marker,obj,ccplJs) {		
	google.maps.event.addListener(marker, 'click', function (event) {	
			
		ccplJs.s.onNMSClick(obj.name);
	});	
}
// Function to undo the Positions dragged.
function undoMove() {
	$("#map_canvas").undoMove();
}
// Save the updated device positions.
function saveMove() {
	$("#map_canvas").saveMove();
	$('.map3saveloc').hide();
	
}

// Handle device Movement.
function deviceLockUnlock(element) {	
	if(element.checked)
		lockNode.setDraggable(false);
	else
		lockNode.setDraggable(true);
	
	lockMode = 'off';
    $(element).parent('div').hide();
}


