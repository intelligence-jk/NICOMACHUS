# Review (24 Nov 2026)

1. Maths checked twice: PASS. Exact tests (16 tests, including a=5,d=3,S=185 giving n=10 with the negative root rejected, and a=10,d=-2,S=10 giving both n=1 and n=10), plus an independent brute-force run: every (a,d,n) with a -6..6, d -5..5, n 1..8, with l and S found by listing the terms, then every 3-of-5 combination solved back. 10,711 solvable cases, 0 misses.
2. Tests pass locally (16 passed) and from a clean virtualenv with `pip install -e . pytest`, as CI does. CI itself has not run: nothing is on GitHub yet.
3. No student data, no board-paper or textbook text, nothing of any other business: PASS (searched).
4. README has what it solves, real example outputs, the maths: PASS.
5. MIT licence, copyright MATH and MYTH FZ-LLC: PASS (template LICENSE).
6. No em dashes, no "Dubai", no outcome promises: PASS (searched). Dependencies: standard library only.
