# sql-without-sql

## How to have some sql functionalities without a database.

When databases didn't exist, there were some tips and tricks to obtain same results with formatted text files.

Usually when you read a stream (it can be a text or binary file or json format, a memory array, or even a cursor database), it looked like this in pseudocode :

```
stream.open()
while not stream.eof():
	stream.read()
	do something
end_while
stream.close()
```

Not a bad idea, but you managed only one record at a time. What the matter if you imagine managing two records :

```
stream.open()
newrec <--- stream.read()
if stream.eof():
	stream.isempty()
	stream.close()
fi
	
while not stream.eof():
	oldrec <--- newrec
	newrec <--- stream.read()
```

Now you are able to imagine a key (one or more) to group items. If a key changes between oldrec and newrec, you are in the last movement (LM) for this key. As you are real genius, you introduce the concept of first mouvement (FM) and realize that a LM will be the FM for this key at the next round !!! So it comes :

```
	FM <--- LM
	if newkey != oldkey:
		LM <--- True
	fi
```

At this moment, you are able to begin the treatment but with two optional events fired (FM and LM) :

```
	if FM:
		do_a_header_for_key_with_oldrec()
	fi

	current_treatment_with_oldrec()

	if LM:
		do_a_footer_for_key_with_oldrec()
	fi
```

Note that for all the treatment you must work with **oldrec** and **NOT newrec**.
Then, next round :

```
end-while
```

This program structure is quite efficient, safe and powerful.

Two examples are given : 
- generating a report in /report with a hierarchy of 3 keys in [/report](https://github.com/ashmorecartier/sql-without-sql/report),
- generating weekly, monthly and yearly barchart from a daily barchart in [/barchart](https://github.com/ashmorecartier/sql-without-sql/barchart).

