# -*- coding:utf-8 -*-
        
import json
import os
import re
import sys
import argparse


        
import logging
logging.basicConfig(level = logging.INFO)
LOG = logging.getLogger("ny_util")

        
        
def read_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-t', '--action_type', help='The Action Type of Python Script.', type=str, required=False)
    parse.add_argument('-d', '--directory', help='The Source Directory of Python Script.', type=str, required=False)
    parse.add_argument('-ext', '--file_extension', help='The Source Directory of Python Script.', type=str, required=False)
    args = parse.parse_args()
    return args
        
        
class NYUtil(object):
    def __init__(self, action_type, directory='', file_extension=''):
        self.action_type = action_type
        self.directory = directory if self.validate_string(directory) else  os.path.dirname(os.path.realpath(__file__))
        self.file_extension = file_extension
    def log_properties(self):
        LOG.info(self.__dict__)
    
    def validate_string(self, instance):
        return instance is not None and isinstance(instance, str) and len(instance) > 0

    def traverse_directory(self, directory='', extension=''):
        LOG.info('Start Traverse >>>>>>>>>>>>>> {}'.format(directory))
        ext_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if self.validate_string(extension):
                    if file.endswith(extension):  # 判断文件是否以 .ets 结尾
                        LOG.info(file_path)
                        if file_path not in ext_files:
                            ext_files.append(file_path)
                else:
                    LOG.info(file_path)
        if self.validate_string(extension):
            LOG.info('There are {} *.{} Files'.format(len(ext_files), extension))
    def run(self):
        self.log_properties()
        if self.action_type == 'traverse_directory':
            self.traverse_directory(directory=self.directory, extension=self.file_extension)

            
        
if __name__ == '__main__':
    args = read_args()
    instance = NYUtil(action_type=args.action_type, directory=args.directory, file_extension=args.file_extension)
    instance.run()
    
        