$(document).ready( function() {

	$(".sortable").sortable()
	
	$(".remove_meal").click(function(){
		$(this).parent().remove()
	})
	
	$(".add_meal").click(function(){
		
		var rel = $(this).attr('rel')
		$(rel).append( '<li><input type="text" name="meal_name" value=""/><input type="text" name="meal_quantity" value=""/><input type="button" name="delete" class="remove_meal" value="Usuń"/></li>')
		alert('a')
		
	})
	
});