#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".dart_tool",
    ".gradle",
    ".idea",
    ".venv",
    "build",
    "coverage",
    "DerivedData",
    "dist",
    "node_modules",
    "Pods",
    "vendor",
}

GENERATED_FILES = (
    "*.g.dart",
    "*.mocks.dart",
    "*.freezed.dart",
    "*.gen.dart",
    "*.pb.go",
    "*.pb.dart",
    "*_generated.*",
    "*.generated.*",
    "*.min.js",
)

ALLOW_ONE_LINE_DOC = False
DOC_PREFIX = "///"
DOC_MAX_LENGTH = 100

ALLOWED_DIRECTIVES = tuple(
    re.compile(pattern)
    for pattern in (
        r"^//\s*ignore(_for_file)?:\s*[\w.\-=]+(\s*,\s*[\w.\-=]+)*\s*$",
        r"^//\s*dart format (off|on|width=\d+)\s*$",
        r"^//\s*@dart=\d+\.\d+\s*$",
        r"^//go:[a-z]+\b",
        r"^//\s*nolint(:[\w,\-]+)?\s*$",
        r"^//\s*swiftlint:(disable|enable)(:next|:this|:previous)?\s+[\w\s]+$",
        r"^//\s*swift-format-ignore(-file)?(:\s*[\w,\s]+)?$",
        r"^//\s*eslint-(disable|enable)(-next-line|-line)?(\s+[\w@/\-]+(\s*,\s*[\w@/\-]+)*)?\s*$",
        r"^/\*\s*eslint-(disable|enable)(\s+[\w@/\-]+(\s*,\s*[\w@/\-]+)*)?\s*\*/$",
        r"^//\s*@ts-(expect-error|ignore|nocheck)\s*$",
        r"^//\s*prettier-ignore\s*$",
        r"^//\s*biome-ignore\s+[\w/\-]+:",
        r"^//\s*ktlint-(disable|enable)(\s+[\w:\-]+)*\s*$",
        r"^#\s*noqa(:\s*[A-Z]+\d+(\s*,\s*[A-Z]+\d+)*)?\s*$",
        r"^#\s*type:\s*ignore(\[[\w\-, ]+\])?\s*$",
        r"^#\s*pylint:\s*(disable|enable)=[\w\-,]+\s*$",
        r"^#\s*fmt:\s*(on|off|skip)\s*$",
        r"^#\s*pragma:\s*no cover\s*$",
        r"^#\s*frozen_string_literal:\s*(true|false)\s*$",
        r"^#\s*rubocop:(disable|enable|todo)\s+[\w/,\s]+$",
    )
)


@dataclass(frozen=True)
class Language:
    line_markers: tuple[str, ...]
    block_markers: tuple[tuple[str, str], ...]
    string_delimiters: tuple[str, ...]
    nested_blocks: bool = False
    raw_delimiters: tuple[str, ...] = ()
    raw_prefixes: frozenset[str] = field(default_factory=frozenset)


C_STYLE_BLOCK = (("/*", "*/"),)

LANGUAGES = {
    "dart": Language(("//",), C_STYLE_BLOCK, ("'''", '"""', "'", '"'), True, (), frozenset({"r"})),
    "swift": Language(("//",), C_STYLE_BLOCK, ('"""', '"'), True),
    "kotlin": Language(("//",), C_STYLE_BLOCK, ('"""', '"', "'"), True, ('"""',)),
    "scala": Language(("//",), C_STYLE_BLOCK, ('"""', '"', "'"), True, ('"""',)),
    "java": Language(("//",), C_STYLE_BLOCK, ('"""', '"', "'")),
    "go": Language(("//",), C_STYLE_BLOCK, ("`", '"', "'"), False, ("`",)),
    "javascript": Language(("//",), C_STYLE_BLOCK, ("`", '"', "'")),
    "c": Language(("//",), C_STYLE_BLOCK, ('"', "'")),
    "rust": Language(("//",), C_STYLE_BLOCK, ('"',), True),
    "python": Language(
        ("#",),
        (),
        ('"""', "'''", '"', "'"),
        False,
        (),
        frozenset({"r", "rb", "br", "rf", "fr"}),
    ),
    "ruby": Language(("#",), (), ('"', "'")),
}

