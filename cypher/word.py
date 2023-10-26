# # def load_dictionary(file_path):
# #     """Load words from a dictionary file into a set."""
# #     with open(file_path, 'r') as f:
# #         words = set(word.strip().lower() for word in f)
# #     return words

# # def permutations(string):
# #     """Generate all permutations of a given string."""
# #     if len(string) == 1:
# #         return string

# #     recursive_perms = []
# #     for c in string:
# #         for perm in permutations(string.replace(c, '', 1)):
# #             recursive_perms.append(c + perm)

# #     return set(recursive_perms)

# # def combinations(string, length):
# #     """Generate combinations of the string of a given length."""
# #     if length == 0:
# #         return ['']
# #     return [c + s for c in string for s in combinations(string.replace(c, '', 1), length-1)]

# # def valid_permutations(word, dictionary):
# #     """Generate and print valid permutations of the given word for the Spelling Bee game."""
# #     central_letter = word[0]
# #     valid_count = 0
# #     seen_words = set()  # To keep track of words we've already printed
# #     for length in range(4, len(word) + 1):
# #         for combo in combinations(word, length):
# #             for perm in set(permutations(combo)):
# #                 if perm.lower() in dictionary and central_letter in perm and perm not in seen_words:
# #                     print(perm)
# #                     seen_words.add(perm)
# #                     valid_count += 1
# #     print(f"Found {valid_count} valid permutations.")

# # if __name__ == "__main__":
# #     word = input("Enter the letters (central letter first): ").lower()
# #     dictionary = load_dictionary('dictionary.txt')
# #     valid_permutations(word, dictionary)

# def load_dictionary(file_path):
#     """Load words from a dictionary file into a set."""
#     with open(file_path, 'r') as f:
#         words = set(word.strip().lower() for word in f)
#     return words

# def valid_words_from_dictionary(chars, dictionary):
#     """Find and print valid words from the dictionary composed only of the specified characters."""
#     valid_count = 0
#     for word in dictionary:
#         if set(word).issubset(chars):  # Ensure word contains only characters from the input set
#             print(word)
#             valid_count += 1
#     print(f"Found {valid_count} valid words.")

# if __name__ == "__main__":
#     chars = set(input("Enter the characters: ").lower())
#     dictionary = load_dictionary('dictionary.txt')
#     valid_words_from_dictionary(chars, dictionary)
def load_dictionary(file_path):
    """Load words from a dictionary file into a set."""
    with open(file_path, 'r') as f:
        words = set(word.strip().lower() for word in f)
    return words

def valid_words_from_dictionary(chars, central_letter, dictionary):
    """Find and print valid words from the dictionary composed only of the specified characters."""
    valid_count = 0
    for word in dictionary:
        if len(word) >= 4 and set(word).issubset(chars) and central_letter in word:  # Ensure word contains only characters from the input set, includes the central letter, and is longer than 4 letters
            print(word)
            valid_count += 1
    print(f"Found {valid_count} valid words.")

if __name__ == "__main__":
    input_chars = input("Enter the characters (central letter first): ").lower()
    central_letter = input_chars[0]
    chars = set(input_chars)
    dictionary = load_dictionary('dictionary.txt')
    valid_words_from_dictionary(chars, central_letter, dictionary)


