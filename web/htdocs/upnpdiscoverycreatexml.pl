#!/usr/bin/perl

#---------------------------------------------------
# author: yogesh kumar (ccpl)
# network discovery using upnp (Net::UPnP)
#---------------------------------------------------

#---------------------------------------------------
# ===================
#  Naming convention
# ===================
# Variables                  :	lowerCamelCase 
# Functions or Subroutines   :	lowerCamelCase
#---------------------------------------------------

# --------------------------------------------------------------------
# ARGV[0]  = <timeout (in sec)>                               required
# ARGV[1]  = <upnpDiscovery.xml file path>                    required
# --------------------------------------------------------------------

# include packages
use warnings;
use strict;
use Net::UPnP::ControlPoint;
use Net::UPnP::Device;
use Net::UPnP::GW::Gateway;
use threads;
use XML::DOM;

#Auto-flush. 
$| = 1;

# verify input parameters
# my ($timeout,$serviceManagement,$hostGroups,$hostFilePath,$serviceFilePath,$useHostTemplate,$useServiceTemplate,$hostCheckCommand,$nmsXmlFile) = shift;
my $timeout            = $ARGV[0] if defined $ARGV[0];
my $nmsXmlFile         = $ARGV[1] if defined $ARGV[1]; # path of upnpDiscovery.xml file which stores the current status of the discovery.

# usage notes
if (
        ( ! defined $timeout ) ||
        ( ! defined $nmsXmlFile )
        ) {
        print   "usage:\n
               $0  <timeout > <nms.xml file path>\n\n";
}
else
{
	#scanNetwork($timeout,$serviceManagement,$hostGroups,$hostFilePath,$serviceFilePath,$useHostTemplate,$useServiceTemplate,$hostCheckCommand,$nmsXmlFile);
	my $tscan = threads->new(sub { scanNetwork($timeout,$nmsXmlFile);});
	$tscan->join();
}
sub scanNetwork
{
	my $timeout            = $_[0] if defined $_[0];
        my $nmsXmlFile         = $_[1] if defined $_[1]; # path of upnpDiscovery.xml file which stores the current status of the discovery.

	my $s = Net::UPnP::ControlPoint->new();
	my @devices = $s->search(st =>'upnp:rootdevice', mx => $timeout); #or die "error: $!";
	my $i = 0;
	my $totalDevice = 0;
	if(scalar(@devices)>0)
	{
		foreach my $dev (@devices)
		{
			my $totalDevice = @devices;
			my $increment = 100/$totalDevice;

			# read nms.xml file and check what is the value of active attribute.
			my $discoveryActive = 0;
			# Create  New XML Dom Object
			my $parser = XML::DOM::Parser->new();

			# parse the xml file
			my $dom = $parser->parsefile($nmsXmlFile);
			my $autoDiscoveryTag = $dom->getElementsByTagName("autoDiscovery")->item(0);
			foreach my $discoveryTag ($autoDiscoveryTag->getElementsByTagName( 'discovery' ))
			{
				if($discoveryTag->getAttribute('type') eq "upnp" && $discoveryTag->getAttribute('active') eq "1")
				{
					my $complete = $discoveryTag->getAttribute('complete') + $increment;
					$i += 1;
					if($i == $totalDevice)
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
					$discoveryDom->setAttribute('current',sprintf("%.2f", $complete));
					$autoDiscoveryTag->replaceChild($discoveryDom,$discoveryTag);
					$dom->printToFile($nmsXmlFile);

					$discoveryActive = 1;
					last;
				}
			}
			$dom->dispose;			# clean up memory
			if($discoveryActive == 1)
			{
				my $hostAddress = $dev->getaddr();
				createHostInXml($hostAddress, $hostAddress, $hostAddress,"Unknown",$nmsXmlFile);
			}
		}
	}
	else
	{
		# Create  New XML Dom Object
		my $parser = XML::DOM::Parser->new();

		# parse the xml file
		my $dom = $parser->parsefile($nmsXmlFile);
		my $autoDiscoveryTag = $dom->getElementsByTagName("autoDiscovery")->item(0);
		foreach my $discoveryTag ($autoDiscoveryTag->getElementsByTagName( 'discovery' ))
		{
			if($discoveryTag->getAttribute('type') eq "upnp" && $discoveryTag->getAttribute('active') eq "1")
			{
				# Create new element
				my $discoveryDom = $autoDiscoveryTag->getOwnerDocument->createElement( 'discovery' );
				$discoveryDom->setAttribute('hostgroup',$discoveryTag->getAttribute('hostgroup') );
				$discoveryDom->setAttribute('username',$discoveryTag->getAttribute('username') );
				$discoveryDom->setAttribute('ip',$discoveryTag->getAttribute('ip') );
				$discoveryDom->setAttribute('start',$discoveryTag->getAttribute('start') );
				$discoveryDom->setAttribute('end',$discoveryTag->getAttribute('end') );
				$discoveryDom->setAttribute('service',$discoveryTag->getAttribute('service') );
				$discoveryDom->setAttribute('timeout',$discoveryTag->getAttribute('timeout') );
				$discoveryDom->setAttribute('active',"0");
				$discoveryDom->setAttribute('complete',$discoveryTag->getAttribute('end'));
				$discoveryDom->setAttribute('type',$discoveryTag->getAttribute('type') );
				$discoveryDom->setAttribute('current',$discoveryTag->getAttribute('end'));
				$autoDiscoveryTag->replaceChild($discoveryDom,$discoveryTag);
				$dom->printToFile($nmsXmlFile);
				last;
			}
		}
		$dom->dispose;			# clean up memory
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
