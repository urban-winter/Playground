import unittest

class Node(object):
    def __init__(self, name, neighbours):
        """init a node with a name and a list of neighbouring nodes"""
        self.name = name
        self.neighbours = neighbours

def is_route_between(from_name, to_name, graph):
    #find starting node
    for node in graph:
        if node.name == from_name:
            return is_route_to( node, to_name)
    return False

def is_route_to(start_node, end_name):
    """is there a route from the start node to the node with specified name?

    Note that a circular graph will cause infinite recursion. This could
    be fixed my maintaining a list of nodes visited and terminating if we
    visit a node for the second time.
    """
    print 'Visiting node ', start_node.name
    if start_node.name == end_name:
        return True
    else:
        for node in start_node.neighbours:
            if is_route_to(node, end_name):
                return True
        return False

class TestFindRoute(unittest.TestCase):
    
    node_d = Node('D',[])
    node_b = Node('B',[node_d])
    node_c = Node('C',[])
    node_a = Node('A',[node_b, node_c])
    graph = [node_a, node_b, node_c, node_d]

    def test_no_route_from_c_to_d(self):
        self.assertFalse( is_route_between('C','D',self.graph))
 
    def test_route_from_a_to_a(self):
        self.assertTrue( is_route_between('A','A',self.graph))
                          
    def test_route_from_b_to_b(self):
        self.assertTrue( is_route_between('B','B',self.graph))

    def test_route_from_c_to_c(self):
        self.assertTrue( is_route_between('C','C',self.graph))

    def test_route_from_b_to_d(self):
        self.assertTrue( is_route_between('B','D',self.graph))
 
    def test_route_from_a_to_d(self):
        self.assertTrue( is_route_between('A','D',self.graph))
        