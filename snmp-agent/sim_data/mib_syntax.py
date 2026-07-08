"""Load full multi-line SYNTAX strings from MIB source files."""
from __future__ import annotations

import re
from pathlib import Path

_MIB_FILES = (
    "Rfc1155.smi",
    "rfc1212.smi",
    "rfc1158.smi",
    "RFC1213-MIB.mib",
    "8004v0134.mib",
    "1103v0125.mib",
    "1201v0227.mib",
    "1202v0218.mib",
)


def _strip_comments(text: str) -> str:
    out: list[str] = []
    for line in text.splitlines():
        if "--" in line:
            line = line[: line.index("--")]
        out.append(line.rstrip())
    return "\n".join(out)


def parse_full_syntax_from_text(text: str) -> dict[str, str]:
    text = _strip_comments(text)
    result: dict[str, str] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = re.match(r"^(\S+)\s+OBJECT-TYPE\s*$", lines[i], re.I)
        if not m:
            i += 1
            continue
        name = m.group(1)
        i += 1
        syntax_parts: list[str] = []
        in_syntax = False
        while i < len(lines):
            line = lines[i]
            if re.match(r"^\s*SYNTAX\s+", line, re.I):
                in_syntax = True
                syntax_parts.append(re.sub(r"^\s*SYNTAX\s+", "", line, flags=re.I).strip())
                i += 1
                continue
            if in_syntax:
                if re.match(r"^\s*(ACCESS|STATUS|DESCRIPTION)\s", line, re.I):
                    break
                syntax_parts.append(line.strip())
            if re.search(r"::=\s*\{", line):
                break
            i += 1
        if syntax_parts:
            result[name] = re.sub(r"\s+", " ", " ".join(syntax_parts)).strip()
        i += 1
    return result


def load_full_syntax_map(mib_dir: Path, deps_dir: Path) -> dict[str, str]:
    merged: dict[str, str] = {}
    for name in _MIB_FILES:
        path = mib_dir / name
        if not path.is_file():
            path = deps_dir / name
        if not path.is_file():
            continue
        merged.update(parse_full_syntax_from_text(path.read_text(encoding="utf-8", errors="replace")))
    return merged
