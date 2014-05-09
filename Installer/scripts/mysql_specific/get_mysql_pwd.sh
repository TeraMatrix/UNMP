#!/bin/bash

# script to get random password set on mysql 5.6 and reset the password

file=~/.mysql_secret
if [ -f $file ]
then
	s=$(<$file)
	arrIN=(${s//:/ })
	mysqlpwd=${arrIN[${#arrIN[@]}-1]}
    query="SET PASSWORD FOR 'root'@'localhost' = PASSWORD('root');"
mysqladmin -uroot -p$mysqlpwd password root
echo " password reset $?"

else
	echo "mysql random file not exits : $file"
	exit 1
fi

