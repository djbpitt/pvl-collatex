#!/usr/bin/env python
# Filename: collatePvlPullParser.py
# Developer: David J. Birnbaum (djbpitt@gmail.com)
# First version: 2015-12-13
# Last revised: 2016-10-29
#
# Syntax: python collatePvlPullParser.py
# Input: pvl.xml
# Output: (currently stdout)
#
# Synopsis: Collates PVL lines using CollateX
#
# Witnesses in input (and eventual output) order:
#   Children of <manuscripts>: Lav, Tro, Rad, Aka, Ipa, Xle, Kom, Tol, NAk
#   Children of <block>: Bych, Shakh, Likh
#   Child of <paradosis>: Ost
# Tags to ignore, with content to keep: pvl, manuscripts, paradosis, marginalia, problem
# Elements to ignore: omitted, textEnd, blank, end
# Structural elements: block
# Inline elements (empty) retained in normalization: lb, pb
# Inline elements (with content) retained in normalization: pageRef, sup, sub, choice, option

import sys
sys.path.insert(0, '/Users/djb/collatex/collatex-pythonport')  # CollateX from repo if not installed
from collatex import *
from xml.dom import pulldom
import string
import re
import json

# GIs fall into one four classes
ignore = ['omitted', 'textEnd', 'blank', 'end']
inlineEmpty = ['lb', 'pb']
inlineContent = ['sup', 'sub', 'pageRef', 'choice', 'option']
sigla = ['Lav', 'Tro', 'Rad', 'Aka', 'Ipa', 'Xle', 'Kom', 'Tol', 'NAk', 'Bych', 'Shakh', 'Likh', 'Ost']

# Precompile regexes; lookahead and lookbehind patterns must be of fixed length (no asterisk or plus)
regexWhitespace = re.compile(r'\s+')
regexTokenize = re.compile(r'\s+(?!<(lb|pb|pageRef))')   # Negative lookahead for '<lb', '<pb', '<pageRef'
regexChoice = re.compile(r'<choice>\s*(<option>.+?</option>).*</choice>') # capture first <option>
regexPageRef = re.compile(r'\s*<pageRef>.+?</pageRef>\s*')
regexTag = re.compile(r'<.+?>')
regexPunc = re.compile("[" + string.punctuation + "]")
regexGeminate = re.compile(r'(.)\1')
regexNoninitialVowel = re.compile(r'\B[аеиоуѧѫѣь]')

def normalizeSpace(inText):
    """Replaces all whitespace spans with single space characters"""
    return regexWhitespace.sub(' ', inText)

def reduceChoice(inText):
    """Keep only first <option> inside <choice>"""
    return regexChoice.sub(r'\1',inText) # Must be done before tokenization, since <option> may contain multiple tokens

def tokenize(inText):
    """Split into word tokens, merging <lb> and <pb> in with preceding token"""
    # Retain only first of <option> elements inside <choice>
    tokens = regexTokenize.split(reduceChoice(normalizeSpace(inText)))
    # TODO: Why does the split create empty tokens that then need to be bypassed?
    return [token for token in tokens if token and not re.match('^<.+?>$',token)]


def processRdg(siglum, inText):
    """Returns JSON data for rdg"""
    witness = {'id': siglum, 'tokens': []}
    for token in inText:
        token = {'t': token, 'n': normalize(token)}
        witness['tokens'].append(token)
    return witness


def normalize(inText):
    """Create normalized shadow token for collation purposes

    Must be executed in this order:
        Strip <pageRef> elements, including content
        Strip all other tags, but not their content
        Strip punctuation and whitespace
    Lowercase
    Soundexify
    """
    # TODO: Is there a more legible way to nest the regex replacements?
    return soundexify(regexWhitespace.sub('',regexPunc.sub('',regexTag.sub('', regexPageRef.sub('',inText)))).lower())


def soundexify(inText):
    """Soundex normalization

    In this order
        process the manyToOne, oneToMany, and oneToOne groups
        degeminate all geminate consonants (e.g., нн > н)
        strip all non-word-initial vowels
        truncate long words to no more than four characters"""
    #http://stackoverflow.com/questions/764360/a-list-of-string-replacements-in-python
    #TODO: Should the variables be defined outside the function to avoid repeated initialization when called?
    manyToOne = [('оу', 'у'), ('шт', 'щ')]
    for k, v in manyToOne:
        inText = inText.replace(k, v)
    oneToMany = [('ѿ','ѡт'), ('ѯ', 'кс'), ('ѱ', 'пс')]
    for k, v in oneToMany:
        inText = inText.replace(k, v)
    #TODO: Is there a more legible way to chain the one-to-one replacements (see the end of this section)?
    #TODO: Same question as above concerning definitions.
    # ja letters
    lettersJa = 'ѧѩꙙꙝꙗя'
    lettersJaReplacement = 'ѧ' * len(lettersJa)
    transJa = str.maketrans(lettersJa, lettersJaReplacement)
    # e letters
    lettersE = 'еєѥ'
    lettersEReplacement = 'е' * len(lettersE)
    transE = str.maketrans(lettersE, lettersEReplacement)
    # i letters
    lettersI = 'ыꙑиіїꙇй'
    lettersIReplacement = 'и' * len (lettersI)
    transI = str.maketrans(lettersI, lettersIReplacement)
    # o letters
    lettersO = 'оꙩꙫꙭꙮѡꙍѽѻ'
    lettersOReplacement = 'о' * len(lettersO)
    transO = str.maketrans(lettersO, lettersOReplacement)
    # u letters
    lettersU = 'уꙋюꙕѵѷӱѹ'
    lettersUReplacement = 'у' * len(lettersU)
    transU = str.maketrans(lettersU, lettersUReplacement)
    # oN letters
    lettersON = 'ѫѭꙛ'
    lettersONReplacement = 'ѫ' * len(lettersON)
    transON = str.maketrans(lettersON, lettersONReplacement)
    # jat letters
    lettersJat = 'ѣꙓ'
    lettersJatReplacement = 'ѣ' * len(lettersJat)
    transJat = str.maketrans(lettersJat, lettersJatReplacement)
    # jer letters
    lettersJer = 'ьъ'
    lettersJerReplacement = 'ь' * len(lettersJer)
    transJer = str.maketrans(lettersJer, lettersJerReplacement)
    # z letters
    lettersZ = 'зꙁꙃѕꙅ'
    lettersZReplacement = 'з' * len(lettersZ)
    transZ = str.maketrans(lettersZ, lettersZReplacement)
    return regexNoninitialVowel.sub('',regexGeminate.sub(r'\1',inText.translate(transJa).translate(transE).\
                             translate(transI).translate(transO).translate(transU).\
                             translate(transON).translate(transJat).translate(transJer).\
                             translate(transZ)))[0:4]

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
            # diagnostic output
            jsonInput = json.dumps(rdgs, ensure_ascii=False)
            print(n + ' input:\n')
            print(jsonInput)
            print(n + ' output:\n')
            table = collate(rdgs, segmentation=False, near_match=False)
            outputFile.write('\n' + n + '\n' + str(table))
            print(table)
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
            if tokenize(currentRdg): # omit witnesses with no content
                witnesses.append(processRdg(currentSiglum, tokenize(currentRdg)))
    return True

with open('pvl.xml', 'rb') as inputFile, open('output_exact.txt', 'w') as outputFile:
    parseResult = extract(inputFile)
