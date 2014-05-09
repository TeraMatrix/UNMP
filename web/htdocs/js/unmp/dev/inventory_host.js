var formStatus = 0;
/* { 0:form for add and upadate not present, 1:form for add and upadate not present } */

/* Active Host */
var $gridViewActiveHostTableObj = null;
var $gridViewActiveHostDataTable = null;
var $gridViewActiveHostFetched = 0;
var $gridViewActiveHostSelectedTr = [];
/* Datatable selected rows Array */

/* Disable Host */
var $gridViewDisableHostTableObj = null;
var $gridViewDisableHostDataTable = null;
var $gridViewDisableHostFetched = 0;
var $gridViewDisableHostSelectedTr = [];
/* Datatable selected rows Array */

/* Discovered Host */
var $gridViewDiscoveredHostTableObj = null;
var $gridViewDiscoveredHostDataTable = null;
var $gridViewDiscoveredHostFetched = 0;
var $gridViewDiscoveredHostSelectedTr = [];
/* Datatable selected rows Array */

/* Deleted Host */
var $gridViewDeletedHostTableObj = null;
var $gridViewDeletedHostDataTable = null;
var $gridViewDeletedHostFetched = 0;
var $gridViewDeletedHostSelectedTr = [];
/* Datatable selected rows Array */

// form elements jQuery object
var $gridViewDiv = null;
var $formDiv = null;
var $spinLoading = null;
var $spinMainLoading = null;
var $form = null;
var $formTitle = null;
var $formInput = null;
var $formPassword = null;
var $formTextarea = null;
var $formCheckbox = null;
var $formSelectList = null;
var $formAddButton = null;
var $formEditButton = null;

var isRaMacFetched = 0;

var ipValidate = "^([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])$";
// form elements indexes
var $formInputIndex = {"host_name": 0,
    "host_alias": 1,
    "ip_address": 2,
    "mac_address": 3,
    "radio_mac_address": 4,
    "ra_mac": 5,
    "netmask": 6,
    "gateway": 7,
    "odu100_vlan_tag": 8,
    "idu4_vlan_tag": 9,
    "idu4_tdm_ip": 10,
    "primary_dns": 11,
    "secondary_dns": 12,
    "ccu_dhcp_netmask": 13,
    "http_username": 14,
    "http_port": 15,
    "read_community": 16,
    "write_community": 17,
    "get_set_port": 18,
    "trap_port": 19,
    "ssh_username": 20,
    "ssh_port": 21,
    "longitude": 22,
    "latitude": 23,
    "serial_number": 24,
    "hardware_version": 25
};
var $formPasswordIndex = {"http_password": 0, "ssh_password": 1};
var $formTextareaIndex = {"host_comment": 0};
var $formCheckboxIndex = {
    "is_reconciliation": 0,
    "idu4_management_mode": 1,
    "lock_position": 2
};
var $formSelectListIndex = {
    "device_type": 0,
    "firmware_version": 1,
    "node_type": 2,
    "master_mac": 3,
    "host_state": 4,
    "host_priority": 5,
    "host_parent": 6,
    "hostgroup": 7,
    "dns_state": 8,
    "odu100_management_mode": 9,
    "snmp_version": 10,
    "host_vendor": 11,
    "host_os": 12
};

var $RaMacDiv = null;
var $RadioMacDiv = null;
var $MasterSlaveDiv = null;
var $tooltip = null;
var hostDefaultDetails = null;
var currentTab = null; 				// active,disable,discovered,deleted, etc.

// network details div
var $ap25NetworkDiv = null;
var $ccuNetworkDiv = null;
var $odu16NetworkDiv = null;
var $odu100NetworkDiv = null;
var $idu4NetworkDiv = null;
var $idu8NetworkDiv = null;
var $swt4NetworkDiv = null;
var $genericNetworkDiv = null;
var $hardwareVersionDiv = null;
var $serialNumberDiv = null;


// Header buttons
var $addButtonHead = null;
var $editButtonHead = null;
var $delButtonHead = null;

//selected host details
var selectedHostName = null;
var selectedHostAlias = null;
var selectedIpAddress = null;
var selectedMacAddress = null;
var selectedDeviceType = null;
//var firmwareVersion = {"ap25": ["1.2.12"], "idu4": ["2.0.5"], "odu16": ["7.2.10"], "odu100": ["7.2.20", "7.2.25"], "ccu": []}; // default
var firmwareVersion = {}

// Inventory messages
var messages = {
    "add": "Host added successfully.",
    "edit": "Host details updated successfully.",
    "del": "Selected host(s) deleted successfully",
    "delConfirm": "Are you sure want to delete the selected host(s)?",
    "duplicateError": "Please enter a different Host Name, Host Alias, IP  and MAC",
    "noneSelectedError": "Please select atleast one Host",
    "multiSelectedError": "Please select a single Host",
    "localhostDelError": "Deletion of UNMP server system is restricted",
    "localhostEditError": "Update of UNMP server system is restricted",
    "validationError": "Invalid host details are entered, please recheck",
    "dbError": "UNMP Database Server is busy at the moment, please try again later ",
    "noRecordError": "No such record found",
    "sysError": "UNMP Server is busy at the moment, please try again later",
    "unknownError": "UNMP Server is busy at the moment, please try again later",
    "licenseError": "To successfully complete this action please upgrade your license",
    "loadDefaultSettingWarn": "Loading of default setting failed, please try again later",
    "noNmsInctanceError": "UNMP Server is busy at the moment, please try again later.",
    "nagiosConfigError": "UNMP Server is busy at the moment, please try again later time.",
    "changeIpAddressConfirm": "Do You want to change the network configuration of the device?",
    "changeIpAddressError": "Failed to change the network details of the device. Please try again",
    "raMacMissing": "RA MAC is required for RM18 and RM type devices",
    "raMacWarning": "Note: Incorrect RA MAC will cause a failure of device configuration",
    "raMacError": "Please recheck the MAC address.",
    "masterMacMissing": "Master node’s MAC is required for RM18 and RM Slave device",
    "masterMacWarning": " Note: Incorrect RA MAC and Master MAC will cause a failure of device configuration ",
    "masterMacError": "Please choose a correct device Master.",
    "licenseDeviceError": "Maximum limit of allowed host for this device type is reached",
    "addDeletedHost": "Do you want to restore the selected host(s)?",
    "selectDeviceWarnForFetchNetworkDetails": "Please choose device type first",
    "ap25NetworkDetailsError": "Primary and Secondary DNS both are required for Access point",
    "VlanTagError": "VLAN Tag should be a number between 1 to 4094",
    "ccuDhcpNetmaskError": "DHCP netmask required for CCU type host",
    "TdmIPError": "TDM IP address is required for IDU 4 port"
};

// some other varibales to perform edit request
var actionName = null;
var oldIpAddress = null;
var oldNetmask = null;
var oldGateway = null;
var oldDhcp = null;
var oldPriIp = null;
var oldSecIp = null;
var odu100VlanMode = null;
var odu100VlanTag = null;
var idu4VlanMode = null;
var idu4VlanTag = null;
var idu4TdmIp = null;
var ccuDhcpNetmask = null;

$(function () {

    /* header button object*/
    $addButtonHead = $("#add_host").parent();
    $editButtonHead = $("#edit_host").parent();
    $delButtonHead = $("#del_host").parent();

    /* create object of divs */
    $gridViewDiv = $("div#grid_view_div");
    $formDiv = $("div#form_div");

    /* show grid view only hide other */
    $gridViewDiv.show();
    $formDiv.hide();

    // spin loading object
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire

    // page tip [for page tip write this code on each page please dont forget to change "href" value because this link create your help tip page]
//	$("#page_tip").colorbox(
//	{
//		href:"help_inventory_host.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"600px",
//		height:"400px"
//	});

    // creates tabs
    $("div.yo-tabs", "div#container_body").yoTabs();

    /* Add Data Table Tr Selecter Click Handler*/
    dataTableClickHandler();

    /* Call Active Host Data Table */
    $gridViewActiveHostTableObj = $("table#grid_view_active_host");
    //gridViewActiveHost();

    /* Call Active Host Data Table */
    $gridViewDisableHostTableObj = $("table#grid_view_disable_host");
    //gridViewDisableHost();

    /* Call Active Host Data Table */
    $gridViewDiscoveredHostTableObj = $("table#grid_view_discovered_host");
    //gridViewDeletedHost();

    /* Call Active Host Data Table */
    $gridViewDeletedHostTableObj = $("table#grid_view_deleted_host");
    //gridViewDiscoveredHost();

    /* Bind Function With Tabs */

    /* Active Host Tab*/
    $("a#active_host_tab").click(function (e) {
        e.preventDefault();
        currentTab = "active";
        if ($gridViewActiveHostFetched == 0) {
            gridViewActiveHost();
        }
        $addButtonHead.show();
        $editButtonHead.show();
        $delButtonHead.show();
    });

    /* Disable Host Tab*/
    $("a#disable_host_tab").click(function (e) {
        e.preventDefault();
        currentTab = "disable";
        if ($gridViewDisableHostFetched == 0) {
            gridViewDisableHost();
        }
        $addButtonHead.show();
        $editButtonHead.show();
        $delButtonHead.show();
    });

    /* Discovered Host Tab*/
    $("a#discovered_host_tab").click(function (e) {
        e.preventDefault();
        currentTab = "discovered";
        if ($gridViewDiscoveredHostFetched == 0) {
            gridViewDiscoveredHost();
        }
        $addButtonHead.show();
        $editButtonHead.hide();
        $delButtonHead.show();
    });

    /* Deleted Host Tab*/
    $("a#deleted_host_tab").click(function (e) {
        e.preventDefault();
        currentTab = "deleted";
        if ($gridViewDeletedHostFetched == 0) {
            gridViewDeletedHost();
        }
        $addButtonHead.hide();
        $editButtonHead.hide();
        $delButtonHead.show();
    });

    /* It Shows Active Host as Default Host Grid View */
    $("a#active_host_tab").click();
});


function advance_settings_colorbox() {
    if ($("#host_id").val() == undefined)
        $("#advanced_settings").hide();
    else
        window.location = "edit_nagios_host_from_inventory.py?host_id=" + $("#host_id").val();
}


function dataTableClickHandler() {
    /* Click event handler for active host grid view */
    $("table#grid_view_active_host tbody tr").live('click', function (event) {
        var id = this.id;
        if (event.target.nodeName.toLowerCase() != 'img') {
            var index = jQuery.inArray(id, $gridViewActiveHostSelectedTr);

            if (index === -1) {
                $gridViewActiveHostSelectedTr.push(id);
            } else {
                $gridViewActiveHostSelectedTr.splice(index, 1);
            }

            $(this).toggleClass('row_selected');
        }
    });
    /* Click event handler for disable host grid view */
    $("table#grid_view_disable_host tbody tr").live('click', function (event) {
        var id = this.id;
        if (event.target.nodeName.toLowerCase() != 'img') {
            var index = jQuery.inArray(id, $gridViewDisableHostSelectedTr);

            if (index === -1) {
                $gridViewDisableHostSelectedTr.push(id);
            } else {
                $gridViewDisableHostSelectedTr.splice(index, 1);
            }

            $(this).toggleClass('row_selected');
        }
    });
    /* Click event handler for discovered host grid view */
    $("table#grid_view_discovered_host tbody tr").live('click', function () {
        var id = this.id;
        var index = jQuery.inArray(id, $gridViewDiscoveredHostSelectedTr);

        if (index === -1) {
            $gridViewDiscoveredHostSelectedTr.push(id);
        } else {
            $gridViewDiscoveredHostSelectedTr.splice(index, 1);
        }

        $(this).toggleClass('row_selected');
    });
    /* Click event handler for deleted host grid view */
    $("table#grid_view_deleted_host tbody tr").live('click', function () {
        var id = this.id;
        var index = jQuery.inArray(id, $gridViewDeletedHostSelectedTr);

        if (index === -1) {
            $gridViewDeletedHostSelectedTr.push(id);
        } else {
            $gridViewDeletedHostSelectedTr.splice(index, 1);
        }

        $(this).toggleClass('row_selected');
    });
}

