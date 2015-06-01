import unittest

def merge_sorted_lists(sorted_list, additional_terms_sorted):
    """merge two ascending lists"""
    i_ats = 0
    i_sl = 0
    retlist = []
    finished = False
    while not finished:
        if i_ats == len(additional_terms_sorted):
            retlist.extend(sorted_list[i_sl:])
            finished = True
        elif i_sl == len(sorted_list):
            retlist.extend(additional_terms_sorted[i_ats:])
            finished = True
        elif sorted_list[i_sl] <= additional_terms_sorted[i_ats]:
            retlist.append(sorted_list[i_sl])
            i_sl += 1
        elif additional_terms_sorted[i_ats] < sorted_list[i_sl]:
            retlist.append(additional_terms_sorted[i_ats])
            i_ats += 1
        else:
            assert False #Can't happen
    return retlist


def add_term_to_sorted_list(sorted_list, term):
    """
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
        