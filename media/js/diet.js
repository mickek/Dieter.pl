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
		if( meals.size() == 0 )  this.add_meal('breakfest');
		
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
				
		/**
		 * Overriding tab and shift-tab logic for meal name
		 */
		$(el).keydown(function(event){
			
			if(event.keyCode == 9){
				
				var meal = $(this).parent();
				
				/**
				 * Moving right
				 */
				if(!event.shiftKey){
					
					if( meal.next().size() == 0 ){
						var meal_type = meal.parent().attr('id');
						if( new Meal(meal).get_meal_name().attr('value') == '' ){	// if meal name is empty removing meal
							event.preventDefault();							
							var next_seq = thiz.meal_types_seq.indexOf(meal_type)+1;
							if( next_seq < 4 ){	// if there's next section ahead moving to it
								
								var meals = thiz.get_meals(thiz.meal_types_seq[next_seq]);
								thiz.remove_meal(meal);
								// if there are meals in next section we should focus on first meal
								if(thiz.meal_types[thiz.meal_types_seq[next_seq]].children().size()!=0){
									new Meal(thiz.meal_types[thiz.meal_types_seq[next_seq]].children()[0]).get_meal_name().focus();
								}else{
									console.log('should add new meal')
									thiz.add_meal(thiz.meal_types_seq[next_seq]);
								}
								
								
							}else{	// no next section moving focus to first meal
								thiz.remove_meal(meal);
								if( $('input.meal_name').size() > 0){
									$('input.meal_name')[0].focus();
								}else{
									thiz.add_meal(thiz.meal_types_seq[0]);	// creating first meal
								}
							}
						}
					}
					
				/**
				 * Moving left
				 */	
				}else{
					
					if( new Meal(meal).get_meal_name().attr('value') == '' ){	// meal input is empty should remove it
						event.preventDefault();
						if( meal.prev().size() == 0 ){	// removing it and going to previous meal type
							var meal_type = meal.parent().attr('id');
							var next_seq = thiz.meal_types_seq.indexOf(meal_type)-1;
							if( next_seq > -1 ){
								var meals = thiz.get_meals(thiz.meal_types_seq[next_seq]);
								thiz.remove_meal(meal);
								thiz.add_meal(thiz.meal_types_seq[next_seq]);
							}							
						}else{	// there are other meals on left, focusing on previous meal name, and removing empty meal
							new Meal(meal.prev()).get_meal_name().focus();
							thiz.remove_meal(meal);
						}
					}else if (meal.prev().size() != 0){	// this meal is not empty, focusing on previous meal name
						event.preventDefault();
						(new Meal(meal.prev())).get_meal_name().focus();
					}
					
				}
			}
		});
				
	};
	
	this._setup_quantity_input = function(el){
		
		thiz = this;
		
		/**
		 * Overriding tab and shift-tab logic for meal quantity
		 */
		$(el).keydown(function(event){
			
			if(event.keyCode == 9){
				
				var meal = $(this).parent();
				
				/**
				 * move right
				 */
				if(!event.shiftKey){
					console.log('next',$(this).parent());
					if( meal.next().size() == 0 ){ // no more meals on right ( last meal in section )
						event.preventDefault();							
						var meal_type = meal.parent().attr('id');
						if( new Meal(meal).get_meal_name().attr('value') != '' ){	// this meal is filled, adding next meal in the same section
							thiz.add_meal(meal_type);
						}else{	// this meal was empty removing it
							thiz.remove_meal(meal);
							var next_seq = thiz.meal_types_seq.indexOf(meal_type)+1;
							if( next_seq < 4 ){	// adding new meal in next section
								var meals = thiz.get_meals(thiz.meal_types_seq[next_seq]);
								
								// if there are meals in next section we should focus on first meal
								if(thiz.meal_types[thiz.meal_types_seq[next_seq]].children().size()!=0){
									new Meal(thiz.meal_types[thiz.meal_types_seq[next_seq]].children()[0]).get_meal_name().focus();
								}else{
									thiz.add_meal(thiz.meal_types_seq[next_seq]);
								}

							}else{	// this meal was in last section, moving focus to first meal
								if( $('input.meal_name').size() > 0){
									$('input.meal_name')[0].focus();	// focus on existing meal
								}else{
									thiz.add_meal(thiz.meal_types_seq[0]);	// adding new meal
								}
							}
						}
					}
					
				}
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
		
		this._setup_meal_input(meal_input);
		this._setup_quantity_input(meal_quantity);
		this._setup_remove_button(meal_remove);
		meal_input[0].focus();
		this._setup_tab_index();
		
		return meal_input;
		
	};
	
	this.remove_meal = function(meal){

		var is_last = meal.next().size() == 0;
		var meal_type = meal.parent().attr('id');
		meal.remove();
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