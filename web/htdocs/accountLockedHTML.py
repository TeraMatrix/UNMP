#! /usr/bin/python

#Author: Grijesh Chauhan
#Date: 10-April-2013
#Version: 0.1
#Organization: Codescape Consultants Pvt. Ltd.


def getHtmlMessage(
        name,
        username, 
        admin_user_name,
        max_login_attempts, 
        lock_duration,
        login_time,
        client_ip,
        message_to
    ):
    '''Create A HTML page for mail 
      -----------------------------
    (1) name: User's Name 
        type: String
    (2) username: NMS username is login ID
        type: String
    (3) max_login_attempts: maximum fail login attempts configured in UNMP System
        type: String
    (4) lock_duration: Account lock time duration configured in UNMP System (in hours)
        type: String
    '''
    if(message_to == "user"):
        htmlMessage = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
<html>
<body>
	<div style="background-color: #f4f4f4; font-size: 16px; padding-top: 20px; padding-right: 20px; padding-left: 20px; padding-bottom: 20px; font-family: Trebuchet MS,Tahoma,Verdana,Arial,Helvetica,sans-serif;">
		<div>
			<div style="background-color: #1d75d6; font-size: 20px; min-height: 50px; color: #fff; line-height: 50px; padding-left: 15px; margin-bottom: 0px;">
			UNMP
			</div>
			<div style="padding-right: 15px; padding-top: 15px; padding-left: 15px; padding-bottom: 15px; background-color: #fff;">
                <table style="font-family: 'Helvetica Neue',Arial,sans-serif; font-size: 12px; line-height: 1.4; color: #212f40; width: 600px; border-left-style: solid; border-right-width: 1px; border-top-width: 1px; border-bottom-width: 1px; border-bottom-style: solid; border-right-style: solid; border-top-style: solid; border-left-color: #ced7e0; border-top-color: #ced7e0; border-right-color: #ced7e0; border-bottom-color: #ced7e0; border-left-width: 1px; margin-bottom: 0; margin-top: 0; margin-right: 0; margin-left: 0; padding-bottom: 0; padding-top: 0; padding-right: 0; padding-left: 0;"
                border="0" cellspacing="0" cellpadding="0">
                	<tbody> 
                        <tr style="text-align: left; vertical-align: baseline;" align="left">
                            <td style="padding-bottom: 10px; padding-right: 10px; padding-top: 10px; padding-left: 20px; font-size: 13px;  background-color: #FAFAFA; color: #E0D0D;"
                            bgcolor="#FAFAFA">
                            	<span style="font-size: 12px;">
                            		Hi {0},
                            	</span>
                            <br><br>
                            Your UNMP account '{1}' is temporarily locked.
                            </td>
                        </tr>
                        <tr style="text-align: left; vertical-align: baseline;" align="left">
                            <td style="padding-left: 20px; padding-top: 1px; padding-bottom: 0px; padding-right: 20px; background-color: #1d75d6;"
                            bgcolor="#FAFAFA">
                            </td>
                        </tr>							
                        <tr style="text-align: left; vertical-align: baseline;" align="left">
                            <td style="padding-bottom: 0; padding-top: 0; padding-right: 10px; padding-left: 20px;">

                        <table style="font-family: 'Helvetica Neue',Arial,sans-serif; font-size: 12px; line-height: 1.4; color: #212f40; width: 590px; border-bottom-width: 1px; border-bottom-color: #e5e5e5; border-bottom-style: solid;"
                        border="0" cellspacing="0" cellpadding="0">
                            <tbody>
                                <tr style="text-align: left; vertical-align: baseline;" align="left">
                                    <td style="padding-left: 0px; padding-right: 0px; padding-top: 10px; width: 90px; color: #E0D0D; font-size: 12px;  padding-bottom: 5px; vertical-align: top;"
                                    valign="top">
                                    Your UNMP account has been automatically locked by the UNMP Security System because of more than {3} or more continuous failed sign in attempts. 
                                    <br>
                                    The System admin have been notified of the same, Please contact the system administrator Mr. {2} for assistance.The account will be reactivated after {4} hours. 
                                    <br>
                                    Try again after {4} hours.     
                                    </td>
                                </tr>																
                            </tbody>
                        </table>

                       <table style="font-family: 'Helvetica Neue',Arial,sans-serif; font-size: 12px; line-height: 1.4; color: #212f40; width: 590px;"
                        border="0" cellspacing="0" cellpadding="0">
                            <tbody>
                                <tr style="min-height: 7px; text-align: left; vertical-align: baseline;"
                                align="left">
                                    <td style="padding-top: 0; padding-right: 0; padding-bottom: 0; padding-left: 0;">
                                    </td>
                                    <td style="padding-top: 0; padding-right: 0; padding-bottom: 0; padding-left: 0;">
                                    </td>
                                </tr>
                                <tr style="text-align: left; vertical-align: baseline;" align="left">
                                	<td style="padding-left: 0px; padding-right: 0px; padding-top: 10px; width: 90px; color: #999999; font-size: 11px; font-weight: bold; padding-bottom: 5px; vertical-align: top;"
                                    valign="top">
                                        UserID:
                                    </td>
                                    <td style="padding-top: 9px; padding-right: 0px; padding-bottom: 5px; padding-left: 0px;">
                                        <span style="font-weight: bold; white-space: nowrap;">
                                            {1}
                                        </span>
                                    </td>
                                </tr>
                                <tr style="text-align: left; vertical-align: baseline;" align="left">
                                	<td style="padding-left: 0px; padding-right: 0px;  width: 90px; color: #999999; font-size: 11px; font-weight: bold; padding-bottom: 0px; vertical-align: top;"
                                    valign="top">
                                        Time:
                                    </td>
                                    <td style=" padding-right: 0px; padding-bottom: 9px; padding-left: 0px;">
                                        <span style="font-weight: bold; white-space: nowrap;">
                                            {5}
                                        </span>
                                    </td>
                                </tr>
                                <tr style="text-align: left; vertical-align: baseline;" align="left">
                                    <td style="padding-left: 0px; padding-right: 0px;  width: 90px; color: #999999; font-size: 11px; font-weight: bold; padding-bottom: 0px; vertical-align: top;"
                                    valign="top">
                                        IP:
                                    </td>
                                    <td style=" padding-right: 0px; padding-bottom: 9px; padding-left: 0px;">
                                        <span style="font-weight: bold; white-space: nowrap;">
                                            {6}
                                        </span>
                                    </td>
                                </tr>
                            </tbody>  
                		</table>
                	</tbody>
                </table>
                <div style="background-color: #fff; padding-top: 15px; padding-right: 15px; padding-left: 15px; padding-bottom: 15px; font-family: Trebuchet MS,Tahoma,Verdana,Arial,Helvetica,sans-serif;">
                    Regards,
                    <br>
                    Team UNMP
                </div>
                
                <div>
                	<table>
                		<td style="border-right:none;color:#999999;font-size:11px;border-bottom:none;font-family:'lucida grande',tahoma,verdana,arial,sans-serif;border:none;border-top:none;padding:30px 20px;border-left:none">
                    You have received this mail because you are a user of UNMP system. 
                    Please click here 
                    <a href="http://localhost/UNMP/check_mk/" style="color:#3b5998;text-decoration:none" target="_blank">
                    to access the UNMP interface                		
		        				</a> 
		        				<br>
		        				This email was sent from an unmonitored account. Do not reply directly to this email.
                		</td>
                	</table>	
                </div>
            </div>
		</div>
	</div>
