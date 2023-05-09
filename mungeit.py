import time
import argparse
from multiprocessing import Pool
import io
import colorama
from typing import List, Tuple

import dicts

LEET_DICT = dicts.leetspeak_dict
SUFFIXES = dicts.suffixes

def generate_wordlist(word_and_level: Tuple[str, int]) -> List[str]:
    wordlist = []
    word, level = word_and_level # Because python pickling has always sucked


    capitalized = word.capitalize()
    uppered = word.upper()
    swapcased = word.swapcase()
    capswapcased = capitalized.swapcase()

    def add_to_wordlist(key: int, word_variant: str) -> None:
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
    # No need to start the timer if we're not ouputting it
    if args.verbose: 
        start = time.time()

    # Takes every line, adds range and suffix additions, and makes tuples with the argument.level
    with open(args.input, "r", encoding="utf-8", errors="ignore") as source:
        lines = generate_lines(source, args.level)

    # This is then fed into generate wordlist
    wordlist = []
    with Pool() as pool:
        results = pool.imap_unordered(generate_wordlist, lines, chunksize=10000)
        for item in results:
            wordlist.extend(item)

    setted = list(set(list(wordlist)))

    # Finally, it's output to a file.
    if args.output:
        with io.open(args.output, "a", encoding="utf-8", errors="ignore") as out:
            for word in setted:
                out.write(word + "\n")

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
    parser.add_argument("-i", "--input", type=str, help="Passlist input path")
    parser.add_argument("-o", "--output", type=str, help="Munged passlist output path")
    parser.add_argument("-l", "--level", type=int, help="Level [0-8] (default 5)", default=5)
    parser.add_argument("-v", "--verbose", action="store_true",
                        help=("Whether to print anything or not"), default=False)
    arguments = parser.parse_args()

    munge(arguments)
