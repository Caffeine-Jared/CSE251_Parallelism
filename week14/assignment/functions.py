"""
Course: CSE 251, week 14
File: functions.py
Author: <your name>

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

<Add your comments here>


Describe how to speed up part 2

<Add your comments here>


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *
import queue

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement Depth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging
      # Request family details
    request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    request.start()
    request.join()

    family_data = request.get_response()
    if family_data:
        family = Family(family_data)
        tree.add_family(family)  # Add the family to the tree

        # Process husband and wife
        if family.get_husband():
            husband_request = Request_thread(f'{TOP_API_URL}/person/{family.get_husband()}')
            husband_request.start()
            husband_request.join()
            husband = Person(husband_request.get_response())
            tree.add_person(husband)  # Add the husband to the tree

        if family.get_wife():
            wife_request = Request_thread(f'{TOP_API_URL}/person/{family.get_wife()}')
            wife_request.start()
            wife_request.join()
            wife = Person(wife_request.get_response())
            tree.add_person(wife)  # Add the wife to the tree

        # Process children
        children_threads = []
        for child_id in family.get_children():
            child_request = Request_thread(f'{TOP_API_URL}/person/{child_id}')
            child_request.start()
            children_threads.append(child_request)

        for child_thread in children_threads:
            child_thread.join()
            child = Person(child_thread.get_response())
            tree.add_person(child)  # Add each child to the tree

            # Call depth_fs_pedigree for each child's family in a new thread
            thread = threading.Thread(target=depth_fs_pedigree, args=(child.get_parentid(), tree))
            thread.start()
            thread.join() 
    pass

# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging
    family_queue = queue.Queue()
    family_queue.put(family_id)

    while not family_queue.empty():
        current_family_id = family_queue.get()

        # Request family details
        family_request = Request_thread(f'{TOP_API_URL}/family/{current_family_id}')
        family_request.start()
        family_request.join()

        family_data = family_request.get_response()
        if family_data:
            family = Family(family_data)
            tree.add_family(family)  # Add the family to the tree

            # Process husband and wife using appropriate methods from the Family class
            if family.get_husband():
                husband_request = Request_thread(f'{TOP_API_URL}/person/{family.get_husband()}')
                husband_request.start()
                husband_request.join()
                husband = Person(husband_request.get_response())
                tree.add_person(husband)

            if family.get_wife():
                wife_request = Request_thread(f'{TOP_API_URL}/person/{family.get_wife()}')
                wife_request.start()
                wife_request.join()
                wife = Person(wife_request.get_response())
                tree.add_person(wife)

            # Process children
            children_threads = []
            for child_id in family.get_children():
                child_request = Request_thread(f'{TOP_API_URL}/person/{child_id}')
                child_request.start()
                children_threads.append(child_request)

            for child_thread in children_threads:
                child_thread.join()
                child = Person(child_thread.get_response())
                tree.add_person(child)

                # Add child's family ID to the queue for further processing
                child_family_id = child.get_parentid()  # Adjust based on the Person class's method
                if child_family_id and child_family_id != current_family_id:
                    family_queue.put(child_family_id)
    pass

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    # TODO - Printing out people and families that are retrieved from the server will help debugging
    family_queue = queue.Queue()
    family_queue.put(family_id)

    # Semaphore to limit the number of concurrent threads to 5
    semaphore = threading.Semaphore(5)

    while not family_queue.empty():
        current_family_id = family_queue.get()

        def process_family(fid):
            with semaphore:
                family_request = Request_thread(f'{TOP_API_URL}/family/{fid}')
                family_request.start()
                family_request.join()

                family_data = family_request.get_response()
                if family_data:
                    family = Family(family_data)
                    tree.add_family(family)  # Add the family to the tree

                    # Process husband and wife using appropriate methods from the Family class
                    if family.get_husband():
                        husband_request = Request_thread(f'{TOP_API_URL}/person/{family.get_husband()}')
                        husband_request.start()
                        husband_request.join()
                        husband = Person(husband_request.get_response())
                        tree.add_person(husband)

                    if family.get_wife():
                        wife_request = Request_thread(f'{TOP_API_URL}/person/{family.get_wife()}')
                        wife_request.start()
                        wife_request.join()
                        wife = Person(wife_request.get_response())
                        tree.add_person(wife)

                    # Process children
                    children_threads = []
                    for child_id in family.get_children():
                        child_request = Request_thread(f'{TOP_API_URL}/person/{child_id}')
                        child_request.start()
                        children_threads.append(child_request)

                    for child_thread in children_threads:
                        child_thread.join()
                        child = Person(child_thread.get_response())
                        tree.add_person(child)

                        # Add child's family ID to the queue for further processing
                        child_family_id = child.get_parentid()  # Adjust based on the Person class's method
                        if child_family_id and child_family_id != fid:
                            family_queue.put(child_family_id)

        thread = threading.Thread(target=process_family, args=(current_family_id,))
        thread.start()
        thread.join()
    pass