import unittest
call_counter = 0

def reset_call_count():
    global call_counter
    call_counter = 0

def call_count():
    return call_counter

def increment_call_count():
    global call_counter
    call_counter += 1

class SubsetFinder(object):
    """Find the subset that sums to a target value
    
    The algorithm is from http://en.wikipedia.org/wiki/Subset_sum_problem.
    """
    
    def __init__(self, values, target):
        """Initialise with list of values and target value for sum of subset
        """
        self.values = values
        self.target = target
        # dict to memoise return values from function q(i,s)
        self.q_res = {} 
        # dict, indexed by (i,s) stores list of bool, showing which elements
        # are used in sum s
        self.elements_used = {} 
        # initial value for elements_used - all False
        self.no_elements_used = [False for _ in values]
        self.subset_found = False
        self.subset_members = None
        self._find_subset()
        
    def subset_exists(self):
        """Return True is a subset has been found
        """
        return self.subset_found
    
    def subset_contents(self):
        """Return a list of bool, True indicates that corresponding element is in the subset
        """
        return self.subset_members

    def _find_subset(self):
        if not self.values:
            return #empty list cannot contain a subset
        self.max_possible = sum(self.values)
        self.min_possible = min(self.values)
        if self.target > self.max_possible or self.target < self.min_possible:
            return #target less than min or more than max - no possible subset

        self._initial_pass()
    
        for i in range(1,len(self.values)+1):
            if self.q(i,self.target):
                self.subset_found = True
                self.subset_members = self.elements_used[(i,self.target)]
                return # subset found - stop looking
        return # finished looking - no subset found

    def _initial_pass(self):
        for s in range(1,self.max_possible+1):
            first_element_matches = (self.values[0] == s)
            self.q_res[(1,s)] = first_element_matches
            self.elements_used[(1,s)] = list(self.no_elements_used)
            if first_element_matches:
                self.elements_used[(1,s)][0] = True

    def q(self,i,s):
        '''Return true if there is a non-empty subset of values[0:i-1] that sums to s

        Args:
            i: 1..len(values) (i.e. array index, base 1 - beware!)
            s: target value
            max_possible: sum of values
            min_possible: min of values
            q_res: dict to record result of function, indexed by (i,s)
        '''
        increment_call_count()
        if i == 0 or i > len(self.values):
            return False
        if s < self.min_possible or s > self.max_possible:
            return False
        if not (i,s) in self.q_res:
            #Either the subset before i matches the sum
            #in which case i isn't involved
            if self.q(i-1,s):
                self.elements_used[(i,s)] = list(self.elements_used[(i-1,s)])
                self.q_res[(i,s)] = True
            elif self.values[i-1] == s:
                #or the value at i matches the sum
                #in which case i is used
                self.elements_used[(i,s)] = self.no_elements_used
                self.elements_used[(i,s)][i-1] = True
                self.q_res[(i,s)] = True
            elif self.q(i-1,s-self.values[i-1]):
                #or the subset before i + the value at i matches the sum
                #in which case i is used
                self.elements_used[(i,s)] = self.elements_used[(i-1,s-self.values[i-1])]
                self.elements_used[(i,s)][i-1] = True
                self.q_res[(i,s)] = True
            else:
                self.q_res[(i,s)] = False
                self.elements_used[(i,s)] = self.no_elements_used
        return self.q_res[(i,s)]    
       
def subset_sum_extended(values,target):
    ssf = SubsetFinder(values, target)
    return ssf.subset_exists(), ssf.subset_contents()

def subset_sum(values,target):
    retval, _ = subset_sum_extended(values, target)
    return retval


class TestSubsetSumExtended(unittest.TestCase):
    
    def test_empty_set(self):
        self.assertEquals(subset_sum_extended(values=[], target=10),(False,None))
       
    def test_sum_larger_than_max_possible(self):
        self.assertEquals(subset_sum_extended(values=[5,4], target=10),(False,None))
           
    def test_sum_smaller_than_min_possible(self):
        self.assertEquals(subset_sum_extended(values=[5,4,3,2], target=1),(False,None))
        
    def test_subset_is_only_value(self):
        self.assertEquals(subset_sum_extended(values=[1], target=1),(True,[True]))
          
    def test_subset_is_first_value(self):
        self.assertEquals(subset_sum_extended(values=[7,8,9], target=7),(True,[True,False,False]))
        s = SubsetFinder(values=[7,8,9], target=7)
        self.assertEqual(s.subset_exists(), True)
        self.assertEqual(s.subset_contents(), [True,False,False])

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
