import unittest
call_counter = 0

def reset_call_count():
    global call_counter
    call_counter = 0
    print call_counter
    
def call_count():
    return call_counter

def increment_call_count():
    global call_counter
    call_counter += 1


def subset_sum_extended(values,target):
    '''Return boolean array if the target is the sum of some subset of values
    
    Assume positive values only for now.
    Algorithm is from http://en.wikipedia.org/wiki/Subset_sum_problem
    '''

    def q(i,s,max_possible,min_possible,values,q_res):
        '''Return true if there is a non-empty subset of values[0:i-1] that sums to s

        Args:
            i: 1..len(values) (i.e. array index, base 1 - beware!)
            s: target value
            max_possible: sum of values
            min_possible: min of values
            q_res: dict to record result of function, indexed by (i,s)
        '''
        increment_call_count()
        if i == 0 or i > len(values):
            return False
        if s < min_possible or s > max_possible:
            return False
        if not (i,s) in q_res:
            #Either the subset before i matches the sum
            #in which case i isn't involved
            if q(i-1,s,max_possible,min_possible,values,q_res):
                elements_used[(i,s)] = list(elements_used[(i-1,s)])
                q_res[(i,s)] = True
            elif values[i-1] == s:
                #or the value at i matches the sum
                #in which case i is used
                elements_used[(i,s)] = no_elements_used
                elements_used[(i,s)][i-1] = True
                q_res[(i,s)] = True
            elif q(i-1,s-values[i-1],max_possible,min_possible,values,q_res):
                #or the subset before i + the value at i matches the sum
                #in which case i is used
                elements_used[(i,s)] = elements_used[(i-1,s-values[i-1])]
                elements_used[(i,s)][i-1] = True
                q_res[(i,s)] = True
            else:
                q_res[(i,s)] = False
                elements_used[(i,s)] = no_elements_used
        return q_res[(i,s)]    
    
    q_res = {}
    elements_used = {}
    no_elements_used = [False for _ in values]
     
    if not values:
        return False, None
    max_possible = sum(values)
    min_possible = min(values)
    if target > max_possible or target < min_possible:
        return False, None
    
    for s in range(1,max_possible+1):
        first_element_matches = (values[0] == s)
        q_res[(1,s)] = first_element_matches
        elements_used[(1,s)] = list(no_elements_used)
        if first_element_matches:
            elements_used[(1,s)][0] = True
#         print q_res[(1,s)]

    for i in range(2,len(values)+1):
        if q(i,target,max_possible,min_possible,values,q_res):
            return True, elements_used[(i,target)]
    return False,None

class TestSubsetSumExtended(unittest.TestCase):
    
    def test_empty_set(self):
        self.assertEquals(subset_sum_extended(values=[], target=10),(False,None))
       
    def test_sum_larger_than_max_possible(self):
        self.assertEquals(subset_sum_extended(values=[5,4], target=10),(False,None))
           
    def test_sum_smaller_than_min_possible(self):
        self.assertEquals(subset_sum_extended(values=[5,4,3,2], target=1),(False,None))
          
    def test_subset_is_first_value(self):
        self.assertEquals(subset_sum_extended(values=[7,8,9], target=7),(True,[True,False,False]))

    def test_subset_is_middle_value(self):
        self.assertEquals(subset_sum_extended(values=[7,8,9], target=8),(True,[False,True,False]))
             
    def test_subset_is_last_value(self):
        self.assertEquals(subset_sum_extended(values=[7,8,9], target=9),(True,[False,False,True]))
             
    def test_other_3_element_combinations(self):
        self.assertEquals(subset_sum_extended(values=[7,8,10], target=15),(True,[True,True,False]))
        self.assertEquals(subset_sum_extended(values=[7,8,10], target=17),(True,[True,False,True]))
        self.assertEquals(subset_sum_extended(values=[7,8,10], target=18),(True,[False,True,True]))
        self.assertEquals(subset_sum_extended(values=[7,8,10], target=25),(True,[True,True,True]))
      
    def test_impossible_total(self):
        reset_call_count()
        self.assertEquals(subset_sum_extended(values=[7,8,10], target=24),(False,None))
        print 'Call_count: %s' % call_count()
         
    def test_multiple_possibilities(self):
        self.assertEquals(subset_sum_extended(values=[7,7,7], target=14),(True,[True,True,False]))
         
    def test_big_one(self):
        values = [10 for _ in range(1,200)]
        expected_list = [True for _ in values]
        target = sum(values)
        reset_call_count()
        self.assertEquals(subset_sum_extended(values, target),(True,expected_list))
        print 'Call_count: %s' % call_count()
