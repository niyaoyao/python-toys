# -*- coding:utf-8 -*-
        
import json
import os
import re
import sys
import argparse


        
import logging
logging.basicConfig(level = logging.INFO)
LOG = logging.getLogger("ny_util")

import os
import zipfile


        
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

    def unzip_files_in_directory(self, directory):
        """
        遍历指定目录，解压所有 *.zip 文件，并以 ZIP 文件名作为解压目录。
        
        Args:
            directory (str): 要遍历的目录路径
        """
        # 确保目录存在
        if not os.path.isdir(directory):
            LOG.info(f"错误: '{directory}' 不是一个有效的目录")
            return
        
        # 遍历目录
        for root, dirs, files in os.walk(directory):
            for file in files:
                # 检查文件是否为 .zip 文件
                if file.lower().endswith('.zip'):
                    zip_path = os.path.join(root, file)  # ZIP 文件的完整路径
                    # 提取文件名（不含扩展名）作为解压目录
                    folder_name = os.path.splitext(file)[0]
                    extract_path = os.path.join(root, folder_name)  # 解压目标目录
                    
                    try:
                        # 创建解压目录（如果不存在）
                        os.makedirs(extract_path, exist_ok=True)
                        
                        # 打开并解压 ZIP 文件
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            LOG.info(f"正在解压: {zip_path} -> {extract_path}")
                            zip_ref.extractall(extract_path)
                        
                        LOG.info(f"解压完成: {zip_path}")
                    except zipfile.BadZipFile:
                        LOG.info(f"错误: '{zip_path}' 不是有效的 ZIP 文件")
                    except PermissionError:
                        LOG.info(f"错误: 没有权限访问 '{zip_path}' 或 '{extract_path}'")
                    except Exception as e:
                        LOG.info(f"解压 '{zip_path}' 时发生错误: {e}")


    def run(self):
        self.log_properties()
        if self.action_type == 'traverse_directory':
            self.traverse_directory(directory=self.directory, extension=self.file_extension)
        elif self.action_type == 'extract_zip':
            self.unzip_files_in_directory(directory=self.directory)

            
        
if __name__ == '__main__':
    args = read_args()
    instance = NYUtil(action_type=args.action_type, directory=args.directory, file_extension=args.file_extension)
    instance.run()
    
        