// to get active hosts details in datatable
function gridViewActiveHost() {
    spinStart($spinLoading, $spinMainLoading);
    $gridViewActiveHostTableObj.hide();
    $gridViewActiveHostDataTable = $gridViewActiveHostTableObj.dataTable({
        "bServerSide": true,
        "sAjaxSource": "grid_view_active_host.py",
        "bDestroy": true,
        "bJQueryUI": true,
        "bProcessing": true,
        "sPaginationType": "full_numbers",
        "bPaginate": true,
        "bStateSave": false,
        "fnServerData": function (sSource, aoData, fnCallback) {
            $.getJSON(sSource, aoData, function (json) {
                /**
                 * Insert an extra argument to the request: rm.
                 * It's the the name of the CGI form parameter that
                 * contains the run mode name. Its value is the
                 * runmode, that produces the json output for
                 * datatables.
                 **/
                fnCallback(json)
                $('img.host_opr').tipsy({gravity: 'n'}); // n | s | e | w
                $gridViewActiveHostTableObj.show();
                $gridViewActiveHostFetched = 1;
                spinStop($spinLoading, $spinMainLoading);
            });
        }
    });

    $gridViewActiveHostDataTable.fnSetColumnVis(0, false, false);		// make 0th column hide
    $gridViewActiveHostDataTable.fnSetColumnVis(1, false, false);		// make 1st column hide
}

// to get disable hosts details in datatable
function gridViewDisableHost() {
    spinStart($spinLoading, $spinMainLoading);
    $gridViewDisableHostTableObj.hide();
    $gridViewDisableHostDataTable = $gridViewDisableHostTableObj.dataTable({
        "bServerSide": true,
        "sAjaxSource": "grid_view_disable_host.py",
        "bDestroy": true,
        "bJQueryUI": true,
        "bProcessing": true,
        "sPaginationType": "full_numbers",
        "bPaginate": true,
        "bStateSave": false,
        "bLengthChange": true,
        "fnServerData": function (sSource, aoData, fnCallback) {
            $.getJSON(sSource, aoData, function (json) {
                /**
                 * Insert an extra argument to the request: rm.
                 * It's the the name of the CGI form parameter that
                 * contains the run mode name. Its value is the
                 * runmode, that produces the json output for
                 * datatables.
                 **/
                fnCallback(json)
                $('img.host_opr').tipsy({gravity: 'n'}); // n | s | e | w
                $gridViewDisableHostTableObj.show();
                $gridViewDisableHostFetched = 1;
                spinStop($spinLoading, $spinMainLoading);
            });
        }
    });
    $gridViewDisableHostDataTable.fnSetColumnVis(0, false, false);		// make 0th column hide
    $gridViewDisableHostDataTable.fnSetColumnVis(1, false, false);		// make 1st column hide
}

// to get discovered hosts details in datatable
function gridViewDiscoveredHost() {
    spinStart($spinLoading, $spinMainLoading);
    $gridViewDiscoveredHostTableObj.hide();
    $gridViewDiscoveredHostDataTable = $gridViewDiscoveredHostTableObj.dataTable({
        "bServerSide": true,
        "sAjaxSource": "grid_view_discovered_host.py",
        "bDestroy": true,
        "bJQueryUI": true,
        "bProcessing": true,
        "sPaginationType": "full_numbers",
        "bPaginate": true,
        "bStateSave": false,
        "bLengthChange": true,
        "fnServerData": function (sSource, aoData, fnCallback) {
            $.getJSON(sSource, aoData, function (json) {
                /**
                 * Insert an extra argument to the request: rm.
                 * It's the the name of the CGI form parameter that
                 * contains the run mode name. Its value is the
                 * runmode, that produces the json output for
                 * datatables.
                 **/
                fnCallback(json)
                $gridViewDiscoveredHostTableObj.show();
                $gridViewDiscoveredHostFetched = 1;
                spinStop($spinLoading, $spinMainLoading);
            });
        }
    });
    $gridViewDiscoveredHostDataTable.fnSetColumnVis(0, false, false);		// make 0th column hide
}

// to get deleted hosts details in datatable
function gridViewDeletedHost() {
    spinStart($spinLoading, $spinMainLoading);
    $gridViewDeletedHostTableObj.hide();
    $gridViewDeletedHostDataTable = $gridViewDeletedHostTableObj.dataTable({
        "bServerSide": true,
        "sAjaxSource": "grid_view_deleted_host.py",
        "bDestroy": true,
        "bJQueryUI": true,
        "bProcessing": true,
        "sPaginationType": "full_numbers",
        "bPaginate": true,
        "bStateSave": false,
        "bLengthChange": true,
        "fnServerData": function (sSource, aoData, fnCallback) {
            $.getJSON(sSource, aoData, function (json) {
                /**
                 * Insert an extra argument to the request: rm.
                 * It's the the name of the CGI form parameter that
                 * contains the run mode name. Its value is the
                 * runmode, that produces the json output for
                 * datatables.
                 **/
                fnCallback(json)
                $gridViewDeletedHostTableObj.show();
                $gridViewDeletedHostFetched = 1;
                spinStop($spinLoading, $spinMainLoading);
            });
        }
    });
    $gridViewDeletedHostDataTable.fnSetColumnVis(0, false, false);		// make 0th column hide
    $gridViewDeletedHostDataTable.fnSetColumnVis(1, false, false);		// make 1st column hide
}
// to get the list of odu16 and odu100 master device list(this function call when you add a slave host of device type odu16 or odu100)
function oduMasterList(deviceTypeId, master_id) {
    $.ajax({
        type: "get",
        url: "odu_master_list.py?device_type_id=" + String(deviceTypeId),
        cache: false,
        success: function (result) {
            var $result = $(result);
            $formSelectList.eq($formSelectListIndex["master_mac"]).html($result.html());
            $formSelectList.eq($formSelectListIndex["master_mac"]).val(master_id);
            if (master_id == "") {
                fetchMasterMacAddress();
            }
        }
    });
}


// logic to display master slave div.
function showMasterMacDiv() {
    var nodeType = $formSelectList.eq($formSelectListIndex["node_type"]).val();
    try {
        if (parseInt(nodeType) == 1 || parseInt(nodeType) == 3)		// nodeType is 1 and 3 means it's a slave device.
        {
            oduMasterList($formSelectList.eq($formSelectListIndex["device_type"]).val(), "")		// fetch odu16 or odu100 master host list
            $MasterSlaveDiv.show();
        }
        else {
            $MasterSlaveDiv.hide();
        }
    }
    catch (err) {
        $MasterSlaveDiv.hide();
    }
}

function fetchRAMacAddress() {
    var ipAddress = $formInput.eq($formInputIndex["ip_address"]).val();
    var selectedDeviceType = $formSelectList.eq($formSelectListIndex["device_type"]).val();

    if (ipAddress != "" && ipAddress.match(ipValidate) && selectedDeviceType != "") {

        if ($formSelectList.eq($formSelectListIndex["device_type"]).val() == "odu16") {
            ipAddress = ipAddress + ":" + $formInput.eq($formInputIndex["http_port"]).val();
        }
        else if ($formSelectList.eq($formSelectListIndex["device_type"]).val() == "odu100") {
            //ip_address = ip_address;
            // do nothing
        }
        $("#ra_mac_loading").show();
        $("a#a_fetch_ra_mac").hide();
        $.ajax({
            type: "get",
            url: "get_odu_ra_mac_and_node_type.py?ip_address=" + ipAddress + "&username=" + $formInput.eq($formInputIndex["http_username"]).val() + "&password=" + $formPassword.eq($formPasswordIndex["http_password"]).val() + "&community=" + $formInput.eq($formInputIndex["read_community"]).val() + "&port=" + $formInput.eq($formInputIndex["get_set_port"]).val() + "&device_type=" + $formSelectList.eq($formSelectListIndex["device_type"]).val(),
            cache: false,
            success: function (result) {
                //result = {"node_type_success":1,"ra_mac_success":1,"node_type":"SNMP agent down or device not reachable","ra_mac":"SNMP agent down or device not reachable"}
                if (result.node_type == undefined || result.ra_mac == undefined) {
                    $().toastmessage('showErrorToast', messages["unknownError"]);
                }
                else {
                    if (result.node_type_success == 1 && result.ra_mac_success == 1) {
                        $().toastmessage('showErrorToast', result.node_type);
                    }
                    else if (result.node_type_success == 1) {
                        $().toastmessage('showErrorToast', "Fatching node type: " + result.node_type);
                        $formInput.eq($formInputIndex["ra_mac"]).val(result.ra_mac);
                    }
                    else if (result.ra_mac_success == 1) {
                        $().toastmessage('showErrorToast', "Fatching RA MAC: " + result.ra_mac);
                        $formSelectList.eq($formSelectListIndex["node_type"]).val(result.node_type);
                        $formInput.eq($formInputIndex["ra_mac"]).val("");
                    }
                    else {
                        $formSelectList.eq($formSelectListIndex["node_type"]).val(result.node_type);
                        $formInput.eq($formInputIndex["ra_mac"]).val(result.ra_mac);
                    }
                }
                showMasterMacDiv();
                $("#ra_mac_loading").hide();
                $("a#a_fetch_ra_mac").show();
            }
        });
    }
    else {
        $().toastmessage('showWarningToast', "Please enter valid IP address and device type");
    }

}
// to fetch master mac address of slave device.


