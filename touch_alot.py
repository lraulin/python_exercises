#!/usr/bin/env python3

"""Create numbered files.

Supply a filename and a number of files to create. Ex: Calling
'<this script> sample.py 10' will create sample01.py, sample02.py
... sample10.py etc. Files will be empty. It shouldn't modify 
existing files, but be careful."""

import sys


def make_files(pattern, number):
    pad = len(str(number))
    for i in range(number):
        nums = str(i).zfill(pad)
        if '.' in pattern:
            splitted = pattern.split('.')
            filename = splitted[0] + nums + '.' + splitted[1]
        else:
            filename = pattern + nums
        open(filename, 'a').close()


def main():
    try:
        name = sys.argv[1]
    except IndexError:
        print('You must supply a filename followed by a number.')
        exit()
    try:
        num = int(sys.argv[2])
    except ValueError:
        print('You must supply a filename followed by a number.')
        exit()
    make_files(name, num)


if __name__ == '__main__':
    main()
