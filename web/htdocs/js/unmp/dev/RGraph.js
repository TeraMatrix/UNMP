var labelType, useGradients, nativeTextSupport, animate;
var json = {}
var nmsShowStatus = true;
(function () {
    var ua = navigator.userAgent,
        iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
        typeOfCanvas = typeof HTMLCanvasElement,
        nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
        textSupport = nativeCanvasSupport
            && (typeof document.createElement('canvas').getContext('2d').fillText == 'function');
    //I'm setting this based on the fact that ExCanvas provides text support for IE
    //and that as of today iPhone/iPad current text support is lame
    labelType = (!nativeCanvasSupport || (textSupport && !iStuff)) ? 'Native' : 'HTML';
    nativeTextSupport = labelType == 'Native';
    useGradients = nativeCanvasSupport;
    animate = !(iStuff || !nativeCanvasSupport);

})();

var Log = {
    elem: false,
    write: function (text) {
        if (!this.elem)
            this.elem = document.getElementById('log');
        this.elem.innerHTML = text;
        //this.elem.style.left = (500 - this.elem.offsetWidth / 2) + 'px';
        this.elem.style.left = '10px';
    }
};

function init() {
    //init RGraph

    var rgraph = new $jit.RGraph({
        //Where to append the visualization
        injectInto: 'infovis',
        //Optional: create a background canvas that plots
        //concentric circles.
        background: {
            CanvasStyles: {
                strokeStyle: '#93C3F2'
            }
        },
        //Add navigation capabilities:
        //zooming by scrolling and panning.
        Navigation: {
            enable: true,
            panning: true,
            zooming: 10
        },
        //Set Node and Edge styles.
        Node: {
            color: '#db4b38'
        },

        Edge: {
            color: '#999',
            lineWidth: 1.5
        },

        onBeforeCompute: function (node) {
            Log.write("centering " + node.name + "...");
            //Add the relation list in the right column.
            //This list is taken from the data property of each JSON node.
            $jit.id('inner_details').innerHTML = node.data.relation;
        },

        //Add the name of the node in the correponding label
        //and a click handler to move the graph.
        //This method is called once, on label creation.
        onCreateLabel: function (domElement, node) {
            domElement.innerHTML = node.name;
            domElement.onclick = function () {
                //alert(node.name);
                showHostDetails(node.name); // function calling for host details
                nmsInNetwork();
                rgraph.onClick(node.id, {
                    onComplete: function () {
                        Log.write("Done");
                    }
                });
            };
        },
        //Change some label dom properties.
        //This method is called each time a label is plotted.
        onPlaceLabel: function (domElement, node) {
            var style = domElement.style;
            style.display = '';
            style.cursor = 'pointer';

            if (node._depth <= 1) {
                style.fontSize = "0.8em";
                style.color = "#0048CE";

            } else if (node._depth == 2) {
                style.fontSize = "0.7em";
                style.color = "#494949";

            } else {
                style.display = 'none';
            }

            var left = parseInt(style.left);
            var w = domElement.offsetWidth;
            style.left = (left - w / 2) + 'px';
        }
    });
    //load JSON data
    rgraph.loadJSON(json);
    //trigger small animation
    rgraph.graph.eachNode(function (n) {
        var pos = n.getPos();
        pos.setc(-200, -200);
    });
    rgraph.compute('end');
    rgraph.fx.animate({
        modes: ['polar'],
        duration: 2000
    });
    //end
    //append information about the root relations in the right column
    $jit.id('inner_details').innerHTML = rgraph.graph.getNode(rgraph.root).data.relation;
    nmsInNetwork();
}


/*function showHideNmsWindow(){
 $("div#ctr").click(function(){
 $(this).parent().toggleClass("hide");
 if($(this).hasClass("h"))
 {
 $(this).removeClass('h').addClass('s');
 }
 else
 {
 $(this).removeClass('s').addClass('h');
 }
 });
 }*/



