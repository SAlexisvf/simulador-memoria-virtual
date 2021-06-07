"""
Running example
>>> python main.py -f test_file.txt -a fifo
"""

import os
import argparse
from parser import instructions_parser
import instructions_set

def virtual_memory_manager(filepath, algorithm):
    instructions, arguments = instructions_parser(filepath)
    for instruction in instructions:
        if instruction == 'P':
            instructions_set.process(arguments.pop(0), arguments.pop(0))
        elif instruction == 'A':
            instructions_set.access(arguments.pop(0), arguments.pop(0), arguments.pop(0))
        elif instruction == 'L':
            instructions_set.free(arguments.pop(0))
        elif instruction == 'C':
            instructions_set.comment(arguments.pop(0))
        elif instruction == 'F':
            instructions_set.finalize()
        else:
            instructions_set.end()    

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Virtual Memory Manager')
    arg_parser.add_argument('-f', '--filepath', type=str, required=True, help='Instructions file path')
    arg_parser.add_argument('-a', '--algorithm', type=str, required=True, help='Page replacement algorithm (fifo | lru)')
    args = arg_parser.parse_args()
    virtual_memory_manager(args.filepath, args.algorithm)