import time
import argparse
from multiprocessing import Pool
import io
import colorama

# from loguru import logger   ##  pip install loguru


colorama.init()
parser = argparse.ArgumentParser(description="generate variations of passwords")
parser.add_argument("-i", type=str, help="passlist path")
parser.add_argument("-o", type=str, help="output path")
parser.add_argument(
    "-level", type=int, help="level [0-8] (default 5)", default=5
)
parser.add_argument(
    "-verbose",
    type=bool,
    help=("wether to print anything or not default=False"),
    default=False,
)
args = parser.parse_args()



leet_speak_dict = leetspeak = {
    1: {
        "a": "4",
        "b": "I3",
        "e": "3",
        "g": "&",
        "l": "1",
        "o": "0",
        "s": "5",
        "t": "7",
        "z": "2",
    },
    2: {
        "a": "/\\",
        "b": "8",
        "c": "¢",
        "e": "&",
        "i": "eye",
        "k": "|<",
        "o": "Q",
        "s": "$",
        "t": "+",
        "x": "><",
        "z": "7_",
    },
}


# @logger.catch()
def munge(args):
    WORDLIST = []
    word, level = args
    capitalized = word.capitalize()
    uppered = word.upper()
    swapcased = word.swapcase()
    capswapcased = capitalized.swapcase()
    if level >= 0:
        WORDLIST.append(word)
        WORDLIST.append(capitalized)
        WORDLIST.append(uppered)
        WORDLIST.append(capswapcased)

    if level > 1:
        temp = " ".strip().join([leet_speak_dict[1].get(x, x) for x in word])
        WORDLIST.append(temp)
    if level > 2:
        temp = " ".strip().join([leet_speak_dict[2].get(x, x) for x in word])
        WORDLIST.append(temp)

    if level > 3:
        temp = " ".strip().join([leet_speak_dict[1].get(x, x) for x in swapcased])
        WORDLIST.append(temp)

    if level > 4:
        temp = " ".strip().join([leet_speak_dict[2].get(x, x) for x in swapcased])
        WORDLIST.append(temp)

    if level > 5:
        temp = " ".strip().join([leet_speak_dict[1].get(x, x) for x in capitalized])
        WORDLIST.append(temp)
    if level > 6:
        temp = " ".strip().join([leet_speak_dict[2].get(x, x) for x in capitalized])
        WORDLIST.append(temp)
    if level > 7:
        temp = " ".strip().join([leet_speak_dict[1].get(x, x) for x in capswapcased])
        WORDLIST.append(temp)
    if level >= 8:
        temp = " ".strip().join([leet_speak_dict[2].get(x, x) for x in capswapcased])
        WORDLIST.append(temp)
    return WORDLIST


start = time.time()

if __name__ == "__main__":
    lines = []
    with open(args.i, "r", encoding="utf-8", errors="ignore") as source:
        for wrd in list(set(list(source))):
            wrd = wrd.lower().rstrip()
            lines.append((wrd, args.level))
            lines.append((wrd + "123456", args.level))
            lines.append((wrd + "12", args.level))
            lines.append((wrd + "2", args.level))
            lines.append((wrd + "123", args.level))
            lines.append((wrd + "!", args.level))
            lines.append((wrd + ".", args.level))
            lines.append((wrd + "?", args.level))
            lines.append((wrd + "_", args.level))
            lines.append((wrd + "0", args.level))
            lines.append((wrd + "01", args.level))
            lines.append((wrd + "69", args.level))
            lines.append((wrd + "21", args.level))
            lines.append((wrd + "22", args.level))
            lines.append((wrd + "23", args.level))
            lines.append((wrd + "1234", args.level))
            lines.append((wrd + "8", args.level))
            lines.append((wrd + "9", args.level))
            lines.append((wrd + "10", args.level))
            lines.append((wrd + "11", args.level))
            lines.append((wrd + "13", args.level))
            lines.append((wrd + "3", args.level))
            lines.append((wrd + "4", args.level))
            lines.append((wrd + "5", args.level))
            lines.append((wrd + "6", args.level))
            lines.append((wrd + "7", args.level))
            lines.append((wrd + "12345", args.level))
            lines.append((wrd + "123456789", args.level))
            lines.append((wrd + "1234567", args.level))
            lines.append((wrd + "12345678", args.level))
            lines.append((wrd + "111111", args.level))
            lines.append((wrd + "111", args.level))
            lines.append((wrd + "777", args.level))
            lines.append((wrd + "666", args.level))
            lines.append((wrd + "101", args.level))

            for i in range(24):
                lines.append((wrd + "0" + str(i), args.level))
                lines.append((wrd + str(i), args.level))
            for i in range(50, 99, 10):
                lines.append((wrd + "0" + str(i), args.level))
                lines.append((wrd + str(i), args.level))
            for i in range(1970, 2015, 5000):
                lines.append((wrd + str(i), args.level))
        lines = list(set(lines))
WORDLIST = []


if __name__ == "__main__":
    with Pool() as pool:
        results = pool.imap_unordered(munge, lines, chunksize=10000)
        for item in results:
            WORDLIST.extend(item)


setted = list(set(list(WORDLIST)))
if args.o:
    with io.open(args.o, "a", encoding="utf-8", errors="ignore") as out:
        for word in setted:
            out.write(word + "\n")


if args.verbose:
    settedln = len(setted)
    if settedln == 0:
        pass
    else:
        print(
            colorama.Fore.GREEN
            + f"GENERATED {settedln} IN {str(int(time.time() - start))} second\s \noutput  -> {args.o}\nlevel   -> {args.level}\nverbose -> {args.verbose}"
        )
