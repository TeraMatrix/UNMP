#!/usr/bin/perl

#---------------------------------------------------
# author: yogesh kumar (ccpl)
# network discovery using snmp get in perl(Net::SNMP)
#---------------------------------------------------

#---------------------------------------------------
# ===================
#  Naming convention
# ===================
# Variables                  :	lowerCamelCase 
# Functions or Subroutines   :	lowerCamelCase
#---------------------------------------------------

# --------------------------------------------------------------------
# ARGV[0]   = <start range of ip address>                     required
# ARGV[1]   = <end range of ip address>                       required
# ARGV[2]   = <community>                                     required
# ARGV[3]   = <timeout (in sec)>                              required
# ARGV[4]   = <version>                                       required
# ARGV[5]   = <port>                                          required
# ARGV[6]   = <snmp user name>                                required
# ARGV[7]   = <auth key>                                      required
# ARGV[8]   = <auth password>                                 required
# ARGV[9]   = <auth protocol>                                 required
# ARGV[10]  = <priv key>                                      required
# ARGV[11]  = <priv password>                                 required
# ARGV[12]  = <priv protocol>                                 required
# ARGV[13]  = <snmpDiscovery.xml file path>                   required
# --------------------------------------------------------------------

# include packages
use Net::SNMP;
use threads;
use XML::DOM;
use warnings;
use strict;


# verify input parameters
my $range1             = $ARGV[0] if defined $ARGV[0];
my $range2             = $ARGV[1] if defined $ARGV[1];
my $community          = $ARGV[2] if defined $ARGV[2];
my $timeout            = $ARGV[3] if defined $ARGV[3];
my $version            = $ARGV[4] if defined $ARGV[4];
my $port               = $ARGV[5] if defined $ARGV[5];
my $snmpUserName       = $ARGV[6] if defined $ARGV[6];
my $snmpAuthKey        = $ARGV[7] if defined $ARGV[7];
my $snmpAuthPassword   = $ARGV[8] if defined $ARGV[8];
my $snmpAuthProtocol   = $ARGV[9] if defined $ARGV[9];
my $snmpPrivKey        = $ARGV[10] if defined $ARGV[10];
my $snmpPrivPassword   = $ARGV[11] if defined $ARGV[11];
my $snmpPrivProtocol   = $ARGV[12] if defined $ARGV[12];
my $nmsXmlFile         = $ARGV[13] if defined $ARGV[13]; # path of snmpDiscovery.xml file which stores the current status of the discovery.


# usage notes
if (
        ( ! defined $range1 ) ||
        ( ! defined $range2 ) ||
        ( ! defined $community ) ||
        ( ! defined $timeout ) ||
        ( ! defined $version) ||
        ( ! defined $port) ||
        ( ! defined $snmpUserName) ||
        ( ! defined $snmpAuthKey) ||
        ( ! defined $snmpAuthPassword) ||
        ( ! defined $snmpAuthProtocol) ||
        ( ! defined $snmpPrivKey) ||
        ( ! defined $snmpPrivPassword) ||
        ( ! defined $snmpPrivProtocol) ||
        ( ! defined $nmsXmlFile )
        ) {
        print   "usage:\n
                $0 <start-ipaddress> <end-ipaddress> <community> <timeout> <version> <port> <snmp user name> <auth key> <auth password> <auth protocol> <priv key> <priv password> <priv protocol> <snmdDiscovery.xml file path>\n\n";
}
else
{
	my $tscan = threads->new(sub { scanNetwork($range1,$range2,$community,$timeout,$version,$port,$snmpUserName,$snmpAuthKey,$snmpAuthPassword,$snmpAuthProtocol,$snmpPrivKey,$snmpPrivPassword,$snmpPrivProtocol,$nmsXmlFile);});
	$tscan->join();
}

