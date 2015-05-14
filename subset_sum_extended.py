import unittest
from collections import namedtuple
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

def subset_sum_fp(values, target):
    """Find a subset of values that sums to target
    
    Values are treated as 2 decimal place fixed-point numbers.
    """
    values = [int(value*100+0.001) for value in values]
    target = int(target*100)
    return subset_sum_extended(values,target)


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

ReconRecord = namedtuple('ReconRecord','date,description,amount')

def subset_objects(records, target, value_attr_name='amount'):
    """Return the subset of records that sum to target
    
    value_attr_amount defines the name of the attribute which will be 
    summed.
    
    Returns a list of records or None if no subset is found that
    sums to target.
    """
    found_records = []
    amounts = [getattr(record,value_attr_name) for record in records]
    found, records_in_sum = subset_sum_extended(amounts, target)
    if found:
        found_records = [record if used else None for used, record in zip(records_in_sum,records)]
        found_records = filter(lambda x: x is not None,found_records)
    return found_records
        
class TestSubsetSumWithObjects(unittest.TestCase):
 
    def test_one_record(self):
        records = [ReconRecord('1 Jan 15','nothing',10)]
        self.assertEqual(subset_objects(records,target=10), [ReconRecord('1 Jan 15','nothing',10)])
        
    def test_no_records(self):
        self.assertEqual(subset_objects([],target=10), [])

    def test_one_record_no_match(self):
        records = [ReconRecord('1 Jan 15','nothing',10)]
        self.assertEqual(subset_objects(records,target=9), [])

    def test_one_record_with_different_value_attribute(self):
        class Record(object):
            value = 11
        record = Record()
        self.assertEqual(subset_objects([record],target=11,value_attr_name='value'), 
                         [record])
        
    def test_matches_two_out_of_three(self):
        class Record(object):
            def __init__(self,amount):
                self.amount = amount
        records = [Record(1),Record(2),Record(4)]
        self.assertEqual(subset_objects(records,target=3), records[0:2])

class TestSubsetSumTwoDigitFixed(unittest.TestCase):
    def test_empty_set(self):
        self.assertEquals(subset_sum_fp(values=[], target=10.00),(False,None))
       
    def test_sum_larger_than_max_possible(self):
        self.assertEquals(subset_sum_fp(values=[5.11,4.22], target=10.0),(False,None))
            
    def test_sum_smaller_than_min_possible(self):
        self.assertEquals(subset_sum_fp(values=[5.1,4.1,3.1,2.1], target=1),(False,None))
         
    def test_subset_is_only_value(self):
        self.assertEquals(subset_sum_fp(values=[1.1], target=1.1),(True,[True]))

    def test_subset_is_first_value(self):
        self.assertEquals(subset_sum_fp(values=[7.11,8.99,9.76], target=7.11),(True,[True,False,False]))

    def test_subset_is_middle_value(self):
        self.assertEquals(subset_sum_fp(values=[7.11,8.22,9.33], target=8.22),(True,[False,True,False]))
              
    def test_subset_is_last_value(self):
        self.assertEquals(subset_sum_fp(values=[7.11,8.22,9.33], target=9.33),(True,[False,False,True]))
              
    def test_other_3_element_combinations(self):
        self.assertEquals(subset_sum_fp(values=[7.01,8.02,10.03], target=15.03),(True,[True,True,False]))
        self.assertEquals(subset_sum_fp(values=[7.01,8.02,10.03], target=17.04),(True,[True,False,True]))
        self.assertEquals(subset_sum_fp(values=[7.01,8.02,10.03], target=18.05),(True,[False,True,True]))
        self.assertEquals(subset_sum_fp(values=[7.01,8.02,10.03], target=25.06),(True,[True,True,True]))
       
    def test_impossible_total(self):
        reset_call_count()
        self.assertEquals(subset_sum_fp(values=[7.01,8.02,10.03], target=24.01),(False,None))
        print 'Call_count: %s' % call_count()
          
    def test_multiple_possibilities(self):
        self.assertEquals(subset_sum_fp(values=[7.11,7.11,7.11], target=14.22),(True,[True,True,False]))
          
    def test_big_one(self):
        values = [10.11 for _ in range(1,200)]
        expected_list = [True for _ in values]
        target = sum([int(value*100+0.001) for value in values])/100.0
        reset_call_count()
        self.assertEquals(subset_sum_fp(values, target),(True,expected_list))
        print 'Call_count: %s' % call_count()
