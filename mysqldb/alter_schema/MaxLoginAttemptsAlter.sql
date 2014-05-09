/*
  Devloper: Grijesh Chauhan
  Date: 04-April-2013
  File: MySQL Query to alter `user_login`
  
	Feature: 727
	User Management - Max Login Attempts
	
	Description: 		Adding to new coloumns:
	------------    (1) failed_login_attempts = How many wrong passwords user can enter before account locks
								  (2) failed_login_time 		= last time user entered a wrong password
								  
  Note: Update query for pre-existing rows is written in MaxLoginAttemptsUpdate.sql
*/

ALTER TABLE `user_login` ADD COLUMN failed_login_attempts tinyint(4) DEFAULT 0, ADD COLUMN failed_login_time datetime;
