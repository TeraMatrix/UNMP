#!/bin/sh

######################################################
#
#	$1	Path where daemon programs resides	/opt/omd/daemon/scripts/
#	$2	Path where daemon programs resides	/opt/omd/daemon/cronfiles/
#
######################################################

# Registers job as a daemon process and starts them

echo ""
echo "Registering crontab entries and daemons.."
echo ""

sh ./pylink.sh

cd $1

#tmp=03456

for i in *
do
if [ "$i" == "unmp-all" ]; then
    rm -rf /etc/init.d/$i
    cp "`pwd`/$i" /etc/init.d/
    chmod 777 /etc/init.d/$i
else    
    rm -rf /etc/init.d/$i
    cp "`pwd`/$i" /etc/init.d/
    chmod 777 /etc/init.d/$i
    #ln -s /etc/init.d/$i /etc/rc.d/init.d/
    chkconfig --add $i
    chkconfig --level 03456 $i on
    #tmp=`expr ${tmp} + 1`
    #echo "Daemon $i has been registered with level $tmp.."
    service $i restart
fi    
done
	
# Adds crontab entry

cd $2
for i in *
do
crontab -u root $i
echo "Crontab entry for $i has been configured.."
done

