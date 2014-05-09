/*
  Devloper: Grijesh Chauhan
  Date		:	14-March-2013
  File		:	MySQL Query to alter `user_login`
  
	Feature: 1060 
	User Management - On Password Expiry Redirect User to Change Password Screen
*/

UPDATE `user_login` SET `change_password_date` = CURRENT_TIMESTAMP;


/*
	(1) A new coloumn added `change_password_date` by ALTER command
	(2) UPDATE `change_password_date` for all existing users = CURRENT_TIMESTAMP 
	(3) First: In user_login a filed `change_password_date` will be set to 
	           data and time on each password change.
*/
