var meal_types = ['breakfest','brunch','lunch','dinner'];

function setup_tab_index(){

	var index = 0;
	
	$(".meals").each(function(i,el){

		$(el).find("li input[type='text']").each(function(i,el){
			$(el).attr('tabindex',++index);
		});
		
		$(el).find('a').attr('tabindex',++index);
		
	});
		
	$('#save_day').attr('tabindex',++index);
	$('#save_diet').attr('tabindex',++index);
	$('#send_diet').attr('tabindex',++index);
	
}

function focus_first_input(){
	if( typeof $(".meals ul li input[type='text']")[0] == "undefined" ){
		add_meal('breakfest');
	}else{
		$(".meals ul li input[type='text']")[0].focus();
	}
}

function remove_button_action(){

	var parent = $(this).parent();
	
	/* get focus on first input before */
	var previous = parent.prev().children()[1];
	if( previous ) previous.focus();
	else focus_first_input();

	parent.remove();
	setup_tab_index();
}

function remove_meal(li, focus){
	
	/* get focus on first input before */
	var previous = li.prev().children()[1];
	if( previous) previous.focus();
	else focus_first_input();

	li.remove();
	setup_tab_index();
	
}

function setup_autocomplete(el){
	$(el).autocomplete(products_autocomplete_url, {
		selectFirst: false
	});
	
//	$(el).blur(function(e){
//		if($(this).attr('value')==''){
//			console.log(e)
//			var current_meal_type = $(this).parent().parent().attr('id');
//			remove_meal($(this).parent(),false);
//			add_meal(meal_types[meal_types.indexOf(current_meal_type)+1]);
//			
//		}
//	});
}

function setup_meal_quantity(el){
	
	$(el).focus( function(){
		if( $(this).prev().attr('value') == '' ){
			var current_meal_type = $(this).parent().parent().attr('id');
			remove_meal($(this).parent());
			add_meal(meal_types[meal_types.indexOf(current_meal_type)+1]);
		}
	});
}

function add_meal(meal_type){

	var el = $('#'+meal_type);
	var meal_name = null, meal_quantity = null;
	$$('li',
		$$('input',{'type':'hidden','value':meal_type, 'name':'meal_type'}),
		meal_name = $$('input',{'type':'text','name':'meal_name','class':'meal_name'}),
		' ',
		meal_quantity = $$('input',{'type':'text','name':'meal_quantity','class':'meal_quantity'}),
		' ',
		$$('input.removal_meal',{'type':'button','name':'delete','value':'Usuń',click:remove_button_action})
	).appendTo(el);
	
	
	setup_autocomplete(meal_name);
	//setup_meal_quantity(meal_quantity);
	meal_name.focus();
	setup_tab_index();

}


$(document).ready( function() {

	$(".sortable").sortable();
	
	$(".remove_meal").click(remove_button_action);
	
	$(".meals ul li input[name='meal_name']").each(function(i,el){
		setup_autocomplete(el);
	});
	
	$(".meals ul li input[name='meal_quantity']").each(function(i,el){
		//setup_meal_quantity(el);
	});
	
	
	$(".add_meal").click(function(){
		add_meal($(this).attr('rel'));
	});
	
	$(".add_meal").focus(function(){
		
		//if(typeof $('#'+$(this).attr('rel')).children()[0] == 'undefined'){
			//add_meal($(this).attr('rel'));
		//}else{
			//$($('#'+$(this).attr('rel')).children()[0]).children()[0].focus()
//		//}
		
		
	});
	
	
	setup_tab_index();
	focus_first_input();
	
});