
        # -*- coding:utf-8 -*-
        
import json
import os
import re
import sys
import argparse


        
import logging
logging.basicConfig(level = logging.INFO)
LOG = logging.getLogger("solution")

        
        
def read_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-p', '--placeholder', help='The Placeholder of Python Script.', type=str, required=False)
    args = parse.parse_args()
    return args
        
        
class Solution(object):
    def __init__(self, placeholder):
        self.placeholder = placeholder
        
    def log_properties(self):
        LOG.info(self.__dict__)
        
    def run(self):
        self.log_properties()
    

            
        
if __name__ == '__main__':
    args = read_args()
        

    instance = Solution(placeholder=args.placeholder)
    instance.run()
    
        