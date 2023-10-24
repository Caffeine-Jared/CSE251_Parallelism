import multiprocessing
from itertools import permutations

def worker(word, part, queue):
    """Generate permutations for a segment of the word."""
    results = [''.join(p) for p in part]
    queue.put(results)

def all_permutations(word):
    """Generate all permutations of the given word using multiprocessing."""
    num_processes = multiprocessing.cpu_count()
    all_perms = list(permutations(word))
    segment_size = len(all_perms) // num_processes
    
    processes = []
    queue = multiprocessing.Queue()
    
    for i in range(num_processes):
        start_index = i * segment_size
        end_index = (i + 1) * segment_size if i != num_processes - 1 else len(all_perms)
        part = all_perms[start_index:end_index]
        p = multiprocessing.Process(target=worker, args=(word, part, queue))
        processes.append(p)
        p.start()

    # Collect results from all processes
    all_results = []
    for _ in range(num_processes):
        all_results.extend(queue.get())

    # Print results
    for result in all_results:
        print(result)

    # Wait for all processes to finish
    for p in processes:
        p.join()

if __name__ == "__main__":
    word = input("Enter a word: ")
    all_permutations(word)
