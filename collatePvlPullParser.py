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
sys.path.append('/Users/djb/collatex/collatex-pythonport')  # CollateX from repo; not installed
from collatex import *
from xml.dom import pulldom
import re
import json

# GIs fall into one four classes
ignore = ['omitted', 'textEnd', 'blank', 'end']
inlineEmpty = ['lb', 'pb']
inlineContent = ['sup', 'sub', 'pageRef', 'choice', 'option']
sigla = ['Lav', 'Tro', 'Rad', 'Aka', 'Ipa', 'Xle', 'Kom', 'Tol', 'NAk', 'Bych', 'Shakh', 'Likh', 'Ost']

# Precompile regexes
regexTokenize = re.compile('\s+(?!<(lb|pb|pageRef))')   # Negative lookahead for '<lb', '<pb', '<pageRef'

def normalizeSpace(inText):
    """Replaces all whitespace spans with single space characters"""
    return re.sub('\s+', ' ', inText)


def tokenize(inText):
    """Split into word tokens, merging <lb> and <pb> in with preceding token"""
    tokens = regexTokenize.split(inText)
    return [token for token in tokens if token] #TODO: Why does the split create empty tokens?


def processRdg(siglum, inText):
    """Returns JSON data for rdg"""
    witness = {'id': siglum, 'tokens': []}
    for token in inText:
        token = {'t': token, 'n': normalize(token)}
        witness['tokens'].append(token)
    return witness


def normalize(inText):
    """Create normalized shadow token for collation purposes

    Strip all tags
    Strip content of <pageRef> elements
    Retain only first of <option> elements inside <choice>
    Lowercase
    Strip punctuation
    Strip whitespace
    """
    return inText.lower()


def extract(input_xml):
    """Process entire input XML document, firing on events"""
    # Start pulling; it continues automatically
    doc = pulldom.parse(input_xml)
    inWit = False
    for event, node in doc:
        # elements to ignore
        if event == pulldom.START_ELEMENT and node.localName in ignore:
            continue
        # process each block as a separate collation set
        elif event == pulldom.START_ELEMENT and node.localName == 'block':
            n = node.getAttribute('column') + '.' + node.getAttribute('line')  # block number
            rdgs = {}
            witnesses = []
            rdgs['witnesses'] = witnesses
        elif event == pulldom.END_ELEMENT and node.localName == 'block':
            print(json.dumps(rdgs, ensure_ascii=False))
        # empty inline elements: lb, pb
        elif event == pulldom.START_ELEMENT and node.localName in inlineEmpty:
            currentRdg += '<' + node.localName + '/>'
        # non-empty inline elements: sup, sub, pageRef
        elif event == pulldom.START_ELEMENT and node.localName in inlineContent:
            currentRdg += '<' + node.localName + '>'
        elif event == pulldom.END_ELEMENT and node.localName in inlineContent:
            currentRdg += '</' + node.localName + '>'
        # readings
        elif event == pulldom.START_ELEMENT and node.localName in sigla:
            inWit = True
            currentSiglum = node.localName
            currentRdg  = ''
        elif event == pulldom.CHARACTERS and inWit:
            currentRdg += normalizeSpace(node.data)
        elif event == pulldom.END_ELEMENT and node.localName in sigla:
            # Witness finished, so process and push its data
            inWit = False
            witnesses.append(processRdg(currentSiglum, tokenize(currentRdg)))
    return True


inputFile = open('pvl.xml', 'rb')
outputFile = open('output.xml', 'w')

parseResult = extract(inputFile)

inputFile.close()
outputFile.close()
