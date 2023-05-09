import time
import argparse
from multiprocessing import Pool
import io
import colorama
from typing import List, Tuple

import dicts

colorama.init()
parser = argparse.ArgumentParser(description="Generate variations of passwords")
parser.add_argument("-i", "--input", type=str, help="Passlist input path")
parser.add_argument("-o", "--output", type=str, help="Munged passlist output path")
parser.add_argument("-l", "--level", type=int, help="Level [0-8] (default 5)", default=5)
parser.add_argument("-v", "--verbose", action="store_true",
                    help=("Whether to print anything or not"), default=False)
arguments = parser.parse_args()


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

    lines = []
    
    for wrd in set(map(str.strip, map(str.lower, source))):
        for suffix in SUFFIXES:
                lines.append((wrd + suffix, level))

        for favored_range in favored_number_ranges:
            for number in favored_range:
                lines.append((wrd + "0" + str(number), level))
                lines.append((wrd + str(number), level))

        for i in range(1970, 2015): # Previously only did it for 1970, fixed! 
            lines.append((wrd + str(i), level))

    return list(set(lines))

start = time.time()

if __name__ == "__main__":
    lines = []
    # Takes every line, adds range and suffix additions, and makes tuples with the argument.level
    with open(arguments.input, "r", encoding="utf-8", errors="ignore") as source:
        lines = generate_lines(source, arguments.level)

    WORDLIST = []

    with Pool() as pool:
        results = pool.imap_unordered(generate_wordlist, lines, chunksize=10000)
        for item in results:
            WORDLIST.extend(item)


    setted = list(set(list(WORDLIST)))
    if arguments.output:
        with io.open(arguments.output, "a", encoding="utf-8", errors="ignore") as out:
            for word in setted:
                out.write(word + "\n")


    if arguments.verbose:
        settedln = len(setted)
        if settedln == 0:
            pass
        else:
            print(
                colorama.Fore.GREEN
                + f"GENERATED {settedln} IN {str(int(time.time() - start))} second\s \noutput  -> {arguments.output}\nlevel   -> {arguments.level}\nverbose -> {arguments.verbose}"
            )
