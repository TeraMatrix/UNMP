
/*
  Devloper: Grijesh Chauhan
  Date: 12-March-2013
  File: MySQL Query to alter `user_login`

        Feature: 890
        User Management - Notifying User That They Entered Old Passwords

        if password is not correct but maches(==) to old password then
        user will get a message:
            "you password has been change,
            Please enter new password"
*/


ALTER TABLE `user_login` ADD `old_password` VARCHAR(60) AFTER password;

/*
        The old value of old_password initially(bydefault) is NULL

        after each password update query its value will be update to
        previous password. find in default_data directory
*/



/*
  Devloper: Grijesh Chauhan
  Date          :       14-March-2013
  File          :       MySQL Query to alter `user_login`

        Feature: 1060
        User Management - On Password Expiry Redirect User to Change Password Screen
*/
ALTER TABLE `user_login` ADD `change_password_date` TIMESTAMP ;

/*
        (1) First: In user_login a filed `change_password_date` will be set to
                   data and time on each password change.

*/

