var aSelectedLog = [];
var oTableLog = null;
var $spinLoading = null;
var $spinMainLoading  = null;

$(document).ready(function(){
	$spinLoading = $("div#spin_loading");        // create object that hold loading circle
	$spinMainLoading = $("div#main_loading");    // create object that hold loading squire
	var cur_date=new Date();
	var d=cur_date.getDate();
	var y=cur_date.getFullYear();
	var m=cur_date.getMonth();
	var cdate=new Date(y,m,d);
	oTable = $('#log_table').dataTable({
		"bJQueryUI": true,
		"sPaginationType": "full_numbers",
		"bProcessing": true,
		"bServerSide": true,
		"sAjaxSource": "get_log_data.py",
		"aaSorting": [[0,'desc']]
	});
	
	$("#page_tip").colorbox(  			//page tip
	    {
		href:"view_page_tip_log_user.py",
		title: "Page Tip",
		opacity: 0.4,
		maxWidth: "80%",
		width:"600px",
		height:"400px"
	    });
});
