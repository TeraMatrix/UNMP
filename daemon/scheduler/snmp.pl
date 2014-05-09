#!/usr/bin/perl

#--------------------------------------------------------------------------
# author: yogesh kumar (ccpl)
# get tx rx and interface information using snmp get in perl(Net::SNMP)
#--------------------------------------------------------------------------

#---------------------------------------------------
# ===================
#  Naming convention
# ===================
# Variables                  :	lowerCamelCase 
# Functions or Subroutines   :	lowerCamelCase
#---------------------------------------------------

# --------------------------------------------------------------------
# ARGV[0]   = <ip address>                     required
# --------------------------------------------------------------------

# include packages
use Net::SNMP;
use warnings;
use strict;

# verify input parameters
my $ipAddress             = $ARGV[0] if defined $ARGV[0];
my $seconds               = 1;
my $port                  = 161;
my $version               = 2;
my $community             = "public";

# list all OIDs to be queried
my $sysUpTime           = ".1.3.6.1.2.1.1.3.0";
my $interface             = ".1.3.6.1.2.1.2.1.0";

# interface 1 [lo]
my $interfaceName1        = ".1.3.6.1.2.1.2.2.1.2.1";
my $interfaceTx1          = ".1.3.6.1.2.1.2.2.1.16.1";
my $interfaceRx1          = ".1.3.6.1.2.1.2.2.1.10.1";

# interface 2 [eth0]
my $interfaceName2        = ".1.3.6.1.2.1.2.2.1.2.2";
my $interfaceTx2          = ".1.3.6.1.2.1.2.2.1.16.2";
my $interfaceRx2          = ".1.3.6.1.2.1.2.2.1.10.2";

# interface 3 [br0]
my $interfaceName3        = ".1.3.6.1.2.1.2.2.1.2.3";
my $interfaceTx3          = ".1.3.6.1.2.1.2.2.1.16.3";
my $interfaceRx3          = ".1.3.6.1.2.1.2.2.1.10.3";

# interface 4 [wifi0]
my $interfaceName4        = ".1.3.6.1.2.1.2.2.1.2.4";
my $interfaceTx4          = ".1.3.6.1.2.1.2.2.1.16.4";
my $interfaceRx4          = ".1.3.6.1.2.1.2.2.1.10.4";

# interface 5 [ath0]
my $interfaceName5        = ".1.3.6.1.2.1.2.2.1.2.5";
my $interfaceTx5          = ".1.3.6.1.2.1.2.2.1.16.5";
my $interfaceRx5          = ".1.3.6.1.2.1.2.2.1.10.5";

# interface 6 [ath1]
my $interfaceName6        = ".1.3.6.1.2.1.2.2.1.2.6";
my $interfaceTx6          = ".1.3.6.1.2.1.2.2.1.16.6";
my $interfaceRx6          = ".1.3.6.1.2.1.2.2.1.10.6";

# interface 7 [ath2]
my $interfaceName7        = ".1.3.6.1.2.1.2.2.1.2.7";
my $interfaceTx7          = ".1.3.6.1.2.1.2.2.1.16.7";
my $interfaceRx7          = ".1.3.6.1.2.1.2.2.1.10.7";

# interface 8 [ath3]
my $interfaceName8        = ".1.3.6.1.2.1.2.2.1.2.8";
my $interfaceTx8          = ".1.3.6.1.2.1.2.2.1.16.8";
my $interfaceRx8          = ".1.3.6.1.2.1.2.2.1.10.8";

# interface 9 [ath4]
my $interfaceName9        = ".1.3.6.1.2.1.2.2.1.2.9";
my $interfaceTx9          = ".1.3.6.1.2.1.2.2.1.16.9";
my $interfaceRx9          = ".1.3.6.1.2.1.2.2.1.10.9";

# interface 10 [ath5]
my $interfaceName10       = ".1.3.6.1.2.1.2.2.1.2.10";
my $interfaceTx10         = ".1.3.6.1.2.1.2.2.1.16.10";
my $interfaceRx10         = ".1.3.6.1.2.1.2.2.1.10.10";

# interface 11 [ath6]
my $interfaceName11       = ".1.3.6.1.2.1.2.2.1.2.11";
my $interfaceTx11         = ".1.3.6.1.2.1.2.2.1.16.11";
my $interfaceRx11         = ".1.3.6.1.2.1.2.2.1.10.11";

# interface 12 [ath7]
my $interfaceName12       = ".1.3.6.1.2.1.2.2.1.2.12";
my $interfaceTx12         = ".1.3.6.1.2.1.2.2.1.16.12";
my $interfaceRx12         = ".1.3.6.1.2.1.2.2.1.10.12";

