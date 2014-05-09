#!/bin/ksh

###########################################
# $1 = Linux-x86 / Linux-x86_64
# $2 = el5 / el6
# $3 = Version Number
# $4 = MPI File Name / Path
# $5 = --build-for-release [Optional]
# $basedir = Base Directory for Installer
###########################################

export toolname="`basename $0`"

export usage="${toolname} <Linux-x86|Linux-x86_64> <el5|el6> <Build Revision> UNMP_Linux.mpi [--build-for-release]"

if [ $# -lt 4 ]; then
	echo "$toolname:Error:!Wrong invocation!"
	echo "$usage"
	exit 1
fi

report_error()
{
export STEP=$1
export File=$2
export W_D=$3
case $STEP in
1) export opr="Copying";;
2) export opr="Extracting";;
3) export opr="Compressing";;
4) export opr="Removing";;
esac
if [ $# -eq 3 ]; then
	echo "${toolname}:Error:Error in ${opr} ${File_name} in ${W_D} directory! Please Check !!"
else
	echo "${toolname}:Error:Error in ${opr} ${File_name}! Please Check !!"
fi
exit 1
}

export ThirdParty_64_bit_List="MySQL-client-community-5.1.60-1.rhel5.x86_64.rpm MySQL-community-debuginfo-5.1.60-1.rhel5.x86_64.rpm MySQL-devel-community-5.1.60-1.rhel5.x86_64.rpm  MySQL-server-community-5.1.60-1.rhel5.x86_64.rpm MySQL-shared-compat-5.1.60-1.rhel5.x86_64.rpm postgresql-libs-8.1.18-2.el5_4.1.x86_64.rpm"

export ThirdParty_32_bit_List="MySQL-client-community-5.1.60-1.rhel5.i386.rpm MySQL-community-debuginfo-5.1.60-1.rhel5.i386.rpm MySQL-devel-community-5.1.60-1.rhel5.i386.rpm MySQL-server-community-5.1.60-1.rhel5.i386.rpm MySQL-shared-compat-5.1.60-1.rhel5.i386.rpm postgresql-libs-8.1.11-1.el5_1.1.i386.rpm"

export Target=$1

export CWD=${PWD}
cd ${CWD}

export WRK_DIR=${CWD}/WRK_DIR
if [ -d ${WRK_DIR} ]; then
	rm -fr ${WRK_DIR}
fi

mkdir -p ${WRK_DIR}/ThirdParty_DB

echo "${toolname}:msg:Extracting InstallJammer.zip"
unzip -q InstallJammer.zip -d ${WRK_DIR} || report_error 2 InstallJammer.zip ${WRK_DIR}

if [ "${Target}" = "Linux-x86_64" ]; then

	echo "${toolname}:msg:Copying 64-Bit Third Party RPMs"
	for file_name in  ${ThirdParty_64_bit_List}
	do
		cp -f ${CWD}/../../ThirdParty/64-bit/${file_name} ${WRK_DIR}/ThirdParty_DB || report_error 1 ${file_name} ${WRK_DIR}/ThirdParty_DB
	done
else
	echo "${toolname}:msg:Copying 32-Bit Third Party RPMs"
	for file_name in ${ThirdParty_32_bit_List}
	do
		cp -f ${CWD}/../../ThirdParty/32-bit/${file_name} ${WRK_DIR}/ThirdParty_DB || report_error 1 ${file_name} ${WRK_DIR}/ThirdParty_DB
	done 
fi 

echo "${toolname}:msg:Removing extra folders/files "
rm -rf ${CWD}/../config/skel/etc/apache || report_error 4 ${CWD}/../config/skel/etc/apache
rm -fr ${CWD}/../initscripts/unmp-nbi*  || report_error 4 ${CWD}/../initscripts/unmp-nbi* 
rm -fr ${CWD}/../daemon/lib             || report_error 4 ${CWD}/../daemon/lib
rm -fr ${CWD}/../daemon/nbi_backup      || report_error 4 ${CWD}/../daemon/nbi_backup

echo "${toolname}:msg:Compressing scripts folder "
zip -r -q ${WRK_DIR}/scripts.zip scripts || report_error 3 scripts ${CWD}
cd ${CWD}/../
echo "${toolname}:msg:Compressing plugins folder "
tar zcf ${WRK_DIR}/plugins.tar plugins || report_error 3 plugins ${CWD}/../
cd config 
echo "${toolname}:msg:Compressing config folder "
tar zcf ${WRK_DIR}/config.tar * || report_error 3 config ${CWD}/../config
cd ..
echo "${toolname}:msg:Compressing daemon folder "
tar zcf ${WRK_DIR}/daemon.tar daemon || report_error 3 daemon ${CWD}/../
echo "${toolname}:msg:Compressing initscripts folder "
tar zcf ${WRK_DIR}/initscripts.tar initscripts || report_error 3 initscripts ${CWD}/../
cd misc
echo "${toolname}:msg:Compressing misc folder "
tar zcf ${WRK_DIR}/misc.tar *  || report_error 3 misc ${CWD}/../misc
cd ..
cd mysqldb
echo "${toolname}:msg:Compressing mysqldb folder "
tar zcf ${WRK_DIR}/mysqldb.tar *  || report_error 3 mysqldb ${CWD}/../mysqldb
cd ..
echo "${toolname}:msg:Compressing web folder "
tar zcf ${WRK_DIR}/web.tar web || report_error 3 mysqldb ${CWD}/../
cd ${CWD}/../../
echo "${toolname}:msg:Compressing ThirdParty folder "
zip -r -q ${WRK_DIR}/ThirdParty.zip ThirdParty  || report_error 3 ThirdParty ${CWD}/../../
echo "${toolname}:msg:Compressing ThirdParty_DB folder "
zip -r  -q ${WRK_DIR}/ThirdParty_DB.zip ${WRK_DIR}/ThirdParty_DB || report_error 3  ${WRK_DIR}/ThirdParty_DB ${WRK_DIR}/


echo "${toolname}:msg:Removing ThirdParty_DB folder "
rm -fr ${WRK_DIR}/ThirdParty_DB  || report_error 4 ${WRK_DIR}/ThirdParty_DB

echo -e "\n${toolname}:msg:Base Directory - ${WRK_DIR}"
echo -e "\n${toolname}:msg:Building the UNMP Installer.."
chmod +x  ${WRK_DIR}/InstallJammer/installjammer
${WRK_DIR}/InstallJammer/installjammer -DVersion $3 -DBaseDir ${WRK_DIR} --output-dir ${CWD}/../linux/$2/ --platform $1 --verbose $5 --build ${WRK_DIR}/../$4
if [ $? -ne 0 ]; then
	echo -e "\n${toolname}:Error:Error encountered during installjammer execution. Please Check!!"
	exit 1
else
	echo -e "\n${toolname}:msg:Installer has been created successfully in ${CWD}/../linux/$2 folder."	
	echo -e "\nCleaning up"
	rm -fr ${WRK_DIR}	
	exit 0
fi
