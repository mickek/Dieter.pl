/**
 * Prosty plugin jquery tworzący płynne pole zmiany wagi.
 * Przykład użycia:
 *   $("#weight_knob").weight_knob('/dashboard/save_weight/2009/10/3/', 90.0)
 * Utworzy kontrolkę wewnątrz elementu #weight_knob wysyłającą informacje o zmianie wagi na: '', z wartością początkową 90.0
 * 
 * Po udanym zapisie wagi wysyłana jest wiadomość za pomocą jGrowl
 * 
 * @endpoint_url adres url na który ma być wysyłane post z informacją o zmianie wagi
 * @current_weight wartość początkowa
 */

(function($) {
	
	function save_weight(el,endpoint){
		var current_weight = parseFloat($(el).attr('value'));
		$.post(endpoint, {'weight': current_weight}, function(){
			$.jGrowl("Zapisano wagę", { life: 500 });
		},"text");
	}

	function go_up(el){
		if($(el).attr('going_up')){
			current_weight = parseFloat($(el).attr('value'));
			$(el).attr('value', (current_weight+0.1).toFixed(1));
			setTimeout(go_up, 100);
		}
	}

	function go_down(el){
		if($(el).attr('going_down')){
			current_weight = parseFloat($(el).attr('value'));
			$(el).attr('value', (current_weight-0.1).toFixed(1));
			setTimeout(go_down, 100);
		}
	}

	function start_weight_up(el){
		el.attr('going_up',true);
		go_up(el);	
	}

	function start_weight_down(el){
		el.attr('going_down',true);
		go_down(el);
	}	
	
    $.fn.extend({
        weight_knob: function(endpoint_url, current_weight) {
    	
    		return this.each(function(){
    			
    			var el = this;
    			
    			$(this).attr('going_up',false);
    			$(this).attr('going_down',false);

				var weight_up = $$('a','+', {'href':'javascript:void(0);'}).appendTo(this);
				var weight = $$('input',{'value':current_weight}).appendTo(this);
				var weight_down = $$('a','-',{'href':'javascript:void(0);'}).appendTo(this);

    			
    			$(weight_up).mousedown( function(){
    				start_weight_up(weight);
    			});
    		
	    		$(weight_up).mouseup( function(){
	    			going_up = false;
	    			save_weight(weight,endpoint_url);
	    		});
    		
	    		$(weight_down).mousedown( function(){
	    			start_weight_down(weight);
	    		});
    		
	    		$(weight_down).mouseup( function(){
	    			going_down = false;
	    			save_weight(weight,endpoint_url);
	    		});	    			
    			
    		});
        }
    
    });
})(jQuery);