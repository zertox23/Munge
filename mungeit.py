"""
This module generates variations of passwords based on the input passlist file.

Authors: iqthegoat & stochasticsanity
Based on the work done by Th3S3cr3tAg3nt

Functions:
- generate_wordlist(word: str, level: int) -> List[str]: 
    - Generates a list of variations of a given word based on the specified level.
- generate_lines(source: io.TextIOWrapper, level: int) -> List[Tuple[str, int]]: 
    - Generates a list of tuples containing a word and its corresponding level.
- munge(arguments: argparse.Namespace) -> None: 
    - Uses generate_wordlist() and generate_lines() to create variations of
      passwords and write them to an output file.

"""

import argparse
from multiprocessing import Pool
import io
import os
import time
from typing import List, Tuple
import colorama

import dictionaries

LEET_DICT = dictionaries.leetspeak_dict
SUFFIXES = dictionaries.suffixes

def caesar_cipher(word: str, shift: int) -> str:
    """
    Applies a Caesar cipher shift to the given word.

    Args:
        word (str): The word to apply the Caesar cipher to.
        shift (int): The shift value for the Caesar cipher.

    Returns:
        str: The word after applying the Caesar cipher shift.
    """
    result = []
    for c in word:
        if c.isupper():
            result.append(chr((ord(c) - 65 + shift) % 26 + 65))
        elif c.islower():
            result.append(chr((ord(c) - 97 + shift) % 26 + 97))
        else:
            result.append(c)
    return ''.join(result)

def generate_wordlist(word_and_level: Tuple[str, int]) -> List[str]:
    """
    Generates a list of variations of a given word based on the specified level. 

    The variations include:
    - The original word, capitalized, uppercased, swapcased, 
      and capitalized swapcased versions of the word.
    - Leetspeak variations of these word versions based on the level.

    Args:
        word_and_level (Tuple[str, int]): A tuple containing a word and a level.
            word (str): The original word to generate variations of.
            level (int): The higher the level, the more complex the variations.

    Returns:
        List[str]: A list of variations of the original word, dependant on the level.
    """
    wordlist = []
    word, level = word_and_level # Because python pickling has always sucked


    capitalized = word.capitalize()
    uppered = word.upper()
    swapcased = word.swapcase()
    capswapcased = capitalized.swapcase()

    def add_to_wordlist(key: int, word_variant: str) -> None:
        """
        Converts a given word variant into leetspeak and appends it to the wordlist. 
        Note: This function modifies the 'wordlist' variable from the outer function's scope.

        Args:
            key (int): The key for the leetspeak dictionary to use.
            word_variant (str): The variant of the original word to convert into leetspeak.

        Returns:
            None: This function doesn't return anything. It modifies the 'wordlist' list in place.
        """
        leeted_words = " ".join([LEET_DICT[key].get(x, x) for x in word_variant])
        wordlist.append(leeted_words)

    if level >= 0:
        wordlist.extend([word, capitalized, uppered, swapcased, capswapcased])
    if level > 1:
        add_to_wordlist(1, word)
    if level > 2:
        add_to_wordlist(2, word)
    if level > 3:
        add_to_wordlist(1, swapcased)
    if level > 4:
        add_to_wordlist(2, swapcased)
    if level > 5:
        add_to_wordlist(1, capitalized)
    if level > 6:
        add_to_wordlist(2, capitalized)
    if level > 7:
        add_to_wordlist(1, capswapcased)
    if level >= 8:
        add_to_wordlist(2, capswapcased)

    return wordlist

def generate_lines(source: io.TextIOWrapper, level: int) -> List[Tuple[str, int]]:
    """
    Generates a list of tuples containing a word and its corresponding level.
    Also appends range and suffix additions to the words

    Args:
    - source (io.TextIOWrapper): The input passlist file.
    - level (int): The level of variation to generate.

    Returns:
    - List[Tuple[str, int]]: A list of tuples containing a word and its corresponding level.
    """

    favored_number_ranges = [
        range(24),
        range(50, 99, 10),
    ]

    word_variants = []

    for wrd in set(map(str.strip, map(str.lower, source))):
        for suffix in SUFFIXES:
            word_variants.append(wrd + suffix)

        for favored_range in favored_number_ranges:
            for number in favored_range:
                word_variants.append(wrd + "0" + str(number))
                word_variants.append(wrd + str(number))

        for i in range(1970, 2015):  # Previously only did it for 1970, fixed!
            word_variants.append(wrd + str(i))

    # Create tuples (word, level) at the end
    lines = [(word_variant, level) for word_variant in set(word_variants)]

    return lines

def munge(args: argparse.Namespace) -> None:
    """
    Uses generate_wordlist() and generate_lines() to create variations of 
    passwords and write them to an output file.
    
    Args:
    - arguments (argparse.Namespace): The parsed command-line arguments.
    """
    # No need to start the timer if we're not ouputting it
    if args.verbose:
        start = time.time()

    # Takes every line, adds range and suffix additions, and makes tuples with the argument.level
    with io.open(args.input, "r", encoding="utf-8", errors="ignore") as source:
        lines = generate_lines(source, args.level)

    # This is then fed into generate wordlist
    wordlist = []
    with Pool() as pool:
        results = pool.imap_unordered(generate_wordlist, lines, chunksize=10000)
        for item in results:
            wordlist.extend(item)

    setted = list(set(list(wordlist)))

    # Finally, it's output to a file.
    if not args.output:
        filename, file_extension = os.path.splitext(args.input)
        args.output = f"{filename}_munged{file_extension}"

    with open(args.output, "a", encoding="utf-8", errors="ignore") as out:
        for word in setted:
            cleaned_word = word.strip().replace(" ", "")
            out.write(cleaned_word + "\n")

        if args.caesar:
            # Apply Caesar cipher shifts from 1 to 26
            all_words = setted.copy()
            for shift in range(1, 27):
                for word in setted:
                    word_no_spaces = word.replace(" ", "")
                    shifted_word = caesar_cipher(word_no_spaces, shift)
                    shifted_word = shifted_word.replace(" ", "")
                    if shifted_word not in all_words:
                        out.write(shifted_word + "\n")
                        all_words.append(shifted_word)

    # Output a timer for cred.
    if args.verbose:
        settled_len = len(setted)
        if settled_len == 0:
            pass
        print(
            colorama.Fore.GREEN
            + f"GENERATED {settled_len} IN {str(int(time.time() - start))} seconds\n"
            + f"output  -> {args.output}\n"
            + f"level   -> {args.level}\n"
            + f"verbose -> {args.verbose}"
        )

if __name__ == "__main__":
    colorama.init()
    parser = argparse.ArgumentParser(description="Generate variations of passwords")
    parser.add_argument("-C", "--caesar", action="store_true", default=False, help="Apply Caesar cipher shifts")
    parser.add_argument("-i", "--input", type=str, required=True, help="Passlist input file")
    parser.add_argument("-o", "--output", type=str, help="Munged passlist output file")
    parser.add_argument("-l", "--level", type=int, help="Level [0-8] (default 5)", default=5)
    parser.add_argument("-v", "--verbose", action="store_true", help=("Whether to print anything or not"), default=False)
    arguments = parser.parse_args()

    munge(arguments)
