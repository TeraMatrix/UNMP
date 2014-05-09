#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 04-Nov-2011
@version: 0.1
@note: All Views That are use in License.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''


class License(object):
    @staticmethod
    def manage_license(company="", date="", return_dict={}):
        html_li = ['']
        html_li = ['\
        <div class="form-div">\
        <table class="tt-table" cellspacing="0" cellpadding="0" width="100%%">\
        <thead>\
            <tr>\
                <th class="cell-title" colspan="2">\
                    License Information\
                </th>\
            </tr>\
        </thead>\
        <tbody>\
            <tr>\
              <td class="cell-label">\
                Company Name\
              </td>\
              <td class="cell-info">\
		%s\
              </td>\
            </tr>\
            <tr>\
              <td class="cell-label">\
                Expires in\
              </td>\
              <td class="cell-info">\
		%s\
              </td>\
            </tr>\
        </tbody>\
        </table>\
        <table class="tt-table" cellspacing="0" cellpadding="0" width="100%%">\
        <thead>\
            <tr>\
                <th class="cell-title cell-title2">\
                    System Object\
                </th>\
                <th class="cell-title cell-title2">\
                     Allowed\
                </th>\
                <th class="cell-title cell-title2">\
                    Used\
                </th>\
                <th class="cell-title cell-title2">\
                    Remaining\
                </th>\
            </tr>\
        </thead>\
        <tbody>' % (company, date)]

        for item in return_dict:
            if len(return_dict[item]) > 1:
                mid_dict = return_dict[item]
                mid_list = mid_dict.pop('allow')
                html_li.append('<tr>\
                                  <td class="cell-label cell-label2" id="%s" style="cursor:pointer;">\
                                    <span class="nxt" style="height:16px;width:16px;display:block;float:left;">\
                                    </span>\
                                    <span style="display:block;float:left;margin:4px 10px;">\
                                        %s\
                                    </span>\
                              </td>\
                              <td class="cell-info">\
                        		    %s\
                              </td>\
                              <td class="cell-info cell-info1">\
                        		    %s\
                              </td>\
                              <td class="cell-info cell-info1">\
		                            %s\
                              </td>\
                            </tr>\
                    %s\
                    ' % (item, mid_list[0], mid_list[1], mid_list[2], mid_list[3], License.para_type(mid_dict, item))
                )
            else:
                mid_list = return_dict[item].get('allow')
                html_li.append('<tr>\
                                  <td class="cell-label cell-label2" style="cursor:pointer;">\
                                    <span class="" style="height:16px;width:16px;display:block;float:left;"></span>\
                                    <span style="display:block;float:left;margin:4px 10px;">%s</span>\
                                  </td>\
                                  <td class="cell-info">\
		                    %s\
                                  </td>\
                                  <td class="cell-info cell-info1">\
		                    %s\
                                  </td>\
                                  <td class="cell-info cell-info1">\
		                    %s\
                                  </td>\
                                </tr>' % (mid_list[0], mid_list[1], mid_list[2], mid_list[3])
                )
        html_li.append('</tbody> </table> </div>\
                            <div class="form-div-footer">\
                                <form action="license_upload.py" enctype=\"multipart/form-data\" method=\"post\">\
                                 <label class="lbl" style="margin-top:15px;">License File</label>\
                                 <input type="file" id="file_uploader" name="file_uploader" />\
                                 <button class="yo-button yo-small" type="file" id="button_uploader" name="button_uploader"><span class="upload">Upload</span></button>\
                                </form>\
                            </div>'
        )
        return ''.join(html_li)

    @staticmethod
    def para_type(di={}, name=''):
        inter_list = ['']
        try:
            html_view = '\
                <tr class="%s_p">' % (name) + '\
                <td class="cell-info cell-info1 cell-info2 cell-info3">\
	    	<span style="display:block;float:left;margin:4px 0px 4px 35px;">%s</span>\
                  </td>\
                  <td class="cell-info cell-info1 cell-info2 cell-info3">\
	    	%s\
                  </td>\
                  <td class="cell-info cell-info1 cell-info2 cell-info3">\
	    	%s\
                  </td>\
                  <td class="cell-info cell-info1 cell-info2 cell-info3">\
	    	%s\
                  </td>\
                </tr>'

            for k, li in di.items():
                inter_list.append(html_view % tuple(li))
        except Exception, e:
            # import traceback
            # with open('/omd/sites/UNMP/share/check_mk/web/htdocs/lic_problem','w') as f:
            # f.write(traceback.format_exc()+'\n\n'+html_view+'\n\n'+str(di))
            inter_list = ['']

        return ''.join(inter_list)

    @staticmethod
    def para_type2(di={}, name=''):
        inter_list = ['']
        try:
            html_view = '\
                <tr class="%s_p">' % (name) + '\
                <td class="cell-info cell-info1 cell-info2 cell-info3">\
	    	<span style="display:block;float:left;margin:4px 0px 4px 35px;%s">%s</span>\
                  </td>\
                  <td class="cell-info cell-info1 cell-info2 cell-info3">\
	    	%s\
                  </td>\
                  <td class="cell-info cell-info1 cell-info2 cell-info3">\
	    	%s\
                  </td>\
                  <td class="cell-info cell-info1 cell-info2 cell-info3">\
	    	%s\
                  </td>\
                </tr>'

            for k, li in di.items():
                inter_list.append(html_view % tuple(li))
        except Exception, e:
            # import traceback
            # with open('/omd/sites/UNMP/share/check_mk/web/htdocs/lic_problem','w') as f:
            # f.write(traceback.format_exc()+'\n\n'+html_view+'\n\n'+str(di))
            inter_list = ['']

        return ''.join(inter_list)

    @staticmethod
    def license_toast_msg(msg_type, msg_text):
        type = {"success": "showSuccessToast", "error":
            "showErrorToast", "warning": "showWarningToast"}
        msg = "<script type=\"text/javascript\">\
                $().toastmessage('%s', '%s');\
            </script>" % (type[msg_type], msg_text)
        return msg

    # @staticmethod
    # def page_tip_license():
    #     import defaults
    #     f = open(defaults.web_dir + "/htdocs/locale/page_tip_license.html", "r")
    #     html_view = f.read()
    #     f.close()
    #     return str(html_view)

    @staticmethod
    def invalid_license(return_dict={}):
        html_li = ['\
        <div> <span> Warning: Please review your new license details&nbsp;</span>\
        <table class="tt-table" cellspacing="0" cellpadding="0" width="100%%">\
        <thead>\
            <tr>\
                <th class="cell-title cell-title2">\
                    System Object\
                </th>\
                <th class="cell-title cell-title2">\
                     Allowed\
                </th>\
                <th class="cell-title cell-title2">\
                    Used\
                </th>\
                <th class="cell-title cell-title2">\
                    Remaining\
                </th>\
            </tr>\
        </thead>\
        <tbody>']

        for item in return_dict:
            if len(return_dict[item]) > 1:
                mid_dict = return_dict[item]
                mid_list = mid_dict.pop('allow')
                html_li.append('<tr>\
                                  <td class="cell-label cell-label2" id="%s" style="cursor:pointer;%s">\
                                    <span class="nxt" style="height:16px;width:16px;display:block;float:left;">\
                                    </span>\
                                    <span style="display:block;float:left;margin:4px 10px;">\
                                        %s\
                                    </span>\
                              </td>\
                              <td class="cell-info">\
                        		    %s\
                              </td>\
                              <td class="cell-info cell-info1">\
                        		    %s\
                              </td>\
                              <td class="cell-info cell-info1">\
		                            %s\
                              </td>\
                            </tr>\
                    %s\
                    ' % (item, mid_list[0], mid_list[1], mid_list[2], mid_list[3], mid_list[4],
                         License.para_type2(mid_dict, item))
                )
            else:
                mid_list = return_dict[item].get('allow')
                html_li.append('<tr>\
                                  <td class="cell-label cell-label2" style="cursor:pointer;%s">\
                                    <span class="" style="height:16px;width:16px;display:block;float:left;"></span>\
                                    <span style="display:block;float:left;margin:4px 10px;">%s</span>\
                                  </td>\
                                  <td class="cell-info">\
		                    %s\
                                  </td>\
                                  <td class="cell-info cell-info1">\
		                    %s\
                                  </td>\
                                  <td class="cell-info cell-info1">\
		                    %s\
                                  </td>\
                                </tr>' % (mid_list[0], mid_list[1], mid_list[2], mid_list[3], mid_list[4])
                )
        html_li.append(
            '</tbody> </table> <span> Note: You can not exceed your allowed limit&nbsp;&nbsp;[Check Red Font Titles]</span></div>')
        return ''.join(html_li)

    @staticmethod
    def license_colorbox(msg_type, msg_text, html_str):
        # toast_type = {"success":"showSuccessToast","error":"showErrorToast","warning":"showWarningToast"}
        # msg = "<script
        # type=\"text/javascript\">$().colorbox({html:'<p>Hello</p>'});</script>"
        msg = """<style type="text/css">
    .toast-container {
        width: 520px;
        z-index: 9999;
    }
    .toast-item p {
        text-align: left;
        margin-left: 0px;
    }
    .toast-position-top-center {
        position: fixed;
        top: 50px;
        left: 50%%;
        margin-left: -140px;
    }
    .toast-item-image {
        width:32px;
        height: 32px;
        margin-left: 10px;
        margin-right: 10px;
        margin-top: -10px;
        float:left;
    }
    .toast-item {
	    height: auto;
	    background: #333;
        opacity: 1.0;
	    -moz-border-radius: 10px;
	    -webkit-border-radius: 10px;
	    color: #eee;
	    padding-top: 20px;
	    padding-bottom: 20px;
	    padding-left: 6px;
	    padding-right: 6px;
	    /*font-family: lucida Grande;*/
	    font-size: 11px;
	    font-weight:bold;
	    border: 2px solid #999;
	    display: block;
	    position: relative;
	    margin: 0 0 12px 0;
	    overflow:hidden;
    }
</style>\
        \<script type=\"text/javascript\">\
                $().toastmessage('showToast', {
                    text     : '%s',
                    sticky   : true,
                    type     : '%s',
                    position :  'top-center'
                });
            </script>""" % (html_str, msg_type)
        return msg
