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
    index1,index2= 0,0 
    while index1 <= len(list_1): 
        if index1 >= len(list_1):
            for i in range(index2, len(list_2)):
                print_line(list_2[index2], outfile)
        if index2 >= len(list_2):
            for i in range(index1, len(list_1)): 
                print_line(list_1[index1], outfile)
        if list_1[index1].chrom <= list_2[index2].chrom:
            if list_1[index1].chrom_start <= list_2[index2].chrom_start:
                print_line(list_1[index1],outfile)
                index1 += 1 
                continue
        print_line (list_2[index2],outfile)
        index2 += 1 





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
