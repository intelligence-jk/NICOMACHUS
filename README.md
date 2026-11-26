# APEX: Arithmetic Progression EXplorer

Formerly `ap-explorer`.

Arithmetic progression explorer: give any three of a, d, n, the nth term and S_n, and get the rest, with the working.

## What it does
It solves all ten "three given, two to find" cases for an arithmetic progression, using exact `Fraction` arithmetic. When the unknown n comes from a quadratic, it keeps a root only when n is a positive whole number and says why each other root was rejected. It also answers "is this number in the AP?" and "what is the first negative term?".

## Example
```bash
python -m ap_explorer solve --a 5 --d 3 --s 185
```
```text
Given: a = 5, d = 3, s = 185
Working:
  S = n/2 (2a + (n-1)d) rearranges to d n^2 + (2a - d) n - 2S = 0.
  Quadratic in n: (3)n^2 + (7)n + (-370) = 0.
  Discriminant = 4489.
  n = -37/3 rejected: n counts terms, so it must be a whole number.
  n = 10 kept: a positive whole number.
Result: a = 5, d = 3, n = 10, nth term = 32, S_n = 185
```

```bash
python -m ap_explorer contains --a 3 --d 4 99
```
```text
x = a + (n-1)d gives n = (x - a)/d + 1 = 25. That is a positive whole number, so x is term number 25.
Answer: yes, term 25
```

```bash
python -m ap_explorer first-negative --a 100 --d -7
```
```text
Need a + (n-1)d < 0, so n - 1 > a/|d| = 100/7; the smallest whole n is 16, and term 16 = -5.
Answer: term 16 = -5
```

Options for solve: `--a`, `--d`, `--n`, `--l` (the nth term), `--s` (the sum). Use any three. Values can be fractions such as 1/2.

## The maths behind it
Terms: a, a + d, a + 2d, ... The nth term is l = a + (n - 1)d. The sum of the first n terms is S = n/2 (2a + (n - 1)d) = n(a + l)/2.

When S is given with a and d, expand to d n^2 + (2a - d) n - 2S = 0. When S is given with d and l, use d n^2 - (2l + d) n + 2S = 0. Because n counts terms, only positive whole number roots are kept. A number x is in the AP when n = (x - a)/d + 1 is a positive whole number. The first negative term, for a >= 0 and d < 0, is term floor(a/|d|) + 2.

A few combinations cannot be solved (for example a = 1 with n = 1 and d unknown, since d does not affect a single term). The tool says so instead of guessing.

## Install and run
Python 3.10 or later. Standard library only.
```bash
python -m pip install -e .
python -m pytest
```

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