</body>
</html>
""".format(
        name,
        username, 
        admin_user_name,
        max_login_attempts, 
        lock_duration,
        login_time,
        client_ip
    )

    if(message_to == "admin"):
        htmlMessage = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
<html>
<body>
    <div style="background-color: #f4f4f4; font-size: 16px; padding-top: 20px; padding-right: 20px; padding-left: 20px; padding-bottom: 20px; font-family: Trebuchet MS,Tahoma,Verdana,Arial,Helvetica,sans-serif;">
        <div>
            <div style="background-color: #1d75d6; font-size: 20px; min-height: 50px; color: #fff; line-height: 50px; padding-left: 15px; margin-bottom: 0px;">
            UNMP
            </div>
            <div style="padding-right: 15px; padding-top: 15px; padding-left: 15px; padding-bottom: 15px; background-color: #fff;">
                <table style="font-family: 'Helvetica Neue',Arial,sans-serif; font-size: 12px; line-height: 1.4; color: #212f40; width: 600px; border-left-style: solid; border-right-width: 1px; border-top-width: 1px; border-bottom-width: 1px; border-bottom-style: solid; border-right-style: solid; border-top-style: solid; border-left-color: #ced7e0; border-top-color: #ced7e0; border-right-color: #ced7e0; border-bottom-color: #ced7e0; border-left-width: 1px; margin-bottom: 0; margin-top: 0; margin-right: 0; margin-left: 0; padding-bottom: 0; padding-top: 0; padding-right: 0; padding-left: 0;"
                border="0" cellspacing="0" cellpadding="0">
                    <tbody> 
                        <tr style="text-align: left; vertical-align: baseline;" align="left">
                            <td style="padding-bottom: 10px; padding-right: 10px; padding-top: 10px; padding-left: 20px; font-size: 13px;  background-color: #FAFAFA; color: #E0D0D;"
                            bgcolor="#FAFAFA">
                                <span style="font-size: 12px;">
                                    Hi {0},
                                </span>
                            <br><br>
                            UNMP user account '{1}' is temporarily locked.
                            </td>
                        </tr>
                        <tr style="text-align: left; vertical-align: baseline;" align="left">
                            <td style="padding-left: 20px; padding-top: 1px; padding-bottom: 0px; padding-right: 20px; background-color: #1d75d6;"
                            bgcolor="#FAFAFA">
                            </td>
                        </tr>                           
                        <tr style="text-align: left; vertical-align: baseline;" align="left">
                            <td style="padding-bottom: 0; padding-top: 0; padding-right: 10px; padding-left: 20px;">

                        <table style="font-family: 'Helvetica Neue',Arial,sans-serif; font-size: 12px; line-height: 1.4; color: #212f40; width: 590px; border-bottom-width: 1px; border-bottom-color: #e5e5e5; border-bottom-style: solid;"
                        border="0" cellspacing="0" cellpadding="0">
                            <tbody>
                                <tr style="text-align: left; vertical-align: baseline;" align="left">
                                    <td style="padding-left: 0px; padding-right: 0px; padding-top: 10px; width: 90px; color: #E0D0D; font-size: 12px;  padding-bottom: 5px; vertical-align: top;"
                                    valign="top">
                                    This is to be inform you that the UNMP account of user '{2}' has been temporarily locked by the UNMP Security System, because of {3} or more continuous failed sign in attempts. The account will be reactivated after {4} hours. 
                                    <br>
                                    You are being notified because you are system administrator. 
                                    </td>
                                </tr>                                                               
                            </tbody>
                        </table>

                       <table style="font-family: 'Helvetica Neue',Arial,sans-serif; font-size: 12px; line-height: 1.4; color: #212f40; width: 590px;"
                        border="0" cellspacing="0" cellpadding="0">
                            <tbody>
                                <tr style="min-height: 7px; text-align: left; vertical-align: baseline;"
                                align="left">
                                    <td style="padding-top: 0; padding-right: 0; padding-bottom: 0; padding-left: 0;">
                                    </td>
                                    <td style="padding-top: 0; padding-right: 0; padding-bottom: 0; padding-left: 0;">
                                    </td>
                                </tr>
                                <tr style="text-align: left; vertical-align: baseline;" align="left">
                                    <td style="padding-left: 0px; padding-right: 0px; padding-top: 10px; width: 90px; color: #999999; font-size: 11px; font-weight: bold; padding-bottom: 5px; vertical-align: top;"
                                    valign="top">
                                        Name:
                                    </td>
                                    <td style="padding-top: 9px; padding-right: 0px; padding-bottom: 5px; padding-left: 0px;">
                                        <span style="font-weight: bold; white-space: nowrap;">
                                            {2}
                                        </span>
                                    </td>
                                </tr>                                
                                <tr style="text-align: left; vertical-align: baseline;" align="left">
                                    <td style="padding-left: 0px; padding-right: 0px; padding-top: 10px; width: 90px; color: #999999; font-size: 11px; font-weight: bold; padding-bottom: 5px; vertical-align: top;"
                                    valign="top">
                                        UserID:
                                    </td>
                                    <td style="padding-top: 9px; padding-right: 0px; padding-bottom: 5px; padding-left: 0px;">
                                        <span style="font-weight: bold; white-space: nowrap;">
                                            {1}
                                        </span>
                                    </td>
                                </tr>
                                <tr style="text-align: left; vertical-align: baseline;" align="left">
                                    <td style="padding-left: 0px; padding-right: 0px;  width: 90px; color: #999999; font-size: 11px; font-weight: bold; padding-bottom: 0px; vertical-align: top;"
                                    valign="top">
                                        Time:
                                    </td>
                                    <td style=" padding-right: 0px; padding-bottom: 9px; padding-left: 0px;">
                                        <span style="font-weight: bold; white-space: nowrap;">
                                            {5}
                                        </span>
                                    </td>
                                </tr>
                                <tr style="text-align: left; vertical-align: baseline;" align="left">
                                    <td style="padding-left: 0px; padding-right: 0px;  width: 90px; color: #999999; font-size: 11px; font-weight: bold; padding-bottom: 0px; vertical-align: top;"
                                    valign="top">
                                        IP:
                                    </td>
                                    <td style=" padding-right: 0px; padding-bottom: 9px; padding-left: 0px;">
                                        <span style="font-weight: bold; white-space: nowrap;">
                                            {6}
                                        </span>
                                    </td>
                                </tr>
                            </tbody>  
                        </table>
                    </tbody>
                </table>
                <div style="background-color: #fff; padding-top: 15px; padding-right: 15px; padding-left: 15px; padding-bottom: 15px; font-family: Trebuchet MS,Tahoma,Verdana,Arial,Helvetica,sans-serif;">
                    Regards,
                    <br>
                    Team UNMP
                </div>
                
                <div>
                    <table>
                        <td style="border-right:none;color:#999999;font-size:11px;border-bottom:none;font-family:'lucida grande',tahoma,verdana,arial,sans-serif;border:none;border-top:none;padding:30px 20px;border-left:none">
                    You have received this mail because you are a user of UNMP system. 
                    Please click here 
                    <a href="http://localhost/UNMP/check_mk/" style="color:#3b5998;text-decoration:none" target="_blank">
                    to access the UNMP interface                        
                                </a> 
                                <br>
                                This email was sent from an unmonitored account. Do not reply directly to this email.
                        </td>
                    </table>    
                </div>
            </div>
        </div>
    </div>
</body>
</html>
""".format(
        name,
        username, 
        admin_user_name,
        max_login_attempts, 
        lock_duration,
        login_time,
        client_ip
    )

    return htmlMessage
