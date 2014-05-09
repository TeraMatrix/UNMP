#! /usr/bin/python

#Author: Grijesh Chauhan
#Date: 18-March-2013
#Version: 0.1
#Organization: Codescape Consultants Pvt. Ltd.

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail(
		sender_mail, 
		sender_mail_password, 
		recipient_mail,
		subject,
		html,
		text = "Hi!"
	):
	'''Send HTML/Text mail: 
	  ----------------------
	(1) sender_mail: sender's gmail ID  
			type: String 
	
	(2) sender_mail_password: sender's email-password
			type: String

	(3) recipient_mail: seciver's email ID
			type: String

	(4)	subject: a subject to email message 
			type: String

	(5) html: part of message to be send in HTML
			type: String

	(6) text: part of message to be send in Text
			type: String, optional argument 

	Note:         
	sendMail() sends mail via Googlemail/Gmail SMTP Server
	- smtp.gmail.com
	- StartTLS Port 587
	'''
	try:
		# STEP-1: Create message container - the correct MIME type is multipart/alternative.
		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From'] = sender_mail
		msg['To'] = recipient_mail

		# STEP-2: Create the body of the message (a plain-text and an HTML version).
		text = "Hi!"
		# taken from argument 

		# STEP-3: Record the MIME types of both parts - text/plain and text/html.
		part1 = MIMEText(text, 'plain')
		part2 = MIMEText(html, 'html')

		# STEP-4:
		# Attach parts into message container.
		# According to RFC 2046, the last part of a multipart message, in this case
		# the HTML message, is best and preferred.
		msg.attach(part1)
		msg.attach(part2)

		# STEP-5:
		# Send the message via local SMTP server.
		s = smtplib.SMTP('smtp.gmail.com', 587)

		# STEP-6,7,8
		s.ehlo()
		s.starttls()
		s.ehlo()

		# STEP- get login first 
		s.login(sender_mail, sender_mail_password) 

		# STEP: Send mail finally
		# sendmail function takes 3 arguments: sender's address, recipient's address
		# and message to send - here it is sent as one string.
		s.sendmail(sender_mail, recipient_mail, msg.as_string())
		s.quit()
		return True;
	except:
		return False; 
