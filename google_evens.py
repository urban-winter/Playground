import unittest

#Build an algorithm that returns true when every digit is even. 1234 = false. 2468 = true. Assume the input is a number > 0

# def all_digits_even(n):
#     # break down into digits
#     num_str = str(n)
#     # for each digit
#     for i in range(len(num_str)):
#     # if digit is odd
#     #    return False
# #     return True
#         if (int(num_str[i]) % 2 == 1):
#             return False
#         return True
    
def all_digits_even(a_number):
    """return true if all digits are even"""
    while a_number > 0:
        if a_number % 2 == 1:
            return False
        a_number /= 10
    return True 

class TestEvens(unittest.TestCase):
    
    def test_1_is_false(self):
        self.assertFalse(all_digits_even(1))

    def test_2_is_true(self):
        self.assertTrue(all_digits_even(2))

    def test_3_is_false(self):
        self.assertFalse(all_digits_even(3))

    def test_4_is_true(self):
        self.assertTrue(all_digits_even(4))

    def test_12_is_false(self):
        self.assertFalse(all_digits_even(12))

    def test_2468_is_true(self):
        self.assertTrue(all_digits_even(2468))

    def test_1234_is_false(self):
        self.assertFalse(all_digits_even(1234))
