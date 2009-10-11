$(document).ready( function() {
		
	$(".diet").click(function(){
		
		var diet_id = $(this).attr('id');
		$('#details').load(details_url + diet_id + "/")
		$('.diet').removeClass('active');
		$(this).addClass('active');
	});
		
});