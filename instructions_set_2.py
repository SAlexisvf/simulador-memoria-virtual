import math

# main variables
memory_size = None
swap_memory_size = None
page_size = None
algorithm = None
memory = None
swap_memory = None

# this will be global to all functions
time = 0

# helper variables
fifo_queue = []
lru_queue = []

def set_variables(m, s, p, a):
    global memory_size, swap_memory_size, page_size, algorithm, memory, swap_memory

    memory_size = m
    swap_memory_size = s
    page_size = p
    algorithm = a

    memory = [None] * memory_size
    swap_memory = [None] * swap_memory_size

def loadPage(address_offset, process, page):
    address_value = None
    if process != None and page != None:
        address_value = 'Address occupied by process {}, page {}'.format(process, page)
    for i in range(page_size):
        memory[address_offset + i] = address_value


def process(n, p):
    global time
    pages = math.ceil(n / page_size)
    used_frames = []

    print('Running instruction P with parameters {}, {}'.format(n,p))
    
    for current_page in range (pages):
        for i in range (memory_size):
            # empty space
            if memory[i] == None:
                used_frames.append(math.floor(i/page_size))
                if(algorithm == 'fifo'):
                    fifo_queue.insert(0,i)
                else:
                    lru_queue.insert(0,i)
                loadPage(i,p,current_page)
                time = time + 1
                break
            
    print('frames {} were assigned to process {}'.format(used_frames, p))