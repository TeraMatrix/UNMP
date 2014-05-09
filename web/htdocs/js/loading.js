$.fn.loading_div = function(time,msg,start,color){
	if(color == null)
		color = "#B3F83D";
	return this.each(function()
	{
		var lDiv = $(this);
		lDiv.html("");
		$("<div id=\"loadingSms\">" + msg + "</div>").appendTo(lDiv);
		$("<div id=\"infoProgress\">" + start + "%</div>").appendTo(lDiv);
		$("<br class=\"clear\" />").appendTo(lDiv);
		$("<div id=\"loadingBar\"><div id=\"progressBar\" style=\"width: " + start + "%;background-color:" + color + "\"></div></div>").appendTo(lDiv);
		update($(this),start,time);
	});
	function update(obj,val,time)
	{
		if(val <100)
		{
			val++;
			obj.find("#infoProgress").html(val + "%");
			obj.find("#progressBar").css("width",(val + "%"));
			setTimeout(function(){update(obj,val,time);},(time/100));
		}
		
	}
};
/*
$(function(){
	$("#loading_div").loading_div(10000,"LOADING",0,null);
	setTimeout(function(){$("#update_div").loading_div(4000,"UPDATING",0,"green");},11000);
	setTimeout(function(){$("#activate_div").loading_div(1000,"ACTIVATE",0,"yellow");},15000);
});
*/
