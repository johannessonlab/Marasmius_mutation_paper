#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: nuclseqTools
    :synopsis: nuclseqTools contains functions to manipulate nucleotide strings
    during the merge.py pipeline.

Copyright (c) 2019, Johannesson lab
Licensed under the GPL3 license. See LICENSE file.
"""

def reverse_complement(nuclstring):
    rev_comped = ""
    for l in reversed(nuclstring):
        if l == "A" or l == "a":
            rev_comped += "T"
        elif l == "T" or l == "t":
            rev_comped += "A"
        elif l == "C" or l == "c":
            rev_comped += "G"
        elif l == "G" or l == "g":
            rev_comped += "C"
        elif l == "N" or l == "n":
            rev_comped += "N"
    return rev_comped

def createConsensus(delta,string1,string2):
    '''
    Given two overlapping nucleotide strings (excluding overhangs) and alignment information,
    returns the merged sequence
    delta = [int,int,int, ...]
    strings = "ATCG..."
    '''
    new_string1 = string1
    new_string2 = string2
    start = 0
    for i in delta:
        # Positive integers in the delta mean gaps in the query sequence, insert these
        if i > 0:
            start += i
            new_string2 = new_string2[:start-1] + "." + new_string2[start-1:]

        # Negative integers in the delta mean gaps in the reference sequence, insert these
        else:
            i = -i
            start += i
            new_string1 = new_string1[:start-1] + "." + new_string1[start-1:]

    # Write the new string. Insertions are favoured over deletions.
    # N's are put at mismatches
    cons = ""
    for i in range(0,len(new_string1),1):
        if new_string1[i] == new_string2[i]:
            cons += new_string1[i]
        elif new_string1[i] == ".":
            cons += new_string2[i]
        elif new_string2[i] == ".":
            cons += new_string1[i]
        else:
            # At disagreeing bases, take base from string1. This is better than
            # inserting an N or IUPAC coded base as some mappers don't support this.
            # After a round of polishing this will be fixed
            cons += new_string1[i]

    return cons
