#!/usr/bin/python2.6

"""
@author:   Mahipal Choudhary
@date:     14-11-2011
@version:  0.1
@summary:  this is the View for the user to give inputs and generate a report for it
@organisation:  Codescape Consultants Pvt ltd
"""

from datetime import datetime


class User(object):
    @staticmethod
    def create_settings_form():
        try:
            s = """
                <div id=\"grid_view_div\">
                    <div class=\"yo-tabs\">
                        <ul>
                            <li id=\"information\" href="help_change_user_setting.py">
                                <a class=\"active\"  href=\"#content_1\" id=\"personal_information_tab\">Personal Information</a>
                            </li>
                            <li id=\"password\" href="help_change_password.py">
                                <a href=\"#content_2\" id=\"change_password_tab\">Change Password</a>
                            </li>
                        </ul>
                        <div id=\"content_1\" class=\"tab-content\" style=\"display:block;height:100%;\">
                            <table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_personal_information_tab\">
                            </table>
                        </div>
                        <div id=\"content_2\" class=\"tab-content\"></div>
                    </div>
                </div>"""
            return s
        except Exception, e:
            return str(e)

    @staticmethod
    def change_password(is_first_login, is_password_expired):
        try:
            div_id = "is_first_login"
            if is_password_expired:
                div_id = "is_password_expired"
            s = """
                <div id=\"grid_view_div\">
                    <div id=\"{0}\" class=\"yo-tabs\" >
                        <ul>
                            <li>
                                <a class=\"active\"href=\"#content_1\" id=\"change_password_tab\">Change Password</a>
                            </li>
                        </ul>
                        <div id=\"content_1\" class=\"tab-content\" style=\"display:block;height:100%;\">
                            <table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"grid_view_personal_information_tab\"></table>
                        </div>
                    </div>
                </div>""".format(div_id)
            return s
        except Exception, e:
            return str(e)

    @staticmethod
    def create_user_settings_form(first_name, last_name, designation, company, mobile, address, email_id):
        try:
            s = """
                <form action=\"save_user_settings_personal.py\" method=\"get\" id=\"edit_user_form\" name=\"edit_user_form\">
                    <div class=\"form-div\" style=\"margin-top:25px\">
                        <div class=\"form-body\" style=\"overflow:hidden;\">

                            <div class=\"row-elem\">
                                 <label class=\"lbl lbl-big\" for=\"first_name\">First Name</label>
                                 <input type=\"text\" id=\"first_name\" name=\"first_name\" title=\"Must be at least 4 characters.\" value=\"%s\">
                            </div>
                            <div class=\"row-elem\">
                                 <label class=\"lbl lbl-big\" for=\"last_name\">Last Name</label>
                                 <input type=\"text\" id=\"last_name\" name=\"last_name\" title=\"Must be at least 4 characters.\" value=\"%s\">
                            </div>
                            <div class=\"row-elem\">
                                 <label class=\"lbl lbl-big\" for=\"company\">Company</label>
                                 <input type=\"text\" id=\"company\" name=\"company\" title=\"Please Enter your Company Name.\" value=\"%s\">
                            </div>
                            <div class=\"row-elem\">
                                 <label class=\"lbl lbl-big\" for=\"designation\">Designation</label>
                                 <input type=\"text\" id=\"designation\" name=\"designation\" title=\"Please Enter your Designation.\" value=\"%s\">
                            </div>
                            <div class=\"row-elem\">
                                 <label class=\"lbl lbl-big\" for=\"address\">Address</label>
                                <textarea id=\"address\" name=\"address\" title=\"Please Enter your own Address.\">
                                    %s\
                                </textarea>
                            </div>
                            <div class=\"row-elem\">
                                 <label class=\"lbl lbl-big\" for=\"mobile\">Mobile Number</label>
                                 <input type=\"text\" id=\"mobile\" name=\"mobile\" title=\"Please Enter your Mobile Number&lt;br/&gt; Does't include +91 or 0.\" value=\"%s\">
                            </div>
                            <div class=\"row-elem\">
                                 <label class=\"lbl lbl-big\" for=\"email_id\">E-Mail ID</label>
                                 <input type=\"text\" id=\"email_id\" name=\"email_id\" title=\"Please Enter your E-Mail ID.\" value=\"%s\">
                            </div>
                        </div>
                    </div>
                    <div class=\"form-div-footer\">
                         <button type=\"submit\" class=\"yo-small yo-button\"><span class=\"edit\">Save</span></button>
                         <button type=\"reset\" class=\"yo-small yo-button\" id=\"close_edit_user\"><span class=\"cancel\">Cancel</span></button>
                    </div>
                </form>
                """ % (first_name, last_name, company,
                       designation, address, mobile, email_id)
            return s
        except Exception, e:
            return str(e)

    @staticmethod
    def create_user_settings_password_form():
        try:
            s = """
            <form action=\"save_user_settings_password.py\" method=\"get\" id=\"edit_password_form\" name=\"edit_password_form\">
                <div class=\"form-div\" style=\"margin-top:25px\">
                    <div class=\"form-body\">
                        <div class=\"row-elem\">
                            <label class=\"lbl lbl-big\" for=\"password\">Enter Old Password:</label>
                            <input type=\"password\" id=\"password\" name=\"password\" title=\"Please Enter your old Password.\">
                        </div>
                        <div class=\"row-elem\">
                            <label class=\"lbl lbl-big\" for=\"confirm_password_1\">Enter New Password:</label>
                            <input type=\"password\" id=\"confirm_password_1\" name=\"confirm_password_1\" title=\"Please Enter your new password. \">
                        </div>
                        <div class=\"row-elem\">
                            <label class=\"lbl lbl-big\" for=\"confirm_password_2\">Confirm New Password:</label>
                            <input type=\"password\" id=\"confirm_password_2\" name=\"confirm_password_2\" title=\"Please Confirm your new password. \">
                        </div>
                    </div>
                </div>
                <div class=\"form-div-footer\">
                    <button type=\"submit\" class=\"yo-small yo-button\"><span class=\"edit\">Save</span></button>
                    <button type=\"reset\" class=\"yo-small yo-button\" id=\"close_edit_password\"><span class=\"cancel\">Cancel</span></button>
                </div>
            </form>""" % ()
            return s

        except Exception, e:
            return str(e)
