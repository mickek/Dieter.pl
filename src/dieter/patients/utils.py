from dieter.utils import today


def approximate_user_data(user_data_list, field = 'weight', extend_left=None):
    """
    Gets a user data list witch doesn't have to be consistent and transforms it into
    consisten values list with either weight, bmi or waist values
    
    Approximates only gaps in data, if there's no data in the beginning or in the end it leavs them
    """
    
    if len(user_data_list) == 0: return None

    min_date = min(user_data_list).date
    max_date = max(user_data_list).date
    
    days = (max_date - min_date).days+1
    values = [ 0 for i in range(days) ]
    
    # build consistent value list with zeroes where there's no data
    for ud in user_data_list:
        index = (ud.date - min_date).days
        val = getattr(ud, field)
        if val and val != 0: values[index] = val
    
    # determine consistent no values areas
    approximation_areas = []
    current_area = []
    for i,v in enumerate(values):

        if v == 0:  # checking if theres lack of data
            if current_area == []: current_area.append(i)
            else:
                if current_area[len(current_area)-1]+1 == i: # consistent area
                    current_area.append(i)
                else:
                    approximation_areas.append(current_area)
                    current_area = [i]

    # adding last area
    if current_area != []: approximation_areas.append(current_area)

    min_index = 0 
    max_index = days-1
    
    # now doing the linear approximation
    for approximation_area in approximation_areas:
        #approximating all areas except for those  with begining index or ending index
        border_values = filter(lambda e: e in [min_index, max_index], approximation_area)        
        if border_values == []:
            size = len(approximation_area)  # area size
            start_value = values[approximation_area[0]-1] 
            end_value = values[approximation_area[size-1]+1]
            approximation_step = (end_value - start_value)/(size+1)
            
            for i,index in enumerate(approximation_area):
                values[index] = start_value + approximation_step*(i+1)
        elif border_values == [min_index]:
            # set first weight
            weight = values[approximation_area[len(approximation_area)-1]+1]
            for index in approximation_area: values[index] = weight
        elif border_values == [max_index]:
            # set last weight
            weight = values[approximation_area[0]-1]
            for index in approximation_area: values[index] = weight
            pass 
        
    if extend_left and len(values) < extend_left:
        extended_values = [ values[0] for i in range(extend_left-len(values)) ]
        for v in values: extended_values.append(v)
        return extended_values
            
    return values

def approximate_user_data_for_date(user_data_list, field = 'weight', day = today()):
    
    if len(user_data_list) == 0: return None

    min_day = min(user_data_list).date
    index = (day - min_day).days
    approximated_data = approximate_user_data(user_data_list, field)
    
    if index < 0: index = 0
    if index > len(approximated_data)-1: index = len(approximated_data)-1 
    
    return approximated_data[index]
    