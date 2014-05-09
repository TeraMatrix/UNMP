

/*This change in DB accroding to Bug #889
  :When a user will be deleted his/her login informations are also deleted.
  (1) Added an index on user_login(user_name)
  (2) Added FK FK-table: login_info & PK-table: user_login
  Devloper: Grijesh Chauhan
*/
CREATE INDEX name_index ON `user_login` (`user_name`);

ALTER TABLE `login_info` ADD CONSTRAINT FK_login_info_to_user_login FOREIGN KEY (`user_name`) REFERENCES `user_login` (`user_name`)  ON DELETE CASCADE ON UPDATE CASCADE;


/*To implement Feture #688 "Password change Mandatory at first login" A filed `is_first_login` in `login_info` is added
 Grijesh
*/
ALTER TABLE `login_info` ADD COLUMN `is_first_login` TINYINT DEFAULT 1;


/* For session management : rgautam*/
ALTER TABLE  `login_info` ADD  `last_accessed_time` DATETIME NOT NULL;
