#!/usr/bin/env python3
"""Sanitize files for agent consumption.

Strips Unicode characters that break JSON serialization in the ACP hook
pipeline — specifically U+2028 (LINE SEPARATOR) and U+2029 (PARAGRAPH
SEPARATOR), which are valid Unicode whitespace but illegal inside JSON
string literals.

Also removes ASCII control characters (U+0000–U+001F) except for the
three that are essential: tab (U+0009), newline (U+000A), and carriage
return (U+000D).

Usage:
    python3 scripts/sanitize-for-agent.py FILE [FILE ...]
    python3 scripts/sanitize-for-agent.py --check FILE [FILE ...]

With --check, reports problems without modifying files (exit 1 if dirty).
Without --check, cleans in-place and reports what was fixed.
"""

import re
import sys

# JSON-hostile characters: U+2028, U+2029, and ASCII control chars
# (excluding tab, newline, carriage return which are fine)
HOSTILE_PATTERN = re.compile(r'[\u2028\u2029\x00-\x08\x0b\x0c\x0e-\x1f]')

REPLACEMENTS = {
    '\u2028': ' ',   # LINE SEPARATOR → space
    '\u2029': '\n',  # PARAGRAPH SEPARATOR → newline
}


def sanitize(text: str) -> tuple[str, int]:
    """Replace hostile characters. Returns (cleaned_text, count)."""
    count = len(HOSTILE_PATTERN.findall(text))
    if count == 0:
        return text, 0

    def replace(m):
        ch = m.group()
        return REPLACEMENTS.get(ch, '')  # control chars → delete

    return HOSTILE_PATTERN.sub(replace, text), count


def main():
    args = sys.argv[1:]
    check_only = False
    if '--check' in args:
        check_only = True
        args.remove('--check')

    if not args:
        print(__doc__.strip())
        sys.exit(2)

    any_dirty = False
    for path in args:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (OSError, UnicodeDecodeError) as e:
            print(f"SKIP {path}: {e}")
            continue

        cleaned, count = sanitize(content)

        if count == 0:
            print(f"CLEAN {path}")
        elif check_only:
            print(f"DIRTY {path}: {count} hostile character(s)")
            any_dirty = True
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            print(f"FIXED {path}: replaced {count} hostile character(s)")

    sys.exit(1 if any_dirty else 0)


if __name__ == '__main__':
    main()
