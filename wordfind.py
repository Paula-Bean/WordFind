#!/usr/bin/env python3

# Exercise the index prepared by 'wordfindmake.py'.
#
# The set of words which match a given pattern is whittled out using
# progressive set intersection.
#
# An intersection of two sets is a set of items common to both sets:
#
#     >>> a = set([1, 2, 3])
#     >>> b = set([2, 3, 4])
#     >>> a.intersection(b)
#     set([2, 3])
#     >>> a & b   # & is the operator version of intersect()
#     set([2, 3])
#     >>> a &= b  # &= is the updating version of &, intersection_update()
#     >>> a
#     set([2, 3])
#
# Pattern "..l.n" means: five-letter words ending on 'n', with an 'l'
#                        as the 3d letter. E.g. 'melon' or 'balun'.

from collections import defaultdict
import os
import sys
import random
import time

def readwords(fn):
    """The index is a dictionary of dictionaries of sets, keyed on
       position and letter.
    """
    index = defaultdict(lambda: defaultdict(set)) #
    for line in open(fn):
        parts = line.split()
        pos = int(parts[0])
        letter = parts[1]
        words = parts[2:]
        index[pos][letter] = set(words)
    return index


def findwords(index, pattern):
    """Return a list of all the words that satisfy the supplied pattern.
       The pattern is a regexp which only contains letters and dots,
       for example: 'd.l.n'. The word 'dylan' would match that pattern.
    """
    # Check if the pattern is made up of only dots. If so, return all
    # the words of the specified length.
    letters = set(pattern)
    if len(letters) == 1 and letters.pop() == ".":
        return index[len(pattern)]["*"]

    letters_encountered = 0
    foundwords = None
    for pos, letter in enumerate(pattern):
        if letter == ".":
            continue
        letters_encountered += 1
        if letters_encountered == 1:
            foundwords = set(index[pos][letter]) # First letter in pattern.
        else:
            foundwords &= index[pos][letter] # Subsequent letters.
            if not foundwords:
                break
    if foundwords:
        # Keep only words which have the same length as the search pattern.
        patternlen = len(pattern)
        return [word for word in foundwords if len(word) == patternlen]
    else:
        return []


def randompattern():
    patlen = int(random.triangular(2, 14, 9)) # 2...14, skewed towards the 9
    patchars = ['.'] * patlen
    lettercount = 1 + int(patlen / 4)
    for i in range(lettercount):
        pos = int(random.uniform(0, patlen))
        alphabet = "etaoinsrhdlucmfywgpbvkxqjz" # Ordered on frequency.
        letter = alphabet[int(random.triangular(0, 26, 0))]
        patchars[pos] = letter
    return "".join(patchars)


if __name__ == "__main__":
    if not os.path.exists("wordfinder.txt"):
        print("Can't open 'wordfinder.txt'.")
        print("Please run 'python makewordfind.py' first.")
        sys.exit()

    index = readwords("wordfinder.txt")

    examplewords = [word for word in index[3]["e"] if len(word) == 5]
    print("\nWelcome to PaulaBean's blindingly fast wordfinder, for crosswords and scrabble!")
    print("These are some five-letter words I know:", ", ".join(examplewords[:6]) + ".")
    print("Try a pattern like 'z...y' to find five-letter words starting with 'z' and ending on 'y'.")
    print("Or find something more interesting, like '..e..a.' or '...st...'.")
    print("Enter 'quit' or 'q' to end the program. Just press Enter to accept the suggestion.")
    while True:
        suggestion = randompattern()
        try:
            prompt = "\nSearch pattern [%s] (or 'q' to end): " % suggestion
            pattern = input(prompt)
        except (KeyboardInterrupt, EOFError):
            print()
            break
        if pattern == "":
            pattern = suggestion
        if pattern in ("q", "quit"):
            break
        start = time.time()
        words = findwords(index, pattern)
        duration = time.time() - start
        if not words:
            print("\nNo matches")
        else:
            print("\n" + ", ".join(word for word in words))
            if len(words) > 10:
                msec = duration * 1000
                print("%s words found in %.2f msec" % (len(words), msec))
