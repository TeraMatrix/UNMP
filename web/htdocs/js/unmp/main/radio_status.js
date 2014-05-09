function disableRadio(ip, username, password, port) {
    $(".loading").show();
    $.ajax({
        type: "post",
        url: "change_redio.py?ipaddress=" + ip + "&username=" + username + "&password=" + password + "&port=" + port + "&action=Disable",
        success: function (result) {
            if (result == "Enable") {
                alert("Radio Enabled Successfully");
                $(".loading").hide();
                window.location.reload()
            }
            else if (result == "Disable") {
                alert("Radio Disabled Successfully");
                $(".loading").hide();
                window.location.reload()
            }
            else if (result == "Enable1") {
                setTimeout(function () {
                    alert("Radio Enabled Successfully");
                    $(".loading").hide();
                    window.location.reload();
                }, 5000);
            }
            else if (result == "Disable1") {
                setTimeout(function () {
                    alert("Radio Disabled Successfully");
                    $(".loading").hide();
                    window.location.reload();
                }, 5000);
            }
            else {
                alert(result + ", Try Again");
                $(".loading").hide();
                window.location.reload()
            }
        }
    });
}
function enableRadio(ip, username, password, port) {
    $(".loading").show();
    $.ajax({
        type: "post",
        url: "change_redio.py?ipaddress=" + ip + "&username=" + username + "&password=" + password + "&port=" + port + "&action=Enable",
        success: function (result) {
            if (result == "Enable") {
                alert("Radio Enabled Successfully");
                $(".loading").hide();
                window.location.reload()
            }
            else if (result == "Disable") {
                alert("Radio Disabled Successfully");
                $(".loading").hide();
                window.location.reload()
            }
            else if (result == "Enable1") {
                setTimeout(function () {
                    alert("Radio Enabled Successfully");
                    $(".loading").hide();
                    window.location.reload();
                }, 5000);
            }
            else if (result == "Disable1") {
                setTimeout(function () {
                    alert("Radio Disabled Successfully");
                    $(".loading").hide();
                    window.location.reload();
                }, 5000);
            }
            else {
                alert(result + ", Try Again");
                $(".loading").hide();
                window.location.reload()
            }
        }
    });
}
