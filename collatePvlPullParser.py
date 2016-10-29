#!/usr/bin/env python
# Filename: collatePVL.py
# Developer: David J. Birnbaum (djbpitt@gmail.com)
# First version: 2015-12-13
# Last revised: 2016-10-29
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
# Tags to ignore, with content to keep: pvl, manuscripts, paradosis, marginalia, problem
# Elements to ignore: omitted, textEnd, blank, end
# Structural elements: block
# Inline elements (empty) retained in normalization: lb, pb
# Inline elements (with content) retained in normalization: pageRef, sup, sub, choice, option

import sys

sys.path.append('/Users/djb/collatex/collatex-pythonport')
from collatex import *
from xml.dom import pulldom
import re

ignore = ['omitted', 'textEnd', 'blank', 'end']
inlineEmpty = ['lb', 'pb']
inlineContent = ['sup', 'sub', 'pageRef', 'choice', 'option']
sigla = ['Lav', 'Tro', 'Rad', 'Aka', 'Ipa', 'Xle', 'Kom', 'Tol', 'NAk', 'Bych', 'Shakh', 'Likh', 'Ost']


def normalizeSpace(inText):
    return re.sub('\s+', ' ', inText)


def extract(input_xml):
    # Start pulling; it continues automatically
    doc = pulldom.parse(input_xml)
    inBlock = False
    inWit = False
    for event, node in doc:
        # elements to ignore
        if event == pulldom.START_ELEMENT and node.localName in ignore:
            continue
        # process each block as a separate collation set
        elif event == pulldom.START_ELEMENT and node.localName == 'block':
            inBlock = True
            n = node.getAttribute('column') + '.' + node.getAttribute('line')  # block number
            inputText = {}
        elif event == pulldom.END_ELEMENT and node.localName == 'block':
            inBlock = False
            print(inputText)
        # empty inline elements: lb, pb
        elif event == pulldom.START_ELEMENT and node.localName in inlineEmpty:
            currentWit += '<' + node.localName + '/>'
        # non-empty inline elements: sup, sub, pageRef
        elif event == pulldom.START_ELEMENT and node.localName in inlineContent:
            currentWit += '<' + node.localName + '>'
        elif event == pulldom.END_ELEMENT and node.localName in inlineContent:
            currentWit += '</' + node.localName + '>'
        # readings
        elif event == pulldom.START_ELEMENT and node.localName in sigla:
            inWit = True
            currentSiglum = node.localName
            currentWit = ''
        elif event == pulldom.CHARACTERS and inWit:
            currentWit += normalizeSpace(node.data)
        elif event == pulldom.END_ELEMENT and node.localName in sigla:
            inWit = False
            inputText[currentSiglum] = currentWit
    return


inputFile = open('pvl.xml', 'rb')
outputFile = open('output.xml', 'w')

parseResult = extract(inputFile)

inputFile.close()
outputFile.close()
