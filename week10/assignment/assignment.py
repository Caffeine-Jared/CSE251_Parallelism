"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: <your name>

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:

"""
import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2
SPECIAL_END_VALUE = -1

def writer(shared_list, empty_semaphore, filled_semaphore, access_lock, items_to_send, writer_id):
    current_item = 1
    while current_item <= items_to_send:
        empty_semaphore.acquire()
        with access_lock:
            tail = shared_list[BUFFER_SIZE + 2]
            shared_list[tail] = current_item
            shared_list[BUFFER_SIZE + 2] = (tail + 1) % BUFFER_SIZE
            current_item += 1
        filled_semaphore.release()

    for _ in range(READERS):
        empty_semaphore.acquire()
        with access_lock:
            tail = shared_list[BUFFER_SIZE + 2]
            shared_list[tail] = SPECIAL_END_VALUE
            shared_list[BUFFER_SIZE + 2] = (tail + 1) % BUFFER_SIZE
        filled_semaphore.release()

def reader(shared_list, empty_semaphore, filled_semaphore, access_lock, reader_id, read_count_index):
    read_count = 0
    end_count = 0
    while True:
        filled_semaphore.acquire()
        with access_lock:
            head = shared_list[BUFFER_SIZE + 1]
            item = shared_list[head]
            shared_list[BUFFER_SIZE + 1] = (head + 1) % BUFFER_SIZE
            if item == SPECIAL_END_VALUE:
                end_count += 1
                if end_count == WRITERS:
                    shared_list[read_count_index] = read_count
                    break
                continue
            print(item, end=', ', flush=True)
            read_count += 1
        empty_semaphore.release()



def main():
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    #      - The buffer should be size 10 PLUS at least three other
    #        values (ie., [0] * (BUFFER_SIZE + 3)).  The extra values
    #        are used for the head and tail for the circular buffer.
    #        The another value is the current number that the writers
    #        need to send over the buffer.  This last value is shared
    #        between the writers.
    #        You can add another value to the sharedable list to keep
    #        track of the number of values received by the readers.
    #        (ie., [0] * (BUFFER_SIZE + 4))
    read_count_indices = [BUFFER_SIZE + 4 + i for i in range(READERS)]
    shared_list = smm.ShareableList([0] * (BUFFER_SIZE + 4 + READERS))

    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    empty_semaphore = mp.Semaphore(BUFFER_SIZE)
    filled_semaphore = mp.Semaphore(0)
    access_lock = mp.Lock()

    # TODO - create reader and writer processes
    writers = [mp.Process(target=writer, args=(shared_list, empty_semaphore, filled_semaphore, access_lock, items_to_send, i)) for i in range(WRITERS)]
    readers = [mp.Process(target=reader, args=(shared_list, empty_semaphore, filled_semaphore, access_lock, i, read_count_indices[i])) for i in range(READERS)]

    # TODO - Start the processes and wait for them to finish
    for w in writers:
        w.start()
    for r in readers:
        r.start()

    for w in writers:
        w.join()
    for r in readers:
        r.join()

    print(f'{items_to_send} values sent')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    total_values_received = sum(shared_list[index] for index in read_count_indices)
    print(f'\n{items_to_send} values sent')
    print(f'Total values received: {total_values_received}')

    smm.shutdown()

if __name__ == '__main__':
    main()