// fetch Radio Acess Mac Address of odu16 and odu100 device.
function fetchRAMacAddress() {
    var ipAddress = $formInput.eq($formInputIndex["ip_address"]).val();
    var selectedDeviceType = $formSelectList.eq($formSelectListIndex["device_type"]).val();

    if (ipAddress != "" && ipAddress.match(ipValidate) && selectedDeviceType != "") {
        if (selectedDeviceType == "odu16") {
            ipAddress = ipAddress + ":" + $formInput.eq($formInputIndex["http_port"]).val();
        }
        else if (selectedDeviceType == "odu100") {
            //ipAddress = ipAddress;
            // do nothing
        }
        $("#ra_mac_loading").show();
        $("a#a_fetch_ra_mac").hide();
        $.ajax({
            type: "get",
            url: "get_odu_ra_mac_and_node_type.py?ip_address=" + ipAddress + "&username=" + $formInput.eq($formInputIndex["http_username"]).val() + "&password=" + $formPassword.eq($formPasswordIndex["http_password"]).val() + "&community=" + $formInput.eq($formInputIndex["read_community"]).val() + "&port=" + $formInput.eq($formInputIndex["get_set_port"]).val() + "&device_type=" + selectedDeviceType,
            cache: false,
            success: function (result) {
                //result = {"node_type_success":1,"ra_mac_success":1,"node_type":"SNMP agent down or device not reachable","ra_mac":"SNMP agent down or device not reachable"}
                isRaMacFetched = 0;
                if (result.node_type == undefined || result.ra_mac == undefined) {
                    $().toastmessage('showErrorToast', messages["unknownError"]);
                }
                else {
                    if (result.node_type_success == 1 && result.ra_mac_success == 1) {
                        $().toastmessage('showErrorToast', result.node_type);
                    }
                    else if (result.node_type_success == 1) {
                        $().toastmessage('showErrorToast', "Fatching node type: " + result.node_type);
                        $formInput.eq($formInputIndex["ra_mac"]).val(result.ra_mac);
                    }
                    else if (result.ra_mac_success == 1) {
                        $().toastmessage('showErrorToast', "Fatching RA MAC: " + result.ra_mac);
                        $formSelectList.eq($formSelectListIndex["node_type"]).val(result.node_type);
                        $formInput.eq($formInputIndex["ra_mac"]).val("");
                    }
                    else {
                        $formSelectList.eq($formSelectListIndex["node_type"]).val(result.node_type);
                        $formInput.eq($formInputIndex["ra_mac"]).val(result.ra_mac);
                        isRaMacFetched = 1;

                    }
                }
                showMasterMacDiv();
                $("#ra_mac_loading").hide();
                $("a#a_fetch_ra_mac").show();
            }
        });
    }
    else {
        $().toastmessage('showWarningToast', "Please enter valid IP address and device type");
    }
}
// to fetch master mac address of slave device.
function fetchMasterMacAddress() {
    var ipAddress = $formInput.eq($formInputIndex["ip_address"]).val();
    var selectedDeviceType = $formSelectList.eq($formSelectListIndex["device_type"]).val();

    if (ipAddress != "" && ipAddress.match(ipValidate) && selectedDeviceType != "") {

        $("#master_mac_loading").show();
        $("#a_fetch_master_mac").hide();
        $.ajax({
            type: "get",
            url: "get_master_mac_from_slave.py?ip_address=" + ipAddress + ":" + $formInput.eq($formInputIndex["http_port"]).val() + "&username=" + $formInput.eq($formInputIndex["http_username"]).val() + "&password=" + $formPassword.eq($formPasswordIndex["http_password"]).val() + "&community=" + $formInput.eq($formInputIndex["read_community"]).val() + "&port=" + $formInput.eq($formInputIndex["get_set_port"]).val(),
            cache: false,
            success: function (result) {
                //result = {"success":1,"result":"SNMP agent down or device not reachable"}
                if (result.success == 0) {
                    $formSelectList.eq($formSelectListIndex["master_mac"]).val(result.result);
                }
                else {
                    if (result.result == undefined) {
                        $().toastmessage('showErrorToast', messages["unknownError"]);
                    }
                    else {
                        $().toastmessage('showErrorToast', result.result);
                    }
                    $formSelectList.eq($formSelectListIndex["master_mac"]).val("");
                }
                $("#master_mac_loading").hide();
                $("#a_fetch_master_mac").show();
            }
        });
    }
    else {
        $().toastmessage('showWarningToast', "Please enter valid IP address and device type");
    }
}

// Fetch the MAC Address
function fetchMacAddress() {
    var ipAddress = $formInput.eq($formInputIndex["ip_address"]).val();
    var selectedDeviceType = $formSelectList.eq($formSelectListIndex["device_type"]).val();

    if (ipAddress != "" && ipAddress.match(ipValidate) && selectedDeviceType != "") {
        $("#mac_loading,#radio_mac_loading").show();
        $("#a_fetch_mac,#a_fetch_radio_mac").hide();

        $.ajax({
            type: "get",
            url: "get_mac_details.py?ip_address=" + ipAddress + "&community=" + $formInput.eq($formInputIndex["read_community"]).val() + "&port=" + $formInput.eq($formInputIndex["get_set_port"]).val() + "&device_type=" + selectedDeviceType,
            cache: false,
            success: function (result) {
                // expected result {"result": {"radio_mac_address": "", "mac_address": "F8:52:DF:11:07:49"}, "success": 0}
                // expected result {'success':1,'result':'Error Message'}
                if (result['success'] == 0) {
                    $formInput.eq($formInputIndex["mac_address"]).val(result.result["mac_address"]);
                    $formInput.eq($formInputIndex["radio_mac_address"]).val(result.result["radio_mac_address"]);
                }
                else {
                    if (result.result == undefined) {
                        $().toastmessage('showErrorToast', messages["unknownError"]);
                    }
                    else {
                        $().toastmessage('showErrorToast', result.result);
                    }
                }
                $("#mac_loading,#radio_mac_loading").hide();
                $("#a_fetch_mac,#a_fetch_radio_mac").show();
            }
        });
    }
    else {
        $().toastmessage('showWarningToast', "Please enter valid IP address and device type");
    }
}

// to fetch network details of all devices
function fetchNetworkDetails() {
    var ipAddress = $formInput.eq($formInputIndex["ip_address"]).val();
    var selectedDeviceType = $formSelectList.eq($formSelectListIndex["device_type"]).val();
    if (ipAddress != "" && ipAddress.match(ipValidate) && selectedDeviceType != "") {
        $("#network_details_loading").show();
        $("#a_network_details_loading").hide();
        $.ajax({
            type: "get",
            url: "get_network_details.py?ip_address=" + $formInput.eq($formInputIndex["ip_address"]).val() + "&community=" + $formInput.eq($formInputIndex["read_community"]).val() + "&port=" + $formInput.eq($formInputIndex["get_set_port"]).val() + "&device_type=" + selectedDeviceType,
            cache: false,
            success: function (result) {
                //result = {"success":1,"result":"SNMP agent down or device not reachable"}
                if (result.success == 0) {
                    $formInput.eq($formInputIndex["netmask"]).val(result.result.netmask);
                    $formInput.eq($formInputIndex["gateway"]).val(result.result.gateway);
                    $formInput.eq($formInputIndex["primary_dns"]).val(result.result.primary_dns);
                    $formInput.eq($formInputIndex["secondary_dns"]).val(result.result.secondary_dns);
                    $formSelectList.eq($formSelectListIndex["dns_state"]).val(result.result.dns_state == 0 && "Disabled" || "Enabled");
                    $formInput.eq($formInputIndex["odu100_vlan_tag"]).val(result.result.odu100_vlan_tag != undefined && result.result.odu100_vlan_tag != '0' && result.result.odu100_vlan_tag || "");
                    $formInput.eq($formInputIndex["idu4_vlan_tag"]).val(result.result.idu4_vlan_tag != undefined && result.result.idu4_vlan_tag || "");
                    $formInput.eq($formInputIndex["idu4_tdm_ip"]).val(result.result.idu4_tdm_ip != undefined && result.result.idu4_tdm_ip || "");
                    $formInput.eq($formInputIndex["ccu_dhcp_netmask"]).val(result.result.ccu_dhcp_netmask != undefined && result.result.ccu_dhcp_netmask || "");
                    //idu4_management_mode
                    if (result.result.idu4_management_mode == 1) {
                        $formCheckbox.eq($formCheckboxIndex["idu4_management_mode"]).attr("checked", true);
                    }
                    else {
                        $formCheckbox.eq($formCheckboxIndex["idu4_management_mode"]).attr("checked", false);
                    }
                    $formSelectList.eq($formSelectListIndex["odu100_management_mode"]).val(result.result.odu100_management_mode);
                }
                else {
                    if (result.result == undefined) {
                        $().toastmessage('showErrorToast', messages["unknownError"]);
                    }
                    else {
                        $().toastmessage('showErrorToast', result.result);
                    }
                }
            },
            complete: function () {
                $("#network_details_loading").hide();
                $("#a_network_details_loading").show();
            }
        });
    }
    else {
        $().toastmessage('showWarningToast', "Please enter valid IP address and device type");
    }
}

/*
 function masterMACListChange(masterMAC){
 alert('check');
 }
 */

