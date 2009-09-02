going_up = false;
going_down = false;

function save_weight(){
	
	var current_weight = parseFloat($('#id_weight').attr('value'));
	$.post(save_weight_url, {'weight': current_weight}, function(){},"text");
}

function go_up(){

	if(going_up){
		current_weight = parseFloat($('#id_weight').attr('value'));
		$('#id_weight').attr('value', (current_weight+0.1).toFixed(1));
		setTimeout(go_up, 100);
	}
	
}

function go_down(){

	if(going_down){
		current_weight = parseFloat($('#id_weight').attr('value'));
		$('#id_weight').attr('value', (current_weight-0.1).toFixed(1));
		setTimeout(go_down, 100);
	}
	
}


function start_weight_up(){

	going_up = true;
	go_up();
	
}

function start_weight_down(){

	going_down = true;
	go_down();
	
}


$(document).ready( function() {
	
	$('#weight_up').mousedown( function(){
		start_weight_up();
	});
	
	$('#weight_up').mouseup( function(){
		going_up = false;
		save_weight();
	});
	
	$('#weight_down').mousedown( function(){
		start_weight_down();
	});
	
	$('#weight_down').mouseup( function(){
		going_down = false;
		save_weight();
	});	
	
	
});