EXTENSIONS = {
    ".dart": "dart",
    ".swift": "swift",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".scala": "scala",
    ".java": "java",
    ".go": "go",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "javascript",
    ".tsx": "javascript",
    ".c": "c",
    ".h": "c",
    ".cc": "c",
    ".cpp": "c",
    ".hpp": "c",
    ".m": "c",
    ".mm": "c",
    ".cs": "c",
    ".rs": "rust",
    ".py": "python",
    ".rb": "ruby",
}


@dataclass(frozen=True)
class Comment:
    line: int
    text: str


def _starts_with_any(source: str, index: int, options) -> str | None:
    for option in options:
        if source.startswith(option, index):
            return option
    return None


def _has_raw_prefix(source: str, index: int, prefixes: frozenset[str]) -> bool:
    if not prefixes:
        return False
    start = index
    while start > 0 and (source[start - 1].isalnum() or source[start - 1] == "_"):
        start -= 1
    return source[start:index].lower() in prefixes


def _skip_block(source: str, index: int, opener: str, closer: str, nested: bool, line: int) -> tuple[int, int]:
    depth = 1
    position = index + len(opener)
    while position < len(source) and depth > 0:
        if nested and source.startswith(opener, position):
            depth += 1
            position += len(opener)
        elif source.startswith(closer, position):
            depth -= 1
            position += len(closer)
        else:
            if source[position] == "\n":
                line += 1
            position += 1
    return position, line


def _skip_string(source: str, index: int, quote: str, raw: bool, line: int) -> tuple[int, int]:
    position = index + len(quote)
    single_line = quote in ('"', "'")
    while position < len(source):
        character = source[position]
        if character == "\\" and not raw:
            if source[position + 1 : position + 2] == "\n":
                line += 1
            position += 2
            continue
        if source.startswith(quote, position):
            return position + len(quote), line
        if character == "\n":
            if single_line:
                return position, line
            line += 1
        position += 1
    return position, line


def find_comments(source: str, language: Language) -> list[Comment]:
    comments: list[Comment] = []
    delimiters = sorted(language.string_delimiters, key=len, reverse=True)
    openers = [opener for opener, _ in language.block_markers]
    position = 0
    line = 1
    while position < len(source):
        character = source[position]
        if character == "\n":
            line += 1
            position += 1
            continue
        opener = _starts_with_any(source, position, openers)
        if opener is not None:
            closer = dict(language.block_markers)[opener]
            end, end_line = _skip_block(source, position, opener, closer, language.nested_blocks, line)
            comments.append(Comment(line, source[position:end]))
            position, line = end, end_line
            continue
        if _starts_with_any(source, position, language.line_markers) is not None:
            end = source.find("\n", position)
            end = len(source) if end == -1 else end
            comments.append(Comment(line, source[position:end].rstrip()))
            position = end
            continue
        quote = _starts_with_any(source, position, delimiters)
        if quote is not None:
            raw = quote in language.raw_delimiters or _has_raw_prefix(source, position, language.raw_prefixes)
            position, line = _skip_string(source, position, quote, raw, line)
            continue
        position += 1
    return comments


def is_allowed(comment: Comment, neighbours: set[int]) -> bool:
    text = comment.text.strip()
    if comment.line == 1 and text.startswith("#!"):
        return True
    if comment.line <= 2 and re.match(r"^#.*coding[:=]\s*[\w.\-]+", text):
        return True
    if any(pattern.match(text) for pattern in ALLOWED_DIRECTIVES):
        return True
    if ALLOW_ONE_LINE_DOC and text.startswith(DOC_PREFIX) and "\n" not in text:
        alone = (comment.line - 1) not in neighbours and (comment.line + 1) not in neighbours
        return alone and len(text) <= DOC_MAX_LENGTH
    return False