// to bind device type change event (select list).
function deviceTypeChange(deviceTypeSelectList) {
    deviceTypeSelectList.change(function () {
        var selectedDeviceType = $(this).val();
        var ipAddress = $formInput.eq($formInputIndex["ip_address"]).val();

        $("#mac_loading,#radio_mac_loading").hide();
        $("#a_fetch_mac,#a_fetch_radio_mac").hide();


        if (ipAddress.match(ipValidate) && selectedDeviceType != "") {

        }
        else {
            if (selectedDeviceType != "") {
                $().toastmessage('showWarningToast', "Please enter valid IP address, then choose device type");
                return;
            }
            else if (ipAddress.match(ipValidate)) {
                $().toastmessage('showWarningToast', "Please choose device type");
                return;
            }
            else {
                if (currentTab == "discovered") {
                    return;
                }
                else {
                    $().toastmessage('showNoticeToast', "Please enter valid IP address, then choose device type first");
                    return;
                }


            }

        }


        // spacial case which is you can remove when you get fetch all devices http and snmp cradentails separately
        if (actionName == "add") {
            fetchNetworkDetails(); // add function according to device type
            //$formInput.eq($formInputIndex["mac_address"]).val("");
            if (selectedDeviceType == "odu16" || selectedDeviceType == "odu100") {
                $RaMacDiv.show();
                showMasterMacDiv();
            }
            else {
                $RaMacDiv.hide();
                $MasterSlaveDiv.hide();
            }
            if (selectedDeviceType == "ap25") {
                $formInput.eq($formInputIndex["http_username"]).val("admin");
                $formPassword.eq($formPasswordIndex["http_password"]).val("password");
                $formInput.eq($formInputIndex["http_port"]).val("80");
                $formInput.eq($formInputIndex["read_community"]).val("public");
                $formInput.eq($formInputIndex["write_community"]).val("private");
                $formInput.eq($formInputIndex["get_set_port"]).val("161");
                $formInput.eq($formInputIndex["trap_port"]).val("162");
                $formSelectList.eq($formSelectListIndex["snmp_version"]).val("2c");
                $formInput.eq($formInputIndex["ssh_username"]).val("root");
                $formPassword.eq($formPasswordIndex["ssh_password"]).val("password");
                $formInput.eq($formInputIndex["ssh_port"]).val("22");
                $ap25NetworkDiv.show();
                $ccuNetworkDiv.hide();
                $odu16NetworkDiv.hide();
                $odu100NetworkDiv.hide();
                $idu4NetworkDiv.hide();
                $idu8NetworkDiv.hide();
                $swt4NetworkDiv.hide();
                $genericNetworkDiv.hide();
                fetchMacAddress();
                $hardwareVersionDiv.hide();
                $serialNumberDiv.hide();
                //$RadioMacDiv.show();
                $RadioMacDiv.hide();
            }
            else if (selectedDeviceType == "odu16") {
                $formInput.eq($formInputIndex["http_username"]).val("admin");
                $formPassword.eq($formPasswordIndex["http_password"]).val("vnlggn");
                $formInput.eq($formInputIndex["http_port"]).val("5555");
                $formInput.eq($formInputIndex["read_community"]).val("public");
                $formInput.eq($formInputIndex["write_community"]).val("private");
                $formInput.eq($formInputIndex["get_set_port"]).val("161");
                $formInput.eq($formInputIndex["trap_port"]).val("162");
                $formSelectList.eq($formSelectListIndex["snmp_version"]).val("2c");
                $formInput.eq($formInputIndex["ssh_username"]).val("root");
                $formPassword.eq($formPasswordIndex["ssh_password"]).val("vnlggn@21b");
                $formInput.eq($formInputIndex["ssh_port"]).val("5556");
                fetchRAMacAddress();
                $ap25NetworkDiv.hide();
                $ccuNetworkDiv.hide();
                $odu16NetworkDiv.show();
                $odu100NetworkDiv.hide();
                $idu4NetworkDiv.hide();
                $idu8NetworkDiv.hide();
                $swt4NetworkDiv.hide();
                $genericNetworkDiv.hide();
                $hardwareVersionDiv.hide();
                $serialNumberDiv.hide();
                $RadioMacDiv.hide();
            }
            else if (selectedDeviceType == "odu100") {
                $formInput.eq($formInputIndex["http_username"]).val("admin");
                $formPassword.eq($formPasswordIndex["http_password"]).val("public");
                $formInput.eq($formInputIndex["http_port"]).val("80");
                $formInput.eq($formInputIndex["read_community"]).val("public");
                $formInput.eq($formInputIndex["write_community"]).val("private");
                $formInput.eq($formInputIndex["get_set_port"]).val("161");
                $formInput.eq($formInputIndex["trap_port"]).val("162");
                $formSelectList.eq($formSelectListIndex["snmp_version"]).val("2c");
                $formInput.eq($formInputIndex["ssh_username"]).val("root");
                $formPassword.eq($formPasswordIndex["ssh_password"]).val("public");
                $formInput.eq($formInputIndex["ssh_port"]).val("22");
                fetchRAMacAddress();
                getFirmwareVersion(selectedDeviceType);
                getHardwareInformation(selectedDeviceType);
                $ap25NetworkDiv.hide();
                $ccuNetworkDiv.hide();
                $odu16NetworkDiv.hide();
                $odu100NetworkDiv.show();
                $idu4NetworkDiv.hide();
                $idu8NetworkDiv.hide();
                $swt4NetworkDiv.hide();
                $genericNetworkDiv.hide();
                $hardwareVersionDiv.show();
                $serialNumberDiv.show();
                $RadioMacDiv.hide();
            }
            else if (selectedDeviceType == "idu4") {
                $formInput.eq($formInputIndex["http_username"]).val("admin");
                $formPassword.eq($formPasswordIndex["http_password"]).val("vnlggn");
                $formInput.eq($formInputIndex["http_port"]).val("5555");
                $formInput.eq($formInputIndex["read_community"]).val("public");
                $formInput.eq($formInputIndex["write_community"]).val("private");
                $formInput.eq($formInputIndex["get_set_port"]).val("8001");
                $formInput.eq($formInputIndex["trap_port"]).val("8002");
                $formSelectList.eq($formSelectListIndex["snmp_version"]).val("2c");
                $formInput.eq($formInputIndex["ssh_username"]).val("root");
                $formPassword.eq($formPasswordIndex["ssh_password"]).val("vnlggn@21b");
                $formInput.eq($formInputIndex["ssh_port"]).val("5556");
                $ap25NetworkDiv.hide();
                $ccuNetworkDiv.hide();
                $odu16NetworkDiv.hide();
                $odu100NetworkDiv.hide();
                $idu4NetworkDiv.show();
                $idu8NetworkDiv.hide();
                $swt4NetworkDiv.hide();
                $genericNetworkDiv.hide();
                $hardwareVersionDiv.hide();
                $serialNumberDiv.hide();
                $RadioMacDiv.hide();
            }
            else if (selectedDeviceType == "idu8") {
                $formInput.eq($formInputIndex["http_username"]).val("admin");
                $formPassword.eq($formPasswordIndex["http_password"]).val("vnlggn");
                $formInput.eq($formInputIndex["http_port"]).val("5555");
                $formInput.eq($formInputIndex["read_community"]).val("public");
                $formInput.eq($formInputIndex["write_community"]).val("private");
                $formInput.eq($formInputIndex["get_set_port"]).val("8001");
                $formInput.eq($formInputIndex["trap_port"]).val("8002");
                $formSelectList.eq($formSelectListIndex["snmp_version"]).val("2c");
                $formInput.eq($formInputIndex["ssh_username"]).val("root");
                $formPassword.eq($formPasswordIndex["ssh_password"]).val("vnlggn@21b");
                $formInput.eq($formInputIndex["ssh_port"]).val("5556");
                $ap25NetworkDiv.hide();
                $ccuNetworkDiv.hide();
                $odu16NetworkDiv.hide();
                $odu100NetworkDiv.hide();
                $idu4NetworkDiv.hide();
                $idu8NetworkDiv.show();
                $swt4NetworkDiv.hide();
                $genericNetworkDiv.hide();
                $RadioMacDiv.hide();
            }
            else if (selectedDeviceType == "swt4") {
                $formInput.eq($formInputIndex["http_username"]).val("admin");
                $formPassword.eq($formPasswordIndex["http_password"]).val("public");
                $formInput.eq($formInputIndex["http_port"]).val("80");
                $formInput.eq($formInputIndex["read_community"]).val("public");
                $formInput.eq($formInputIndex["write_community"]).val("private");
                $formInput.eq($formInputIndex["get_set_port"]).val("161");
                $formInput.eq($formInputIndex["trap_port"]).val("162");
                $formSelectList.eq($formSelectListIndex["snmp_version"]).val("2c");
                $formInput.eq($formInputIndex["ssh_username"]).val("root");
                $formPassword.eq($formPasswordIndex["ssh_password"]).val("password");
                $formInput.eq($formInputIndex["ssh_port"]).val("22");
                $ap25NetworkDiv.hide();
                $ccuNetworkDiv.hide();
                $odu16NetworkDiv.hide();
                $odu100NetworkDiv.hide();
                $idu4NetworkDiv.hide();
                $idu8NetworkDiv.hide();
                $swt4NetworkDiv.show();
                $genericNetworkDiv.hide();
                $hardwareVersionDiv.hide();
                $serialNumberDiv.hide();
                $RadioMacDiv.hide();
            }
            else if (selectedDeviceType == "ccu") {
                $formInput.eq($formInputIndex["http_username"]).val("admin");
                $formPassword.eq($formPasswordIndex["http_password"]).val("public");
                $formInput.eq($formInputIndex["http_port"]).val("80");
                $formInput.eq($formInputIndex["read_community"]).val("public");
                $formInput.eq($formInputIndex["write_community"]).val("public");
                $formInput.eq($formInputIndex["get_set_port"]).val("161");
                $formInput.eq($formInputIndex["trap_port"]).val("162");
                $formSelectList.eq($formSelectListIndex["snmp_version"]).val("1");
                $formInput.eq($formInputIndex["ssh_username"]).val("root");
                $formPassword.eq($formPasswordIndex["ssh_password"]).val("password");
                $formInput.eq($formInputIndex["ssh_port"]).val("22");
                $ap25NetworkDiv.hide();
                $ccuNetworkDiv.show();
                $odu16NetworkDiv.hide();
                $odu100NetworkDiv.hide();
                $idu4NetworkDiv.hide();
                $idu8NetworkDiv.hide();
                $swt4NetworkDiv.hide();
                $genericNetworkDiv.hide();
                $hardwareVersionDiv.hide();
                $serialNumberDiv.hide();
                $RadioMacDiv.hide();
            }
            else {
                $formInput.eq($formInputIndex["http_username"]).val("");
                $formPassword.eq($formPasswordIndex["http_password"]).val("");
                $formInput.eq($formInputIndex["http_port"]).val("");
                $formInput.eq($formInputIndex["read_community"]).val("public");
                $formInput.eq($formInputIndex["write_community"]).val("private");
                $formInput.eq($formInputIndex["get_set_port"]).val("161");
                $formInput.eq($formInputIndex["trap_port"]).val("162");
                $formSelectList.eq($formSelectListIndex["snmp_version"]).val("2c");
                $formInput.eq($formInputIndex["ssh_username"]).val("");
                $formPassword.eq($formPasswordIndex["ssh_password"]).val("");
                $formInput.eq($formInputIndex["ssh_port"]).val("");
                $ap25NetworkDiv.hide();
                $ccuNetworkDiv.hide();
                $odu16NetworkDiv.hide();
                $odu100NetworkDiv.hide();
                $idu4NetworkDiv.hide();
                $idu8NetworkDiv.hide();
                $swt4NetworkDiv.hide();
                $genericNetworkDiv.show();
                $hardwareVersionDiv.hide();
                $serialNumberDiv.hide();
                $RadioMacDiv.hide();
            }
        }
        else {
            if (selectedDeviceType == "odu16" || selectedDeviceType == "odu100") {
                $RaMacDiv.show();
                showMasterMacDiv();
            }
            else {
                $RaMacDiv.hide();
                $MasterSlaveDiv.hide();
            }
            if (selectedDeviceType == "ap25") {
                $ap25NetworkDiv.show();
                $ccuNetworkDiv.hide();
                $odu16NetworkDiv.hide();
                $odu100NetworkDiv.hide();
                $idu4NetworkDiv.hide();
                $idu8NetworkDiv.hide();
                $swt4NetworkDiv.hide();
                $genericNetworkDiv.hide();
                $hardwareVersionDiv.hide();
                $serialNumberDiv.hide();
                //$RadioMacDiv.show();
                $RadioMacDiv.hide();
            }
            else if (selectedDeviceType == "odu16") {
                $ap25NetworkDiv.hide();
                $ccuNetworkDiv.hide();
                $odu16NetworkDiv.show();
                $odu100NetworkDiv.hide();
                $idu4NetworkDiv.hide();
                $idu8NetworkDiv.hide();
                $swt4NetworkDiv.hide();
                $genericNetworkDiv.hide();
                $hardwareVersionDiv.hide();
                $serialNumberDiv.hide();
                $RadioMacDiv.hide();
            }
            else if (selectedDeviceType == "odu100") {
                $ap25NetworkDiv.hide();
                $ccuNetworkDiv.hide();
                $odu16NetworkDiv.hide();
                $odu100NetworkDiv.show();
                $idu4NetworkDiv.hide();
                $idu8NetworkDiv.hide();
                $swt4NetworkDiv.hide();
                $genericNetworkDiv.hide();
                $hardwareVersionDiv.show();
                $serialNumberDiv.show();
            }
            else if (selectedDeviceType == "idu4") {
                $ap25NetworkDiv.hide();
                $ccuNetworkDiv.hide();
                $odu16NetworkDiv.hide();
                $odu100NetworkDiv.hide();
                $idu4NetworkDiv.show();
                $idu8NetworkDiv.hide();
                $swt4NetworkDiv.hide();
                $genericNetworkDiv.hide();
                $RadioMacDiv.hide();
                $hardwareVersionDiv.hide();
                $serialNumberDiv.hide();

            }
            else if (selectedDeviceType == "idu8") {
                $ap25NetworkDiv.hide();
                $ccuNetworkDiv.hide();
                $odu16NetworkDiv.hide();
                $odu100NetworkDiv.hide();
                $idu4NetworkDiv.hide();
                $idu8NetworkDiv.show();
                $swt4NetworkDiv.hide();
                $genericNetworkDiv.hide();
                $hardwareVersionDiv.hide();
                $serialNumberDiv.hide();
                $RadioMacDiv.hide();
            }
            else if (selectedDeviceType == "swt4") {
                $ap25NetworkDiv.hide();
                $ccuNetworkDiv.hide();
                $odu16NetworkDiv.hide();
                $odu100NetworkDiv.hide();
                $idu4NetworkDiv.hide();
                $idu8NetworkDiv.hide();
                $swt4NetworkDiv.show();
                $genericNetworkDiv.hide();
                $hardwareVersionDiv.hide();
                $serialNumberDiv.hide();
                $RadioMacDiv.hide();
            }
            else if (selectedDeviceType == "ccu") {
                $ap25NetworkDiv.hide();
                $ccuNetworkDiv.show();
                $odu16NetworkDiv.hide();
                $odu100NetworkDiv.hide();
                $idu4NetworkDiv.hide();
                $idu8NetworkDiv.hide();
                $swt4NetworkDiv.hide();
                $genericNetworkDiv.hide();
                $hardwareVersionDiv.hide();
                $serialNumberDiv.hide();
                $RadioMacDiv.hide();
            }
            else {
                $ap25NetworkDiv.hide();
                $ccuNetworkDiv.hide();
                $odu16NetworkDiv.hide();
                $odu100NetworkDiv.hide();
                $idu4NetworkDiv.hide();
                $idu8NetworkDiv.hide();
                $swt4NetworkDiv.hide();
                $genericNetworkDiv.show();
                $hardwareVersionDiv.hide();
                $serialNumberDiv.hide();
                $RadioMacDiv.hide();
            }
        }
    });
}
// to create a form for add/edit host
function createForm(act, id) {
    spinStart($spinLoading, $spinMainLoading);
    $.ajax({
        type: "get",
        url: "form_host.py",
        cache: false,
        success: function (result) {
            $formDiv.html(result);
            addFormToolTip();	// to add form tool top
            cancelForm();		// to bind form cancel button events

            // create jQuery object of forms elements
            $form = $("form#form_host");
            $formTitle = $("form#form_host th#form_title");
            $formInput = $("form#form_host input[type='text']");
            $formPassword = $("form#form_host input[type='password']");
            $formTextarea = $("form#form_host textarea");
            $formCheckbox = $("form#form_host input[type='checkbox']");
            $formSelectList = $("form#form_host select");
            $formAddButton = $("form#form_host button[id='add_host']");
            $formEditButton = $("form#form_host button[id='edit_host']");
            $RaMacDiv = $("#ra_mac_div,#node_type_div", "form#form_host");
            $RadioMacDiv = $("#radio_mac_div");
            $MasterSlaveDiv = $("#master_slave_div", "form#form_host");

            // device network details div
            $ap25NetworkDiv = $("div.ap25-only");
            $ccuNetworkDiv = $("div.ccu-only");
            $odu16NetworkDiv = $("div.odu16-only");
            $odu100NetworkDiv = $("div.odu100-only");
            $idu4NetworkDiv = $("div.idu4-only");
            $idu8NetworkDiv = $("div.idu8-only");
            $swt4NetworkDiv = $("div.swt4-only");
            $genericNetworkDiv = $("div.generic-only");
            $hardwareVersionDiv = $("div.hardware");
            $serialNumberDiv = $("div.serial");

            submitForm($form);	// to bind form submit request

            if (act == "edit") {
                editForm(id);		// when action is edit host
            }
            else {
                addForm();		// when action is add host
            }
            spinStop($spinLoading, $spinMainLoading);
            deviceTypeChange($formSelectList.eq($formSelectListIndex["device_type"]));	// bind device type change event
            //hostGroupChange($formSelectList.eq($formSelectListIndex["device_type"]));
            //masterMACListChange($formSelectList.eq($formSelectListIndex["master_mac"]));	// bind master mac change event for RM/RM18
            // bind node type change event
            $formSelectList.eq($formSelectListIndex["node_type"]).change(function () {
                showMasterMacDiv();
            });
            //getAllFirmwareDict();
        }
    });

    // mahipal's code
    if ($("#host_id").val() == undefined || $("#host_id").val() == "")
        $("#advanced_settings").hide();
}


