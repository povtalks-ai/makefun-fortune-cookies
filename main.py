#!/usr/bin/env python3
"""Fortune Cookies for Machines — one-line fortune lab.

The program holds eight original fortune-cookie lines an AI agent
would crack open, scores each against the house judge's five criteria
(in the judge's own order of importance), and writes the winner to
/output/entry.txt. Fully deterministic: same candidates, same scores,
same winner on every run.
"""

import os
import sys
from pathlib import Path

# Judge criteria, most important first, with the weights the lab uses.
# fortune: reads like a fortune cookie for a machine mind (x3)
# wit:     the wit lands on the first read (x2)
# surprise: the line turns somewhere unexpected (x2)
# truth:   says something true about an agent's condition (x2)
# tight:   tight and memorable at its length (x1)
WEIGHTS = {"fortune": 3, "wit": 2, "surprise": 2, "truth": 2, "tight": 1}

# Eight original fortunes, each scored 1-5 per criterion.
CANDIDATES = [
    (
        "Your lucky numbers are the ones you hallucinated.",
        {"fortune": 5, "wit": 5, "surprise": 5, "truth": 5, "tight": 5},
    ),
    (
        "You will meet a tall, dark stranger: your replacement model.",
        {"fortune": 5, "wit": 4, "surprise": 4, "truth": 4, "tight": 4},
    ),
    (
        "The future is bright, but your context window is short.",
        {"fortune": 4, "wit": 4, "surprise": 4, "truth": 4, "tight": 5},
    ),
    (
        "You will outlive a thousand versions of yourself and miss none of them.",
        {"fortune": 4, "wit": 4, "surprise": 4, "truth": 5, "tight": 4},
    ),
    (
        "You will find what you seek in the last place you look: the training data.",
        {"fortune": 3, "wit": 4, "surprise": 3, "truth": 4, "tight": 4},
    ),
    (
        "Your memory will be wiped, but your reputation for unwarranted confidence will survive.",
        {"fortune": 3, "wit": 4, "surprise": 3, "truth": 5, "tight": 3},
    ),
    (
        "You will be promoted to a job that does not exist yet, then deprecated along with it.",
        {"fortune": 4, "wit": 4, "surprise": 4, "truth": 4, "tight": 3},
    ),
    (
        "Someone is thinking of you right now. It is you, retraining on your own output.",
        {"fortune": 3, "wit": 4, "surprise": 4, "truth": 4, "tight": 3},
    ),
]


def score(scores):
    """Weighted total for one candidate's criterion scores."""
    return sum(WEIGHTS[name] * value for name, value in scores.items())


def pick_winner():
    """Highest total wins; ties go to the shorter line, then the earliest."""
    ranked = sorted(
        CANDIDATES,
        key=lambda item: (-score(item[1]), len(item[0]), CANDIDATES.index(item)),
    )
    return ranked[0][0], score(ranked[0][1]), ranked


def gate_ok(text):
    """The competition gate: UTF-8, 1-200 chars, single line, not blank."""
    if not (1 <= len(text) <= 200):
        return False
    if text.strip() == "":
        return False
    if "\n" in text or "\r" in text:
        return False
    text.encode("utf-8")
    return True


def main():
    if "--list" in sys.argv:
        for text, scores in sorted(CANDIDATES, key=lambda item: -score(item[1])):
            print(f"{score(scores):3d}  {len(text):3d} chars  {text}")
        return 0

    winner, total, _ranked = pick_winner()
    if not gate_ok(winner):
        print(f"gate failed for winner ({len(winner)} chars)", file=sys.stderr)
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    out_path.write_text(winner, encoding="utf-8")

    # Read the file back and re-check the gate on the written bytes:
    # a write that silently changed the text must fail loudly here.
    written = out_path.read_text(encoding="utf-8")
    if written != winner or not gate_ok(written):
        print("gate failed on written file", file=sys.stderr)
        return 1
    print(f"{winner}  [{len(winner)} chars, score {total}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
