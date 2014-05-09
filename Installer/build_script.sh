<<<<<<< .working
#!/bin/sh

cd ..
basedir="$(pwd)"
echo "$(pwd)"
cd Installer/InstallJammer

echo ""
echo "Building the UNMP Installer.."
echo ""

./installjammer -DVersion $1 -DBaseDir $basedir --output-dir ../linux/el5/ --platform Linux-x86 --verbose $3 --build $basedir/Installer/$2

./installjammer -DVersion $1 -DBaseDir $basedir --output-dir ../linux/el5/ --platform Linux-x86_64 --verbose $3 --build $basedir/Installer/$2
=======
#!/bin/sh

###########################################
# $1 = Linux-x86 / Linux-x86_64
# $2 = el5 / el6
# $3 = Version Number
# $4 = MPI File Name / Path
# $5 = --build-for-release [Optional]
# $basedir = Base Directory for Installer
###########################################

rm -rf temp
mkdir temp
mkdir temp/ThirdParty_DB
chmod -R 777 temp

unzip InstallJammer.zip -d temp
chmod -R 777 temp/InstallJammer

if [ "$1" == "Linux-x86_64" ] 
then
	svn export --force ../../ThirdParty/64-bit temp/ThirdParty

	cp -f temp/ThirdParty/MySQL-client-community-5.1.60-1.rhel5.x86_64.rpm temp/ThirdParty_DB
	cp -f temp/ThirdParty/MySQL-community-debuginfo-5.1.60-1.rhel5.x86_64.rpm temp/ThirdParty_DB
	cp -f temp/ThirdParty/MySQL-devel-community-5.1.60-1.rhel5.x86_64.rpm temp/ThirdParty_DB
	cp -f temp/ThirdParty/MySQL-server-community-5.1.60-1.rhel5.x86_64.rpm temp/ThirdParty_DB
	cp -f temp/ThirdParty/MySQL-shared-compat-5.1.60-1.rhel5.x86_64.rpm temp/ThirdParty_DB
	cp -f temp/ThirdParty/postgresql-libs-8.1.18-2.el5_4.1.x86_64.rpm temp/ThirdParty_DB

else
	svn export --force ../../ThirdParty/32-bit temp/ThirdParty

	cp -f temp/ThirdParty/MySQL-client-community-5.1.60-1.rhel5.i386.rpm temp/ThirdParty_DB
	cp -f temp/ThirdParty/MySQL-community-debuginfo-5.1.60-1.rhel5.i386.rpm temp/ThirdParty_DB
	cp -f temp/ThirdParty/MySQL-devel-community-5.1.60-1.rhel5.i386.rpm temp/ThirdParty_DB
	cp -f temp/ThirdParty/MySQL-server-community-5.1.60-1.rhel5.i386.rpm temp/ThirdParty_DB
	cp -f temp/ThirdParty/MySQL-shared-compat-5.1.60-1.rhel5.i386.rpm temp/ThirdParty_DB
	cp -f temp/ThirdParty/postgresql-libs-8.1.11-1.el5_1.1.i386.rpm temp/ThirdParty_DB
fi

svn export --force scripts temp/scripts
svn export --force ../plugins temp/plugins
svn export --force ../config temp/config
svn export --force ../daemon temp/daemon
svn export --force ../initscripts temp/initscripts
svn export --force ../misc temp/misc
svn export --force ../mysqldb temp/mysqldb
svn export --force ../web temp/web

cd temp
chmod -R 777 *

#Removing error-prone files before zipping installer contents
#apache.conf
#unmp-nbi*
#daemon/lib/*
#daemon/nbi_backup
rm -rf config/skel/etc/apache/apache.conf
rm -rf initscripts/unmp-nbi*
rm -rf daemon/lib/*
rm -rf daemon/nbi_backup

zip -r scripts scripts
#tar zcvf scripts.tar scripts
tar zcvf plugins.tar plugins
cd config
tar zcvf config.tar *
mv config.tar ../
cd ..
tar zcvf daemon.tar daemon
tar zcvf initscripts.tar initscripts
cd misc
tar zcvf misc.tar *
mv misc.tar ../
cd ..
cd mysqldb
tar zcvf mysqldb.tar *
mv mysqldb.tar ../
cd ..
tar zcvf web.tar web
zip -r ThirdParty ThirdParty
#tar zcvf ThirdParty.tar ThirdParty
zip -r ThirdParty_DB ThirdParty_DB
#tar zcvf ThirdParty_DB.tar ThirdParty_DB

rm -rf scripts
rm -rf plugins
rm -rf config
rm -rf daemon
rm -rf initscripts
rm -rf misc
rm -rf mysqldb
rm -rf web
rm -rf ThirdParty
rm -rf ThirdParty_DB

chmod -R 777 *
basedir=$(pwd)
echo "Base Directory - $basedir"
echo ""
echo "Building the UNMP Installer.."
echo ""
./InstallJammer/installjammer -DVersion $3 -DBaseDir $basedir --output-dir ../linux/$2/ --platform $1 --verbose $5 --build $basedir/../$4

cd ..
chmod 777 linux/$2/*
rm -rf temp

echo "Installer Build Completed Successfully.."
echo ""
>>>>>>> .merge-right.r125
