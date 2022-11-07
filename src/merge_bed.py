"""Tool for cleaning up a BED file."""

import argparse
from ast import Return  # we use this module for option parsing. See main for details.

import sys
from tkinter.messagebox import RETRY
from typing import TextIO, Generator
from bed import (
    parse_line, print_line, BedLine
)


def read_bed_file(f: TextIO) -> list[BedLine]:
    """Read an entire sorted bed file."""
    # Handle first line...
    line = f.readline()
    if not line:
        return []

    res = [parse_line(line)]
    for line in f:
        feature = parse_line(line)
        prev_feature = res[-1]
        assert prev_feature.chrom < feature.chrom or \
            (prev_feature.chrom == feature.chrom and
             prev_feature.chrom_start <= feature.chrom_start), \
            "Input files must be sorted"
        res.append(feature)

    return res



def merge(list_1: list[BedLine], list_2: list[BedLine], outfile: TextIO) -> None:
    """Merge features and write them to outfile."""
    result = []
    i, j = 0, 0 
    while i < len(list_1) and j < len(list_2):
        f1 = list_1[i]
        f2 = list_2[j]
        if f1.chrom < f2.chrom:
            print_line(f1, outfile)
            i += 1
        elif f2.chrom < f1.chrom:
            print_line(f2, outfile)
            j += 1
        else:
            if f1.chrom_start < f2.chrom_start:
                print_line(f1, outfile)
                i += 1
            else:
                print_line(f2, outfile)
                j += 1
    for line in list_1[i:]:
        print_line(line, outfile)
    for line in list_2[j:]:
        print_line(line, outfile)





def main() -> None:
    """Run the program."""
    # Setting up the option parsing using the argparse module
    argparser = argparse.ArgumentParser(description="Merge two BED files")
    argparser.add_argument('f1', type=argparse.FileType('r'))
    argparser.add_argument('f2', type=argparse.FileType('r'))
    argparser.add_argument('-o', '--outfile',  # use an option to specify this
                           metavar='output',   # name used in help text
                           type=argparse.FileType('w'),  # file for writing
                           default=sys.stdout)

    # Parse options and put them in the table args
    args = argparser.parse_args()

    # With all the options handled, we just need to do the real work
    features1 = read_bed_file(args.f1)
    features2 = read_bed_file(args.f2)
    merge(features1, features2, args.outfile)


if __name__ == '__main__':
    main()
