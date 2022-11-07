"""
Module for experimenting with lower and upper bounds.

Unlike in the BED functionality, where we need to search for a lower bound in
a list of features, here we only concern ourselves with lists of integers.
"""


def lower_bound(x: list[int], v: int) -> int:
    """Get the index of the lower bound of v in x.

    If all values in x are smaller than v, return len(x).
    """
    start = 0 # start of search interval
    end = len(x) # end of search interval

    while start < end:
        middle = (start+end)//2 # middle of interval
        if  v <= x[middle]:
            end = middle
        else:
            start = middle + 1
    return start
 

def upper_bound(x: list[int], v: int) -> int:
    """Get the index of the upper bound of v in x.

    If all values in x are smaller than v, return len(x).
    """
    start = 0 # start of search interval
    end = len(x) # end of search interval

    while start < end:
        middle = (start+end)//2 # middel of interval
        if  v < x[middle]:
            end = middle
        else:
            start = middle + 1
    return start