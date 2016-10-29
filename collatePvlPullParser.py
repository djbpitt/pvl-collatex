#!/usr/bin/env python
# Filename: collatePVL.py
# Developer: David J. Birnbaum (djbpitt@gmail.com)
# First version: 2015-12-13
#
# Syntax: python collatePvl.py
# Input: pvl.xml
# Output: pvl-collated.xml
#
# Synopsis: Collates PVL lines using CollateX
#
# Witnesses in order:
#   Children of <manuscripts>: Lav, Tro, Rad, Aka, Ipa, Xle, Kom, Tol, NAk
#   Children of <block>: Bych, Shakh, Likh
#   Children of <paradosis>: Ost
#
# Tags to ignore, with content to keep: pvl, manuscripts, paradosis, marginalia,
#   problem
#
# Elements to ignore: omitted, textEnd, blank, end
#
# Structural elements: block
#
# Inline elements retained in normalization: sup, sub, lb, pb, choice
#
# Inline elements ignored in normalization: pageRef
#
# Special case: keep choice/option[1] and ignore other <option> elements (arbitrary)

import sys

sys.path.append('/Users/djb/collatex/collatex-pythonport')
from collatex import *
from xml.dom import pulldom
import re

def normalizeSpace(inText):
    return re.sub('\s+', ' ', inText)

def extract(input_xml):
    # Start pulling; it continues automatically
    doc = pulldom.parse(input_xml)
    inBlock = False
    inLav = False
    for event, node in doc:
        if event == pulldom.START_ELEMENT and node.localName == 'block':
            inBlock = True
            n = node.getAttribute('column') + '.' + node.getAttribute('line') # block number
            inputText = {}
        elif event == pulldom.END_ELEMENT and node.localName == 'block':
            inBlock = False
            print(inputText)
        # empty inline elements: lb, pb
        elif event == pulldom.START_ELEMENT and node.localName in ['lb', 'pb']:
            currentWit = currentWit + '<' + node.localName + '/>'
        # non-empty inline elements: sup, sub, pageRef
        elif event == pulldom.START_ELEMENT and node.localName in ['sup', 'sub', 'pageRef']:
            currentWit = currentWit + '<' + node.localName + '>'
        elif event == pulldom.END_ELEMENT and node.localName in ['sup', 'sub', 'pageRef']:
            currentWit = currentWit + '</' + node.localName + '>'
        elif event == pulldom.START_ELEMENT and node.localName == 'Lav':
            inLav = True
            currentWit = ''
        elif event == pulldom.CHARACTERS and inLav:
            currentWit = currentWit + normalizeSpace(node.data)
        elif event == pulldom.END_ELEMENT and node.localName == 'Lav':
            inLav = False
            inputText['Lav'] = currentWit
    return


inputFile = open('pvl.xml', 'rb')
outputFile = open('output.xml', 'w')

parseResult = extract(inputFile)

inputFile.close()
outputFile.close()
