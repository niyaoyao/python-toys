# -*- coding:utf-8-sig -*-

import json
import os
import re
import sys
import argparse
import csv
import time
        
import logging
logging.basicConfig(level = logging.INFO)
LOG = logging.getLogger("NYCSV")

        
        
def read_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-i', '--input_file', help='The Input File Path of Python Script.', type=str, required=True)
    parse.add_argument('-t', '--action_type', help='The Action Type of Python Script.', type=str, required=False)
    parse.add_argument('-o', '--output_file', help='The Output of Python Script.', type=str, required=False)
    parse.add_argument('-col', '--column_name', help='The Output of Python Script.', type=str, required=False)
    parse.add_argument('-cc', '--count_column', help='The Output of Python Script.', type=bool, required=False)

    args = parse.parse_args()
    return args
        
        
class NYCSVProcessor(object):
    def __init__(self, input_file, action_type='', column_name='', should_count_column=False):
        self.input_file = input_file
        self.action_type = action_type
        self.column_name = column_name
        self.should_count_column = should_count_column
        
    def log_properties(self):
        LOG.info(self.__dict__)
        
    def run(self):
        self.log_properties()
        if self.action_type == 'read' or self.action_type == 'r':
            self.read_and_print_csv()
        elif self.action_type == 'sort' or self.action_type == 's':
            self.sort_data(output_file='output_data.csv', sort_key=self.column_name)
        elif self.action_type == 'print_column' or self.action_type == 'pc':
            self.print_column()
        elif self.action_type == 'check_vc':
            self.check_vc()

    def check_vc(self):
        LOG.info('Check Column VC ---->')
        start = time.time()
        unique_arr = []
        with open(self.input_file, mode='r', newline='', encoding='utf-8-sig') as infile:
            csv_reader = csv.DictReader(infile)
            for row in csv_reader:
                LOG.info(row)
                if self.column_name in row:
                    value = row[self.column_name]
                    if value not in unique_arr:
                        unique_arr.append(value)
        if self.should_count_column:
            LOG.info('{} Unique Value Count: {}'.format(self.column_name, len(unique_arr)))
        LOG.info('Cost {}s'.format(time.time() - start))

    def print_column(self):
        LOG.info('Print Column ---->')
        start = time.time()
        unique_arr = []
        vc_arr = {}
        with open(self.input_file, mode='r', newline='', encoding='utf-8-sig') as infile:
            csv_reader = csv.DictReader(infile)
            for row in csv_reader:
                LOG.info(row)
                if 'kv' in row:
                    data_dict = json.loads(row['kv'])
                    if 'college_vc' in data_dict:
                        college_vc = data_dict['college_vc']
                        vc_arr[college_vc] = []
                        if row['cuid'] not in vc_arr[college_vc]:
                            vc_arr[college_vc].append(row['cuid'])
                if self.column_name in row:
                    value = row[self.column_name]
                    if value not in unique_arr:
                        unique_arr.append(value)
        LOG.info('vc_arr: {}'.format(vc_arr))
        if self.should_count_column:
            LOG.info('{} Unique Value Count: {}'.format(self.column_name, len(unique_arr)))
        LOG.info('Cost {}s'.format(time.time() - start))
    
    def read_and_print_csv(self):
        with open(self.input_file, mode='r', newline='', encoding='utf-8-sig') as infile:
            csv_reader = csv.DictReader(infile)
            for row in csv_reader:
                LOG.info(row)

    def filter_data(self, output_file, filter_condition):
        with open(self.input_file, mode='r', newline='', encoding='utf-8-sig') as infile, \
             open(output_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
            
            csv_reader = csv.DictReader(infile)
            fieldnames = csv_reader.fieldnames
            csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            csv_writer.writeheader()
            
            for row in csv_reader:
                if filter_condition(row):
                    csv_writer.writerow(row)
    
    def sort_data(self, output_file, sort_key):
        with open(self.input_file, mode='r', newline='', encoding='utf-8-sig') as infile, \
             open(output_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
            
            csv_reader = csv.DictReader(infile)
            rows = list(csv_reader)
            rows.sort(key=lambda row: row[sort_key])
            
            fieldnames = csv_reader.fieldnames
            csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(rows)

    def modify_data(self, output_file):
        with open(self.input_file, mode='r', newline='', encoding='utf-8-sig') as infile, \
             open(output_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
            
            csv_reader = csv.DictReader(infile)
            fieldnames = csv_reader.fieldnames
            csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            csv_writer.writeheader()
            
            for row in csv_reader:
                if 'channel' in row and not row['channel']:
                    row['channel'] = 'Unknown'
                csv_writer.writerow(row)

            
        
if __name__ == '__main__':
    args = read_args()
        

    instance = NYCSVProcessor(input_file=args.input_file, action_type=args.action_type, column_name=args.column_name, should_count_column=args.count_column)
    instance.run()
    
        