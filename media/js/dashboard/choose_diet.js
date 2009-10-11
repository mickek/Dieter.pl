$(document).ready( function() {
		
	$(".diet").click(function(){
		
		var diet_id = $(this).attr('id');
		$('#details').load(details_url + diet_id + "/")
	});
		
});