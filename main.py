"""
Running example
>>> python main.py -f test_file.txt -a fifo
"""

import os
import argparse
from parser import instructions_parser
import instructions_set

def virtual_memory_manager(filepath, algorithm, memory_size, swap_memory_size, page_size):
    instructions, arguments = instructions_parser(filepath)
    instructions_set.set_variables(memory_size, swap_memory_size, page_size, algorithm)
    print('Starting execution of instructions...')
    for num_instruction, instruction in enumerate(instructions, start=1):
        # leave space betweet instructions
        print()
        print('INSTRUCTION {}'.format(num_instruction))
        if instruction == 'P':
            instructions_set.process(arguments.pop(0), arguments.pop(0))
        elif instruction == 'A':
            instructions_set.access(arguments.pop(0), arguments.pop(0), arguments.pop(0))
        elif instruction == 'L':
            instructions_set.free(arguments.pop(0))
        elif instruction == 'C':
            print('// {}'.format(arguments.pop(0)))
        elif instruction == 'F':
            instructions_set.finalize()
        else:
            instructions_set.end() 

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Virtual Memory Manager')
    arg_parser.add_argument('-f', '--filepath', type=str, required=True, help='Instructions file path')
    arg_parser.add_argument('-a', '--algorithm', type=str, required=True, help='Page replacement algorithm (fifo | lru)')
    arg_parser.add_argument('-m', '--memory_size', type=int, required=False, help='Memory Size', default=2048)
    arg_parser.add_argument('-s', '--swap_memory_size', type=int, required=False, help='Swap memory size', default=4096)
    arg_parser.add_argument('-p', '--page_size', type=int, required=False, help='Page size', default=16)
    args = arg_parser.parse_args()
    virtual_memory_manager(args.filepath, args.algorithm, args.memory_size, args.swap_memory_size, args.page_size)