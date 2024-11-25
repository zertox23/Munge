# Munge
A password munger inspired by [Th3S3cr3tAg3nt/Munge](https://github.com/Th3S3cr3tAg3nt/Munge).

**If it already exists, why did you remake it?**

**Python3**
- Th3S3cr3tAg3nt version was made 6 years ago in Python 2!

**Performance**
- My script is built with performance in mind. It can go through 50k passwords in 6 seconds and has approximately 2X the edits (around 4M) compared to the Th3S3cr3tAg3nt version (approximately 2M).

**Bug Fixes**
[StochasticSanity](https://github.com/StochasticSanity) refactored the code, fixing a bug or two in the process.
The code should be more maintainable, and modifyable to the users preference for munging. 

## Script tags
`-i <inputfile> and --input <inputfile>` specify the password list to be munged.
`-o <outputfile> and --output <outputfile>`specify the file name for the munged password list.
`-v and --verbose` show how many passwords generated in how many seconds, as well as the name of the output and the level.
`-l <1-10> or --level <1-10>` specify the level for the output.
`-C and --caesar` enables caesar cipher shifts

## Caesar cipher
A caesar cipher is a kind of simple substitution cipher where the alphabet is shifted by a certain number of spaces for example, a shift of three turns a into d, b becomes e and so on. When caesar cipher is enabled it applies all these shifts to all of the letters in the password for every shift 1 through 26 resulting in 26 times the amounts of password outcomes(17550 munged passwords per unmunged!)