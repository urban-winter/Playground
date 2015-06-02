import unittest

def pop_least(list1,list2):
    """return the smaller element from two ordered lists, and remove it
    
    If an element is the same in both lists then it is returned and removed
    from both list which effectively deduplicates when called successively
    to merge two ordered lists.
    """
    if list1[0] < list2[0]:
        return list1.pop(0)
    if list2[0] < list1[0]:
        return list2.pop(0)
    list1.pop(0)
    return list2.pop(0)

def merge_sorted_lists(sorted_list, additional_terms_sorted):
    """merge two ascending lists"""
    retlist = []
    finished = False
    while not finished:
        if not sorted_list:
            retlist.extend(additional_terms_sorted)
            finished = True
        elif not additional_terms_sorted:
            retlist.extend(sorted_list)
            finished = True
        else:
            retlist.append(pop_least(sorted_list,additional_terms_sorted))
    return retlist


def add_term_to_sorted_list(sorted_list, term):
    """
    From Wikipedia:
    However, given a sorted list of sums for k elements, the list can be expanded to two 
    sorted lists with the introduction of a (k + 1)st element, and these two sorted lists 
    can be merged in time O(2k)
    """
    if not sorted_list:
        return [term]
    additional_terms_sorted = [term]
    additional_terms_sorted.extend([x + term for x in sorted_list])
    return merge_sorted_lists(sorted_list, additional_terms_sorted)

class TestAddTermToSortedList(unittest.TestCase):
    def test_length_zero(self):
        result = add_term_to_sorted_list([],1)
        self.assertEqual(result, [1])

    def test_length_one(self):
        result = add_term_to_sorted_list([3],4)
        self.assertEqual(result, [3,4,7])    
        
    def test_length_two(self):
        result = add_term_to_sorted_list([3,4,7],5)
        self.assertEqual(result, [3,4,5,7,8,9,12])
        
    def test_duplicates_are_removed(self):
        result = add_term_to_sorted_list([1],1)
        self.assertEqual(result, [1,2])

def sums_for_all_combinations(values):
    """returns sorted list of all combination sums with dups removed"""
    sums = []
    for value in values:
        sums = add_term_to_sorted_list(sums, value)
    return sums        
        
def subset_sum_exponential_time(values, target):
    if len(values) == 1:
        return values[0] == target
    #split values list in half
    midpoint = len(values)/2
    values1 = values[0:midpoint]
    values2 = values[midpoint:]
    #generate all combination sums for each list, sorted
    sums1 = sums_for_all_combinations(values1)
    sums2 = sums_for_all_combinations(values2)
    if target in sums2:
        return True
    #iterate through both results, one up, one down and check for target
    for sum1 in reversed(sums1):
        for sum2 in sums2:
            if sum1 == target or sum1 + sum2 == target:
                return True
            if sum1 + sum2 > target:
                break
    return False

class TestSubsetSumExtended(unittest.TestCase):
    
    def test_empty_set(self):
        self.assertFalse(subset_sum_exponential_time(values=[], target=10))
       
    def test_sum_larger_than_max_possible(self):
        self.assertFalse(subset_sum_exponential_time(values=[5,4], target=10))
            
    def test_sum_smaller_than_min_possible(self):
        self.assertFalse(subset_sum_exponential_time(values=[5,4,3,2], target=1))
         
    def test_subset_is_only_value(self):
        self.assertTrue(subset_sum_exponential_time(values=[1], target=1))
           
    def test_subset_is_first_value(self):
        self.assertTrue(subset_sum_exponential_time(values=[7,8,9], target=7))
 
    def test_subset_is_middle_value(self):
        self.assertTrue(subset_sum_exponential_time(values=[7,8,9], target=8))
              
    def test_subset_is_last_value(self):
        self.assertTrue(subset_sum_exponential_time(values=[7,8,9], target=9))
              
    def test_other_3_element_combinations(self):
        self.assertTrue(subset_sum_exponential_time(values=[7,8,10], target=15))
        self.assertTrue(subset_sum_exponential_time(values=[7,8,10], target=17))
        self.assertTrue(subset_sum_exponential_time(values=[7,8,10], target=18))
        self.assertTrue(subset_sum_exponential_time(values=[7,8,10], target=25))
       
    def test_impossible_total(self):
        self.assertFalse(subset_sum_exponential_time(values=[7,8,10], target=24))
          
    def test_multiple_possibilities(self):
        self.assertTrue(subset_sum_exponential_time(values=[7,7,7], target=14))
          
    def test_big_one(self):
        values = [10 for _ in range(200)]
        target = sum(values)
        self.assertTrue(subset_sum_exponential_time(values, target))
        
# TODO: Random subset tester
# Generate set of random numbers then generate subset sum from random subset

        