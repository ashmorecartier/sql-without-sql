# sql-without-sql

## How to have some sql functionalities without a database.

### Example 1 : a report

First of all, the code is written in the poorest python3 possible, hoping it will be easy to understand and translate ; a sort of elementary pseudo-python3.

It must run in any linux, macosx or windows/cygwin (bash4, sort, python3 (sys, random, argparse, datetime should be in every distro)).
Just type :

	./trt.sh --num 1

or for a normal run with num = 500,000, redirect to a file :

	./trt.sh > ./imprim.txt

A one minute job on an antic Pentium 4, XP Pro/cygwin32. 10 seconds on an Intel-I5-8300H, Win 10/cygwin64.

The footers are equivalent to :

	SELECT key1, key2, key3, count(id), sum(mnt) FROM Datas GROUP BY key1, key2, key3 ORDER BY key1, key2, key3;
	SELECT key1, key2, count(id), sum(mnt) FROM Datas GROUP BY key1, key2 ORDER BY key1, key2;
	SELECT key1, count(id), sum(mnt) FROM Datas GROUP BY key1 ORDER BY key1;

