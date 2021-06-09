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

    memory = [{
        'process': None,
        'page': None
    }] * memory_size

    swap_memory = [{
        'process': None,
        'page': None
    }] * swap_memory_size

def loadPage(address_offset, process, page, selected_memory):
    global time
    address_value = {
        'process': None,
        'page': None
    }
    if process != None and page != None:
        address_value['process'] = process
        address_value['page'] = page
        time = time + 1
    else:
        time = time + 0.1

    if selected_memory == 'memory':
        for i in range(page_size):
            memory[address_offset + i] = address_value
    else:
        for i in range(page_size):
            swap_memory[address_offset + i] = address_value
    
def swap_frames(current_page, process):
    if algorithm == 'fifo':
        # get the 'first in' page
        removed_frame = fifo_queue.pop(0)
        # return back the page at the end
        fifo_queue.append(removed_frame)
    else:
        pass

    removed_address = memory[removed_frame]
    removed_process = removed_address['process']
    removed_page = removed_address['page']

    # find empty space
    for i in range(swap_memory_size):
        if (swap_memory[i]['process'] == None):
            loadPage(i, removed_process, removed_page, 'swap_memory')
            loadPage(removed_frame, process, current_page, 'memory')

            print('Page {} from process {} was swapped to the swap memory on frame {}'
                    .format(removed_page, removed_process, math.floor(i/page_size)))

            new_frame = math.floor(removed_frame/page_size)
            print('Page {} from process {} was placed in memory on frame {}'
                    .format(current_page, process, new_frame))
            return new_frame

def process(n, p):
    pages = math.ceil(n / page_size)
    used_frames = []

    print('Running instruction P with parameters {}, {}'.format(n,p))
    
    for current_page in range (pages):
        # plus one to detect when no free memory was found
        for i in range (memory_size + 1):

            # in case there is no free memory
            if i == memory_size:
                new_frame = swap_frames(current_page + 1, p)
                used_frames.append(new_frame)
                break

            # in case there is empty space in memory
            if memory[i]['process'] == None:
                used_frames.append(math.floor(i/page_size))
                if(algorithm == 'fifo'):
                    fifo_queue.append(i)
                else:
                    lru_queue.append(i)
                loadPage(i, p, current_page + 1, 'memory')
                break

    print('frames {} were assigned to process {}'.format(used_frames, p))

def access(d, p, m):
    print('Running instruction A with parameters {}, {}, {}'.format(d,p,m))
    page = math.ceil(d / page_size)
    used_frame = None

    # check if page is in memory
    for i in range (memory_size):
        if memory[i]['process'] == p and memory[i]['page'] == page:
            if(algorithm == 'fifo'):
                pass
            else:
                # update LRU
                pass
            print('Virtual address: {}. Real address: {}.'.format(d, i + (d - (page-1)*page_size)))
            return
    
    # check if page is in swap memory
    for i in range (swap_memory_size):
        if swap_memory[i]['process'] == p and swap_memory[i]['page'] == page:
            # checks if there is empty space
            for j in range (memory_size + 1):
                # in case there is no free memory
                if j == memory_size:
                    new_frame = swap_frames(page, p)
                    used_frame = new_frame
                    print('Virtual address: {}. Real address: {}.'.format(d, used_frame*page_size + (d - (page-1)*page_size)))

                # in case there is empty space in memory
                elif memory[j]['process'] == None:
                    used_frame = math.floor(j/page_size)
                    if(algorithm == 'fifo'):
                        fifo_queue.append(j)
                    else:
                        lru_queue.append(j)
                    loadPage(j, p, page, 'memory')
                    print('Virtual address: {}. Real address: {}.'.format(d, j + (d - (page-1)*page_size)))

            print('frame {} was assigned to process {}'.format(used_frame, p))
            # free page from swap memory
            loadPage(i, None, None, 'swap')
            return
    
    print('Page {} form process {} does not exist!')

def free(p):
    print('Running instruction L with parameters {}'.format(p))
    free_frames_memory = []
    free_frames_swap_memory = []
    
    # free pages in memory
    for i in range (memory_size):
        if memory[i]['process'] == p:
            loadPage(i, None, None, 'memory')
            free_frames_memory.append(math.floor(i/page_size))
            # remove process frames from queues
            if(algorithm == 'fifo'):
                if i in fifo_queue:
                    fifo_queue.remove(i)
            else:
                if i in lru_queue:
                    lru_queue.remove(i)
    
    # free pages in swap memory
    for i in range (swap_memory_size):
        if swap_memory[i]['process'] == p:
            loadPage(i, None, None, 'swap')
            free_frames_swap_memory.append(math.floor(i/page_size))
            # remove process frames from queues
            if(algorithm == 'fifo'):
                if i in fifo_queue:
                    fifo_queue.remove(i)
            else:
                if i in lru_queue:
                    lru_queue.remove(i)

    print('Frames {} from process {} were removed from memory'.format(free_frames_memory, p))
    print('Frames {} from process {} were removed from swap memory'.format(free_frames_swap_memory, p))

def finalize():
    pass

def end():
    print('-------- End of program! --------')
