# sql-without-sql

## How to have some sql functionalities without a database.

### Example 2 : Calculate Barcharts

First of all, the code is written in the poorest python3 possible, hoping it will be easy to understand and translate ; a sort of elementary pseudo-python3.

A bar chart is a standard concept of the market prices for a financial instrument. For each period of time, we have : "open" (the first price), "high" (the maximum price), "low" (the minimum price) and "close" (the last price). So, from a daily bar chart, we are able to calculate weekly, monthly and yearly bar chart in one path.

It must run in any linux, macosx and windows/cygwin (python3 (sys, argparse, datetime should be in every distro)).

An input file "cote.txt" is provided (2100 daily EUR/USD), just type in this directory :

	./barchart.py

The equivalent SQL query will be :

	SELECT first(Open), max(high), min(low), last(Close) FROM Datas GROUP BY ... ORDER BY ...;
