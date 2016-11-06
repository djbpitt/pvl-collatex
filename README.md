# pvl-collatex
CollateX collation of the _Rus′ Primary Chronicle_.

## Overview

* **Syntax:** python collatePvlPullParser.py
* **Input:** pvl.xml
* **Output:** (currently stdout)
* **Synopsis:** Collates PVL lines using CollateX

## Input markup
* **Witnesses in input (and eventual output) order:**

	* Children of `<manuscripts>`: `<Lav>`, `<Tro>`, `<Rad>`, `<Aka>`, `<Ipa>`, `<Xle>`, `<Kom>`, `<Tol>`, `<NAk>`
	* Children of `<block>`: `<Bych>`, `<Shakh>`, `<Likh>`
	* Child of `<paradosis>`: <Ost>

* **Tags to ignore, with content to keep:** `<pvl>`, `<manuscripts>`, `<paradosis>`, `<marginalia>`, `<problem>`

* **Elements to ignore:** `<omitted>`, `<textEnd>`, `<blank>`, `<end>`

* **Structural element:** ``<block>``

* **Inline elements (empty) retained in normalization:** `<lb>`, `<pb>`

* **Inline elements (with content) retained in normalization:** `<pageRef>`, `<sup>`, `<sub>`, `<choice>`, `<option>`