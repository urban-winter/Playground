import unittest

class StackFull(Exception):
    pass

class StackEmpty(Exception):
    pass

class StackNumberOutOfRange(Exception):
    pass

ARRAY_SIZE = 300
class Stack(object):
    max_stacks = 3
    max_length = ARRAY_SIZE / 300

    def __init__(self):
        self.stack_ptr = []
        self.stack_ptr = [0 for _ in range(self.max_stacks)]
        self.stack_array = [None for _ in range(ARRAY_SIZE)]

    def push(self, item,stack_number):
        """Push item onto one of three stacks"""
        if stack_number not in range(3):
            raise StackNumberOutOfRange
        if self.stack_ptr[stack_number] == self.max_length:
            raise StackFull()
        self.stack_array[stack_number * self.max_length + self.stack_ptr[stack_number]] = item
        self.stack_ptr[stack_number] += 1

    def pop(self, stack_number):
        """Pop item from one of three stacks"""
        if stack_number not in range(3):
            raise StackNumberOutOfRange
        if self.stack_ptr[stack_number] == 0:
            raise StackEmpty()
        self.stack_ptr[stack_number] -= 1
        return self.stack_array[stack_number * self.max_length + self.stack_ptr[stack_number]]
    

class TestStack(unittest.TestCase):
    def test_pop_empty(self):
        stack = Stack()
        self.assertRaises(StackEmpty, stack.pop, 0)
        self.assertRaises(StackEmpty, stack.pop, 1)
        self.assertRaises(StackEmpty, stack.pop, 2)

    def test_push_then_pop_each_stack(self):
        stack = Stack()
        for stack_number in range(stack.max_stacks):
            stack.push(stack_number,stack_number)
            self.assertEqual(stack.pop(stack_number), stack_number)

    def test_push_when_full_each_stack(self):
        stack = Stack()
        for stack_number in range(stack.max_stacks):
            for i in range(stack.max_length):
                stack.push(i,stack_number)
                self.assertRaises(StackFull, stack.push, 1, stack_number)

    def test_full_then_empty(self):
        stack = Stack()
        pushvals = range(stack.max_length)
        expected = pushvals[::-1]
        for stack_number in range(stack.max_stacks):
            for val in pushvals:
                stack.push(val,stack_number)
            actual = [stack.pop(stack_number) for _ in expected]
            self.assertEqual(actual, expected)

    def test_stack_index_out_of_range(self):
        stack = Stack()
        self.assertRaises(StackNumberOutOfRange,stack.push, 1,-1)
        self.assertRaises(StackNumberOutOfRange,stack.push, 1,3)
        self.assertRaises(StackNumberOutOfRange,stack.pop, -1)
        self.assertRaises(StackNumberOutOfRange,stack.pop, 3)
