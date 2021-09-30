import mm_ci_ag as cm 

def abs_factors(p1,p2,matrix):
    #absolute factors that make or break the algo and mm
    #includes what gender u are looking for and what they are looking for
    #for location, problems were caused because people dont know lat/long so couldn't use it
    #but api's that let me search city names for lat/long dont permit enough requests - defeats purpose of multithreading
    #and using a local db would take too long to search, because it would be sequential, O(n)
    #so just using zip codes - extremely accurate for populated areas but can lead to matches 1.5hr+ away when far away from city
    #80% of people are properly accounted for then, urban areas, but # is biggest due to measured audience
    #because of how python deals with and statements, we lose a lot of runtime by condensing into 1 line, but it is messy
    #i really hate it honestly, but it is the most efficent, since once 1 condition is wrong it will cut off instead of checking every one
    return age_approximate(matrix["Age"][p1],matrix["Age"][p2]) == True and gender_match(matrix["Gender"][p1], matrix["Gender"][p2], matrix["LF"][p1], matrix["LF"][p2]) == True and zip_match(matrix["Location"][p1], matrix["Location"][p2]) == True

def moderate_factors(p1,p2,matrix):
    match_score = 0
    s_score = one_zero_weighed(matrix["Similar_hobbies"][p1], matrix["Similar_hobbies"][p2])
    l_score = looks(matrix["Looks"][p1], matrix["Looks"][p2])
    match_score = (d_score+s_score+l_score)/3
    return match_score 

def loose_factors(p1,p2,matrix):
    #gets scores for importance factor, partying, and intro/extroversion and weights them in an unbalanced manner, then scaled to one
    imp_fact = importance_factor(matrix["Importance_Factor"][p1],matrix["Importance_Factor"][p2])
    part_fact = z_o_t(matrix["Party"][p1],matrix["Party"][p2])
    ie_fact = one_zero_weighed(matrix["Vert"][p1],matrix["Vert"][p2])
    return (.6*imp_fact + .2*part_fact + .2*ie_fact)/3 + (2/3)

#strict parsers
def age_approximate(a1,a2):
    #must be within 1 year
    if abs(a1-a2) > 1:
        return False
    return True

def gender_match(g1,g2,pref1,pref2):
    #ensures you only match with those who you asked to be
    if pref1 != g2 and pref2 != g1:
        return False
    return True

def zip_match(zip1,zip2):
    #formats zips to make them all standard length, then cuts off last two digits of zip
    zip1_standardized = str(f'{zip1}:0>5')
    zip2_standardized = str(f'{zip2}:0>5')
    if zip1_standardized[0:2] != zip2_standardized[0:2]:
        return False
    return True

#moderate parses
def looks(p1,p2):
    #uses custom scale, otherwise i would use z_o_t, may in future attempt to use kwargs so that i can use z_o_t and pass a custom amount of variables in for scaling 
    if abs(p1-p2) == 0:
        return 1
    if abs(p1-p2) == 1:
        return .75
    if abs(p1-p2) == 2:
        return .5
    return 0

#loose parsers
def importance_factor(p1,p2):
    #converts importance factors into a list, was having weird compatability problems at first, idk why, but then just used split
    list_p1 = list(p1.split(","))
    list_p2 = list(p2.split(","))
    similarity_factor = cm.comp(list_p1,list_p2)
    return similarity_factor

def z_o_t(p1,p2):
    #converts scores to either a zero score, one score, or two, and weighs them
    if abs(p1-p2) == 0:
        return 1
    if abs(p1-p2) == 1:
        return .5
    if abs(p1-p2) == 2:
        return 0

def one_zero_weighed(p1,p2):
    #same thing as z_o_t but only with 1,0 and checks boolean
    if p1 == p2:
        return 1
    if p1 != p2:
        return 0

def strict_parser(matrix, match_dict):
    #for every value in the matrix, it runs it against absolute factors and removes from potential matches if it fails an abs match
    for k, v in matrix["Age"].items():
        temp = []
        for key, value in matrix["Age"].items():
            if abs_factors(k,key, matrix) and k != key:
                temp.append(key)
        match_dict[k] = temp
    return match_dict
    
def main_parser(matrix):
    #after calling strict, it runs every potential match agaisnt moderate and loose and then weights them on 2:1 scale.
    match_dict = {}
    stricted_dict = strict_parser(matrix,match_dict)
    #print(stricted_dict)
    purged_dict = {}
    for k,v in stricted_dict.items():
        if v != []:
            t_list = []
            for i in v:
                mf_value = (moderate_factors(k,i,matrix))*2/3
                lf_value = (loose_factors(k,i,matrix))*1/3
                t_list.append((matrix["Username"][i],mf_value+lf_value))
            purged_dict[k] = t_list
    print(purged_dict)
    return purged_dict
