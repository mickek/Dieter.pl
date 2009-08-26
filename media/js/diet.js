function setup_tab_index(){

	var index = 0;
	$(".meals ul li input[type='text']").each(function(i,el){
		$(el).attr('tabindex',i+1)
		index++;
	})
	
	$('#save_day').attr('tabindex',++index)
	$('#save_diet').attr('tabindex',++index)
	$('#send_diet').attr('tabindex',++index)
	
}

function focus_first_input(){
	$(".meals ul li input[type='text']")[0].focus()
}

function remove_button_action(){
	
	var previous = $(this).parent().prev().children()[1]
	if( previous ) previous.focus()
	else focus_first_input()

	$(this).parent().remove()
	setup_tab_index()
}

function setup_autocomplete(el){
	$(el).autocomplete(products_autocomplete_url, {
		selectFirst: false
	});
	

}


$(document).ready( function() {

	$(".sortable").sortable()
	
	$(".remove_meal").click(remove_button_action)
	
	$(".meals ul li input[name='meal_name']").each(function(i,el){
		setup_autocomplete(el)
	})
	
	$(".add_meal").click(function(){
	
		var meal_type = $(this).attr('rel')
		var el = $('#'+meal_type)
		var meal_name = null
		$$('li',
			$$('input',{'type':'hidden','value':meal_type, 'name':'meal_type'}),
			meal_name = $$('input',{'type':'text','name':'meal_name'}),
			' ',
			$$('input',{'type':'text','name':'meal_quantity'}),
			' ',
			$$('input.removal_meal',{'type':'button','name':'delete','value':'Usuń',click:remove_button_action})
		).appendTo(el)
		
		
		setup_autocomplete(meal_name)
		meal_name.focus()
		setup_tab_index()

	})
	
	setup_tab_index()
	focus_first_input()
	
});