sub scanNetwork
{
	# verify input parameters
	my $range1             = $_[0] if defined $_[0];
	my $range2             = $_[1] if defined $_[1];
	my $community          = $_[2] if defined $_[2];
	my $timeout            = $_[3] if defined $_[3];
	my $version            = $_[4] if defined $_[4];
	my $port               = $_[5] if defined $_[5];
	my $snmpUserName       = $_[6] if defined $_[6];
	my $snmpAuthKey        = $_[7] if defined $_[7];
	my $snmpAuthPassword   = $_[8] if defined $_[8];
	my $snmpAuthProtocol   = $_[9] if defined $_[9];
	my $snmpPrivKey        = $_[10] if defined $_[10];
	my $snmpPrivPassword   = $_[11] if defined $_[11];
	my $snmpPrivProtocol   = $_[12] if defined $_[12];
	my $nmsXmlFile         = $_[13] if defined $_[13]; # path of snmpDiscovery.xml file which stores the current status of the discovery.

	# verify the ip address ranges (start/end)

	my @rangeArray1 = split(/\./, $range1);
	my @rangeArray2 = split(/\./, $range2);

	my $validate = 1; 
	if(@rangeArray1 == @rangeArray2 && @rangeArray1 == 4)
	{
		# varify the ip address format
		for (my $count = 0; $count <4; $count++)
		{
			if($rangeArray1[$count] <= $rangeArray2[$count])
			{
				if($rangeArray1[$count] < $rangeArray2[$count])
				{
					last;
				}
			}
			else
			{
				$validate = 0;
				last;
			}
		}
		if($validate == 1)
		{
			#print "ip range is correct.\n";
			while(checkIpAddress(\@rangeArray1, \@rangeArray2) == 1)
			{
				#print "IP : $rangeArray1[0].$rangeArray1[1].$rangeArray1[2].$rangeArray1[3] \n";
				
				# read nms.xml file and check what is the value of active attribute.
				my $discoveryActive = 0;
				# Create  New XML Dom Object
				my $parser = XML::DOM::Parser->new();

				# parse the xml file
				my $dom = $parser->parsefile($nmsXmlFile);
				my $autoDiscoveryTag = $dom->getElementsByTagName("autoDiscovery")->item(0);
				foreach my $discoveryTag ($autoDiscoveryTag->getElementsByTagName( 'discovery' ))
				{
					if($discoveryTag->getAttribute('type') eq "snmp" && $discoveryTag->getAttribute('active') eq "1")
					{
						my $complete = $rangeArray1[3] - $discoveryTag->getAttribute('start') + 0.0;
						my $total = $discoveryTag->getAttribute('end') - $discoveryTag->getAttribute('start') + 1.0;
						$complete = ($complete * 100)/$total;
						
						if($discoveryTag->getAttribute('end')-$rangeArray1[3] == 0)
						{
							$complete = 100;
							$discoveryTag->setAttribute('active',0);
						}
						# Create new element
						my $discoveryDom = $autoDiscoveryTag->getOwnerDocument->createElement( 'discovery' );
						$discoveryDom->setAttribute('hostgroup',$discoveryTag->getAttribute('hostgroup') );
						$discoveryDom->setAttribute('username',$discoveryTag->getAttribute('username') );
						$discoveryDom->setAttribute('ip',$discoveryTag->getAttribute('ip') );
						$discoveryDom->setAttribute('start',$discoveryTag->getAttribute('start') );
						$discoveryDom->setAttribute('end',$discoveryTag->getAttribute('end') );
						$discoveryDom->setAttribute('service',$discoveryTag->getAttribute('service') );
						$discoveryDom->setAttribute('timeout',$discoveryTag->getAttribute('timeout') );
						$discoveryDom->setAttribute('active',$discoveryTag->getAttribute('active') );
						$discoveryDom->setAttribute('complete',sprintf("%.2f", $complete));
						$discoveryDom->setAttribute('type',$discoveryTag->getAttribute('type') );
						$discoveryDom->setAttribute('current',$rangeArray1[3]);
						$discoveryDom->setAttribute('authKey',$snmpAuthKey );
						$discoveryDom->setAttribute('authProtocol',$snmpAuthProtocol );
						$discoveryDom->setAttribute('password',$snmpAuthPassword );
						$discoveryDom->setAttribute('privKey',$snmpPrivKey );
						$discoveryDom->setAttribute('privPassword',$snmpPrivPassword );
						$discoveryDom->setAttribute('privProtocol',$snmpPrivProtocol );
						$discoveryDom->setAttribute('snmpUser',$snmpUserName );
						$discoveryDom->setAttribute('port',$port );
						$discoveryDom->setAttribute('version',$version );
						$discoveryDom->setAttribute('community',$community );
						$autoDiscoveryTag->replaceChild($discoveryDom,$discoveryTag);
						$dom->printToFile($nmsXmlFile);

						$discoveryActive = 1;
						last;
					}
				}
				$dom->dispose;			# clean up memory
				if($discoveryActive == 1)
				{
					snmpGetAndCreateHostInXml("$rangeArray1[0].$rangeArray1[1].$rangeArray1[2].$rangeArray1[3]", $timeout, $community, $version, $port,$snmpUserName,$snmpAuthKey,$snmpAuthPassword,$snmpAuthProtocol,$snmpPrivKey,$snmpPrivPassword,$snmpPrivProtocol,$nmsXmlFile);
				}
				else
				{
					exit 0;
				}

				#snmpGet("$rangeArray1[0].$rangeArray1[1].$rangeArray1[2].$rangeArray1[3]", $timeout, $community, $version, $port);
				$rangeArray1[3] += 1;
				if($rangeArray1[3]>255)
				{
					$rangeArray1[3] = 0;
					$rangeArray1[2] += 1;
					if($rangeArray1[2]>255)
					{
						$rangeArray1[2] = 0;
						$rangeArray1[1] += 1;
						if($rangeArray1[1]>255)
						{
							$rangeArray1[1] = 0;
							$rangeArray1[0] += 1;
							if($rangeArray1[0]>255)
							{
								last;
							}
						}
					}
				}
			}
			#print "\n";
		}
		else
		{
			#print "ip range is incorrect.\n\n";
		}
	}
	else
	{
		#print "wrong Ip address range.\n";
	}
}

