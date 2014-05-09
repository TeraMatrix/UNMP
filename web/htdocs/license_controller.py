#!/usr/bin/python2.6

from license_bll import LicenseBll
from license import License
from mod_python import util


def manage_license(h):
    global html
    html = h
    css_list = []
    js_list = ["js/unmp/main/manage_license.js"]
    header_btn = ""
    html.new_header(
        "Manage License", "manage_license.py", header_btn, css_list, js_list)
    lic = LicenseBll()
    license_objects = lic.allowed_license()
    if isinstance(license_objects, tuple):
        html.write(License.manage_license(*license_objects))
    elif isinstance(license_objects, str):
        html.write(License.manage_license(
            "", "Sorry, License has been corrupted, please renew your License."))
    elif isinstance(license_objects, Exception):
        html.write(License.manage_license(
            "", "Sorry, License has been corrupted, please renew your License."))
    else:
        html.write(License.manage_license("", "Sorry, No License Available."))
    html.new_footer()


def license_upload(h):
    global html
    html = h
    nms_instance = __file__.split(
        "/")[3]       # it gives instance name of nagios system
    error_msg = {
        "expiredLicenseFile": "License has been expired, Please renew you License.",
        "invalidLicenseFile": "Invalid License : Please provide valid license.",
        "noLicenseFile": "No License File Detected."
    }
    license_msg = ""
    lic = LicenseBll()
    file_path = "/omd/sites/%s/share/check_mk/web/htdocs/xml/license" % (
        nms_instance)
    form = util.FieldStorage(html.req, keep_blank_values=1)
    upfile = form.getlist('file_uploader')[0]
    filename = upfile.filename
    filedata = upfile.value

    css_list = []
    js_list = ["js/unmp/main/manage_license.js"]
    header_btn = ""
    html.new_header(
        "Manage License", "manage_license.py", header_btn, css_list, js_list)

    # validate license file
    decoded_str = lic.validate_license(filedata)
    if isinstance(decoded_str, dict):
        if decoded_str["success"] == 0:
            fobj = open(file_path, 'w')  # 'w' is for 'write'
            fobj.write(filedata)
            fobj.close()
            lic.update_device_type(
            )  # update device_type table according license
            lic.update_license_details()
            license_msg = License.license_toast_msg(
                "success", "Your License Renewed successfully.")
        elif decoded_str["success"] == 2:
            # decoded_str["data"]
            license_msg = License.license_colorbox(
                "warning", decoded_str["msg"], decoded_str["data"])
        else:
            license_msg = License.license_toast_msg(
                "error", error_msg[decoded_str["msg"]])
    else:
        license_msg = License.license_toast_msg(
            "error", "Sorry, License has been corrupted, please renew your License.")

    html.write(license_msg)
    license_objects = lic.allowed_license()
    if isinstance(license_objects, tuple):
        html.write(License.manage_license(*license_objects))
    elif isinstance(license_objects, str):
        html.write(License.manage_license(
            "", "Sorry, License has been corrupted, please renew your License."))
    elif isinstance(license_objects, Exception):
        html.write(License.manage_license(
            "", "Sorry, License has been corrupted, please renew your License."))
    else:
        html.write(License.manage_license("", "Sorry, No License Available."))
    html.new_footer()


# def page_tip_license(h):
#     global html
#     html = h
#     html.write(License.page_tip_license())