def check_source(source: str, language: Language) -> list[Comment]:
    comments = find_comments(source, language)
    lines = {comment.line for comment in comments}
    return [comment for comment in comments if not is_allowed(comment, lines - {comment.line})]


def is_generated(path: Path) -> bool:
    return any(fnmatch.fnmatch(path.name, pattern) for pattern in GENERATED_FILES)


def source_files(roots: list[str]):
    for root in roots:
        root_path = Path(root)
        if root_path.is_file():
            if root_path.suffix in EXTENSIONS and not is_generated(root_path):
                yield root_path
            continue
        for directory, subdirectories, files in os.walk(root_path):
            subdirectories[:] = sorted(name for name in subdirectories if name not in SKIP_DIRS)
            for name in sorted(files):
                path = Path(directory) / name
                if path.suffix in EXTENSIONS and not is_generated(path):
                    yield path


def display_path(path: Path) -> str:
    return Path(os.path.relpath(path)).as_posix()


def read_approved(path: str | None) -> set[tuple[str, str]]:
    if not path or not Path(path).exists():
        return set()
    approved: set[tuple[str, str]] = set()
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.startswith("#"):
            continue
        file_part, _, quoted = raw.partition("\t")
        approved.add((file_part, json.loads(quoted)))
    return approved


def write_approved(path: str, violations: list[tuple[str, Comment]]) -> None:
    lines = ["# Comments the owner approved one by one: <path><TAB><JSON-quoted comment>. Agents never add to this file."]
    lines += sorted(f"{file}\t{json.dumps(comment.text.strip(), ensure_ascii=False)}" for file, comment in violations)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def preview(text: str) -> str:
    first = text.strip().splitlines()[0] if text.strip() else ""
    return first if len(first) <= 80 else first[:77] + "..."


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reports every comment in the source code that is not an allowed directive.")
    parser.add_argument("paths", nargs="*", default=["."])
    parser.add_argument("--approved", help="file with the comments the owner approved")
    parser.add_argument("--write-approved", action="store_true", help="owner only: approve every comment reported now")
    parser.add_argument("--full", action="store_true", help="print the whole text of each reported comment")
    arguments = parser.parse_args(argv)

    approved = read_approved(arguments.approved)
    violations: list[tuple[str, Comment]] = []
    used: set[tuple[str, str]] = set()
    for path in source_files(arguments.paths):
        language = LANGUAGES[EXTENSIONS[path.suffix]]
        try:
            source = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        file = display_path(path)
        for comment in check_source(source, language):
            key = (file, comment.text.strip())
            if key in approved:
                used.add(key)
                continue
            violations.append((file, comment))

    if arguments.write_approved:
        if not arguments.approved:
            parser.error("--write-approved needs --approved <file>")
        write_approved(arguments.approved, violations + [(file, Comment(0, text)) for file, text in used])
        print(f"wrote {len(violations) + len(used)} approved comment(s) to {arguments.approved}")
        return 0

    for file, comment in violations:
        print(f"{file}:{comment.line}: comment not allowed: {preview(comment.text)}")
        if arguments.full:
            print("    " + comment.text.strip().replace("\n", "\n    "))
    for file, text in sorted(approved - used):
        print(f"note: approved comment no longer found in {file}: {preview(text)}", file=sys.stderr)
    files = len({file for file, _ in violations})
    print(f"{len(violations)} comment(s) not allowed in {files} file(s)", file=sys.stderr)
    if violations:
        print(
            "Move what each comment explains into docs/ or the feature map, then delete the comment. "
            "See docs/architecture/code-style-and-lint.md.",
            file=sys.stderr,
        )
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
