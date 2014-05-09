#!/usr/bin/perl

#---------------------------------------------------
# author: yogesh kumar (ccpl)
# Port Scanning and
# Write host's services in a file for nagios
#---------------------------------------------------

#---------------------------------------------------
# ===================
#  Naming convention
# ===================
# Variables                  :	lowerCamelCase 
# Functions or Subroutines   :	lowerCamelCase
#---------------------------------------------------


# --------------------------------------------------
# ARGV[0] = <discovery type>   		    required
# ARGV[1] = <host list>		            required
# ARGV[2] = <file path>                     required
# ARGV[3] = <service-template>              required
# --------------------------------------------------


use strict; 
use warnings; 
use IO::Socket::INET; 
use Net::SNMP;

#Auto-flush. 
# $| = 1;


# verify input parameters
my $discoveryType       = $ARGV[0] if defined $ARGV[0];
my $hostList            = $ARGV[1] if defined $ARGV[1];
my $serviceFilePath     = $ARGV[2] if defined $ARGV[2];
my $useServiceTemplate  = $ARGV[3] if defined $ARGV[3];

# usage notes
if (
	( ! defined $discoveryType ) ||
	( ! defined $hostList ) ||
	( ! defined $serviceFilePath ) ||
	( ! defined $useServiceTemplate )
	) {
	print "usage:\n\tportscan ( <discovery type>, <host list>, <file-path>, <service-template> );\n\n";
}
else
{
	my @hosts = split(/\,/, $hostList);	
	foreach my $host (@hosts)
	{
		if($discoveryType eq "snmp")
		{
			createService($serviceFilePath,$useServiceTemplate,$host,"SNMP System Up Time", "check_snmp!-C public -o .1.3.6.1.2.1.1.3.0");
		}
		else
		{
			checkSnmpService($host,$serviceFilePath,$useServiceTemplate,"3","161","2","public");
		}
		# Create a service for ping
		createService($serviceFilePath,$useServiceTemplate,$host,"PING", "check_ping!100.0,20%!500.0,60%");
		# scan post and create services
		portscan($host,$serviceFilePath,$useServiceTemplate);
	}
	print "0";
}


# scan posts of host and create service configuration in config file.
sub portscan
{
	# verify input parameters
	my $host                = $_[0] if defined $_[0];
	my $serviceFilePath     = $_[1] if defined $_[1];
	my $useServiceTemplate  = $_[2] if defined $_[2];

	# usage notes
	if (
		( ! defined $host ) ||
		( ! defined $serviceFilePath ) ||
		( ! defined $useServiceTemplate )
		) {
		print   "usage:\n\tportscan ( <host>, <file-path>, <service-template> );\n\n";
		exit;
	}

	my $port = 0;
	my @ports = (21, 22,23,25,80,110,119,137,139,194,220,389,443,445,465,655,993,994,1080,1812,1194,1433,1434,2049,3493,3306,5432,5666,6667,12340,33333);
	my @portName = ("FTP","SSH","Telnet","SMTP","HTTP","POP3","NNTP","NETBIOS name service","NETBIOS session service","IRC on port 194","IMAP3","LDAP","SSL enabled HTTP server","Microsoft naked CIFS","SMTP over SSL","TINC","IMAP over SSL","POP3 over SSL","Socks","Radius","OpenVPN","Microsoft SQL server","Microsoft SQL monitor","NFS","Network UPS Tools","MySQL database","PostgreSQL database","NRPE remote checks daemon","IRC on port 6667","CoffeeSaint webserver","Nagios status");
	my @portCommand = ("check_ftp","check_ssh","check_telnet","check_tcp!25","check_http","check_tcp!110","check_tcp!119","check_tcp!137","check_tcp!139","check_tcp!194","check_tcp!220","check_tcp!389","check_https","check_tcp!445","check_tcp!465","check_tcp!655","check_tcp!993","check_tcp!994","check_tcp!1080","check_tcp!1812","check_tcp!1194","check_tcp!1433","check_tcp!1434","check_tcp!2049","check_tcp!3493","check_mysql","check_tcp!5432","check_nrpe","check_tcp!6667","check_http!12340","check_tcp!33333");

	my $i = 0;
	for ($i = 0; $i < @ports; $i++)
	{
		#print "Port: ",$ports[$i],"\n";
		$port = $ports[$i];
		my $socket; 
		my $success = eval { 
					$socket = IO::Socket::INET->new( 
									PeerAddr => $host, 
									PeerPort => $port, 
									Proto => 'tcp',
									Timeout => "1"
									) 
				}; 
		# my code - get the port service name
		#my $getservicename= getservbyport($port,"tcp");

		#If the port was opened, say it was and close it. 
		if ($success) 
		{ 
			#if (defined($getservicename))
			#{
			#	#print "Port $port: Open and Type: $getservicename \n";
			#}
			#else
			#{
			#	#print "Port $port : Open\n"
			#}
			createService($serviceFilePath,$useServiceTemplate,$host,$portName[$i], $portCommand[$i]);
			shutdown($socket, 2); 
		}
	}
}

# check snmp service and create service configutation in config file
sub checkSnmpService
{
	my $hostAddress         = $_[0] if defined $_[0];
	my $serviceFilePath     = $_[1] if defined $_[1];
	my $useServiceTemplate  = $_[2] if defined $_[2];
	my $timeout             = $_[3] if defined $_[3];
	my $port                = $_[4] if defined $_[4];
	my $version             = $_[5] if defined $_[5];
	my $community           = $_[6] if defined $_[6];
	my $sysUpTime           = ".1.3.6.1.2.1.1.3.0";

	# create session object
	my ($session, $error) = Net::SNMP->session(
                        -hostname      => $hostAddress,
                        -timeout       => $timeout,
                        -port          => $port,
                        -version       => $version,
                        -community     => $community,
			);
	# print "snmp port","\n";
	if (defined($session))
	{
		my $result = $session->get_request(
		                 -varbindlist      => [$sysUpTime]
		               );
		if (defined($result)) 
		{
			createService($serviceFilePath,$useServiceTemplate,$hostAddress,"SNMP System Up Time", "check_snmp!-C public -o .1.3.6.1.2.1.1.3.0");
		}
		$session->close;
	}
}

