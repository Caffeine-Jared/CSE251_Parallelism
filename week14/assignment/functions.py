"""
Course: CSE 251, week 14
File: functions.py
Author: <jared linare>

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
request = Request_thread(f'{TOP_API_URL}/family/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
request = Request_thread(f'{TOP_API_URL}/person/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

So in part one i decided to use a set which helped avoid some repeated processing. This really sped up the first part! 

by using a set, it fixed some of the issues I had during coding, like 404s, which now rarely if ever occur. Additionally, it means that 
the code will be able be more efficient


Describe how to speed up part 2

Using a queue helped manage the family processing, and did result in a 3 sec reduction in time from my old code to the current code.


Extra (Optional) 10% Bonus to speed up part 3

I tried to use a semaphore here, but kinda struggled, overall I tried, and I think i got it down to a reasonable time. 

"""
from common import *
import queue
import threading

# -----------------------------------------------------------------------------
# by using the processed families argument i discovered i can more easily manage or keep track of family ids - seriously fixed so many issues
# glad i went over some older notes and got this idea

def depth_fs_pedigree(family_id, tree, processed_families=set()):
# KEEP this function even if you don't implement it
# TODO - implement Depth first retrieval
# TODO - Printing out people and families that are retrieved from the server will help debugging
    if family_id in processed_families:
        return
    processed_families.add(family_id)

    request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    request.start()
    request.join()

    family_data = request.get_response()
    if family_data:
        family = Family(family_data)
        if not tree.does_family_exist(family.get_id()):
            tree.add_family(family)

        person_ids = [family.get_husband(), family.get_wife()] + family.get_children()
        person_threads = []

        def process_person(person_id):
            if person_id and not tree.does_person_exist(person_id):
                person_request = Request_thread(f'{TOP_API_URL}/person/{person_id}')
                person_request.start()
                person_request.join()
                person_data = person_request.get_response()
                if person_data:
                    person = Person(person_data)
                    tree.add_person(person)

                    parent_family_id = person.get_parentid()
                    if parent_family_id and not tree.does_family_exist(parent_family_id):
                        depth_fs_pedigree(parent_family_id, tree, processed_families)

        for person_id in person_ids:
            thread = threading.Thread(target=process_person, args=(person_id,))
            person_threads.append(thread)
            thread.start()

        for thread in person_threads:
            thread.join()
    pass

# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree):
# KEEP this function even if you don't implement it
# TODO - implement breadth first retrieval
# TODO - Printing out people and families that are retrieved from the server will help debugging
    family_queue = queue.Queue()
    family_queue.put(family_id)
    processed_families = set()

    while not family_queue.empty():
        current_family_id = family_queue.get()
        if current_family_id in processed_families:
            continue
        processed_families.add(current_family_id)

        family_request = Request_thread(f'{TOP_API_URL}/family/{current_family_id}')
        family_request.start()
        family_request.join()

        family_data = family_request.get_response()
        if family_data:
            family = Family(family_data)
            if not tree.does_family_exist(family.get_id()):
                tree.add_family(family)

            person_ids = [family.get_husband(), family.get_wife()] + family.get_children()
            person_threads = []

            def process_person(person_id):
                if person_id and not tree.does_person_exist(person_id):
                    person_request = Request_thread(f'{TOP_API_URL}/person/{person_id}')
                    person_request.start()
                    person_request.join()
                    person_data = person_request.get_response()
                    if person_data:
                        person = Person(person_data)
                        tree.add_person(person)

                        parent_family_id = person.get_parentid()
                        if parent_family_id and parent_family_id != current_family_id:
                            family_queue.put(parent_family_id)

            for person_id in person_ids:
                thread = threading.Thread(target=process_person, args=(person_id,))
                person_threads.append(thread)
                thread.start()

            for thread in person_threads:
                thread.join()
    pass

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(start_family_id, tree):
# KEEP this function even if you don't implement it
# TODO - implement breadth first retrieval
#      - Limit number of concurrent connections to the FS server to 5
# TODO - Printing out people and families that are retrieved from the server will help debugging
    family_queue = queue.Queue()
    family_queue.put((start_family_id, 1))
    processed_families = set()

    semaphore = threading.Semaphore(5)

    while not family_queue.empty():
        current_family_id, generation = family_queue.get()

        if current_family_id in processed_families:
            continue

        processed_families.add(current_family_id)

        def process_family(fid, gen):
            with semaphore:
                family_request = Request_thread(f'{TOP_API_URL}/family/{fid}')
                family_request.start()
                family_request.join()

                family_data = family_request.get_response()
                if family_data:
                    family = Family(family_data)
                    tree.add_family(family)

                    person_ids = [family.get_husband(), family.get_wife()] + family.get_children()
                    for person_id in person_ids:
                        if person_id and not tree.does_person_exist(person_id):
                            person_request = Request_thread(f'{TOP_API_URL}/person/{person_id}')
                            person_request.start()
                            person_request.join()
                            person_data = person_request.get_response()
                            if person_data:
                                person = Person(person_data)
                                tree.add_person(person)

                                child_family_id = person.get_parentid()
                                if child_family_id and child_family_id != fid:
                                    family_queue.put((child_family_id, gen + 1))

        thread = threading.Thread(target=process_family, args=(current_family_id, generation))
        thread.start()
        thread.join()  
    pass