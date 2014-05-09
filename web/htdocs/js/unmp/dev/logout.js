var request = new XMLHttpRequest();
function clearAuthData() {

    if (document.all) {
        // Internet Explorer: 'ClearAuthenticationCache' is only available in IE
        document.execCommand('ClearAuthenticationCache');
    }
    else {
        var xmlhttp;
        if (window.XMLHttpRequest) {
            xmlhttp = new XMLHttpRequest();
            //var request = new XMLHttpRequest();
            var path = window.location;
            request.open("GET", path, true);
            request.setRequestHeader("Authorization", "");
            request.send(null);
        }
        else if (window.ActiveXObject) {
            try {
                xmlhttp = new ActiveXObject('Msxml2.XMLHTTP');
            }
            catch (ex) {
                try {
                    xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
                } catch (ex) {

                }
            }
        }
        if (xmlhttp.readyState < 4) {
            xmlhttp.abort();
        }
        // Firefox/Mozilla: use anonymous "login" to trigger a "logout"
        //xmlhttp.open('GET', '/?sling:authRequestLogin=1', false, 'anonymous', 'null');
        //xmlhttp.send('');
        //xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        //request.open("GET", window.location, true);
        //request.send(null);
    }
    alert("Not completed yet.");
    return true;

}

