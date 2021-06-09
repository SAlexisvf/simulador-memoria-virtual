"""
Running example
>>> python main.py -f test.txt -a fifo
"""

import os
import argparse
from parser import instructions_parser
import instructions_set_2

memory_size = 2048
swap_memory_size = 4096
page_size = 16

def virtual_memory_manager(filepath, algorithm):
    instructions, arguments = instructions_parser(filepath)
    instructions_set_2.set_variables(memory_size, swap_memory_size, page_size, algorithm)
    print('Starting execution of instructions...')
    for num_instruction, instruction in enumerate(instructions, start=1):
        # leave space betweet instructions
        print()
        print('INSTRUCTION {}'.format(num_instruction))
        if instruction == 'P':
            instructions_set_2.process(arguments.pop(0), arguments.pop(0))
        elif instruction == 'A':
            instructions_set_2.access(arguments.pop(0), arguments.pop(0), arguments.pop(0))
        elif instruction == 'L':
            instructions_set_2.free(arguments.pop(0))
        elif instruction == 'C':
            print('// {}'.format(arguments.pop(0)))
        elif instruction == 'F':
            instructions_set_2.finalize()
        # else:
        #     instructions_set_2.end() 

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Virtual Memory Manager')
    arg_parser.add_argument('-f', '--filepath', type=str, required=True, help='Instructions file path')
    arg_parser.add_argument('-a', '--algorithm', type=str, required=True, help='Page replacement algorithm (fifo | lru)')
    args = arg_parser.parse_args()
    virtual_memory_manager(args.filepath, args.algorithm)