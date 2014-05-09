<?php
/**
 * Available POST variables:
 *
 * $type string image/png format string
 * $svg1 string Chart1 SVG data
 * $svg2 string Chart2 SVG data
 * $filename1 string filename for chart1
 * $filename2 string filename for chart2
 * $submit string Submit button value
 */
// Options
define ('BATIK_PATH', 'batik-1.7/batik-rasterizer.jar');

///////////////////////////////////////////////////////////////////////////////
ini_set('magic_quotes_gpc', 'off');

$type = (string) $_POST['type'];
$svg1 = (string) $_POST['svg1'];
$filename1 = (string) $_POST['filename'];
$download = (string) $_POST['download'];

// prepare variables
if (!$filename1) $filename1 = 'chart1';
if (get_magic_quotes_gpc()) {
	$svg1 = stripslashes($svg1);	
}

$tempName1 = $filename1;	//md5(rand());

// allow no other than predefined types
if ($type == 'image/png') {
	$typeString = '-m image/png';
	$ext = 'png';
	
} elseif ($type == 'image/jpeg') {
	$typeString = '-m image/jpeg';
	$ext = 'jpg';

} elseif ($type == 'application/pdf') {
	$typeString = '-m application/pdf';
	$ext = 'pdf';

} elseif ($type == 'image/svg+xml') {
	$ext = 'svg';	
}

//$typeString = '-m application/pdf';
//$ext = 'pdf';

$outfile1 = "download/$tempName1.$ext";

if (isset($typeString)) {
	
	// size
	if ($_POST['width']) {
		$width = (int)$_POST['width'];
		if ($width) $width = "-w $width";
	}
	else	$width = "-w 1000";
	
	
	// generate the temporary file
	if (!file_put_contents("download/$tempName1.svg", $svg1)) { 
		die("Couldn't create temporary file. Check that the directory permissions for the /temp directory are set to 777.");
	}

	// do the conversion
	$output1 = shell_exec("java -jar ". BATIK_PATH ." $typeString -d $outfile1 $width download/$tempName1.svg");
	
	// catch error while converting SVG 1
	if (!is_file($outfile1)){
		echo "Error while converting image from graph.";
		if (filesize($outfile1) < 10)
			echo "Error while converting SVG";
		//echo "<pre>$output1</pre>";
		//echo "Error while converting SVG";
	} 

	// stream it
	else {
		#$output = shell_exec("python reportGenerator.py download/$outfile1");
		#header("Content-Disposition: attachment; filename=report.pdf");
		#header("Content-Type: application/pdf");
		#echo file_get_contents("report.pdf");
		echo "successfull creation";
	}
	
} else {
	echo "Invalid type";
}
?>
