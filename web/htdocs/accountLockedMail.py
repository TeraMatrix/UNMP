#! /usr/bin/python


#Author: Grijesh Chauhan
#Date: 10-April-2013
#Version: 0.1
#Organization: Codescape Consultants Pvt. Ltd.


from sendmail import sendMail
from accountLockedHTML import getHtmlMessage


def notifyAccountLock(
		sender_mail,
		sender_mail_password, 
		recipient_name,
		recipient_mail,
		username,
		admin_user_name,
		login_time,
		client_ip,
		max_login_attempts, 
		lock_duration,
		message_to
	):
	'''Send HTML mail: username and password 
	  ----------------------------------------
	(1) sender_mail: sender's gmail ID, Its a UNMP mail ID 
		type: String

	(2)	sender_mail_password: sender's email-password
		type: String

	(3) recipient_name: mail reciver's name 
		type: String

	(4) recipient_mail: 
		type: String

	(5) username: A valid UNMP login ID 
		Note: 'recipient_name and username can be diffrent(or same)'
		type: String

	Additional, Parameters for HTML

	(6) admin_user_name: UNMP System admin name
		type: String

	(7) login_time: 
		type: String

	(8) client_ip: IP of system from which login request arised

	(9) max_login_attempts: maximum fail login attempts configured in UNMP System
  		type: String

  	(10) lock_duration: Account lock time duration configured in UNMP System (in hours)
      	type: String  		
   
   	(11) message_to:** can be {"user", "admin"} for HTML use

  Note:-
	(i) getHtmlMessage(	name,
						username,
						)
		returns HTML message with username 
		
		type: both String

	(ii) sendMail(_...) 
		 uses smtp.gmail.com Mail Sever 
	'''
	
	subject = "UNMP Account Notification - Account locked"
	html = getHtmlMessage(
			recipient_name, 
			username,
			admin_user_name, 
			max_login_attempts, 
			lock_duration,
			login_time,
			client_ip,
			message_to
		)
	if sendMail(
		sender_mail, 
		sender_mail_password,  
		recipient_mail, 
		subject, 
		html):
		return True	#"Mail Successfuly sent!"
	return False	#"Mail Delivery Failure!"

