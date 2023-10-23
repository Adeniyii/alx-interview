#!/usr/bin/python3
"""Over engineered package which parses log
files and provides useful metrics."""
import sys
import signal
from logParser.lexer import newLexer
from logParser.parser import newParser


out = {}
lines = 0
totalFileSize = 0


def main():
    """Entry point. Reads from stdin and calls our parsers."""
    global out, totalFileSize, lines
    for line in sys.stdin:
        ll = newLexer(line)
        pp = newParser(ll)

        result = pp.parseProgram()
        totalFileSize += result['filesize']
        status = result['status']
        if status in out.keys():
            out[status] = out[status] + 1
        else:
            out[status] = 1

        lines += 1

        if lines != 0 and lines % 10 == 0:
            print_result()


def print_result():
    print("File size:", totalFileSize)
    for k, v in out.items():
        print("{}: {}".format(k, v))


def sigint_handler(sig, frame):
    """Handles SIGINT signals."""
    print_result()
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)

if __name__ == "__main__":
    main()
