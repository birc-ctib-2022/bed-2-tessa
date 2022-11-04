"""Tool for cleaning up a BED file."""

import argparse  # we use this module for option parsing. See main for details.

import sys
from bed import (
    read_bed_file, print_line, BedLine
)


def extract_region(features: list[BedLine],
                   start: int, end: int) -> list[BedLine]:
    """Extract region chrom[start:end] and write it to outfile."""
    index_start = index_stop = binary_search_region_start(features, start)
    for i in range(index_start, len(features)):
        if features[i].chrom_start >= end: 
            break
        index_stop +=1 
    return features [index_start:index_stop]

def is_overlapping(interval_1: tuple[int,int], interval_2: tuple[int,int]) -> bool: 
    """check if overlapping
    >>> is_overlapping ((1,10), (2,5))
    True
    """
    return max (interval_1[0], interval_2 [0]) <min(interval_1[1], interval_2[1])


def is_feature_in (feat: BedLine, start:int, end: int): 
    """check if bedline is in a given intercal 
    >>> is_feature_in(BedLine("chr1", 0,3, "foo"), 0, 10) 
    True
    """
    interval= (feat.chrom_start,feat.chrom_end)
    return is_overlapping(interval, (start,end))

def binary_search_region_start (bed_lines: list[BedLine], start: int):
    """
    Find first index in BedLine list for which the chromosome start is equal 
    or greater than a given number.
    """
    low, high = 0, len(bed_lines)
    while low <high: 
        mid = (high + low) //2 
        if bed_lines [mid].chrom_start <start: 
            low= mid+ 1 
        else: 
            high= mid 
    return low 


def main() -> None:
    """Run the program."""
    # Setting up the option parsing using the argparse module
    argparser = argparse.ArgumentParser(
        description="Extract regions from a BED file")
    argparser.add_argument('bed', type=argparse.FileType('r'))
    argparser.add_argument('query', type=argparse.FileType('r'))

    # 'outfile' is either provided as a file name or we use stdout
    argparser.add_argument('-o', '--outfile',  # use an option to specify this
                           metavar='output',  # name used in help text
                           type=argparse.FileType('w'),  # file for writing
                           default=sys.stdout)

    # Parse options and put them in the table args
    args = argparser.parse_args()

    # With all the options handled, we just need to do the real work
    features = read_bed_file(args.bed)
    for query in args.query:
        chrom, start, end = query.split()
        # Extract the region from the chromosome, using your extract_region()
        # function. If you did your job well, this should give us the features
        # that we want.
        region = extract_region(
            features.get_chrom(chrom), int(start), int(end))
        for line in region:
            print_line(line, args.outfile)


if __name__ == '__main__':
    main()
