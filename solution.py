
        # -*- coding:utf-8 -*-
        
import json
import os
import re
import sys
import argparse
from typing import List, Optional, TypeVar
import logging
logging.basicConfig(level = logging.INFO)
LOG = logging.getLogger("solution")

        
        
def read_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-n', '--algorithm_number', help='The Number of Algorithm.', type=int, required=False)
    args = parse.parse_args()
    return args

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
class Solution(object):
    def __init__(self, algorithm_number=0):
        self.algorithm_number = algorithm_number if algorithm_number is not None else 0

        
    def log_properties(self):
        LOG.info(self.__dict__)
        
    def run(self):
        self.log_properties()
        if self.algorithm_number == 0:
            nums = [2,7,11,15]
            target = 9
            nums = [3,2,4]
            target = 6
            nums = [3,3]
            target = 6
            self.twoSum(nums=nums, target=target)
        elif self.algorithm_number == 1:
            n0 = ListNode()
            n1 = ListNode(val=1)
            n2 = ListNode(val=2)
            n3 = ListNode(val=3)
            n4 = ListNode(val=4)
            n0.next = n1
            n1.next = n2
            n2.next = n3
            n3.next = n4
            
            self.reverseList(head=n0)
        

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        differ_map = {}
        sum_index = []
        for index, value in enumerate(nums):
            LOG.info(f"{index}:{value}")
            if value not in  differ_map:
                differ_map[target - value]  = index
            else:
                return  [differ_map[value], index]
            
        LOG.info(differ_map)
        LOG.info(sum_index)

    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        LOG.info('Reverse List')
        current:ListNode = head
        previous:ListNode = None

        while current != None:
            temp = current.next
            current.next = previous
            previous = current
            current = temp
        
        p:ListNode = previous
        q:ListNode = previous

        while q.next != None:
            LOG.info(f"{p.val}")
            q = p
            p = p.next

if __name__ == '__main__':
    args = read_args()

    instance = Solution(algorithm_number=args.algorithm_number)
    instance.run()
    
        