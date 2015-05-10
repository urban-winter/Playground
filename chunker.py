'''
Created on 24 Feb 2015

@author: Piers
'''
import unittest

def chunkify(the_list, num_chunks):
    if num_chunks <= 1:
        return the_list
    chunk_size = len(the_list)/float(num_chunks)
    start = 0
    retval = []
    while start < len(the_list):
        end = int(start + chunk_size + 0.5)
        retval.append(the_list[int(start):end])
        start = end
    return retval

def verify_chunking(the_list, num_chunks, chunks):
    pass
    # number of chunks is correct
    # size of chunks


class TestChunkify(unittest.TestCase):
    
    def test_empty_list(self):
        self.assertEqual(chunkify([],3), [])
        
    def test_zero_chunks(self):
        self.assertEqual(chunkify([1,2,3],0), [1,2,3])
        
    def test_one_chunk(self):
        self.assertEqual(chunkify([1,2,3],1), [1,2,3])
        
    def test_exact(self):
        self.assertEqual(chunkify([1,2,3,4],2), [[1,2],[3,4]])
        
    def test_inexact(self):
        self.assertEqual(chunkify([1,2,3,4,5],2), [[1,2,3],[4,5]])
        
    def test_more_chunks_than_things(self):
        self.assertEqual(chunkify([1,2],3), [[1],[2]])
        
    def test_three_chunks(self):
        self.assertEqual(chunkify(range(1,15),3), [range(1,6),range(6,11),range(11,15)])