# usage notes
if ( ! defined $ipAddress )
{
	print   "usage:\
                $0 <ip-address>\n
result: \
                Total Interface\
                Interfaces Name (comma separated)\
                Tx (comma separated)\
                Rx (comma separated)\
                System Uptime\n\n";
}
else
{
	my ($session, $error) = Net::SNMP->session(
		                -hostname      => $ipAddress,
		                -timeout       => $seconds,
		                -port          => $port,
		                -version       => $version,
		                -community     => $community,
		                );

	# on error: exit
	if (!defined($session)) 
	{
		#printf("SESSION ERROR: %s.\n", $error);
	        #printf("\n\nError in Host %s parameter", $hostAddress);
		print "1";
	}
	else
	{
		# perform get requests for all wanted OIDs
		my $result = $session->get_request(
		                 -varbindlist      => [$sysUpTime,$interface, $interfaceName1, $interfaceTx1, $interfaceRx1
							, $interfaceName1, $interfaceTx1, $interfaceRx1
							, $interfaceName2, $interfaceTx2, $interfaceRx2
							, $interfaceName3, $interfaceTx3, $interfaceRx3
							, $interfaceName4, $interfaceTx4, $interfaceRx4
							, $interfaceName5, $interfaceTx5, $interfaceRx5
							, $interfaceName6, $interfaceTx6, $interfaceRx6
							, $interfaceName7, $interfaceTx7, $interfaceRx7
							, $interfaceName8, $interfaceTx8, $interfaceRx8
							, $interfaceName9, $interfaceTx9, $interfaceRx9
							, $interfaceName10, $interfaceTx10, $interfaceRx10
							, $interfaceName11, $interfaceTx11, $interfaceRx11
							, $interfaceName12, $interfaceTx12, $interfaceRx12
							]
		);
		# on error: exit
		if (!defined($result)) 
		{
			#printf("RESULT ERROR: %s.\n", $session->error);
			#printf("\n\nSNMP not Enabled in %s",$hostAddress);
			#$session->close;
			print "1";
		}
		else
		{
			my $snmpResult = "";
			my $name = "";
			my $tx = "";
			my $rx = "";
			if(int($result->{$interface}) >=1)
			{
				$name .= $result->{$interfaceName1};
				$tx .= $result->{$interfaceTx1};
				$rx .= $result->{$interfaceRx1};
			}
			
			if(int($result->{$interface}) >=2)
			{
				$name .= "," . $result->{$interfaceName2};
				$tx .= "," . $result->{$interfaceTx2};
				$rx .= "," . $result->{$interfaceRx2};
			}

			if(int($result->{$interface}) >=3)
			{
				$name .= "," . $result->{$interfaceName3};
				$tx .= "," . $result->{$interfaceTx3};
				$rx .= "," . $result->{$interfaceRx3};
			}

			if(int($result->{$interface}) >=4)
			{
				$name .= "," . $result->{$interfaceName4};
				$tx .= "," . $result->{$interfaceTx4};
				$rx .= "," . $result->{$interfaceRx4};
			}

			if(int($result->{$interface}) >=5)
			{
				$name .= "," . $result->{$interfaceName5};
				$tx .= "," . $result->{$interfaceTx5};
				$rx .= "," . $result->{$interfaceRx5};
			}

			if(int($result->{$interface}) >=6)
			{
				$name .= "," . $result->{$interfaceName6};
				$tx .= "," . $result->{$interfaceTx6};
				$rx .= "," . $result->{$interfaceRx6};
			}

			if(int($result->{$interface}) >=7)
			{
				$name .= "," . $result->{$interfaceName7};
				$tx .= "," . $result->{$interfaceTx7};
				$rx .= "," . $result->{$interfaceRx7};
			}

			if(int($result->{$interface}) >=8)
			{
				$name .= "," . $result->{$interfaceName8};
				$tx .= "," . $result->{$interfaceTx8};
				$rx .= "," . $result->{$interfaceRx8};
			}

			if(int($result->{$interface}) >=9)
			{
				$name .= "," . $result->{$interfaceName9};
				$tx .= "," . $result->{$interfaceTx9};
				$rx .= "," . $result->{$interfaceRx9};
			}

			if(int($result->{$interface}) >=10)
			{
				$name .= "," . $result->{$interfaceName10};
				$tx .= "," . $result->{$interfaceTx10};
				$rx .= "," . $result->{$interfaceRx10};
			}

			if(int($result->{$interface}) >=11)
			{
				$name .= "," . $result->{$interfaceName11};
				$tx .= "," . $result->{$interfaceTx11};
				$rx .= "," . $result->{$interfaceRx11};
			}

			if(int($result->{$interface}) >=12)
			{
				$name .= "," . $result->{$interfaceName12};
				$tx .= "," . $result->{$interfaceTx12};
				$rx .= "," . $result->{$interfaceRx12};
			}
			$snmpResult = $result->{$interface} . "\n" . $name . "\n" . $tx . "\n" . $rx . "\n" . $result->{$sysUpTime};
			print $snmpResult;
		}
	}
}
