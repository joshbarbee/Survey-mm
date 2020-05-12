#order sensitive equivalent of difflib
#requires that all elements of l1=l2
def comp(l1,l2):
    count = 0
    for i, value in enumerate(l1):
        l2_index = l2.index(value)
        count += (abs(l2_index - i)**2)
    return (1/(1+count))**(1/len(l1))
