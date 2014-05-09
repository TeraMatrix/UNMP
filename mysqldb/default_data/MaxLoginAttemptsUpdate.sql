/*
  Devloper: Grijesh Chauhan
  Date: 12-April-2013
  File: MySQL Query to UPDATE `user_login`
  
	Feature: 727
	User Management - Max Login Attempts
	
	Description: 		UPDATE with default values, to new coloumns added via `MaxLoginAttemptsAlter.sql`:
	------------    (1) failed_login_attempts = number of wrong sign in attempts = 0 bydefault
								  (2) failed_login_time 		= 0 initializes to 0000-00-00 00:00:00
								      + Python code will handle None (default values)
								      
  Note: Alter Query to Add these columns is written in MaxLoginAttemptsAlter.sql
*/


mysql> UPDATE `user_login` SET `failed_login_attempts`=0 , `failed_login_time` = 0;
