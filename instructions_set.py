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
# this will be needed to calculate turnaround
process_time_tracker = []
swap_in_out_count = 0

def set_variables(m, s, p, a):
    '''
    This function set the variables with the values passed from main
    '''
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
    '''
    This function loads a page to a specific memory (memory/swap_memory).
    If you pass None values to process and page it can alse be used to free memory
    '''
    global time
    address_value = {
        'process': None,
        'page': None
    }
    # if the process and page are not None, fills the values with the process/page info
    if process != None and page != None:
        address_value['process'] = process
        address_value['page'] = page
        time = time + 1
    else:
        time = time + 0.1

    # load page on the selected_memory
    if selected_memory == 'memory':
        for i in range(page_size):
            memory[address_offset + i] = address_value
    else:
        for i in range(page_size):
            swap_memory[address_offset + i] = address_value
    
def swap_frames(current_page, process):
    '''
    This function swap frames to swap_memory to create space in primary memory
    '''
    if algorithm == 'fifo':
        # get the 'first in' page
        removed_frame = fifo_queue.pop(0)
        # return back the page at the end
        fifo_queue.append(removed_frame)
    else:
        # get the 'first in' page
        removed_frame = lru_queue.pop(0)
        # return back the page at the end
        lru_queue.append(removed_frame)

    # get the information of the frame to be removed
    removed_address = memory[removed_frame]
    removed_process = removed_address['process']
    removed_page = removed_address['page']

    # find empty space
    for i in range(swap_memory_size):
        if (swap_memory[i]['process'] == None):
            # load to swap memory
            loadPage(i, removed_process, removed_page, 'swap_memory')
            # load new frame to memory
            loadPage(removed_frame, process, current_page, 'memory')

            print('Page {} from process {} was swapped to the swap memory on frame {}'
                    .format(removed_page, removed_process, math.floor(i/page_size)))

            new_frame = math.floor(removed_frame/page_size)
            print('Page {} from process {} was placed in memory on frame {}'
                    .format(current_page, process, new_frame))
            return new_frame

def process(n, p):
    '''
    This function loads a specific number of bytes from a specific process to memory
    '''
    global swap_in_out_count

    # check for invalid cases
    if n <= 0 or n > memory_size:
        print('Error! Invalid number of bits, skipping intructions...')
        return
    for process in process_time_tracker:
        if process['process'] == p:
            print('Error! The process already exist, skipping instruction...')
            return

    pages = math.ceil(n / page_size)
    used_frames = []
    # append process to process_time_tracker structure
    process_time_tracker.append({
        'process': p,
        'start_time': time,
        'end_time': None,
        'page_fault': 0
    })

    print('Running instruction P with parameters {}, {}'.format(n,p))
    
    for current_page in range (pages):
        # plus one to detect when no free memory was found
        for i in range (memory_size + 1):

            # in case there is no free memory
            if i == memory_size:
                new_frame = swap_frames(current_page + 1, p)
                used_frames.append(new_frame)
                swap_in_out_count = swap_in_out_count + 1
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
    '''
    This function access a specific virtual address and shows the real address
    If the page is not in memory makes the swap process
    '''
    global swap_in_out_count, time

    # check invalid case
    is_process = False
    for process in process_time_tracker:
        if process['process'] == p:
            is_process = True
    if is_process == False:
        print('Error! The process does not exist, skipping instruction...')
        return

    print('Running instruction A with parameters {}, {}, {}'.format(d,p,m))
    page = math.ceil(d / page_size)
    used_frame = None

    # check if page is in memory
    for i in range (memory_size):
        if memory[i]['process'] == p and memory[i]['page'] == page:
            if(algorithm == 'lru'):
                # update LRU
                if i in lru_queue:
                    lru_queue.remove(i)
                    lru_queue.append(i)
            print('Virtual address: {}. Real address: {}.'.format(d, i + (d - (page-1)*page_size)))
            # time to access a page already in memory
            time = time + 0.1
            return
    
    # check if page is in swap memory
    for i in range (swap_memory_size):
        if swap_memory[i]['process'] == p and swap_memory[i]['page'] == page:
            # add page fault to process
            for process in process_time_tracker:
                if process['process'] == p:
                    process['page_fault'] = process['page_fault'] + 1
            # checks if there is empty space
            for j in range (memory_size + 1):
                # in case there is no free memory
                if j == memory_size:
                    new_frame = swap_frames(page, p)
                    used_frame = new_frame
                    swap_in_out_count = swap_in_out_count + 2
                    print('Virtual address: {}. Real address: {}.'.format(d, used_frame*page_size + (d - (page-1)*page_size)))

                # in case there is empty space in memory
                elif memory[j]['process'] == None:
                    swap_in_out_count = swap_in_out_count + 1
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
    
    print('Page {} form process {} does not exist!'.format(d, p))

def free(p):
    '''
    This function frees all the memory that is occupied by the provided process
    '''
    print('Running instruction L with parameters {}'.format(p))

    # check invalid case
    is_process = False
    for process in process_time_tracker:
        if process['process'] == p:
            is_process = True
    if is_process == False:
        print('Error! The process does not exist, skipping instruction...')
        return

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

    # update time for turnaround purposes
    for process in process_time_tracker:
        if process['process'] == p:
            process['end_time'] = time
            break

    print('Frames {} from process {} were removed from memory'.format(free_frames_memory, p))
    print('Frames {} from process {} were removed from swap memory'.format(free_frames_swap_memory, p))

def finalize():
    '''
    This function creates an output report containing some stadistics about the instructions
    '''
    global time, fifo_queue, lru_queue, process_time_tracker, swap_in_out_count, memory, swap_memory

    print('-------- End of instructions! --------')
    print('Output Report: \n')
    print('------ TURNAROUND AND PAGE FAULTS ------')
    total_time = 0
    for process in process_time_tracker:
        if process['end_time'] == None:
            print('Process {} was not freed from memory!! Skipping...'.format(process['process']))
            continue
        else:
            process_time = process['end_time'] - process['start_time']
            total_time = total_time + process_time
            print('Process {}:'.format(process['process']))
            print('      Time: {}'.format(process_time))
            print('      Page fault: {}'.format(process['page_fault']))

    print('\n------ AVERAGE TURNAROUND ------')
    print('Number of process: {}'.format(len(process_time_tracker)))
    if len(process_time_tracker) != 0:
        print('Average turnaround: {}'.format(total_time / len(process_time_tracker)))

    print('\n------ TOTAL SWAP-OUT/SWAP-IN OPERATIONS ------')
    print('Count: {}'.format(swap_in_out_count))

    # reset variables
    time = 0
    fifo_queue = []
    lru_queue = []
    process_time_tracker = []
    swap_in_out_count = 0

    memory = [{
        'process': None,
        'page': None
    }] * memory_size

    swap_memory = [{
        'process': None,
        'page': None
    }] * swap_memory_size

def end():
    print('-------- End of program! --------')
