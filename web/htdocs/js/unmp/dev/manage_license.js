var $spinLoading = null;
var $spinMainLoading = null;

$(function () {
    // spin loading object
    $spinLoading = $("div#spin_loading");		// create object that hold loading circle
    $spinMainLoading = $("div#main_loading");	// create object that hold loading squire

    // page tip [for page tip write this code on each page please dont forget to change "href" value because this link create your help tip page]
// Removing PAGE TIP : possible error - use of javascript in python files
//	$("#page_tip").colorbox(
//	{
//		href:"help_license.py",
//		title: "Page Tip",
//		opacity: 0.4,
//		maxWidth: "80%",
//		width:"600px",
//		height:"400px"
//	});
    $("button[id='button_uploader']").click(function () {
        spinStart($spinLoading, $spinMainLoading);
    });
    $("td#host").toggle(function () {
            var $this = $(this);
            var $span = $this.find("span").eq(0);
            $span.removeClass("nxt");
            $span.addClass("dwn");
            showHostP();
        },
        function () {
            var $this = $(this);
            var $span = $this.find("span").eq(0);
            $span.removeClass("dwn");
            $span.addClass("nxt");
            hideHostP();
        });
    $("td#user").toggle(function () {
            var $this = $(this);
            var $span = $this.find("span").eq(0);
            $span.removeClass("nxt");
            $span.addClass("dwn");
            showUserP();
        },
        function () {
            var $this = $(this);
            var $span = $this.find("span").eq(0);
            $span.removeClass("dwn");
            $span.addClass("nxt");
            hideUserP();
        });
    hideHostP();
    hideUserP();
});
function hideHostP() {
    $("tr.host_p").hide();
}
function showHostP() {
    $("tr.host_p").show();
}
function hideUserP() {
    $("tr.user_p").hide();
}
function showUserP() {
    $("tr.user_p").show();
}
