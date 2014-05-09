#!/bin/sh

######################################################
#
#	$1	$Temp/scripts	The path where scripts / conf files resides
#
######################################################

echo ""
echo "The UNMP installer is configuring FTP server.."
echo "" 

mv /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf.bak	
rm /etc/vsftpd/vsftpd.conf
cp ./vsftpd.conf /etc/vsftpd/

mv /etc/vsftpd/user_list /etc/vsftpd/user_list.bak
cp ./user_list /etc/vsftpd

mv /etc/vsftpd/chroot_list /etc/vsftpd/chroot_list.bak
cp ./chroot_list /etc/vsftpd

iptables -A INPUT -p tcp --dport 21 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 20 -j ACCEPT

mv /etc/sysconfig/iptables-config /etc/sysconfig/iptables-config.bak
rm /etc/sysconfig/iptables-config
cp ./iptables-config /etc/sysconfig/

service iptables save
service iptables restart

egrep "^unmpftp" /etc/passwd >/dev/null
if [ $? -eq 0 ]; then
    echo
else
    adduser unmpftp      
fi        

echo "unmpftp@123" | passwd --stdin "unmpftp"
mkdir -p /omd/unmpftp/unmpftp
chmod 777 -R /omd/unmpftp
chown unmpftp:unmpftp -R /omd/unmpftp
chcon -R -t public_content_rw_t /omd/unmpftp
setsebool -P ftp_home_dir 1
setsebool -P allow_ftpd_anon_write 1

service vsftpd restart

