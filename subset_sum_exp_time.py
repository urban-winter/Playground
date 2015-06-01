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
    # TODO: obvious checks - more than 1 value, target not greater than max
    
    #split values list in half
    midpoint = len(values)/2
    values1 = values[0:midpoint]
    values2 = values[midpoint:]
    #generate all combination sums for each list, sorted
    sums1 = sums_for_all_combinations(values1)
    sums2 = sums_for_all_combinations(values2)
    #iterate through both results, one up, one down and check for target
    for sum1 in sums1:
        for sum2 in sums2.reverse():
            if sum1 + sum2 == target:
                return True
            if sum1 + sum2 > target:
                break
    return False
        