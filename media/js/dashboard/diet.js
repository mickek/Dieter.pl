$(document).ready( function() {
		
	$("#requested_day").datepicker({
		defaultDate: requested_day,
		gotoCurrent: true,
		maxDate: '+0d',
		dateFormat: 'yy/mm/dd',
		onSelect: function(dateText, inst) {
			window.location=dashboard_url+dateText;
		}
	});
	
});