# createHost("hosts.cfg","generic-host","ap-5.33","Access Point", "192.168.5.31", "check-host-alive");

# create nagios file for hosts
sub createHost
{
	# verify input parameters
	my $filePath       = $_[0] if defined $_[0];
	my $useTemplate    = $_[1] if defined $_[1];
	my $hostName       = $_[2] if defined $_[2];
	my $hostAlias      = $_[3] if defined $_[3];
	my $hostAddress    = $_[4] if defined $_[4];
	my $checkCommand   = $_[5] if defined $_[5];
	my $hostGroups     = $_[6] if defined $_[6];
	# usage notes
	if (
		( ! defined $filePath ) ||
		( ! defined $useTemplate ) ||
		( ! defined $hostName ) ||
		( ! defined $hostAlias ) ||
		( ! defined $hostAddress) ||
		( ! defined $checkCommand) ||
		( ! defined $hostGroups)
		) {
		print   "usage:\n\tcreateHost ( <file-path>, <host-template>, <host-name>, <host-alias>, <address>, <check-command>, <host-groups> );\n\n";
		exit;
	}
	if(checkHostExist($filePath, $hostName) == 0)
	{
		open FILE, ">>$filePath" or die $!;
		print FILE "\n#host-" . trim($hostName) . "\n";
		print FILE "define host {\n";
		print FILE "\tuse\t\t" . trim($useTemplate) . "\n";
		print FILE "\thost_name\t" . trim($hostName) . "\n";
		print FILE "\talias\t\t" . trim($hostAlias) . "\n";
		print FILE "\taddress\t\t" . trim($hostAddress) . "\n";
		if($checkCommand ne "")
		{
			print FILE "\tcheck_command\t" . trim($checkCommand) . "\n";
		}
		if($hostGroups ne "")
		{
			print FILE "\thostgroups\t" . trim($hostGroups) . "\n";
		}
		print FILE "}\n";
		print FILE "#endhost-" . trim($hostName);
		close FILE;
	}
}

# Check for Existing host in the File [ this function return 0 if host does not exit otherwise 1 ]
sub checkHostExist
{
	# varify input variables
        my $filePath       = $_[0] if defined $_[0];
	my $hostName       = $_[1] if defined $_[1];
	my $isExist        = 0; 
	# Check file exist or not
	if(-e $filePath)
	{
		open FILE, "<$filePath" or die $!;
		while (<FILE>) 
		{ 
			if(trim($_) eq "#host-" . trim($hostName))
			{
				$isExist = 1;
				last;
			}
		}
		close FILE;
	}
	return $isExist;
}


# --------------------------------------------------
# ARGV[0] = <file path>   		    required
# ARGV[1] = <use template>		    required
# ARGV[2] = <host name>                     required
# ARGV[3] = <service description>           required
# ARGV[4] = <check command>                 required
# --------------------------------------------------

# createService("services.cfg","generic-service","ap-5.31","PING", "check_ping");

# create nagios file for hosts
sub createService
{
	# verify input parameters
	my $filePath       = $_[0] if defined $_[0];
	my $useTemplate    = $_[1] if defined $_[1];
	my $hostName       = $_[2] if defined $_[2];
	my $serviceDesc    = $_[3] if defined $_[3];
	my $checkCommand   = $_[4] if defined $_[4];

	# usage notes
	if (
		( ! defined $filePath ) ||
		( ! defined $useTemplate ) ||
		( ! defined $hostName ) ||
		( ! defined $serviceDesc) ||
		( ! defined $checkCommand)
		) {
		print   "usage:\n\tcreateService ( <file-path>, <service-template>, <host-name>, <service-description>, <check-command> );\n\n";
		exit;
	}
	if(checkServiceExist($filePath, $hostName, $checkCommand) == 0)
	{
		open FILE, ">>$filePath" or die $!;
		print FILE "\n#service-" . trim($hostName) . "-" . trim($checkCommand) . "\n";
		print FILE "define service {\n";
		print FILE "\tuse\t\t" . trim($useTemplate) . "\n";
		print FILE "\thost_name\t" . trim($hostName) . "\n";
		print FILE "\tservice_description\t" . trim($serviceDesc) . "\n";
		print FILE "\tcheck_command\t" . trim($checkCommand) . "\n";
		print FILE "}\n";
		print FILE "#endservice-" . trim($hostName) . "-" . trim($checkCommand);
		close FILE;
	}
}

# Check for Existing host in the File [ this function return 0 if host does not exit otherwise 1 ]
sub checkServiceExist
{
	# varify input variables
        my $filePath       = $_[0] if defined $_[0];
	my $hostName       = $_[1] if defined $_[1];
	my $checkCommand   = $_[2] if defined $_[2];
	my $isExist        = 0; 
	# Check file exist or not
	if(-e $filePath)
	{
		open FILE, "<$filePath" or die $!;
		while (<FILE>) 
		{ 
			if(trim($_) eq "#service-". trim($hostName) . "-" . trim($checkCommand))
			{
				$isExist = 1;
				last;
			}
		}
		close FILE;
	}
	return $isExist;
}


# Perl trim function to remove whitespace from the start and end of the string
sub trim($)
{
	my $string = shift;
	$string =~ s/^\s+//;
	$string =~ s/\s+$//;
	return $string;
}
