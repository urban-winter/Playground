import unittest
from subset_sum_extended import subset_sum
 
def many_to_many_match(list1,list2):
    """Return the sum of the highest value subset of list1 and list2
    
    Returns None is there are no subsets with the same sum.
    
    Note that the time taken is proportional to min(sum(list1),(list2)) i.e.
    high valued take longer than low-valued lists. The time taken is probably
    polynomial by list length.
    """
    if not list1 or not list2:
        return None
    highest_possible_common_sum = min(sum(list1),sum(list2))
    lowest_possible_common_sum = min(min(list1),min(list2))
    for try_sum in range(highest_possible_common_sum,lowest_possible_common_sum-1,-1):
        if subset_sum(list1,try_sum) and subset_sum(list2,try_sum):
            return try_sum
    return None
 
class TestManyToMany(unittest.TestCase):
    
    def test_empty_lists(self):
        self.assertEquals(many_to_many_match([],[]),None)
        
    def test_identical_single_element_lists(self):
        self.assertEquals(many_to_many_match([1],[1]),1)

    def test_lists_with_subset_is_not_whole_list(self):
        self.assertEquals(many_to_many_match([1,2,3,10],[9,3,3,8]),15)

    def test_lists_with_subset_is_whole_list(self):
        self.assertEquals(many_to_many_match([1,2,3,4,5],[6,9]),15)
         
    def test_lists_with_no_common_subset(self):
        self.assertEquals(many_to_many_match([11,17],[19,23]),None)
        
    def test_big_lists(self):
        list1 = [x for x in range(1,100)]
        list2 = [x for x in range(1,101)]
        self.assertEquals(many_to_many_match(list1,list2),sum(list1))
        