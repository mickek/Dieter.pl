var show_datepicker = function(id){
	$(id).datepicker( 'show' );
}

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

	$("#weight_knob").weight_knob(save_weight_url, current_weight)
		
});