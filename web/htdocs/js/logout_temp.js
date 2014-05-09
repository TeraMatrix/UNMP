function unmp_logout()
{
	$.ajax({
			type:"post",
			url:"unmp_logout.py",
			success:function(result){
				if(result==0 || result == "0")
				{
					window.location.reload();
				}
				else
				{
					alert("There is some error in logout. Please Contact Your Administrator.");
				}
			}
		});
}
