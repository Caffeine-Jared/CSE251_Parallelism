"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: <Your name here>
Purpose: Process Task Files

Instructions:  See I-Learn

TODO

Add your comments here on the pool sizes that you used for your assignment and
why they were the best choices.

pool_prime - this was probably the more cpu intensive task, and i decided to throw as much cpu power that i had at it, which was 12 cores
pool_word - i thought that maybe by inceasing the pool size, any I/O bottlenecks might not be an issue
pool_upper - just flexing w/ my cpu tbh
pool_sum - having the higer number of processes helped this get done faster
pool_name - this was io bound, and having more processes allowed it to get done faster

"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
 
def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    if is_prime(value):
        return f'{value:,} is prime'
    else:
        return f'{value:,} is not prime'


def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open('words.txt') as f:
        words = f.read().splitlines()
    if word in words:
        return f'{word} Found'
    else:
        return f'{word} not found *****'

def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    return f'{text} ==> {text.upper()}'

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    total = sum(range(start_value, end_value + 1))
    return f'sum of {start_value:,} to {end_value:,} = {total:,}'


def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        name = response.json().get('name')
        return f'{url} has name {name}'
    except requests.RequestException as e:
        return f'{url} had an error receiving the information: {e}'

def callback_prime(result):
    result_primes.append(result)

def callback_word(result):
    result_words.append(result)

def callback_upper(result):
    result_upper.append(result)

def callback_sum(result):
    result_sums.append(result)

def callback_name(result):
    result_names.append(result)

def main(result_primes, result_words, result_upper, result_sums, result_names):
    log = Log(show_terminal=True)
    log.start_timer()

# TODO Create process pools
    pool_prime = mp.Pool(12)
    pool_word = mp.Pool(8)
    pool_upper = mp.Pool(4)
    pool_sum = mp.Pool(8)
    pool_name = mp.Pool(12)

    # TODO you can change the following
    # TODO start and wait pools
    
    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        task = load_json_file(filename)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            pool_prime.apply_async(task_prime, args=(task['value'],), callback=callback_prime)
        elif task_type == TYPE_WORD:
            pool_word.apply_async(task_word, args=(task['word'],), callback=callback_word)
        elif task_type == TYPE_UPPER:
            pool_upper.apply_async(task_upper, args=(task['text'],), callback=callback_upper)
        elif task_type == TYPE_SUM:
            pool_sum.apply_async(task_sum, args=(task['start'], task['end']), callback=callback_sum)
        elif task_type == TYPE_NAME:
            pool_name.apply_async(task_name, args=(task['url'],), callback=callback_name)
        else:
            log.write(f'Error: unknown task type {task_type}')

    pool_prime.close()
    pool_word.close()
    pool_upper.close()
    pool_sum.close()
    pool_name.close()

    pool_prime.join()
    pool_word.join()
    pool_upper.join()
    pool_sum.join()
    pool_name.join()


    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    with mp.Manager() as manager:
        result_primes = manager.list()
        result_words = manager.list()
        result_upper = manager.list()
        result_sums = manager.list()
        result_names = manager.list()

        main(result_primes, result_words, result_upper, result_sums, result_names)