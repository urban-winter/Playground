import unittest

class StackFull(Exception):
    pass

class StackEmpty(Exception):
    pass

class Stack(object):
    def __init__(self, max_size):
        self.max_size = max_size
        self.stack = [None for _ in range(max_size)]
        self.count = 0

    def is_empty(self):
        return self.count == 0

    def push(self, item):
        if self.count == self.max_size:
            raise StackFull()
        self.stack[self.count] = item
        self.count += 1

    def pop(self):
        if self.is_empty():
            raise StackEmpty()
        self.count -= 1
        return self.stack[self.count]
    
    def top(self):
        if self.is_empty():
            raise StackEmpty()
        return self.stack[self.count-1]
    
    def remove(self, item):
        """Remove the first instance of item from the stack"""
        pos = self.stack.index(item)
        for i in range(pos, len(self.stack)):
            self.stack[i] = self.stack[i+1]
        self.count -= 1

class SetOfStacks(object):

# create a new stack each time a stack exceeds the max size

    def _new_stack(self):
        self.stacks.push(Stack(self.max_size))

    def _discard_stack(self):
        self.stacks.pop()

    def __init__(self,max_size):
        self.max_size = max_size
        self.stacks = Stack(self.max_size)
        self._new_stack()

    def push(self, item):
        # Will raise StackFull if last stack is full
        try:
            self.stacks.top().push(item)
        except StackFull:
            self._new_stack()
            self.stacks.top().push(item)

    def pop(self):
        # Will raise StackEmpty if last stack is empty
        try:
            return self.stacks.top().pop()
        except StackEmpty:
            self._discard_stack()
            return self.stacks.top().pop()
        
    def pop_at(self, stack_no):
        """Remove an element from the stack denoted by stack_no"""
        stack = self.stacks.stack[stack_no] # may throw an IndexError
        retval = stack.pop()
        if stack.is_empty():
            self.stacks.remove(stack)
        return retval
    

class TestSetOfStacks(unittest.TestCase):
    def test_pop_empty(self):
        stacks = SetOfStacks(1)
        self.assertRaises(StackEmpty, stacks.pop)
    def test_push_then_pop(self):
        stacks = SetOfStacks(2)
        stacks.push(1)
        stacks.push(2)
        self.assertEqual(stacks.pop(),2)
        self.assertEqual(stacks.pop(),1)
    def test_push_more_than_max_creates_new_stack(self):
        stacks = SetOfStacks(2)
        stacks.push(1)
        stacks.push(2)
        stacks.push(3)
        self.assertEqual(stacks.pop(),3)
        self.assertEqual(stacks.pop(),2)
        self.assertEqual(stacks.pop(),1)
    def test_push_more_than_max(self):
        stacks = SetOfStacks(1)
        stacks.push(1)
        self.assertRaises(StackFull, stacks.push, 2)
    def test_pop_at(self):
        stacks = SetOfStacks(2)
        stacks.push(1)
        stacks.push(2)
        stacks.push(3)
        self.assertEqual(stacks.pop_at(0), 2)
