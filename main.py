import os
import argparse
from parser import instructions_parser

def virtual_memory_manager(filepath, algorithm):
    instructions, arguments = instructions_parser(filepath)
    print('instructions:')
    print(instructions)
    print('arguments:')
    print(arguments)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Virtual Memory Manager')
    arg_parser.add_argument('-f', '--filepath', type=str, required=True, help='Instructions file path')
    arg_parser.add_argument('-a', '--algorithm', type=str, required=True, help='Page replacement algorithm (fifo | lru)')
    args = arg_parser.parse_args()
    virtual_memory_manager(args.filepath, args.algorithm)