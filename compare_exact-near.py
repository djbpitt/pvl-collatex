#!/usr/bin/env python
# Filename: compare_exact-near.py
# Developer: David J. Birnbaum (djbpitt@gmail.com)
# First version: 2016-12-17
# Last revised: 2016-12-17
#
# Syntax: python compare_exact-near.py
# Input: output_exact.txt, output_near.txt
# Output: (currently stdout)
#
# Synopsis: Identifies PVL blocks where near matching is applied
#
# Assumes identical line count and identical block divisions

import re

block_no_regex = re.compile('^\d')
block_start_regex = re.compile('^\+')
line_start_regex = re.compile('^\|')

with open('output_exact.txt', 'r') as exact_file, open('output_near.txt', 'r') as near_file:
    state = 'initial'
    exact_buffer = ''
    near_buffer = ''
    for line in exact_file:
        if block_no_regex.match(line):
            if state in ['block_end', 'empty_line']:
                state = 'block_no'
                exact_buffer = line
                near_buffer = near_file.readline()
            else:
                raise Exception('Unexpected state: ' + line)
        elif block_start_regex.match(line):
            if state == 'block_no':
                state = 'block_start'
                exact_buffer += line
                near_buffer += near_file.readline()
            elif state == 'line':
                state = 'block_end'
                exact_buffer += line
                near_buffer += near_file.readline()
                if exact_buffer != near_buffer:
                    print('Exact block:\n' + exact_buffer)
                    print('Near block:\n' + near_buffer)
            else:
                raise Exception('Unexpected state: ' + line)
        elif line_start_regex.match(line):
            if state in ['block_start', 'line'] :
                state = 'line'
                exact_buffer += line
                near_buffer += near_file.readline()
            else:
                raise Exception('Unexpected state: ' + line)
        elif line == '\n':
            state = 'empty_line'
            exact_buffer += line
            near_buffer += near_file.readline()
            print('empty line')
        else:
            raise Exception('Unexpected state: ' + line)

