#!/usr/bin/env python
import sys
sys.path.append('/Users/djb/collatex/collatex-pythonport')  # CollateX from repo; not installed
from collatex import *
from xml.dom import pulldom
import string
import re
import json

jsonInput = {
  "witnesses": [
    {
      "id": "Lav",
      "tokens": [
        {
          "t": "рѣша.",
          "n": "рш"
        }
      ]
    },
    {
      "id": "Rad",
      "tokens": [
        {
          "t": "рекоша",
          "n": "ркш"
        }
      ]
    },
    {
      "id": "Aka",
      "tokens": [
        {
          "t": "рекоша",
          "n": "ркш"
        }
      ]
    },
    {
      "id": "Ipa",
      "tokens": [
        {
          "t": "ркоша.",
          "n": "ркш"
        }
      ]
    },
    {
      "id": "Xle",
      "tokens": [
        {
          "t": "рекоша, <lb/>",
          "n": "ркш"
        }
      ]
    },
    {
      "id": "Bych",
      "tokens": [
        {
          "t": "рѣша.",
          "n": "рш"
        }
      ]
    },
    {
      "id": "Shakh",
      "tokens": [
        {
          "t": "рѣша.",
          "n": "рш"
        }
      ]
    },
    {
      "id": "Likh",
      "tokens": [
        {
          "t": "рѣша.",
          "n": "рш"
        }
      ]
    },
    {
      "id": "Ost",
      "tokens": [
        {
          "t": "рекоша.",
          "n": "ркш"
        }
      ]
    }
  ]
}
table = collate(jsonInput, segmentation=False)
print(table)