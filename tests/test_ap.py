from fractions import Fraction as Fr

import pytest

from ap_explorer import first_negative, is_term, solve
from ap_explorer.__main__ import main


def one(**kw):
    sols = solve(**kw)
    assert len(sols) == 1
    return sols[0]


def test_a_d_n():
    s = one(a=2, d=3, n=10)
    assert (s.l, s.s) == (29, 155)


def test_fractions():
    s = one(a="1/2", d="1/4", n=5)
    assert (s.l, s.s) == (Fr(3, 2), 5)


def test_a_d_l():
    s = one(a=3, d=4, l=99)
    assert (s.n, s.s) == (25, 25 * (3 + 99) // 2)
    assert solve(a=3, d=4, l=100) == []  # 100 is not in the AP


def test_a_d_s_rejects_negative_root():
    s = one(a=5, d=3, s=185)
    assert (s.n, s.l) == (10, 32)


def test_a_d_s_two_valid_roots():
    sols = solve(a=10, d=-2, s=10)
    assert sorted(x.n for x in sols) == [1, 10]
    assert {x.l for x in sols} == {10, -8}


def test_a_n_l_and_a_n_s():
    assert one(a=7, n=6, l=32).d == 5
    assert one(a=7, n=6, s=117).d == 5


def test_a_l_s():
    s = one(a=7, l=32, s=117)
    assert (s.n, s.d) == (6, 5)


def test_d_n_l_and_d_n_s():
    assert one(d=5, n=6, l=32).a == 7
    assert one(d=5, n=6, s=117).a == 7


def test_d_l_s_quadratic():
    s = one(d=5, l=32, s=117)
    assert (s.n, s.a) == (6, 7)


def test_n_l_s():
    s = one(n=6, l=32, s=117)
    assert (s.a, s.d) == (7, 5)


def test_no_solution_when_n_not_whole():
    assert solve(a=1, d=1, s=14) == []  # n^2 + n - 28 = 0 has no rational root


def test_bad_input():
    with pytest.raises(ValueError):
        solve(a=1, d=2)
    with pytest.raises(ValueError):
        solve(a=1, d=2, n=0)
    with pytest.raises(ValueError):
        solve(a=1, n=1, l=1)


def test_is_term():
    assert is_term(3, 4, 99) == (True, 25, is_term(3, 4, 99)[2])
    assert is_term(3, 4, 100)[0] is False
    assert is_term(3, 4, -1)[0] is False  # before the first term
    assert is_term("1/2", "1/2", 5) == (True, 10, is_term("1/2", "1/2", 5)[2])
    assert is_term(4, 0, 4)[0] and not is_term(4, 0, 5)[0]


def test_first_negative():
    assert first_negative(100, -7)[:2] == (16, -5)
    assert first_negative(9, -3)[:2] == (5, -3)   # term 4 is 0, not negative
    assert first_negative(-2, 5)[:2] == (1, -2)
    assert first_negative(5, 0)[0] is None
    assert first_negative("1/2", "-1/3")[:2] == (3, Fr(-1, 6))


def test_every_combination_round_trips():
    base = one(a=-4, d="3/2", n=9)
    vals = {"a": base.a, "d": base.d, "n": base.n, "l": base.l, "s": base.s}
    from itertools import combinations
    for trio in combinations(vals, 3):
        try:
            sols = solve(**{k: vals[k] for k in trio})
        except ValueError:
            continue  # a legitimately undetermined case
        assert any((x.a, x.d, x.n) == (base.a, base.d, base.n) for x in sols), trio


def test_cli(capsys):
    assert main(["solve", "--a", "5", "--d", "3", "--s", "185"]) == 0
    out = capsys.readouterr().out
    assert "n = 10" in out and "rejected" in out
    assert main(["first-negative", "--a", "100", "--d", "-7"]) == 0
