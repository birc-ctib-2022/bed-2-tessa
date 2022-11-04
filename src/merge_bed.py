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

def is_BEDline_before (el1:BedLine, el2:BedLine) -> bool:
    """check if a BEDline is before another
    >>> is_BEDline_before(BedLine("chr1", 1, 2, "foo"), BedLine("chr1", 5, 6, "foo"))
    True
    """
    for i in ['chrom', 'chrom_start', 'chrom_end']:
        if getattr(el1,i) > getattr(el2,i):
            return False
    return True 

def merge_sort_generator (list_1: list[BedLine], list_2: list[BedLine]) -> Generator [BedLine, None, None ]:
    """merges 2 sorted lists and gives elements."""
    iter1,iter2= iter(list_1), iter(list_2)
    for (el1, el2) in zip(iter1,iter2): 
        if is_BEDline_before (el1,el2):
            yield el1
        yield el2 
    for el1 in iter1: 
        yield el1 
    for el2 in iter2: 
        yield el2 

def merge(list_1: list[BedLine], list_2: list[BedLine], outfile: TextIO) -> None:
    """Merge features and write them to outfile."""
    for elem in merge_sort_generator (list_1, list_2): 
        print_line(elem,outfile)











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
