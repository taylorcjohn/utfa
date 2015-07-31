utfa
====

**UTF-8 analysis for files and web pages**

utfa.py is a Python script which analyses files or web pages into counts of all UTF-8 characters.  It can also (using -b byte mode) analyse the data into component bytes, e.g. where a file or web page is not encoded using UTF-8.

See the document `ufta.pdf` for background and usage examples using supplied test files `256` and `u256` and various web pages.

utfa.py supports both Python 2.7 and Python 3.x versions.  

Examples:

  * utfa.py -u https://en.wikipedia.org/wiki/UTF-8
  * utfa.py u256
  * utfa.py -b 256
```
usage: utfa.py [-h] [-u URL] [-b] [-e] [-t] [-l] [-n] [-m] [-x] [-o OFFSET]
          [-s SIZE] [-v]
          [file]

file analysis

positional arguments:
  file

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     url e.g. -u http://bbc.co.uk
  -b, --bytes           analyse 256 possible bit patterns
  -e, --errors          enable unicode error replacement
  -t, --time            show run time
  -l, --legend          disable legend display
  -n, --name            disable unicode block names
  -m, --mask            show only characters present in file/url
  -x, --number          disable individual counts
  -o OFFSET, --offset OFFSET
  -s SIZE, --size SIZE
  -v, --version         python version, encoding and max code point
```