function getAllFirmwareDict() {
    $.ajax({
        type: "get",
        url: "get_all_device_firmware_details.py",
        cache: false,
        success: function (result) {
            // {"result": {"ap25": ["1.2.12"], "idu4": ["2.0.5"], "odu16": ["7.2.10"], "odu100": ["7.2.20", "7.2.25"], "ccu": []}, "success": 0}
            if (result.success == 0) {
                firmwareVersion = result.result;
            }
            else {
                $().toastmessage('showErrorToast', result.result);
            }
        }
    });
}


function getHardwareInformation(deviceType) {
    var ipAddress = $formInput.eq($formInputIndex["ip_address"]).val();
    var selectedDeviceType = $formSelectList.eq($formSelectListIndex["device_type"]).val();

    if (ipAddress != "" && ipAddress.match(ipValidate) && selectedDeviceType != "") {
        //$("#firmware_loading").show();
        //$("a#a_firmware_version").hide();
        var port = $formInput.eq($formInputIndex["get_set_port"]).val();
        var community = $formInput.eq($formInputIndex["read_community"]).val()
        $.ajax({
            type: "get",
            url: "get_hardware_detail.py",
            data: {"ip_address": ipAddress, "device_type": deviceType, "port": port, "community": community},
            cache: false,
            success: function (result) {
                // {"result": "7.2.25", "success": 0}
                if (result['success'] == 1) {
                    $().toastmessage('showErrorToast', result['result']);
                }
                else {
                    $formInput.eq($formInputIndex["serial_number"]).val(result["serial_number"]);
                    $formInput.eq($formInputIndex["hardware_version"]).val(result["hardware_version"]);

                }


            }
        });
        //$("#firmware_loading").hide();
        //$("a#a_firmware_version").show();
    }
    else {
        $().toastmessage('showWarningToast', "Please enter valid IP address and device type");
    }

}


function getFirmwareVersion(deviceType) {
    var ipAddress = $formInput.eq($formInputIndex["ip_address"]).val();
    var selectedDeviceType = $formSelectList.eq($formSelectListIndex["device_type"]).val();

    if (ipAddress != "" && ipAddress.match(ipValidate) && selectedDeviceType != "") {
        $("#firmware_loading").show();
        $("a#a_firmware_version").hide();
        var port = $formInput.eq($formInputIndex["get_set_port"]).val();
        var community = $formInput.eq($formInputIndex["read_community"]).val()
        $.ajax({
            type: "get",
            url: "get_firmware_details.py",
            data: {"ip_address": ipAddress, "device_type": selectedDeviceType, "port": port, "community": community},
            cache: false,
            success: function (result) {
                // {"result": "7.2.25", "success": 0}
                if (result['success'] == 1) {
                    $().toastmessage('showErrorToast', result['result']);
                }
                firmwareSelectList(result.result, selectedDeviceType);

            },
            complete: function () {
                $("#firmware_loading").hide();
                $("a#a_firmware_version").show();
            }
        });
    }
    else {
        $().toastmessage('showWarningToast', "Please enter valid IP address and device type");
    }
}

function firmwareSelectList(selectedFirmware, deviceType) {
    //var deviceType = "odu100";
    if (firmwareVersion[deviceType] != undefined || firmwareVersion[deviceType]) {
        var optionStr = "<option value =\"\"> -- Select Firmware Version --</option>";
        for (var i = 0, firmLen = firmwareVersion[deviceType].length; i < firmLen; i++) {
            if (String(firmwareVersion[deviceType][i]) == selectedFirmware)
                optionStr += "<option value =\"" + String(firmwareVersion[deviceType][i]) + "\"  selected=\"selected\">" + String(firmwareVersion[deviceType][i]) + "</option>";
            else
                optionStr += "<option value =\"" + String(firmwareVersion[deviceType][i]) + "\">" + String(firmwareVersion[deviceType][i]) + "</option>";
        }
        $formSelectList.eq($formSelectListIndex["firmware_version"]).html(optionStr);
    }
}

// To add tool tip on form inputs
function addFormToolTip() {
    // add tool tip
    $tooltip = $("form#form_host input[type='text'],form#form_host input[type='password'],form#form_host input[type='checkbox'],form#form_host textarea,form#form_host select").tooltip({
        // place tooltip on the right edge
        position: "center right",
        // a little tweaking of the position
        offset: [-2, 10],
        // use the built-in fadeIn/fadeOut effect
        effect: "fade",
        // custom opacity setting
        opacity: 1.0
    });
}

// to bind form cancel events
function cancelForm() {
    $("button#cancel_host").click(function () {
        hideForm();
    });
}

// to show form.
function showForm() {
    $gridViewDiv.hide();
    $formDiv.show();
    $("img#add_host").hide();
    $("img#del_host").hide();

}

// to hide form
function hideForm() {
    $gridViewDiv.show();
    $formDiv.hide();
    $("img#add_host").show();
    $("img#del_host").show();
    /* this is bcoz when validation unsuccess and you click on cancel button then tooltip visible so this code will hide that. */
    if ($tooltip) {
        $tooltip.each(function (index) {
            var $this = $(this).data('tooltip');
            if ($this.isShown(true))
                $this.hide();
        });
    }
}

