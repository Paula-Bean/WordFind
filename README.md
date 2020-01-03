# WordFind
Quickly find words with patterns like "..r....f." (e.g. personify, wordcraft, foreshift)

How to use
----------

1) Run the program `wordfindmake.py` to read */usr/share/dict/words* and output the file *wordfinder.txt*

2) Run the program `wordfind.py` to quickly find crossword-puzzle and Scrabble words



This software will be used in my upcoming crossword fitting program. The regexp library was a too slow for my recursive backtracking algorithm, so I came up with an idea to use multiple indexes and set intersections to quickly find words of which a few letters are already known.

```
k o f f . c h a r s h a f
e . o . . . . . a . a . a
k a v a . c u r r a t o w
o . e . m . . . e . t . n
t r a d e c r a f t . . .
e . t . l . . . i . d . k
n * e * i . . . a . a . i
e . d . c . s . b . f . d
. . . t r i p o l i t a n
. . d . a . u . e . n . a
a q u a t o n e . l e e p
. . r . o . k . . . s . e
p r o e n z y m . . s . r
```
