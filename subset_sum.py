import unittest
from collections import namedtuple

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
    
def subset_sum(values,target):
    '''Return True if the target is the sum of some subset of values
    
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
            #or the value at i matches the sum
            #or the subset before i + the value at i matches the sum
            q_res[(i,s)] = q(i-1,s,max_possible,min_possible,values,q_res) \
                            or values[i-1] == s \
                            or q(i-1,s-values[i-1],max_possible,min_possible,values,q_res)
        return q_res[(i,s)]    
    
    q_res = {}
     
    if not values:
        return False
    max_possible = sum(values)
    min_possible = min(values)
    if target > max_possible or target < min_possible:
        return False
    
    for s in range(1,max_possible+1):
        q_res[(1,s)] = (values[0]==s)
    for i in range(2,len(values)+1):
        if q(i,target,max_possible,min_possible,values,q_res):
            return True
    return False
    
class TestSubsetSum(unittest.TestCase):
    
    def test_empty_set(self):
        self.assertFalse(subset_sum(values=[], target=10))
      
    def test_sum_larger_than_max_possible(self):
        self.assertFalse(subset_sum(values=[5,4], target=10))
          
    def test_sum_smaller_than_min_possible(self):
        self.assertFalse(subset_sum(values=[5,4,3,2], target=1))
          
    def test_subset_is_first_value(self):
        self.assertTrue(subset_sum(values=[7,8,9], target=7))
          
    def test_subset_is_middle_value(self):
        self.assertTrue(subset_sum(values=[7,8,9], target=8))
            
    def test_subset_is_last_value(self):
        self.assertTrue(subset_sum(values=[7,8,9], target=9))
            
    def test_other_3_element_combinations(self):
        self.assertTrue(subset_sum(values=[7,8,10], target=15))
        self.assertTrue(subset_sum(values=[7,8,10], target=17))
        self.assertTrue(subset_sum(values=[7,8,10], target=18))
        self.assertTrue(subset_sum(values=[7,8,10], target=25))
     
    def test_impossible_total(self):
        reset_call_count()
        self.assertFalse(subset_sum(values=[7,8,10], target=24))
        print 'Call_count: %s' % call_count()
        
    def test_multiple_possibilities(self):
        self.assertTrue(subset_sum(values=[7,7,7], target=14))
        
    def test_big_one(self):
        values = [10 for i in range(1,200)]
        print values
        target = sum(values)
        reset_call_count()
        self.assertFalse(subset_sum(values, target=1989))
        print 'Call_count: %s' % call_count()

ValueWithReference = namedtuple('ValueWithReference',['reference','value'])
        
def subset_sum_references(values,target):
    '''return the set of references that describe the subset that sums to target
    
    Args:
        values: iterable of ValueWithReference
        target: sum
    
    Returns:
        set of references which define a subset that sums to target or None if
        no such subset exists
    '''
    return ['foo']
        
class TestSubsetSumWithIdentifiedMembers(unittest.TestCase):
    def test_single_match(self):
        values = [ValueWithReference('foo',1)]
        target = 1
        self.assertEqual(subset_sum_references(values,target), ['foo'])
