# import itertools

# def generate_permutations(word):
    
#     permutations = [''.join(p) for p in itertools.permutations(word)]
    
#     r_permutations = [p for p in permutations if p[0] == 'R']
    
#     return r_permutations

# word = "NOITCELFER"
# results = generate_permutations(word)

# print("Permutations that start with 'R':")
# for r in results:
#     print(r)
from collections import Counter
import multiprocessing

def load_dictionary(filename):
    with open(filename, 'r') as f:
        return [word.strip().upper() for word in f.readlines()]

def is_valid_word(word, letter_count):
    return Counter(word) == letter_count

def process_chunk(chunk, letter_count):
    return [word for word in chunk if is_valid_word(word, letter_count)]

def generate_permutations_to_file(input_word, output_filename, dictionary_filename):
    word_set = load_dictionary(dictionary_filename)
    letter_count = Counter(input_word)
    valid_count = 0

    # Filtering dictionary words
    filtered_words = [word for word in word_set if word.startswith("TH") and len(word) == len(input_word)]

    # Chunking the filtered words to process in parallel
    num_processes = 4
    chunk_size = len(filtered_words) // num_processes
    chunks = [filtered_words[i:i+chunk_size] for i in range(0, len(filtered_words), chunk_size)]

    with open(output_filename, 'w') as f:
        with multiprocessing.Pool(num_processes) as pool:
            results = pool.starmap(process_chunk, [(chunk, letter_count) for chunk in chunks])
            for valid_words in results:
                valid_count += len(valid_words)
                for word in valid_words:
                    f.write(word + '\n')

    print(f"Finished searching dictionary!")
    print(f"Found {valid_count} valid words starting with 'TH' and using the letters from '{input_word}'!")

print("Starting script...")
if __name__ == '__main__':
    print("Inside main...")
    input_word = "THEEEESRHDBENAHEMRE"
    output_filename = "permutations.txt"
    dictionary_filename = "dictionary.txt"
    generate_permutations_to_file(input_word, output_filename, dictionary_filename)

