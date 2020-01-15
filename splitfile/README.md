# sql-without-sql

## How to have some sql functionalities without a database.

### Example 3 : Split a file according a key 

First of all, the code is written in the poorest python3 possible, hoping it will be easy to understand and translate ; a sort of elementary pseudo-python3.

Given a big file contening a key, we want to split this file in many according this key in one path and ignoring the number of occurences for this keys. 

It must run in any linux, macosx and windows/cygwin (python3 (sys, argparse, datetime should be in every distro)).

Just type :

	./trt.sh --num 1

or for a normal run with num = 500,000 :

	./trt.sh

!!! This job creates many files in current directory !!! 
