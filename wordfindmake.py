#!/usr/bin/env python3

'''
This program reads a list of words from a file 
like '/usr/share/dict/words' (every word on its own
line), and builds multiple indexes into these words.

The goal is to quickly find words for crosswords and Scrabble, where 
often certain letters of a word are known, but others have to be 
filled in.

The indexes are identified by:

  1) position in the word
  2) letter of the alfabet

Thus, there is a separate index for every combination of position and
letter. The maximum word length is 14, the minimum is 2. This gives
approximately 26 * 12 = 312 indexes.

Examples:

  index[4]['a'] <-- set of words which have an 'a' as the 5th letter,
                    like 'cobra' and 'valiant'.
                    
  index[0]['b'] <-- set of words which start with a 'b', 
                    like 'brawler' and 'bye'.

Later on, these indexes are combined to narrow down search results in
a specific way, for example to answer this question: "What are the 
words that start with a 'd', have a 'l' as the 3rd letter, and 
a 'n' as the last letter?"

This could be solved as follows: start with a set of all words with
a 'd' in the 1st position (index[0]['d']), intersect it with the set
of words with a 'l' in the 3rd position (index[2]['n']), and then
intersect the remaining words with the set of words with a 'n' in 
the 5th position (index[4]['r']).
Finally, remove from the set all the words which are shorter or longer
than 5 letters. This algorithm is remarkably fast. Note that this 
specific example could also be written as a regexp: "d.l.n".
                       
There is an index using the special letter '*', which means 'all letters':

  index[4]['*'] <-- set of all words with length 4


PS. Idea for even more speedup: instead of putting the words themselves
into sets, use an integer instead. This integer denotes the position
of the word in a words[] list. Maybe set intersection operations
will perform quicker on integers than on strings? This has to be
timed.
'''

        
from collections import defaultdict
index = defaultdict(lambda: defaultdict(set))

fn = "/usr/share/dict/words"

# Alternative text files, for testing purposes
#
# fn = "dutch-words.txt"
# fn = "15492.txt"

print("Reading...")
words = []
for line in open(fn):
    word = line.strip().lower() 
    if 2 <= len(word) <= 14:
        if "-" in word: 
            continue
        words.append(word)

print("Indexing...")
for nr, word in enumerate(words):
    if not nr % 16000:
        print(f"  {word} ({nr}/{len(words)})")
    for pos, c in enumerate(word):
        index[pos][c].add(word)
    index[len(word)]["*"].add(word)
    
print("Writing...")
with open("wordfinder.txt", "wt") as f:
    for position in sorted(index.keys()):
        for letter in sorted(index[position].keys()):
            words = " ".join(s for s in index[position][letter])
            f.write(f"{position} {letter} {words}\n")

print("Done! Now please run 'python wordfind.py'")
