#!/usr/bin/perl

#---------------------------------------------------
# author: yogesh kumar (ccpl)
# network discovery using ping the device in perl(Net::SNMP)
#---------------------------------------------------

#---------------------------------------------------
# ===================
#  Naming convention
# ===================
# Variables                  :	lowerCamelCase 
# Functions or Subroutines   :	lowerCamelCase
#---------------------------------------------------

# --------------------------------------------------------------------
# ARGV[0]  = <start range of ip address>                      required
# ARGV[1]  = <end range of ip address>                        required
# ARGV[2]  = <timeout (in sec)>                               required
# ARGV[3]  = <pingDiscovery.xml file path>                    required
# --------------------------------------------------------------------


# include packages
use Net::Ping;
use Socket;
use threads;
use XML::DOM;
use warnings;
use strict;

#Auto-flush. 
$| = 1;


# verify input parameters
my $range1             = $ARGV[0] if defined $ARGV[0];
my $range2             = $ARGV[1] if defined $ARGV[1];
my $timeout            = $ARGV[2] if defined $ARGV[2];
my $nmsXmlFile         = $ARGV[3] if defined $ARGV[3]; # path of nms.xml file which stores the current status of the discovery.

# usage notes
if (
        ( ! defined $range1 ) ||
        ( ! defined $range2 ) ||
        ( ! defined $timeout ) ||
        ( ! defined $nmsXmlFile )
        ) {
        print   "usage:\n
                $0 <start-ipaddress> <end-ipaddress> <timeout> <pingDiscovery.xml file path>\n\n";
}
else
{
	my $tscan = threads->new(sub { scanNetwork($range1,$range2,$timeout,$nmsXmlFile);});
	$tscan->join();
}
sub scanNetwork
{
	my $range1             = $_[0] if defined $_[0];
	my $range2             = $_[1] if defined $_[1];
	my $timeout            = $_[2] if defined $_[2];
        my $nmsXmlFile         = $_[3] if defined $_[3]; # path of nms.xml file which stores the current status of the discovery.

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
			# print "ip range is correct.\n";
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
					if($discoveryTag->getAttribute('type') eq "ping" && $discoveryTag->getAttribute('active') eq "1")
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
						$autoDiscoveryTag->replaceChild($discoveryDom,$discoveryTag);
						$dom->printToFile($nmsXmlFile);

						$discoveryActive = 1;
						last;
					}
				}
				$dom->dispose;			# clean up memory
				if($discoveryActive == 1)
				{
					pingDeviceAndWriteInToXml("$rangeArray1[0].$rangeArray1[1].$rangeArray1[2].$rangeArray1[3]", $timeout,$nmsXmlFile);
				}
				else
				{
					exit 0;
				}
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
			# print "\n";
		}
		else
		{
			# print "ip range is incorrect.\n\n";
		}
	}
	else
	{
		# print "wrong Ip address range.\n";
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

sub pingDeviceAndWriteInToXml
{
	# varify function arguments
	my $hostAddress        = $_[0] if defined $_[0];
	my $seconds            = $_[1] if defined $_[1];
	my $nmsXmlFile         = $_[2] if defined $_[2];

	#my $p = Net::Ping->new('icmp') or die "$!";
	my $p = Net::Ping->new();

	my $res = $p->ping($hostAddress, $seconds);
	#unless ($res)
	#{
	#	$res = $p->ping($hostAddress);
	#	unless ($res)
	#	{
	#		return $p->ping($hostAddress);
	#	}
	#}

	if($res == 1)
	{
		my $iaddr = inet_aton($hostAddress); # or whatever address
		my $name  = gethostbyaddr($iaddr, AF_INET);
		if( defined $name)
		{
			# $name = $hostAddress;
		}
		else
		{
			$name = $hostAddress;
		}
		createHostInXml($hostAddress, $name, $hostAddress,"Unknown",$nmsXmlFile);
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