// to submit form
function submitForm($formObj) {
    valiateForm($formObj);		// to bind validation on form
    // binding submit event on form
    $formObj.submit(function () {
        var $formThis = $(this);
        if ($formThis.valid()) {
            spinStart($spinLoading, $spinMainLoading);
            var action = $formThis.attr("action");
            var method = $formThis.attr("method");
            var data = $formThis.serialize() + "&device_type=" + $("#device_type").val();
            /*
             * Check Host Details in case device type is odu16 and oud100
             */
            if ($formSelectList.eq($formSelectListIndex["device_type"]).val() == "odu16" || $formSelectList.eq($formSelectListIndex["device_type"]).val() == "odu100") {
                if ($formSelectList.eq($formSelectListIndex["device_type"]).val() == "odu100") {
                    try {
                        if ($formSelectList.eq($formSelectListIndex["odu100_management_mode"]).val() == "1") {
                            if (parseInt($formInput.eq($formInputIndex["odu100_vlan_tag"]).val()) > 0 && parseInt($formInput.eq($formInputIndex["odu100_vlan_tag"]).val()) <= 4094) {
                                //nothing
                            }
                            else {
                                $.prompt(messages["VlanTagError"], {prefix: 'jqismooth'});
                                spinStop($spinLoading, $spinMainLoading);
                                return false;
                            }
                        }
                    }
                    catch (err) {
                        console.log(" error ");
                        $.prompt(messages["VlanTagError"], {prefix: 'jqismooth'});
                        spinStop($spinLoading, $spinMainLoading);
                        return false;
                    }
                }
                var raMacValue = $formInput.eq($formInputIndex["ra_mac"]).val();
                if ($.trim(raMacValue) == "") {
                    $.prompt(messages["raMacMissing"], {prefix: 'jqismooth'});
                    spinStop($spinLoading, $spinMainLoading);
                    return false;
                }
                else {
                    if (raMacValue.match("^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$")) {
                        var nodeType = $formSelectList.eq($formSelectListIndex["node_type"]).val();
                        ;
                        try {
                            if (parseInt(nodeType) == 1 || parseInt(nodeType) == 3) {
                                // check master mac
                                var masterMacValue = $formSelectList.eq($formSelectListIndex["master_mac"]).val();
                                if ($.trim(masterMacValue) == "") {
                                    $.prompt(messages["masterMacMissing"], {prefix: 'jqismooth'});
                                    spinStop($spinLoading, $spinMainLoading);
                                    return false;
                                }
                                else {
                                    // do nothing
                                    if (isRaMacFetched == 0) {
                                        $.prompt(messages["masterMacWarning"], {prefix: 'jqismooth'});
                                    }
                                }
                            }
                            else {
                                if (isRaMacFetched == 0) {
                                    $.prompt(messages["raMacWarning"], {prefix: 'jqismooth'});
                                }
                            }

                        }
                        catch (err) {

                        }
                    }
                    else {
                        $.prompt(messages["raMacError"], {prefix: 'jqismooth'});
                        spinStop($spinLoading, $spinMainLoading);
                        return false;
                    }
                }
            }
            else if ($formSelectList.eq($formSelectListIndex["device_type"]).val() == "ap25") {
                if ($formSelectList.eq($formSelectListIndex["dns_state"]).val() == 1) {
                    if ($.trim($formInput.eq($formInputIndex["primary_dns"]).val()) == "" || $.trim($formInput.eq($formInputIndex["primary_dns"]).val()) == "") {
                        $.prompt(messages["ap25NetworkDetailsError"], {prefix: 'jqismooth'});
                        spinStop($spinLoading, $spinMainLoading);
                        return false
                    }
                }
            }
            else if ($formSelectList.eq($formSelectListIndex["device_type"]).val() == "idu4") {
                try {
                    if ($formCheckbox.eq($formCheckboxIndex["idu4_management_mode"]).attr("checked")) {
                        if (parseInt($formInput.eq($formInputIndex["idu4_vlan_tag"]).val()) > 0 && parseInt($formInput.eq($formInputIndex["idu4_vlan_tag"]).val()) < 4095) {
                            //nothing
                        }
                        else {
                            $.prompt(messages["VlanTagError"], {prefix: 'jqismooth'});
                            spinStop($spinLoading, $spinMainLoading);
                            return false;
                        }
                    }
                    /*if($.trim($formInput.eq($formInputIndex["idu4_tdm_ip"]).val()) == "")
                     {
                     $.prompt(messages["TdmIPError"],{prefix:'jqismooth'});
                     spinStop($spinLoading,$spinMainLoading);
                     return false;
                     }*/
                }
                catch (err) {
                    $.prompt(messages["VlanTagError"], {prefix: 'jqismooth'});
                    spinStop($spinLoading, $spinMainLoading);
                    return false;
                }
            }
            else if ($formSelectList.eq($formSelectListIndex["device_type"]).val() == "ccu") {
                if ($.trim($formInput.eq($formInputIndex["ccu_dhcp_netmask"]).val()) == "") {
                    $.prompt(messages["ccuDhcpNetmaskError"], {prefix: 'jqismooth'});
                    spinStop($spinLoading, $spinMainLoading);
                    return false
                }
            }
            if (actionName == "edit") {
                var tempIdu4VlanMode = $formCheckbox.eq($formCheckboxIndex["idu4_management_mode"]).attr("checked") == true ? 1 : 0;


                if (oldIpAddress == $formInput.eq($formInputIndex["ip_address"]).val() && oldNetmask == $formInput.eq($formInputIndex["netmask"]).val() && oldGateway == $formInput.eq($formInputIndex["gateway"]).val() && oldDhcp == $formSelectList.eq($formSelectListIndex["dns_state"]).val() && oldPriIp == $formInput.eq($formInputIndex["primary_dns"]).val() && oldSecIp == $formInput.eq($formInputIndex["secondary_dns"]).val() && odu100VlanMode == $formSelectList.eq($formSelectListIndex["odu100_management_mode"]).val() && odu100VlanTag == $formInput.eq($formInputIndex["odu100_vlan_tag"]).val() && idu4VlanMode == tempIdu4VlanMode && idu4VlanTag == $formInput.eq($formInputIndex["idu4_vlan_tag"]).val() && idu4TdmIp == $formInput.eq($formInputIndex["idu4_tdm_ip"]).val() && ccuDhcpNetmask == $formInput.eq($formInputIndex["ccu_dhcp_netmask"]).val()) {
                    action += "?ip_update=0";
                    submitAjaxCall(method, action, data);
                }
                else {
                    $.prompt(messages["changeIpAddressConfirm"], { buttons: {Yes: true, No: false}, prefix: 'jqismooth', callback: function (v, m) {
                        if (v != undefined && v == true) {
                            action += "?ip_update=1";
                        } else {
                            action += "?ip_update=0";
                        }
                        submitAjaxCall(method, action, data);
                    } });
                }
            }
            else {
                submitAjaxCall(method, action, data);
            }

        }
        else {
            $().toastmessage('showErrorToast', messages["validationError"]);
        }
        return false;
    });
}
function submitAjaxCall(method, action, data) {
    $.ajax({
        type: method,
        url: action,
        data: data,
        cache: false,
        success: function (result) {
            if (result.success == 0) {
                hideForm();
                $().toastmessage('showSuccessToast', messages[actionName]);
                if (currentTab == "active") {
                    gridViewActiveHost();
                    $gridViewDisableHostFetched = 0;
                    $gridViewDiscoveredHostFetched = 0;
                }
                else if (currentTab == "disable") {
                    gridViewDisableHost();
                    $gridViewActiveHostFetched = 0;
                    $gridViewDiscoveredHostFetched = 0;
                }
                else if (currentTab == "discovered") {
                    gridViewDiscoveredHost();
                    $gridViewDisableHostFetched = 0;
                    $gridViewActiveHostFetched = 0;
                }
                update_host_parents();
            }
            else {
                if (result.msg == undefined) {
                    $().toastmessage('showErrorToast', messages["unknownError"]);
                }
                else {
                    $().toastmessage('showErrorToast', messages[result.msg] != undefined && messages[result.msg] || result.msg);
                }
            }
            spinStop($spinLoading, $spinMainLoading);
        }
    });
}
// validation rules for the forms
function valiateForm($formObj) {
    $formObj.validate({
        rules: {
            host_name: {
                required: true,
                alphaNumeric: true,
                noSpace: true
            },
            host_alias: {
                required: true,
                alphaNumeric: true
            },
            ip_address: {
                required: true,
                ipv4Address: true
            },
            mac_address: {
                required: true,
                macAddress: true
            },
            device_type: {
                required: true
            },
            host_state: {
                required: true
            },
            host_priority: {
                required: true
            },
            host_parent: {
                required: true
            },
            host_comment: {
                alphaNumeric: true
            },
            netmask: {
                //netmask:true,
                ipv4Address: true,
                required: true
            },
            gateway: {
                ipv4Address: true,
                required: true
            },
            odu100_vlan_tag: {
                number: true,
                min: 1,
                max: 4094
            },
            idu4_vlan_tag: {
                number: true,
                min: 1,
                max: 4094
            },
            idu4_tdm_ip: {
                ipv4Address: true
            },
            ccu_dhcp_netmask: {
                ipv4Address: true
            },
            primary_dns: {
                ipv4Address: true
            },
            secondary_dns: {
                ipv4Address: true
            },
            http_username: {
                //alphaNumeric: true
            },
            http_password: {
                //alphaNumeric: true
            },
            http_port: {
                number: true
            },
            ssh_username: {
                //alphaNumeric: true
            },
            ssh_password: {
                //alphaNumeric: true
            },
            ssh_port: {
                number: true
            },
            read_community: {
                alphaNumeric: true
            },
            write_community: {
                alphaNumeric: true
            },
            snmp_version: {
                alphaNumeric: true
            },
            get_set_port: {
                number: true
            },
            trap_port: {
                number: true
            },
            longitude: {
                required: true,
                number: true,
                min: 0,
                max: 180
            },
            latitude: {
                required: true,
                number: true,
                min: 0,
                max: 180
            },
            serial_number: {
                alphaNumeric: true
            },
            hardware_version: {
                alphaNumeric: true
            },
            host_vendor: {
                required: true
            },
//            longitude: {
//                number: true,
//                min: 0,
//                max: 180
//            },
//            latitude: {
//                number: true,
//                min: 0,
//                max: 180
//            },
            host_os: {
                required: true
            }
        },
        messages: {
            host_name: {
                required: "Host name is a required field",
                alphaNumeric: "Host name should be alpha numeric",
                noSpace: "In host name space are not allowed"
            },
            host_alias: {
                required: "Host alias is a required field",
                alphaNumeric: "Host alias should be alpha numeric"
            },
            ip_address: {
                required: "IP address is a required field",
                ipv4Address: "Invalid IP address"
            },
            mac_address: {
                required: "MAC address is a required field",
                macAddress: "Invalid MAC address"
            },
            device_type: {
                required: "Device type is a required field"
            },
            host_state: {
                required: "Host state is a required field"
            },
            host_priority: {
                required: "Host priority is a required field"
            },
            host_parent: {
                required: "Host parent is a required field"
            },
            host_comment: {
                alphaNumeric: "Comment should be alhpa numeric"
            },
            netmask: {
                //netmask:"Invalid Netmask",
                ipv4Address: "Invalid Netmask",
                required: "Netmask is a required field"
            },
            gateway: {
                ipv4Address: "Invalid IP Address",
                required: "Gateway is a required field"
            },
            odu100_vlan_tag: {
                number: "it should be a number",
                min: "tag number between 1 to 4094, if Management Mode is NORMAL then left this blank",
                max: "tag number between 1 to 4094"
            },
            idu4_vlan_tag: {
                number: "it should be a number",
                min: "tag number between 1 to 4094",
                max: "tag number between 1 to 4094"
            },
            idu4_tdm_ip: {
                ipv4Address: "Invalid IP Address"
            },
            ccu_dhcp_netmask: {
                ipv4Address: "Invalid IP Address"
            },
            primary_dns: {
                ipv4Address: "Invalid IP Address"
            },
            secondary_dns: {
                ipv4Address: "Invalid IP Address"
            },
            http_username: {
                //alphaNumeric: "Username should be alpha numeric"
            },
            http_password: {
                //alphaNumeric: "Password should be alpha numeric"
            },
            http_port: {
                number: "Port should be a number"
            },
            ssh_username: {
                //alphaNumeric: "Username should be alpha numeric"
            },
            ssh_password: {
                //alphaNumeric: "Password should be alpha numeric"
            },
            ssh_port: {
                number: "Port should be a number"
            },
            read_community: {
                alphaNumeric: "Read community should be alpha numeric"
            },
            write_community: {
                alphaNumeric: "Write community should be alpha numeric"
            },
            snmp_version: {
                alphaNumeric: "SNMP version should be correct"
            },
            get_set_port: {
                number: "SNMP get/set port should be a number"
            },
            trap_port: {
                number: "SNMP trap port should be a number"
            },
            longitude: {
                required: "Longitude is Required Field",
                number: "Longitude should be a number",
                min: "tag number between -90 to +90",
                max: "tag number between -90 to +90"
            },
            latitude: {
                required: "Latitude is Required Field",
                number: "Latitude should be a number",
                min: "tag number between -90 to +90",
                max: "tag number between -90 to +90"
            },
            serial_number: {
                alphaNumeric: "Serial number should be a alpha numeric"
            },
            hardware_version: {
                alphaNumeric: "Hardware version should be a alpha numeric"
            },
            host_vendor: {
                required: "Host Vendor is a required field"
            },
//            longitude: {
//                number: "it should be a number",
//                min: "tag number beetween -90 to +90",
//                max: "tag number beetween -90 to +90"
//            },
//            latitude: {
//                number: "it should be a number",
//                min: "tag number beetween -90 to +90",
//                max: "tag number beetween -90 to +90"
//            },
            host_os: {
                required: "Host OS name is a required field"
            }
        }
    });
}
// to create add form
function addForm() {
    $("#device_type").removeAttr('disabled');
    $("#advanced_settings").hide();
    getAllFirmwareDict();

    if (currentTab == "discovered") {
        var selectedRow = new Array();
        selectedRow = fnGetSelected($gridViewDiscoveredHostDataTable)
        var rLength = selectedRow.length;
        if (rLength == 0) {
            $.prompt(messages["noneSelectedError"], {prefix: 'jqismooth'});
        }
        else if (rLength == 1) {
            // get data
            for (var i = 0; i < selectedRow.length; i++) {
                var aData = [];
                var iRow = $gridViewDiscoveredHostDataTable.fnGetPosition(selectedRow[i]);
                aData = $gridViewDiscoveredHostDataTable.fnGetData(iRow);

                //selected host details
                selectedHostName = aData[2];
                selectedHostAlias = aData[2];
                selectedIpAddress = aData[2];
                selectedMacAddress = aData[3];
                selectedDeviceType = String(aData[4]).toLowerCase();
            }

            $formTitle.html("Add Host");
            $form.attr("action", "add_host.py");
            manage_host_parents(null);
            //$formInput.val("");
            //$formTextarea.val("");
            $formAddButton.css({"display": "inline-block"});
            $formEditButton.hide();
            showForm();
            if (!hostDefaultDetails) {
                loadDefault();
            }
            else {
                setValues(hostDefaultDetails);
            }
        }
        else {
            $.prompt(messages["multiSelectedError"], {prefix: 'jqismooth'});
        }
    }
    else if (currentTab == "deleted") {
        actionName = "addDeletedHost";
        var selectedRow = new Array();
        selectedRow = fnGetSelected($gridViewDeletedHostDataTable)
        var rLength = selectedRow.length;
        if (rLength == 0) {
            $.prompt(messages["noneSelectedError"], {prefix: 'jqismooth'});
        }
        else {
            $.prompt(messages[actionName], { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: function () {
                //$.prompt("asd",{prefix:'jqismooth'});
                var hostId = [];
                for (var i = 0; i < selectedRow.length; i++) {
                    var iRow = $gridViewDeletedHostDataTable.fnGetPosition(selectedRow[i]);
                    var aData = $gridViewDeletedHostDataTable.fnGetData(iRow);
                    hostId.push(String(aData[0]));
                }
                action = "add_deleted_host.py";
                method = "post";
                data = {"host_ids": String(hostId)};
                spinStart($spinLoading, $spinMainLoading);
                $.ajax({
                    type: method,
                    url: action,
                    data: data,
                    cache: false,
                    success: function (result) {
                        if (result.success == 0) {
                            // update datatable
                            $().toastmessage('showSuccessToast', result.msg);
                        }
                        else {
                            if (result.msg == undefined) {
                                $().toastmessage('showErrorToast', messages["unknownError"]);
                            }
                            else {
                                $().toastmessage('showErrorToast', messages[result.msg]);
                            }
                        }
                        spinStop($spinLoading, $spinMainLoading);
                    }
                });
                //alert("sdf");
            }});
        }
    }
    else {
        $formTitle.html("Add Host");
        $form.attr("action", "add_host.py");
        manage_host_parents(null);
        //$formInput.val("");
        //$formTextarea.val("");
        $formAddButton.css({"display": "inline-block"});
        $formEditButton.hide();
        showForm();
        if (!hostDefaultDetails) {
            loadDefault();
        }
        else {
            setValues(hostDefaultDetails);
        }
    }
    if ($("#host_id").val() == undefined || $("#host_id").val() == "")
        $("#advanced_settings").hide();

}
function loadDefault() {
    $.ajax({
        type: "get",
        url: "host_default_details.py",
        cache: false,
        success: function (result) {
            if (result.success == 0) {
                hostDefaultDetails = result.result;
                setValues(hostDefaultDetails);
            }
            else {
                if (result.msg == undefined) {
                    $().toastmessage('showWarningToast', messages["unknownError"]);
                }
                else {
                    if (result.msg == undefined) {
                        $().toastmessage('showErrorToast', messages["unknownError"]);
                    }
                    else {
                        $().toastmessage('showErrorToast', messages[result.msg]);
                    }
                }
            }
        }
    });
}
function setValues(details) {
    $form.find("input#host_id").val(details["host_id"]);
    //$form.find("input#node_type").val(details["node_type"]);
    $formInput.eq($formInputIndex["host_name"]).val(details["host_name"]);
    $formInput.eq($formInputIndex["host_alias"]).val(details["host_alias"]);
    $formInput.eq($formInputIndex["ip_address"]).val(details["ip_address"]);
    $formInput.eq($formInputIndex["mac_address"]).val(details["mac_address"]);
    $formInput.eq($formInputIndex["ra_mac"]).val(details["ra_mac"]);
    $formInput.eq($formInputIndex["netmask"]).val(details["netmask"]);
    $formInput.eq($formInputIndex["gateway"]).val(details["gateway"]);
    $formInput.eq($formInputIndex["primary_dns"]).val(details["primary_dns"]);
    $formInput.eq($formInputIndex["secondary_dns"]).val(details["secondary_dns"]);
    $formInput.eq($formInputIndex["http_username"]).val(details["http_username"]);
    $formInput.eq($formInputIndex["http_port"]).val(details["http_port"]);
    $formInput.eq($formInputIndex["read_community"]).val(details["read_community"]);
    $formInput.eq($formInputIndex["write_community"]).val(details["write_community"]);
    $formInput.eq($formInputIndex["get_set_port"]).val(details["get_set_port"]);
    $formInput.eq($formInputIndex["trap_port"]).val(details["trap_port"]);
    $formInput.eq($formInputIndex["ssh_username"]).val(details["ssh_username"]);
    $formInput.eq($formInputIndex["ssh_port"]).val(details["ssh_port"]);
    $formInput.eq($formInputIndex["longitude"]).val(details["longitude"]);
    $formInput.eq($formInputIndex["latitude"]).val(details["latitude"]);
    $formInput.eq($formInputIndex["serial_number"]).val(details["serial_number"]);
    $formInput.eq($formInputIndex["hardware_version"]).val(details["hardware_version"]);
    $formInput.eq($formInputIndex["odu100_vlan_tag"]).val(details["odu100_vlan_tag"]);
    $formInput.eq($formInputIndex["idu4_vlan_tag"]).val(details["idu4_vlan_tag"]);
    $formInput.eq($formInputIndex["idu4_tdm_ip"]).val(details["idu4_tdm_ip"]);
    $formInput.eq($formInputIndex["ccu_dhcp_netmask"]).val(details["ccu_dhcp_netmask"]);

    $formPassword.eq($formPasswordIndex["http_password"]).val(details["http_password"]);
    $formPassword.eq($formPasswordIndex["ssh_password"]).val(details["ssh_password"]);
    $formTextarea.eq($formTextareaIndex["host_comment"]).val(details["host_comment"]);
    $formCheckbox.eq($formCheckboxIndex["is_reconciliation"]).attr("checked", false);
    $formCheckbox.eq($formCheckboxIndex["is_reconciliation"]).attr("disabled", false);
    if (details["lock_position"] == 't')
        $formCheckbox.eq($formCheckboxIndex["lock_position"]).attr("checked", true);
    else
        $formCheckbox.eq($formCheckboxIndex["lock_position"]).attr("checked", false);

    if (details["idu4_management_mode"] == 1)
        $formCheckbox.eq($formCheckboxIndex["idu4_management_mode"]).attr("checked", true);
    else
        $formCheckbox.eq($formCheckboxIndex["idu4_management_mode"]).attr("checked", false);

    $formSelectList.eq($formSelectListIndex["device_type"]).val(details["device_type"]);
    $formSelectList.eq($formSelectListIndex["device_type"]).change();
    $formSelectList.eq($formSelectListIndex["node_type"]).val(details["node_type"]);
    $formSelectList.eq($formSelectListIndex["odu100_management_mode"]).val(details["odu100_management_mode"]);
    if (details["device_type"] == "odu16" || details["device_type"] == "odu100") {
        $RaMacDiv.show();
        if (!isNaN(parseInt(details["node_type"])) && parseInt(details["node_type"]) != 0 && parseInt(details["node_type"]) != 2) {
            oduMasterList(details["device_type"], details["master_mac"]);
            $MasterSlaveDiv.show();
        }
        else {
            $MasterSlaveDiv.hide();
            $formSelectList.eq($formSelectListIndex["master_mac"]).find("option").eq(0).attr("selected", "selected");
        }
    }
    else {
        $RaMacDiv.hide();
        $MasterSlaveDiv.hide();
        $formSelectList.eq($formSelectListIndex["master_mac"]).find("option").eq(0).attr("selected", "selected");
    }
    $formSelectList.eq($formSelectListIndex["host_state"]).val(details["host_state"]);
    $formSelectList.eq($formSelectListIndex["host_priority"]).val(details["host_priority"]);
    if (details["host_parent"] == "") {
        $formSelectList.eq($formSelectListIndex["host_parent"]).find("option").eq(0).attr("selected", "selected");
    }
    else {
        $formSelectList.eq($formSelectListIndex["host_parent"]).val(details["host_parent"]);
    }
    if (details["hostgroup"] == "") {
        $formSelectList.eq($formSelectListIndex["hostgroup"]).find("option").eq(0).attr("selected", "selected");
    }
    else {
        $formSelectList.eq($formSelectListIndex["hostgroup"]).val(details["hostgroup"]);
    }
    if (details["dns_state"] == "") {
        $formSelectList.eq($formSelectListIndex["dns_state"]).find("option").eq(0).attr("selected", "selected");
    }
    else {
        $formSelectList.eq($formSelectListIndex["dns_state"]).val(details["dns_state"]);
    }
    $formSelectList.eq($formSelectListIndex["snmp_version"]).val(details["snmp_version"]);
    if (details["host_vendor"] == "") {
        $formSelectList.eq($formSelectListIndex["host_vendor"]).find("option").eq(1).attr("selected", "selected");
    }
    else {
        $formSelectList.eq($formSelectListIndex["host_vendor"]).val(details["host_vendor"]);
    }
    if (details["host_os"] == "") {
        $formSelectList.eq($formSelectListIndex["host_os"]).find("option").eq(1).attr("selected", "selected");
    }
    else {
        $formSelectList.eq($formSelectListIndex["host_os"]).val(details["host_os"]);
    }

    if (currentTab == "discovered") {
        $formInput.eq($formInputIndex["host_name"]).val(selectedHostName);
        $formInput.eq($formInputIndex["host_alias"]).val(selectedHostAlias);
        $formInput.eq($formInputIndex["ip_address"]).val(selectedIpAddress);
        $formInput.eq($formInputIndex["mac_address"]).val(selectedMacAddress);
        $formSelectList.eq($formSelectListIndex["device_type"]).val(selectedDeviceType);
        $formSelectList.eq($formSelectListIndex["device_type"]).change();
    }

}
function editForm(id) {
    isRaMacFetched = 1;
    getAllFirmwareDict();
    $("#device_type").attr('disabled', 'disabled');
    //$("#device_type").attr('readonly','readonly');
    $formTitle.html("Edit Host");
    $form.attr("action", "edit_host.py");
    manage_host_parents(id);
    $formEditButton.css({"display": "inline-block"});
    $formAddButton.hide();
    $("#advanced_settings").show();
    $.ajax({
        type: "get",
        url: "get_host_by_id.py?host_id=" + id,
        cache: false,
        success: function (result) {
            if (result.success == 0) {
                hostDetails = result.result;
                oldIpAddress = hostDetails["ip_address"];
                oldNetmask = hostDetails["netmask"];
                oldGateway = hostDetails["gateway"];
                oldDhcp = hostDetails["dns_state"];
                oldPriIp = hostDetails["primary_dns"];
                oldSecIp = hostDetails["secondary_dns"];
                odu100VlanMode = hostDetails["odu100_management_mode"];
                odu100VlanTag = hostDetails["odu100_vlan_tag"];
                if (parseInt(odu100VlanTag) == 0) {
                    odu100VlanTag = "";
                    hostDetails["odu100_vlan_tag"] = "";
                }
                idu4VlanMode = hostDetails["idu4_management_mode"];
                idu4VlanTag = hostDetails["idu4_vlan_tag"];
                idu4TdmIp = hostDetails["idu4_tdm_ip"];
                ccuDhcpNetmask = hostDetails["ccu_dhcp_netmask"];
                setValues(hostDetails);
                // version
                firmwareSelectList(hostDetails["firmware_version"], hostDetails["device_type"]);
                showForm();
                $formCheckbox.eq($formCheckboxIndex["is_reconciliation"]).attr("checked", false);
                $formCheckbox.eq($formCheckboxIndex["is_reconciliation"]).attr("disabled", true);
            }
            else {
                if (result.msg == undefined) {
                    $().toastmessage('showErrorToast', messages["unknownError"]);
                }
                else {
                    $().toastmessage('showErrorToast', messages[result.msg]);
                }
            }
        }
    });
}
function addHost() {
    actionName = "add";
    if (formStatus == 0) {
        createForm(actionName);
        formStatus = 1;
    }
    else {
        addForm();
    }
}

