var openDiv = -1;
$(function () {
    $("#addTemplateDiv, #addTemplateForm, #editTemplateDiv, #editTemplateForm, #addService, #templateServiceList").hide();
})
function createTemplate() {
    alert("Add Template!!!");
}
function editTemplate(id) {
    alert(id);
}
function deleteTemplate(id) {
    alert(id);
}
function addTemplate() {
    alert("Add");
}
function cancelAddTemplate() {
    alert("Cancel Add");
}
function hostServiceShowHide(obj, id) {
    if (openDiv != id) {
        $("div.service-list-div").slideUp(1000);
        $("div#serviceListDiv" + id).slideDown(1000);
        openDiv = id;
    }
    else {
        $("div.service-list-div").slideUp(1000);
        openDiv = -1;
    }
}
function updateTemplate() {
    alert("Update");
}
function cancelUpdateTemplate() {
    alert("Cancel Update");
}
function addService() {
    alert("Add Service");
}
