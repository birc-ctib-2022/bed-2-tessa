# This directory will be checked with pytest. It will examine
# all files that start with test_*.py and run all functions with
# names that start with test_

def test_1984():
    assert 2 + 2 == 4
from io import StringIO
import pytest
import sys

from merge_bed import (BedLine, parse_line, read_bed_file, merge)

def test_works_with_different_bedlines():
    """
    The function should work with different string representations of int in base 10
    And it should work with different white spaces
    """
    expected = BedLine('chr1', 20100, 20101, 'foo')
    assert parse_line('chr1 20_100 20_101 foo') == expected
    assert parse_line('chr1 20100     20101         foo') == expected
    assert parse_line('chr1 20100\t20101\nfoo') == expected

def test_error_if_wrong_line():
    """
    And ValueError should be raised with a line with to many or to few columns is parsed
    And AssertionError should be raised if the interval is not a single nucleotide
    """
    line_with_less_columns = 'chr1 20100 20101'
    line_with_more_columns = 'chr1 20100 20101 foo 10'
    line_with_interval_not_SNP = 'chr1 20100 20201 foo'
    with pytest.raises(ValueError):
        parse_line(line_with_less_columns)
    with pytest.raises(ValueError):
        parse_line(line_with_more_columns)
    with pytest.raises(AssertionError):
        parse_line(line_with_interval_not_SNP)

def test_error_if_input_not_sorted():
    """
    Merge should only be used on lists that are already sorted. 
    When the BEDfiles are read into lists it is checked whether they are sorted or not
    """
    lines_with_chromosomes_not_sorted = StringIO("chrom5 201 202 Feature01\n chrom8 203 204 Feature02\nchrom1 404 405 Feature03")
    lines_with_chrom_start_not_sorted = StringIO("chrom1 506 507 Feature01\n chrom1 203 204 Feature02\nchrom1 404 405 Feature03")
    with pytest.raises(AssertionError):
        read_bed_file(lines_with_chromosomes_not_sorted)
    with pytest.raises(AssertionError):
        read_bed_file(lines_with_chrom_start_not_sorted)

def test_merge(capsys):
    """
    Should be able to merge lists with sorted BedLines correctly, so the merged list is also sorted
    In this case merge() would never have to handle a not-sorted list, because they will be captured by read_bed_file()
    """

    merge([], [], sys.stdout)
    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""

    merge([BedLine("chrom1", 203, 204, "Feature02")], [BedLine("chrom1", 201, 202, "Feature01")], sys.stdout)
    out, err = capsys.readouterr()
    assert out == "chrom1\t201\t202\tFeature01\nchrom1\t203\t204\tFeature02\n"
    assert err == ""

    merge([], [BedLine("chrom1", 201, 202, "Feature01"), BedLine("chrom1", 203, 204, "Feature02")], sys.stdout)
    out, err = capsys.readouterr()
    assert out == "chrom1\t201\t202\tFeature01\nchrom1\t203\t204\tFeature02\n"
    assert err == ""

    merge([BedLine("chrom7", 201, 202, "Feature02")], [BedLine("chrom1", 201, 202, "Feature01")], sys.stdout)
    out, err = capsys.readouterr()
    assert out == "chrom1\t201\t202\tFeature01\nchrom7\t201\t202\tFeature02\n"
    assert err == ""

    merge([BedLine("chrom1", 201, 202, "01"), BedLine("chrom1", 201, 202, "02")],
    [BedLine("chrom1", 201, 202, "03"), BedLine("chrom7", 201, 202, "04"), BedLine("chrom9", 400, 401, "05")], 
    sys.stdout)
    out, err = capsys.readouterr()
    assert out == "chrom1\t201\t202\t03\nchrom1\t201\t202\t01\nchrom1\t201\t202\t02\nchrom7\t201\t202\t04\nchrom9\t400\t401\t05\n"
    assert err == ""