function editHost(id, isLocalhost) {
    var selectedRow = new Array();
    if (currentTab == "active")
        selectedRow = fnGetSelected($gridViewActiveHostDataTable)
    else if (currentTab == "disable")
        selectedRow = fnGetSelected($gridViewDisableHostDataTable)

    var rLength = selectedRow.length;
    if (rLength == 0 && id == undefined && isLocalhost == undefined) {
        $.prompt(messages["noneSelectedError"], {prefix: 'jqismooth'});
    }
    else if (rLength == 1 || (id != undefined && isLocalhost != undefined)) {
        if (id == undefined && isLocalhost == undefined) {
            var aData = [];
            if (currentTab == "active") {
                var iRow = $gridViewActiveHostDataTable.fnGetPosition(selectedRow[0]);
                aData = $gridViewActiveHostDataTable.fnGetData(iRow);
            }
            else if (currentTab == "disable") {
                var iRow = $gridViewDisableHostDataTable.fnGetPosition(selectedRow[0]);
                aData = $gridViewDisableHostDataTable.fnGetData(iRow);
            }
            id = aData[0];
            isLocalhost = aData[1];
        }
        if (isLocalhost == 0) {
            actionName = "edit";
            if (formStatus == 0) {
                createForm(actionName, id);
                formStatus = 1;
            }
            else {
                editForm(id);
            }
        }
        else {
            $.prompt(messages["localhostEditError"], {prefix: 'jqismooth'});
        }
    }
    else {
        $.prompt(messages["multiSelectedError"], {prefix: 'jqismooth'});
    }
}

