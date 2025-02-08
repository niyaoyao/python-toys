# -*- coding:utf-8 -*-

import json
import os
import re
import sys
import argparse
import logging
logging.basicConfig(level = logging.INFO)
LOG = logging.getLogger("ScriptGenerator")

def read_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-n', '--script_filename', help='The Filename without extension of Python Script.', type=str, required=True)
    parse.add_argument('-cls', '--class_name', help='The Class Name of Python Script.', type=str, required=False)
    parse.add_argument('-d', '--script_save_directory', help='The Script Directory of Python Script.', type=str, required=False)
    args = parse.parse_args()
    return args

class ScriptGenerator(object):
    def __init__(self, script_filename, class_name=None, script_save_directory=None):
        self.script_filename = script_filename
        self.class_name = class_name if isinstance(class_name, str) and len(class_name) > 0 else None
        self.should_generate_class = self.class_name != None
        filepath = "{}{}".format(self.script_filename, '.py')
        script_path = os.path.join(script_save_directory, filepath) if script_save_directory != None else filepath
        self.script_path = script_path if isinstance(script_path, str) and len(class_name) > 0 else filepath
        
    def write_script_file(self, script_path, script_contents):
        with open(script_path, 'w') as script_file:
            script_file.write(script_contents)
            
    def format_script_file_string(self):
        script_utf8 = "# -*- coding:utf-8 -*-"
        script_import = """
import json
import os
import re
import sys
import argparse\n
"""
        script_logger = """
import logging
logging.basicConfig(level = logging.INFO)
LOG = logging.getLogger("{}")\n
        """.format(self.script_filename)
        
        script_readargs = """
def read_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-p', '--placeholder', help='The Placeholder of Python Script.', type=str, required=False)
    args = parse.parse_args()
    return args
        """
        class_content = ""
        if self.should_generate_class:
            class_content = """
class {}(object):
    def __init__(self, placeholder):
        self.placeholder = placeholder
        
    def log_properties(self):
        LOG.info(self.__dict__)
        
    def run(self):
        self.log_properties()
    \n
            """.format(self.class_name)
        script_entrance = """
if __name__ == '__main__':
    args = read_args()
        """
        if self.class_name is not None:
            script_entrance = """{}\n
    instance = {}(placeholder=args.placeholder)
    instance.run()
    """.format(script_entrance, self.class_name)
        script_content = """
        {}
        {}
        {}
        {}
        {}
        {}
        """.format(
            script_utf8,
            script_import,
            script_logger,
            script_readargs,
            class_content,
            script_entrance
        )
        return script_content

    def run(self):
        # script string
        script_contents = self.format_script_file_string()
        # write file
        self.write_script_file(script_path=self.script_path, script_contents=script_contents)

if __name__ == '__main__':
    args = read_args()
    generator = ScriptGenerator(script_filename=args.script_filename, class_name=args.class_name, script_save_directory=args.script_save_directory)
    generator.run()