class FirmwareUpdateView(object):
    @staticmethod
    def firmware_div(host_id, selected_device):
        """

        @param host_id:
        @param selected_device:
        @return:
        """
        firmware_str = ""
        firmware_str += "<div id=\"firmware_div\" class=\"form-div\" style=\"margin-top: 56px;\"></div>"
        firmware_str += "<div id=\"download_software\" style=\"position:absolute;margin-top:60px;\"><input type=\"button\" name=\"software_download\" id=\"software_download\" value=\"Download Software\" class=\"yo-small yo-button\"/></div>"
        firmware_str += "<div id=\"firmware_table_div\" style=\"margin-bottom: 45px;display:block;bottom:0;position: absolute;width: 100%;left: 0;\"></div>"
        firmware_str += "<div class=\"form-div-footer\">\
                            <div>\
                                <label class=\"lbl\">Selected Firmware</label>\
                                <input type=\"text\" id=\"selected_firmware\" name=\"selected_firmware\" value=\"\" readonly=\"readonly\"/>\
                                <input type=\"button\" name=\"select_file\" id=\"select_file\" value=\"Choose File\" class=\"yo-small yo-button\" onclick=\"selectFirmwareTable();\"/ >\
                                <input type=\"button\" name=\"upload_new_file\" id=\"upload_new_file\" value=\"Upload New File\" class=\"yo-small yo-button\" onClick=\"uploadFile();\"/>\
                            </div>\
                            <input type=\"hidden\" name=\"host_id\" value=\"%s\" />\
                            <input type=\"hidden\" name=\"selected_device\" value=\"%s\" />\
                        </div>" % (host_id, selected_device)
        return firmware_str

    @staticmethod
    def firmware_get_data(host_id, device_type, device_list_parameter):
        """

        @param host_id:
        @param device_type:
        @param device_list_parameter:
        @return:
        """
        tab_str = ""
        if host_id == "" or host_id == "None":
            tab_str += "There is No Host Exist</div>"
        else:
            if device_type == UNMPDeviceType.ap25:
                tab_str += FirmwareUpdateView.firmware_master_slave_data(
                    host_id, device_type,
                    device_list_parameter)  # function call , it is used to make a form of selected profiling
        return tab_str

    @staticmethod
    def upload_form(host_id, device_type):
        """

        @param host_id:
        @param device_type:
        @return:
        """
        upload_str = ""
        upload_str += "<link href=\"css/example.css\" type=\"text/css\" rel=\"stylesheet\">\
                        <form method=\"post\" enctype=\"multipart/form-data\" action=\"firmware_file_upload.py\" style=\"font-size:10px;\">\
                            <input type=\"hidden\" name=\"host_id\" value=\"%s\"/>\
                            <input type=\"hidden\" name=\"device_type\" value=\"%s\"/>\
                            <label style=\"margin-top: 15px;margin-right: 25px;\" class=\"lbl\">Firmware File</label>\
                            <input style=\"font-size:10px;\" type=\"file\" name=\"file_uploader\" id=\"file_uploader\">\
                            <button name=\"button_uploader\" id=\"button_uploader\" type=\"file\" style=\"font-size:10px;\" class=\"yo-button yo-small\">\
                            <span class=\"upload\">Upload</span></button></form>\
                        </form/>" % (host_id, device_type)
        return upload_str
