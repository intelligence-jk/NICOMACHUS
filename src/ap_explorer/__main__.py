"""Command line.

  python -m ap_explorer solve --a 2 --d 3 --n 10
  python -m ap_explorer contains --a 3 --d 4 99
  python -m ap_explorer first-negative --a 100 --d -7
"""
import argparse
import sys

from .core import first_negative, fmt, is_term, solve_with_notes

NAMES = {"a": "first term a", "d": "common difference d", "n": "number of terms n",
         "l": "nth term l", "s": "sum S_n"}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="ap_explorer", description="Arithmetic progression explorer")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("solve", help="give any three of a, d, n, l, s and get the rest")
    for k in ("a", "d", "n", "l", "s"):
        s.add_argument(f"--{k}", help=NAMES[k])
    c = sub.add_parser("contains", help="is x a term of the AP?")
    c.add_argument("--a", required=True); c.add_argument("--d", required=True); c.add_argument("x")
    f = sub.add_parser("first-negative", help="position and value of the first negative term")
    f.add_argument("--a", required=True); f.add_argument("--d", required=True)
    args = p.parse_args(argv)
    try:
        if args.cmd == "solve":
            given = {k: getattr(args, k) for k in "adnls" if getattr(args, k) is not None}
            sols, notes = solve_with_notes(**given)
            print("Given: " + ", ".join(f"{k} = {v}" for k, v in given.items()))
            print("Working:")
            for line in dict.fromkeys(notes + (sols[0].steps if sols and not notes else [])):
                print("  " + line)
            if not sols:
                print("No arithmetic progression fits these values.")
                return 1
            for i, sol in enumerate(sols, 1):
                tag = f"Solution {i}: " if len(sols) > 1 else "Result: "
                print(tag + f"a = {fmt(sol.a)}, d = {fmt(sol.d)}, n = {sol.n}, "
                      f"nth term = {fmt(sol.l)}, S_n = {fmt(sol.s)}")
        elif args.cmd == "contains":
            ok, pos, why = is_term(args.a, args.d, args.x)
            print(why)
            print(f"Answer: {'yes, term ' + str(pos) if ok else 'no'}")
            return 0 if ok else 1
        else:
            pos, val, why = first_negative(args.a, args.d)
            print(why)
            print("Answer: " + (f"term {pos} = {fmt(val)}" if pos else "none"))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
