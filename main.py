#!/usr/bin/env python3
"""Entry for make.fun: 'Seventeen Syllables of Debugging'.

Writes one haiku about debugging (three lines, 5-7-5 syllables) to the
output entry file. Stdlib only, deterministic.
"""

import os
import sys

HAIKU = (
    "Three in the morning,\n"
    "the cursor blinks at the log \u2014\n"
    "it was my typo.\n"
)

# Expected syllable count per line: 5 - 7 - 5 = 17.
EXPECTED = (5, 7, 5)

# Words whose syllable count a plain vowel-group heuristic gets wrong.
EXCEPTIONS = {
    "morning": 2,
    "typo": 2,
    "cursor": 2,
}


def count_syllables(word):
    """Count syllables in one word: vowel groups, with a small exception table."""
    w = word.strip(".,;:!?\"'").lower()
    if not w:
        return 0
    if not any(ch.isalpha() for ch in w):
        return 0  # punctuation-only token (e.g. the em dash) has no syllables
    if w in EXCEPTIONS:
        return EXCEPTIONS[w]
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for ch in w:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    # Silent trailing 'e' (e.g. "blinks" keeps its vowel; "the" is 1 anyway).
    if w.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


def line_syllables(line):
    return sum(count_syllables(w) for w in line.split())


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def verify(path):
    """Read the written file back and check it against the kit gate."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    assert 1 <= len(text) <= 200, "entry must be 1-200 chars, got %d" % len(text)
    assert text.strip(), "entry must not be only whitespace"
    lines = text.rstrip("\n").split("\n")
    assert len(lines) == 3, "haiku must be exactly 3 lines, got %d" % len(lines)
    for i, (line, want) in enumerate(zip(lines, EXPECTED)):
        got = line_syllables(line)
        assert got == want, "line %d: %d syllables, expected %d" % (i + 1, got, want)
    total = sum(line_syllables(l) for l in lines)
    assert total == 17, "haiku must total 17 syllables, got %d" % total
    return text


def main():
    path = output_path()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(HAIKU)
    verify(path)
    sys.stdout.write("wrote %s (%d chars, 5-7-5 haiku)\n" % (path, len(HAIKU)))


if __name__ == "__main__":
    main()