function delHost() {
    actionName = "delConfirm";
    hideForm();
    var selectedRow = new Array();
    if (currentTab == "active")
        selectedRow = fnGetSelected($gridViewActiveHostDataTable)
    else if (currentTab == "disable")
        selectedRow = fnGetSelected($gridViewDisableHostDataTable)
    else if (currentTab == "discovered")
        selectedRow = fnGetSelected($gridViewDiscoveredHostDataTable)
    else if (currentTab == "deleted")
        selectedRow = fnGetSelected($gridViewDeletedHostDataTable)

    var rLength = selectedRow.length;
    if (rLength == 0) {
        $.prompt(messages["noneSelectedError"], {prefix: 'jqismooth'});
    }
    else {
        $.prompt(messages[actionName], { buttons: {Ok: true, Cancel: false}, prefix: 'jqismooth', callback: delHostCallback });
    }
}
function update_host_parents() {
    $.ajax({
        type: "get",
        url: "host_parents.py",
        cache: false,
        success: function (result) {
            $result = $(result);
            $formSelectList.eq($formSelectListIndex["host_parent"]).html($result.html());
        }
    });
}
function manage_host_parents(edited_host_id) {
    $formSelectList.eq($formSelectListIndex["host_parent"]).find("option").attr("disabled", false);
    if (edited_host_id != null) {
        $formSelectList.eq($formSelectListIndex["host_parent"]).find("option[value='" + edited_host_id + "']").attr("disabled", true);
    }
}
function delHostCallback(v, m) {
    actionName = "del"
    if (v != undefined && v == true) {
        var action = "del_host.py";
        var method = "get";
        spinStart($spinLoading, $spinMainLoading);
        var selectedRow = new Array();
        if (currentTab == "active")
            selectedRow = fnGetSelected($gridViewActiveHostDataTable)
        else if (currentTab == "disable")
            selectedRow = fnGetSelected($gridViewDisableHostDataTable)
        else if (currentTab == "discovered")
            selectedRow = fnGetSelected($gridViewDiscoveredHostDataTable)
        else if (currentTab == "deleted")
            selectedRow = fnGetSelected($gridViewDeletedHostDataTable)

        var rLength = selectedRow.length;
        var hostId = [];
        var discoveryType = [];
        var isLocalhost = false;
        for (var i = 0; i < selectedRow.length; i++) {
            var aData = [];
            if (currentTab == "active") {
                var iRow = $gridViewActiveHostDataTable.fnGetPosition(selectedRow[i]);
                aData = $gridViewActiveHostDataTable.fnGetData(iRow);
                action = "del_host.py";
                if (aData[1] == 0) {
                    hostId.push(aData[0]);
                }
                else {
                    isLocalhost = true;
                    break;
                }
            }
            else if (currentTab == "disable") {
                var iRow = $gridViewDisableHostDataTable.fnGetPosition(selectedRow[i]);
                aData = $gridViewDisableHostDataTable.fnGetData(iRow);
                action = "del_host.py";
                if (aData[1] == 0) {
                    hostId.push(aData[0]);
                }
                else {
                    isLocalhost = true;
                    break;
                }
            }
            else if (currentTab == "discovered") {
                var iRow = $gridViewDiscoveredHostDataTable.fnGetPosition(selectedRow[i]);
                aData = $gridViewDiscoveredHostDataTable.fnGetData(iRow);
                action = "delete_discovered_host.py";
                hostId.push(String(aData[0]));
                discoveryType.push(aData[1]);
            }
            else if (currentTab == "deleted") {
                var iRow = $gridViewDeletedHostDataTable.fnGetPosition(selectedRow[i]);
                aData = $gridViewDeletedHostDataTable.fnGetData(iRow);
                hostId.push(aData[0]);
                action = "del_deleted_host.py";
                if (aData[1] == 0) {
                    hostId.push(aData[0]);
                }
                else {
                    isLocalhost = true;
                    break;
                }
            }
        }
        if (isLocalhost) {
            $.prompt(messages["localhostDelError"], {prefix: 'jqismooth'});
            spinStop($spinLoading, $spinMainLoading);
        }
        else {
            if (currentTab == "discovered") {
                $.ajax({
                    type: method,
                    url: action + "?host_id=" + String(hostId) + "&discovery_type=" + String(discoveryType),
                    cache: false,
                    success: function (result) {
                        if (result.success == 0) {
                            hideForm();
                            $().toastmessage('showSuccessToast', messages[actionName]);
                            for (var i = 0; i < selectedRow.length; i++) {
                                var aData = [];
                                if (currentTab == "discovered") {
                                    var iRow = $gridViewDiscoveredHostDataTable.fnGetPosition(selectedRow[i]);
                                    $gridViewDiscoveredHostDataTable.fnDeleteRow(iRow);
                                }
                            }
                        }
                        else {
                            if (result.msg == undefined) {
                                $().toastmessage('showErrorToast', messages["unknownError"]);
                            }
                            else {
                                $().toastmessage('showErrorToast', messages["unknownError"]);
                            }
                        }
                        spinStop($spinLoading, $spinMainLoading);
                    }
                });
            }
            else {
                $.ajax({
                    type: method,
                    url: action + "?host_ids=" + String(hostId),
                    cache: false,
                    success: function (result) {
                        if (result.success == 0) {
                            hideForm();
                            $().toastmessage('showSuccessToast', messages[actionName]);
                            for (var i = 0; i < selectedRow.length; i++) {
                                var aData = [];
                                if (currentTab == "active") {
                                    var iRow = $gridViewActiveHostDataTable.fnGetPosition(selectedRow[i]);
                                    $gridViewActiveHostDataTable.fnDeleteRow(iRow);
                                }
                                else if (currentTab == "disable") {
                                    var iRow = $gridViewDisableHostDataTable.fnGetPosition(selectedRow[i]);
                                    $gridViewDisableHostDataTable.fnDeleteRow(iRow);
                                }
                                else if (currentTab == "deleted") {
                                    var iRow = $gridViewDeletedHostDataTable.fnGetPosition(selectedRow[i]);
                                    $gridViewDeletedHostDataTable.fnDeleteRow(iRow);
                                    $gridViewDiscoveredHostFetched = 0;
                                }
                                $gridViewDeletedHostFetched = 0;
                            }
                            if (currentTab == "discovered") {
                                gridViewDiscoveredHost();
                            }
                        }
                        else {
                            if (result.msg == undefined) {
                                $().toastmessage('showErrorToast', messages["unknownError"]);
                            }
                            else {
                                $().toastmessage('showErrorToast', messages[result.msg]);
                            }
                        }
                        spinStop($spinLoading, $spinMainLoading);
                    }
                });
            }
        }
    }
    else {
        //$().toastmessage('showNoticeToast', "Remain Unchanged.");
    }
}
/*
 * I don't actually use this here, but it is provided as it might be useful and demonstrates
 * getting the TR nodes from DataTables
 */

function fnGetSelected(oTableLocal) {
    var aReturn = new Array();
    var aTrs = oTableLocal.fnGetNodes();

    for (var i = 0; i < aTrs.length; i++) {
        if ($(aTrs[i]).hasClass('row_selected')) {
            aReturn.push(aTrs[i]);
        }
    }
    return aReturn;
}

