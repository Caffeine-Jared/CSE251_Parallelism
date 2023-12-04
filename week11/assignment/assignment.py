"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner: {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count}')
    time.sleep(random.uniform(0, 1))


def cleaner(id, start_time, cleaned_count, people_count, room_lock, cleaner_lock):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    while time.time() < start_time + TIME:
        cleaner_waiting()
        with cleaner_lock:
            print(f"Cleaner {id} is trying to clean. Guest count: {people_count.value}")  # Diagnostic print
            if people_count.value == 0:
                with room_lock:
                    print(STARTING_CLEANING_MESSAGE)
                    cleaner_cleaning(id)
                    print(STOPPING_CLEANING_MESSAGE)
                    with cleaned_count.get_lock():
                        cleaned_count.value += 1


def guest(id, start_time, people_count, party_count, room_lock):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (call guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    while time.time() < start_time + TIME:
        guest_waiting()
        with people_count.get_lock():
            if people_count.value == 0:
                room_lock.acquire()  # Acquire room lock if first guest
            people_count.value += 1
            if people_count.value == 1:
                print(STARTING_PARTY_MESSAGE)
                with party_count.get_lock():
                    party_count.value += 1

        guest_partying(id, people_count.value)

        with people_count.get_lock():
            people_count.value -= 1
            if people_count.value == 0:
                print(STOPPING_PARTY_MESSAGE)
                room_lock.release() 

    pass

def main():
    room_lock = mp.Lock()
    cleaner_lock = mp.Lock()
    people_count = mp.Value('i', 0)
    cleaned_count = mp.Value('i', 0)
    party_count = mp.Value('i', 0)
    start_time = time.time()

    cleaners = []
    guests = []

    for i in range(CLEANING_STAFF):
        p = mp.Process(target=cleaner, args=(i, start_time, cleaned_count, room_lock, cleaner_lock))
        cleaners.append(p)
        p.start()

    for i in range(HOTEL_GUESTS):
        p = mp.Process(target=guest, args=(i, start_time, people_count, party_count, room_lock))
        guests.append(p)
        p.start()

    for p in cleaners + guests:
        p.join()

    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')


if __name__ == '__main__':
    main()

