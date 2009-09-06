DietEditor = function(){
	
	this.decorate_html = function(){

		thiz = this;		
		
		$(".sortable").sortable();

		$(".meals ul li input[name='meal_name']").each(function(i,el){
			thiz._setup_meal_input(el);
		});
		
		$(".meals ul li input[name='meal_quantity']").each(function(i,el){
			thiz._setup_quantity_input(el);
		});
		
		$(".add_meal").each(function(i,el){
			thiz._setup_add_meal(el);
		});
		
		$(".remove_meal").each(function(i,el){
			thiz._setup_remove_button(el);
		});				
		
	};
	
	this.init = function(){
		
		var meals = $('.meals ul li');
		if( meals.size() > 0 ) ($(".add_meal[rel='breakfest']")[0]).focus();
		else this.add_meal('breakfest');
		
		this._setup_tab_index();
	},
	
	this.meal_types = {
		'breakfest': $('#breakfest'),
		'brunch': $('#brunch'),
		'lunch': $('#lunch'),
		'dinner': $('#dinner')
	},
	
	this.meal_types_seq = ['breakfest','brunch','lunch','dinner'];
	
	this._setup_meal_input = function(el){

		var thiz = this;
		$(el).autocomplete(products_autocomplete_url, {
			selectFirst: false
		});
		
		$(el).blur(function(){
			if($(this).attr('value')=='') {
				var meal = $(this).parent();
				console.log('onblur removing', meal);
				thiz.remove_meal(meal);
			}
		});
				
	};
	
	this._setup_quantity_input = function(el){
		
		thiz = this;
		$(el).blur(function(){
			var meal = $(this).parent();
			console.log('blur',this,meal.next().size());

			
//			if( new Meal(meal).get_meal_name().attr('value') == '' ){
//				thiz.remove_meal(meal);
//			}
//			
			if( meal.next().size() == 0 ){
				thiz.add_meal(meal.parent().attr('id'));
			}
		});		
	};
	
	this._setup_remove_button = function(el){
		var thiz = this;
		$(el).click(function(){
			thiz.remove_meal($(this).parent());
		});
	};
	
	this._setup_add_meal = function(el){
		var thiz = this;
		$(el).click(function(){
			thiz.add_meal($(this).attr('rel'));
		});
		
		$(el).focus(function(){
			console.log('focus',el);
		});
	};
	
	this.add_meal = function(meal_type){
		
		var meal_input = null, meal_quantity = null, meal_remove = null;
		$$('li',
			$$('input',{'type':'hidden','value':meal_type, 'name':'meal_type'}),
			meal_input = $$('input',{'type':'text','name':'meal_name','class':'meal_name'}),
			' ',
			meal_quantity = $$('input',{'type':'text','name':'meal_quantity','class':'meal_quantity'}),
			' ',
			meal_remove = $$('input.removal_meal',{'type':'button','name':'delete','value':'Usuń'})
		).appendTo(this.meal_types[meal_type]);
		
		console.log(this.meal_types[meal_type]);
		
		this._setup_meal_input(meal_input);
		this._setup_quantity_input(meal_quantity);
		this._setup_remove_button(meal_remove);
		meal_input.focus();
		this._setup_tab_index();
		
	};
	
	this.remove_meal = function(meal){

		var is_last = meal.next().size() == 0;
		var meal_type = meal.parent().attr('id');
		
		tabindex = new Meal(meal).get_meal_name().attr('tabindex');
		
		
		meal.remove();
		
		if( is_last ){
			
			var next_link = $('a[tabindex='+(parseInt(tabindex)+2)+']');
			if( next_link.size() > 0) next_link.focus();
			
//			var next_seq = this.meal_types_seq.indexOf(meal_type)+1;
//			if( next_seq < 4 ){
//				var meals = this.get_meals(this.meal_types_seq[next_seq]);
//				if( meals.length != 0) meals[0].get_meal_name().focus();
//				else this.add_meal(this.meal_types_seq[next_seq]);
//			}
		}
		
		this._setup_tab_index();
	};
	
	this.get_meals = function(meal_type){

		meals = [];
		meals_node = this.meal_types[meal_type].children();
		for(var i=0; i < meals_node.size(); i++) meals.push(new Meal(meals_node[i]));
		
		return meals;
		
	};
	
	this._setup_tab_index = function(){
		
		var index = 0;
		
		$(".meals").each(function(i,el){

			$(el).find('a').attr('tabindex',++index);			
			
			$(el).find("li input[type='text']").each(function(i,el){
				$(el).attr('tabindex',++index);
			});
			
		});
			
		$('#save_day').attr('tabindex',++index);
		$('#save_diet').attr('tabindex',++index);
		$('#send_diet').attr('tabindex',++index);
		
	};

	
};

Meal = function(node){
	this.node = node;
};

Meal.prototype = {
	
	get_meal_name : function(){
		return $($(this.node).children()[1]);
	},

	get_meal_quantity : function(){
		return $($(this.node).children()[2]);
	}
		
};

$(document).ready( function() {
	
	var editor = new DietEditor();
	editor.decorate_html();
	editor.init();
	
});