// This function show total exists NMS in the system.
function nmsInNetwork() {
    //get the nms detail
    /*     $("div#ctr").click(function(){
     alert('call');
     $(this).parent().toggleClass("hide");
     if($(this).hasClass("h"))
     {
     $(this).removeClass('h').addClass('s');
     }
     else
     {
     $(this).removeClass('s').addClass('h');
     }
     });*/

    if (nmsShowStatus == true) {
        $.ajax({
            type: "post",
            url: "network_nms_details.py",
            success: function (result) {
                try {
                    result = eval("(" + result + ")");
                }
                catch (err) {
                    $().toastmessage('showErrorToast', "Some unknown errored occured, so please contact your Administrator");
                    return;
                }
                if (result.success == 1 || result.success == '1') {
                    $().toastmessage('showErrorToast', 'Some system error occured, so please contact your Administrator');
                }
                else if (result.success == 2 || result.success == '2') {
                    $().toastmessage('showErrorToast', 'Some database error occured, so please contact your Administrator');
                    return;
                }
                else {
                    data = eval(result.output);
                    var html = "";
                    var l = data.length;
                    html += "<ul>";
                    if (l > 0) {
                        for (var i = 0; i < l; i++) {
                            if ($("#nms_instance").val() == data[i].name) {
                                html += "<li class=\"nms_selected\" id=" + data[i].name + "><a href=\"#\" style=\"text-decoration: none\" onClick=\"showNetworkGraph('" + data[i].name + "')\">" + data[i].name + "</a></li>";
                            }
                            else {
                                html += "<li id=" + data[i].name + "><a href=\"#\" style=\"text-decoration: none\" onClick=\"showNetworkGraph('" + data[i].name + "')\">" + data[i].name + "</a></li>";
                            }
                        }
                    }
                    else {
                        html += "<li> No NMS exists.</li>";
                    }
                    html += "</ul>";
                    $('div#nms_div').html(html);
                }
            }
        });
        nmsShowStatus = false;
        return false;
    }
}


// This function copy the all host information result in global json variable.
function showNetworkGraph(nms_name) {
    //get the nms detail
    $("#host_details_div").hide();
    $("div#nms_div ul li").removeClass('nms_selected');
    $("div ul li#" + nms_name).addClass('nms_selected');
    $.ajax({
        type: "post",
        url: "show_network_graph.py?nms_name=" + nms_name,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                $().toastmessage('showErrorToast', "Some unknown errored occured, so please contact your Administrator");
                return;
            }
            if (result.success == 1 || result.success == '1')
                $().toastmessage('showErrorToast', 'Some system error occured, so please contact your Administrator');
            else if (result.success == 2 || result.success == '2') {
                $().toastmessage('showErrorToast', 'Some database error occured, so please contact your Administrator');
                return;
            }
            else {
                json = []
                json = eval("(" + result.output + ")");
                $("div#infovis").html("");
                init();
            }
        }
    });
    return false;
}

function showHostDetails(ipAddress) {
    $("#host_details_div").hide();
    $.ajax({
        type: 'post',
        url: 'show_host_details.py?hostIp=' + ipAddress,
        success: function (result) {
            try {
                result = eval("(" + result + ")");
            } catch (err) {
                $().toastmessage('showErrorToast', "Some unknown errored occured, so please contact your Administrator");
                return;
            }
            if (result.success == 1 || result.success == '1')
                $().toastmessage('showErrorToast', 'Some system error occured, so please contact your Administrator');
            else if (result.success == 2 || result.success == '2') {
                $().toastmessage('showErrorToast', 'Some database error occured, so please contact your Administrator');
                return;
            }
            else {
                $("#host_details_div").show();
                $("#inner_details").html(result.output);
                $("#inner_details").css('display', 'block');
            }
        }
    });

}


// Close the window of the user information.
function closeWindow() {
    $("#host_details_div").hide();
}

$(function () {
    $("div#ctr").click(function () {
        $(this).parent().toggleClass("hide");
        if ($(this).hasClass("s")) {
            $(this).removeClass('h').addClass('s');
        }
        else {
            $(this).removeClass('s').addClass('h');
        }
    });
    nmsInNetwork();
    showNetworkGraph($("#nms_instance").val());
//	$("#page_tip").colorbox(
//	{
//		href:"page_tip_circle_graph.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"450px",
//		height:"350px",
//		onComplte:function(){}
//	});
});

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