# check the ip address (start) is not greater then with another ip adddress (end)
sub checkIpAddress
{
	my ($listaref, $listbref ) = @_;

	# De-reference the array list
	my (@firstArray) = @$listaref;
	my (@secondArray) = @$listbref;

	for (my $count = 0; $count <4; $count++)
	{
		if($firstArray[$count] <= $secondArray[$count])
		{
			if($firstArray[$count] < $secondArray[$count])
			{
				return 1;
			}
		}
		else
		{
			return 0;
		}
	}
	return 1;
}

sub snmpGetAndCreateHostInXml
{
	# varify function arguments
	my $hostAddress        = $_[0] if defined $_[0];
	my $seconds            = $_[1] if defined $_[1];
	my $community          = $_[2] if defined $_[2];
	my $version            = $_[3] if defined $_[3];
	my $port               = $_[4] if defined $_[4];
	my $username           = $_[5] if defined $_[5];
	my $authkey            = $_[6] if defined $_[6];
	my $authpasswd         = $_[7] if defined $_[7];
	my $authproto          = $_[8] if defined $_[8];
	my $privkey            = $_[9] if defined $_[9];
	my $privpasswd         = $_[10] if defined $_[10];
	my $privproto          = $_[11] if defined $_[11];
	my $nmsXmlFile         = $_[12] if defined $_[12];
	
	# list all OIDs to be queried
	#my $sysUpTime           = ".1.3.6.1.2.1.1.3.0";
	#my $sysDesc             = ".1.3.6.1.2.1.1.1.0";
	#my $sysObjectId         = ".1.3.6.1.2.1.1.2.0";
	#my $sysContact          = ".1.3.6.1.2.1.1.4.0";
	my $sysName             = ".1.3.6.1.2.1.1.5.0";
	#my $sysLocation         = ".1.3.6.1.2.1.1.6.0";
	#my $interfaces          = ".1.3.6.1.2.1.2.1.0";
	#my $udpInDatagrams      = ".1.3.6.1.2.1.7.1.0";
	#my $udpOutDatagrams     = ".1.3.6.1.2.1.7.4.0";

	# get information via SNMP
	my $session = "";
	my $error = "";
	# create session object
	if($version eq "3")
	{
		my ($session, $error) = Net::SNMP->session(
		                -hostname      => $hostAddress,
		                -timeout       => $seconds,
		                -port          => $port,
		                -version       => $version,
		                -community     => $community,
		                -username      => $username,    # v3
		                -authkey       => $authkey,     # v3
		                -authpassword  => $authpasswd,  # v3
		                -authprotocol  => $authproto,   # v3
		                -privkey       => $privkey,     # v3
		                -privpassword  => $privpasswd,  # v3
		                -privprotocol  => $privproto,   # v3
		                # please add more parameters if there's a need for them:
		                #   [-localaddr     => $localaddr,]
		                #   [-localport     => $localport,]
		                #   [-nonblocking   => $boolean,]
		                #   [-domain        => $domain,]
		                #   [-retries       => $count,]
		                #   [-maxmsgsize    => $octets,]
		                #   [-translate     => $translate,]
		                #   [-debug         => $bitmask,]
		                );
		# on error: exit
		if (!defined($session)) 
		{
			#printf("SESSION ERROR: %s.\n", $error);
		        #printf("\n\nError in Host %s parameter", $hostAddress);
			#return 1;
			#exit 1;
		}
		else
		{
			# perform get requests for all wanted OIDs
			#my $result = $session->get_request(
			#                 -varbindlist      => [$sysDesc, $sysObjectId, $sysUpTime, $sysContact, $sysName, $sysLocation, $interfaces, $udpInDatagrams, $udpOutDatagrams]
			#               );
			my $result = $session->get_request(
				         -varbindlist      => [$sysName]
				       );

			# on error: exit
			if (!defined($result)) 
			{
				#printf("RESULT ERROR: %s.\n", $session->error);
				#printf("\n\nSNMP not Enabled in %s",$hostAddress);
				#$session->close;
				#return 1;
				#exit 1;
			}
			else
			{
				# print results
				#printf("\n\nDevice Found:\nIP Address : %s \nSystem Description : %s \nSystem Object Id : %s \nSystem Uptime : %s \nSystem Contact : %s \nSystem Name : %s \nSystem Location : %s \nInterface : %s \nudpInDatagrams : %s \nudpOutDatagrams : %s\n",
				#	$hostAddress,
				#	$result->{$sysDesc},
				#	$result->{$sysObjectId},
				#	$result->{$sysUpTime},
				#	$result->{$sysContact},
				#	$result->{$sysName},
				#	$result->{$sysLocation},
				#	$result->{$interfaces},
				#	$result->{$udpInDatagrams},
				#	$result->{$udpOutDatagrams},
				#	);
			 	my $name = $hostAddress;
				if(defined ($result->{$sysName}))
				{
					$name = $result->{$sysName};
					if(trim($name) eq "")
					{
						$name = $hostAddress;
					}
				}
				createHostInXml($hostAddress, $name, $hostAddress,"Unknown",$nmsXmlFile);
			}
			$session->close;
		}
 	}
	else
	{
		my ($session, $error) = Net::SNMP->session(
		                -hostname      => $hostAddress,
		                -timeout       => $seconds,
		                -port          => $port,
		                -version       => $version,
		                -community     => $community,
		                # please add more parameters if there's a need for them:
		                #   [-localaddr     => $localaddr,]
		                #   [-localport     => $localport,]
		                #   [-nonblocking   => $boolean,]
		                #   [-domain        => $domain,]
		                #   [-retries       => $count,]
		                #   [-maxmsgsize    => $octets,]
		                #   [-translate     => $translate,]
		                #   [-debug         => $bitmask,]
		                );
		# on error: exit
		if (!defined($session)) 
		{
			#printf("SESSION ERROR: %s.\n", $error);
		        #printf("\n\nError in Host %s parameter", $hostAddress);
			#return 1;
			#exit 1;
		}
		else
		{
			# perform get requests for all wanted OIDs
			#my $result = $session->get_request(
			#                 -varbindlist      => [$sysDesc, $sysObjectId, $sysUpTime, $sysContact, $sysName, $sysLocation, $interfaces, $udpInDatagrams, $udpOutDatagrams]
			#               );
			my $result = $session->get_request(
				         -varbindlist      => [$sysName]
				       );

			# on error: exit
			if (!defined($result)) 
			{
				#printf("RESULT ERROR: %s.\n", $session->error);
				#printf("\n\nSNMP not Enabled in %s",$hostAddress);
				#$session->close;
				#return 1;
				#exit 1;
			}
			else
			{
				# print results
				#printf("\n\nDevice Found:\nIP Address : %s \nSystem Description : %s \nSystem Object Id : %s \nSystem Uptime : %s \nSystem Contact : %s \nSystem Name : %s \nSystem Location : %s \nInterface : %s \nudpInDatagrams : %s \nudpOutDatagrams : %s\n",
				#	$hostAddress,
				#	$result->{$sysDesc},
				#	$result->{$sysObjectId},
				#	$result->{$sysUpTime},
				#	$result->{$sysContact},
				#	$result->{$sysName},
				#	$result->{$sysLocation},
				#	$result->{$interfaces},
				#	$result->{$udpInDatagrams},
				#	$result->{$udpOutDatagrams},
				#	);
			 	my $name = $hostAddress;
				if(defined ($result->{$sysName}))
				{
					$name = $result->{$sysName};
					if($name eq "")
					{
						$name = $hostAddress;
					}
				}
				createHostInXml($hostAddress, $name, $hostAddress,"Unknown",$nmsXmlFile);
			}
			$session->close;
		}
	}
}

sub createHostInXml
{
	# varify function arguments
	my $hostName           = $_[0] if defined $_[0];
	my $hostAlias          = $_[1] if defined $_[1];
	my $hostAddress        = $_[2] if defined $_[2];
	my $hostType           = $_[3] if defined $_[3];
	my $nmsXmlFile         = $_[4] if defined $_[4];

	# Create  New XML Dom Object
	my $parser = XML::DOM::Parser->new();

	# parse the xml file
	my $dom = $parser->parsefile($nmsXmlFile);
	my $discoveredHostsTag = $dom->getElementsByTagName("discoveredHosts")->item(0);

	# Create new element
	my $hostDom = $discoveredHostsTag->getOwnerDocument->createElement( 'host' );
	$hostDom->setAttribute('name',$hostName);
	$hostDom->setAttribute('alias',$hostAlias);
	$hostDom->setAttribute('address',$hostAddress);
	$hostDom->setAttribute('type',$hostType);
	$discoveredHostsTag->appendChild($hostDom);
	$dom->printToFile($nmsXmlFile);
	$dom->dispose;			# clean up memory
}
