"""Exact arithmetic progression solver.

Symbols: a = first term, d = common difference, n = number of terms,
l = nth term (a + (n-1)d), s = sum of the first n terms.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from math import isqrt
from typing import Dict, List, Optional, Tuple, Union

Num = Union[int, str, Fraction]
KEYS = ("a", "d", "n", "l", "s")


def F(v: Num) -> Fraction:
    return v if isinstance(v, Fraction) else Fraction(v)


def fmt(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


@dataclass
class Solution:
    a: Fraction
    d: Fraction
    n: int
    l: Fraction
    s: Fraction
    steps: List[str] = field(default_factory=list)

    def values(self) -> Dict[str, Fraction]:
        return {"a": self.a, "d": self.d, "n": Fraction(self.n), "l": self.l, "s": self.s}


def _sqrt_frac(v: Fraction) -> Optional[Fraction]:
    if v < 0:
        return None
    p, q = isqrt(v.numerator), isqrt(v.denominator)
    return Fraction(p, q) if p * p == v.numerator and q * q == v.denominator else None


def _quadratic_n(A: Fraction, B: Fraction, C: Fraction) -> Tuple[List[int], List[str]]:
    """Roots of A n^2 + B n + C = 0 kept only when n is a positive integer."""
    notes = [f"Quadratic in n: ({fmt(A)})n^2 + ({fmt(B)})n + ({fmt(C)}) = 0."]
    if A == 0:
        if B == 0:
            raise ValueError("these values do not fix n")
        roots = [-C / B]
        notes.append("The n^2 term vanishes, so it is linear in n.")
    else:
        disc = B * B - 4 * A * C
        notes.append(f"Discriminant = {fmt(disc)}.")
        root = _sqrt_frac(disc)
        if root is None:
            notes.append("The discriminant is negative or not a perfect square, so no rational n exists.")
            return [], notes
        roots = sorted({(-B + root) / (2 * A), (-B - root) / (2 * A)})
    keep: List[int] = []
    for r in roots:
        if r.denominator != 1:
            notes.append(f"n = {fmt(r)} rejected: n counts terms, so it must be a whole number.")
        elif r < 1:
            notes.append(f"n = {fmt(r)} rejected: n must be at least 1.")
        else:
            keep.append(int(r))
            notes.append(f"n = {fmt(r)} kept: a positive whole number.")
    return keep, notes


def _finish(a: Fraction, d: Fraction, n: int, steps: List[str]) -> Solution:
    l = a + (n - 1) * d
    s = Fraction(n, 2) * (2 * a + (n - 1) * d)
    return Solution(a, d, n, l, s, steps)


def _whole(v: Fraction, what: str, notes: List[str]) -> Optional[int]:
    if v.denominator != 1 or v < 1:
        notes.append(f"{what} = {fmt(v)} is not a positive whole number, so no AP fits.")
        return None
    notes.append(f"{what} = {fmt(v)} is a positive whole number.")
    return int(v)


def solve(**given: Num) -> List[Solution]:
    """Give exactly three of a, d, n, l, s. Returns every valid solution.

    The list is empty when no AP fits. `solve_with_notes` also returns the
    working, including why each quadratic root was kept or rejected.
    """
    sols, _ = solve_with_notes(**given)
    return sols


def solve_with_notes(**given: Num) -> Tuple[List[Solution], List[str]]:
    keys = sorted(k for k, v in given.items() if v is not None)
    if any(k not in KEYS for k in keys) or len(keys) != 3:
        raise ValueError("give exactly three of a, d, n, l, s")
    v = {k: F(given[k]) for k in keys}
    if "n" in v and (v["n"].denominator != 1 or v["n"] < 1):
        raise ValueError("n must be a positive whole number")
    key = "".join(keys)
    notes: List[str] = []
    n_list: List[int] = []
    A = v.get("a"); D = v.get("d"); L = v.get("l"); S = v.get("s")

    if key == "adn":
        return [_finish(A, D, int(v["n"]), ["l = a + (n-1)d and S = n/2 (2a + (n-1)d)."])], notes
    N = v.get("n")

    def make(a, d, n, extra):
        return _finish(a, d, n, extra)

    out: List[Solution] = []
    if key == "adl":
        if D == 0:
            if L != A:
                return [], ["d = 0 means every term equals a, but l differs from a."]
            raise ValueError("d = 0 and l = a: n can be any positive whole number")
        notes.append("l = a + (n-1)d, so n = (l - a)/d + 1.")
        n = _whole((L - A) / D + 1, "n", notes)
        return ([make(A, D, n, notes)] if n else []), notes
    if key == "ads":
        notes.append("S = n/2 (2a + (n-1)d) rearranges to d n^2 + (2a - d) n - 2S = 0.")
        if D == 0:
            if A == 0:
                raise ValueError("a = 0 and d = 0 gives S = 0 for every n")
            notes.append("d = 0, so S = n a and n = S/a.")
            n = _whole(S / A, "n", notes)
            n_list = [n] if n else []
        else:
            n_list, q = _quadratic_n(D, 2 * A - D, -2 * S)
            notes += q
        out = [make(A, D, n, notes) for n in n_list]
    elif key == "aln":
        if N == 1:
            raise ValueError("n = 1: the only term is a, so d cannot be found")
        notes.append("l = a + (n-1)d, so d = (l - a)/(n - 1).")
        out = [make(A, (L - A) / (N - 1), int(N), notes)]
    elif key == "ans":
        n = int(N)
        if n == 1:
            raise ValueError("n = 1: the only term is a, so d cannot be found")
        notes.append("S = n/2 (2a + (n-1)d), so d = (2S/n - 2a)/(n - 1).")
        out = [make(A, (2 * S / n - 2 * A) / (n - 1), n, notes)]
    elif key == "als":
        notes.append("S = n(a + l)/2, so n = 2S/(a + l).")
        if A + L == 0:
            raise ValueError("a + l = 0: S = 0 whatever n is, so n cannot be found")
        n = _whole(2 * S / (A + L), "n", notes)
        if n:
            if n == 1:
                if L != A:
                    return [], notes + ["n = 1 needs l = a."]
                raise ValueError("n = 1: d cannot be found")
            out = [make(A, (L - A) / (n - 1), n, notes)]
    elif key == "dln":
        notes.append("l = a + (n-1)d, so a = l - (n-1)d.")
        out = [make(L - (N - 1) * D, D, int(N), notes)]
    elif key == "dns":
        n = int(N)
        notes.append("S = n/2 (2a + (n-1)d), so a = S/n - (n-1)d/2.")
        out = [make(S / n - (n - 1) * D / 2, D, n, notes)]
    elif key == "dls":
        notes.append("With a = l - (n-1)d, S = n l - d n(n-1)/2, i.e. d n^2 - (2l + d) n + 2S = 0.")
        if D == 0:
            if L == 0:
                raise ValueError("l = 0 and d = 0 gives S = 0 for every n")
            notes.append("d = 0, so S = n l and n = S/l.")
            n = _whole(S / L, "n", notes)
            n_list = [n] if n else []
        else:
            n_list, q = _quadratic_n(D, -(2 * L + D), 2 * S)
            notes += q
        out = [make(L - (n - 1) * D, D, n, notes) for n in n_list]
    elif key == "lns":
        n = int(N)
        if n == 1:
            raise ValueError("n = 1: the only term is a, so d cannot be found")
        notes.append("S = n(a + l)/2, so a = 2S/n - l; then d = (l - a)/(n - 1).")
        a = 2 * S / n - L
        out = [make(a, (L - a) / (n - 1), n, notes)]
    else:  # pragma: no cover
        raise ValueError("unsupported combination")
    # last check, exact: every solution must reproduce the three given values
    for sol in out:
        vals = sol.values()
        assert all(vals[k] == v[k] for k in v), "internal check failed"
    return out, notes


def is_term(a: Num, d: Num, x: Num) -> Tuple[bool, Optional[int], str]:
    """Is x a term of the AP a, a+d, a+2d ...? Returns (yes, position, reason)."""
    a, d, x = F(a), F(d), F(x)
    if d == 0:
        if x == a:
            return True, 1, "d = 0, so every term equals a, and x = a."
        return False, None, "d = 0, so every term equals a, and x differs from a."
    n = (x - a) / d + 1
    why = f"x = a + (n-1)d gives n = (x - a)/d + 1 = {fmt(n)}."
    if n.denominator != 1:
        return False, None, why + " That is not a whole number, so x is not in the AP."
    if n < 1:
        return False, None, why + " That is less than 1, so x would come before the first term."
    return True, int(n), why + f" That is a positive whole number, so x is term number {int(n)}."


def first_negative(a: Num, d: Num) -> Tuple[Optional[int], Optional[Fraction], str]:
    """First negative term: (position, value, reason). None when it never happens."""
    a, d = F(a), F(d)
    if a < 0:
        return 1, a, "The first term is already negative."
    if d >= 0:
        return None, None, "The first term is not negative and the terms never decrease, so no term is negative."
    n = int(a // (-d)) + 2
    val = a + (n - 1) * d
    return n, val, (f"Need a + (n-1)d < 0, so n - 1 > a/|d| = {fmt(a / -d)}; "
                    f"the smallest whole n is {n}, and term {n} = {fmt(val)}.")
