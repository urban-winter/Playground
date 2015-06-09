import unittest
import random
import time

class CombinationSum():
    """A subset sum
    
    The sum is formed by combining members of a set.
    self.value is the value of the sum
    self.elements is a list of boolean indicating which elements of the set
        were included in the sum
    """
    def __init__(self,value,elements):
        self.value = value
        self.elements = elements
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    def __ne__(self, other):
        return not self.__eq__(other)

def pop_least(list1,list2):
    """return the smaller element from two ordered lists, and remove it
    
    If an element is the same in both lists then it is returned and removed
    from both list which effectively deduplicates when called successively
    to merge two ordered lists.
    """
    if list1[0].value < list2[0].value:
        return list1.pop(0)
    if list2[0].value < list1[0].value:
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
    sorted_list - list of CombinationSum, all should have same number of elements
    term - the next element
    From Wikipedia:
    However, given a sorted list of sums for k elements, the list can be expanded to two 
    sorted lists with the introduction of a (k + 1)st element, and these two sorted lists 
    can be merged in time O(2k)
    """
    no_elements_used = [False for _ in range(len(sorted_list[0].elements))] if sorted_list else []
    elements_used = no_elements_used
    elements_used.append(True)   
    additional_terms_sorted = [CombinationSum(term, elements_used)]
    if not sorted_list:
        return additional_terms_sorted
#     additional_terms_sorted.extend([CombinationSum(x.value + term) for x in sorted_list])
    for a_sum in sorted_list:
        elements_used = list(a_sum.elements)
        elements_used.append(True)
        additional_terms_sorted.append(CombinationSum(a_sum.value + term, elements_used))
        a_sum.elements.append(False)
    return merge_sorted_lists(sorted_list, additional_terms_sorted)

class TestAddTermToSortedList(unittest.TestCase):

    def test_length_zero(self):
        result = add_term_to_sorted_list([],1)
        self.assertEqual(result, [CombinationSum(1,[True,])])

    def test_length_one(self):
        start = [CombinationSum(3,[True])]
        result = add_term_to_sorted_list(start,4)
        expected = [CombinationSum(3,[True,False]),
                    CombinationSum(4,[False,True]),
                    CombinationSum(7,[True,True])]
        self.assertEqual(result, expected)
        
    def test_length_two(self):
        start = [CombinationSum(3,[True,False]),
                 CombinationSum(4,[False,True]),
                 CombinationSum(7,[True,True])]
        result = add_term_to_sorted_list(start,5)
        expected = [CombinationSum(3,[True,False,False]),
                    CombinationSum(4,[False,True,False]),
                    CombinationSum(5,[False,False,True]),
                    CombinationSum(7,[True,True,False]),
                    CombinationSum(8,[True,False,True]),
                    CombinationSum(9,[False,True,True]),
                    CombinationSum(12,[True,True,True])]
        self.assertEqual(result, expected)

    def test_duplicates_are_removed(self):
        start = [CombinationSum(1,[True])]
        result = add_term_to_sorted_list(start,1)
        expected = [CombinationSum(1,[False,True]),
                    CombinationSum(2,[True,True])]
        self.assertEqual(result, expected)

def sums_for_all_combinations(values):
    """returns sorted list of all combination Sums with dups removed"""
    sums = []
    for value in values:
        sums = add_term_to_sorted_list(sums, value)
    return sums        
        
def merge_elements_used(elements1, elements2):
    assert len(elements1) == len(elements2)
    return [x or y for x,y in zip(elements1, elements2)]

def subset_sum_exponential_time(values, target):
    if len(values) == 1:
        if values[0] == target:
            return True,[]
        else:
            return False, None
    #split values list in half
    midpoint = len(values)/2
    values1 = values[0:midpoint]
    values2 = values[midpoint:]
    #generate all combination sums for each list, sorted
    sums1 = sums_for_all_combinations(values1)
    sums2 = sums_for_all_combinations(values2)
    for sum2 in sums2:
        if sum2.value == target:
            return True, sum2.elements
    #iterate through both results, one up, one down and check for target
    for sum1 in reversed(sums1):
        for sum2 in sums2:
            if sum1.value == target:
                return True, sum1.elements
            if sum1.value + sum2.value == target:
                return True, merge_elements_used(sum1.elements, sum2.elements)
            if sum1.value + sum2.value > target:
                break
    return False, None

# class TestSubsetSumExtended(unittest.TestCase):
#      
#     def test_empty_set(self):
#         self.assertEquals(subset_sum_exponential_time(values=[], target=10),(False,None))
#        
#     def test_sum_larger_than_max_possible(self):
#         self.assertEquals(subset_sum_exponential_time(values=[5,4], target=10),(False,None))
#            
#     def test_sum_smaller_than_min_possible(self):
#         self.assertEquals(subset_sum_exponential_time(values=[5,4,3,2], target=1),(False,None))
#         
#     def test_subset_is_only_value(self):
# #         self.assertEquals(subset_sum_exponential_time(values=[1], target=1),(True,[True]))
#         self.assertEquals(subset_sum_exponential_time(values=[1], target=1),(True,[]))
#            
#     def test_subset_is_first_value(self):
# #         self.assertEquals(subset_sum_exponential_time(values=[7,8,9], target=7),(True,[True,False,False]))
#         self.assertEquals(subset_sum_exponential_time(values=[7,8,9], target=7),(True,[]))
#  
#     def test_subset_is_middle_value(self):
# #         self.assertEquals(subset_sum_exponential_time(values=[7,8,9], target=8),(True,[False,True,False]))
#         self.assertEquals(subset_sum_exponential_time(values=[7,8,9], target=8),(True,[]))
#               
#     def test_subset_is_last_value(self):
# #         self.assertEquals(subset_sum_exponential_time(values=[7,8,9], target=9),(True,[False,False,True]))
#         self.assertEquals(subset_sum_exponential_time(values=[7,8,9], target=9),(True,[]))
#               
#     def test_other_3_element_combinations(self):
# #         self.assertEquals(subset_sum_exponential_time(values=[7,8,10], target=15),(True,[True,True,False]))
# #         self.assertEquals(subset_sum_exponential_time(values=[7,8,10], target=17),(True,[True,False,True]))
# #         self.assertEquals(subset_sum_exponential_time(values=[7,8,10], target=18),(True,[False,True,True]))
# #         self.assertEquals(subset_sum_exponential_time(values=[7,8,10], target=25),(True,[True,True,True]))
#         self.assertEquals(subset_sum_exponential_time(values=[7,8,10], target=15),(True,[]))
#         self.assertEquals(subset_sum_exponential_time(values=[7,8,10], target=17),(True,[]))
#         self.assertEquals(subset_sum_exponential_time(values=[7,8,10], target=18),(True,[]))
#         self.assertEquals(subset_sum_exponential_time(values=[7,8,10], target=25),(True,[]))
#        
#     def test_impossible_total(self):
#         self.assertEquals(subset_sum_exponential_time(values=[7,8,10], target=24),(False,None))
#           
#     def test_multiple_possibilities(self):
# #         self.assertEquals(subset_sum_exponential_time(values=[7,7,7], target=14),(True,[True,True,False]))
#         self.assertEquals(subset_sum_exponential_time(values=[7,7,7], target=14),(True,[]))
#           
# #     def test_big_one(self):
# #         values = [10 for _ in range(1,200)]
# #         expected_list = [True for _ in values]
# #         target = sum(values)
# #         self.assertEquals(subset_sum_exponential_time(values, target),(True,expected_list))
        
def random_set(size, upper_bound, seed=None):
#     random.seed(seed)
    return [random.randint(1,upper_bound) for _ in range(size)]

def random_subset_sum(size, upper_bound, sum_terms, seed=None):
    """Return a set of random ints and a sum of a random subset
    
    Args:
        size - size of resulting set
        upper_bound - set contains ints between 1 and upper_bound
        sum_terms - number of terms in the sum
    """
    random.seed(seed)
    rset = random_set(size, upper_bound)
    subset_sum = sum(random.sample(rset,sum_terms))
    return (rset, subset_sum)

class Stats(object):
    def __init__(self):
        self.maximum = 0
        self.minimum = float('inf')
        self.sample_count = 0
        self.average = 0
    def add_sample(self, sample):
        if sample > self.maximum:
            self.maximum = sample
        if sample < self.minimum:
            self.minimum = sample
        if self.average == 0:
            self.average = sample
        else:
            self.average = (self.average * self.sample_count + sample) / (self.sample_count + 1)
        self.sample_count += 1
    def __str__(self):
        return 'Max: %s, Min: %s, Avg: %s, Samples: %s' % (self.maximum, self.minimum, self.average, self.sample_count)
                    
def performance_sample(size, upper_bound, sum_terms, samples = 5):
    stats = Stats()
    for _ in range(samples):
        values, target = random_subset_sum(size, upper_bound, sum_terms)
        start_time = time.time()
        res = subset_sum_exponential_time(values, target)
        end_time = time.time()
        assert res
        stats.add_sample(end_time - start_time)
    return stats
        

if __name__ == '__main__':
    for set_size in range(10,50):
        stats = performance_sample(set_size, 1000, set_size, 50)
        print '%s,%s,%s,%s,%s' % (set_size, stats.minimum, stats.maximum, stats.average, stats.sample_count)
        
# add tracking of which elements are included in each sum
# refactor so that both algos derive from same class
# compare algos
# wire in to credit card recon
        

        