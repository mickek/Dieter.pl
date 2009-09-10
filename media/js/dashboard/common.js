$(document).ready(function(){
	
	$("#set_start_date").dialog({
		title: "Ustal datę startu diety",
		modal: true,
		autoOpen: false,
		height: 500,
		width: 500,
		open: function() {
			$("#set_start_date").load( set_diet_start_date_url );
		},
		close: function(event, ui) {
			$("#id_start_date").datepicker('hide');
		}
    }); 
	
	$('.open_set_start_day_dialog').click(function(){
		$('#set_start_date').dialog("open");
	});	
	
});