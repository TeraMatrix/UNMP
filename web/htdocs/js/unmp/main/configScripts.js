//This is the common javascript file 
//Any common scripts can be added here and included in html pages(Make sure that you add the page specific functions inline)

//Function for restricting the ipaddress text field key press event
var IPKeyCheck = function (e) {
    var key;
    if (window.event)
        key = window.event.keyCode;
    else key = e.which;
    if ((key >= 48 && key <= 57) || (key == 8) || (key == 46) || (key == 0))
        return true;
    else return false;
};
//Allow only numbers in a text field
var numCheck = function (e) {
    var key;
    if (window.event)
        key = window.event.keyCode;
    else key = e.which;
    if ((key >= 48 && key <= 57) || (key == 8) || (key == 0))
        return true;
    else return false;
};
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


//Checking the ipaddress octactes
//Type 1: (1-254).(0-255).(0-255).(1-254)System ip
//Type 2: (255).(0-255).(0-255).(0-255) Subnet mask
//Type 3: (0-254).(0-255).(0-255).(0-254) DNS IP -->
//
var checkIp = function (Type, id, message) {
    var flag = false;
    var ip, octacts;

    if (Type == 1) {
        ip = document.getElementById(id);
        if (ip.value == '') {
            return false;
        }
        octacts = ip.value.split('.');
        if (octacts.length == 4) {
            if (parseInt(octacts[0], 10) > 0 && parseInt(octacts[0], 10) < 255 && parseInt(octacts[1], 10) < 256 && parseInt(octacts[2], 10) < 256 && parseInt(octacts[3], 10) > 0 && parseInt(octacts[3], 10) < 255) {
                flag = true;
            }
            else {
                flag = false;
            }
        }
    }
    if (Type == 2) {
        ip = document.getElementById(id);
        if (ip.value == '') {
            return false;
        }

        octacts = ip.value.split('.');
        if (octacts.length == 4) {
            if (parseInt(octacts[0], 10) == 255 && parseInt(octacts[1], 10) < 256 && parseInt(octacts[2], 10) < 256 && parseInt(octacts[3], 10) < 256) {
                flag = true;
            }
            else {
                flag = false;
            }
        }
    }
    if (Type == 3) {
        ip = document.getElementById(id);
        if (ip.value == '') {
            return false;
        }

        octacts = ip.value.split('.');
        if (octacts.length == 4) {
            if (parseInt(octacts[0], 10) < 255 && parseInt(octacts[1], 10) < 256 && parseInt(octacts[2], 10) < 256 && parseInt(octacts[3], 10) < 254) {
                flag = true;
            }
            else {
                flag = false;
            }
        }
    }
    if (!flag) {
        alert('Invalid ' + message);
        ip.value = '';
        return false;
    }
    else {
        return true;
    }
};

//Confirmations
//Confirmation messages before making an update/commit/reboot/factoryReset 
var ConfirmAction = function (Action) {
    var message;
    if (Action == 'Update')
        message = "Do you want to Update the Changes ? \n These changes won't be updated to flash.";
    if (Action == 'Commit')
        message = "Do you want to Save  all the changes ?";
    if (Action == 'Reboot')
        message = "Do you want to Reboot the system ?";
    if (Action == 'FactoryReset')
        message = "Do you want to change to the Default Factory Settings?";
    if (Action == 'ApplySettings')
        message = "Do you want to Save and  Apply the new settings?";

    var opt = confirm(message);
    if (opt) {
        return true;
    }
    else {
        return false;
    }


};

//Common method for the pop up message

var ModalPopupsIndicator2 = function (message) {
    ModalPopups.Indicator("idIndicator2",
        "Please wait",
        "<div style=''>" +
            "<div style='float:left;'><img src= '../Externals/popup/spinner.gif' alt=' '></div>" +
            "<div style='float:left; padding-left:10px;'>" +
            message + "... <br/>" +
            "</div>",
        {
            width: 300,
            height: 100,
            titleBackColor: "#BC0000",
            titleFontColor: "white",
            popupBackColor: "FFFFFF",
            popupFontColor: "black",
            footerBackColor: "#BC0000",
            footerFontColor: "white"
        }
    );
    //setTimeout('ModalPopups.Close(\"idIndicator2\");', 3000);
};
//


//End of pop up


//Frame Set For loading Me=ssage
var ShowLoading = function () {
    parent.document.getElementsByTagName("FRAMESET").item(1).cols = '150,100%,0';
};
var ShowContent = function () {
    parent.document.getElementsByTagName("FRAMESET").item(1).cols = '150,0,*';
};


//End Of Loading
