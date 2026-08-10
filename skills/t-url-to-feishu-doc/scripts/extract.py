#!/usr/bin/env python3
"""Extract clean Markdown from Docusaurus-style static HTML.

Stdlib only. Tuned for pages emitted by Docusaurus (the official Hermes docs
use Docusaurus), but works for any simple HTML page.

Usage:
  extract.py <input.html> <output.md> [--strip-front-matter]
"""
import sys
import re
from html.parser import HTMLParser


class Extractor(HTMLParser):
    SKIP = {"script", "style", "nav", "footer", "aside", "noscript"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip_depth = 0
        self.in_pre = False
        self.in_code = False
        self.in_a = False
        self.a_href = None
        self.list_stack = []  # 'ul' / 'ol'

    def _skip(self):
        return self.skip_depth > 0

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        if tag in self.SKIP:
            self.skip_depth += 1
            return
        if self._skip():
            return
        if tag == "pre":
            self.in_pre = True
            self.out.append("\n```\n")
            return
        if tag == "code" and not self.in_pre:
            cls = ad.get("class", "") or ""
            # Docusaurus 3 wraps each code-block line in <code class="codeBlockLines_*">;
            # treat that the same as a <pre> block.
            if "codeBlock" in cls:
                self.in_pre = True
                self.out.append("\n```\n")
                return
            self.in_code = True
            self.out.append("`")
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.out.append("\n\n" + "#" * int(tag[1]) + " ")
            return
        if tag == "p":
            self.out.append("\n\n")
            return
        if tag == "br":
            self.out.append("\n")
            return
        if tag == "a":
            self.in_a = True
            self.a_href = ad.get("href", "")
            self.out.append("[")
            return
        if tag == "img":
            alt = ad.get("alt", "")
            src = ad.get("src", "")
            self.out.append(f"![{alt}]({src})")
            return
        if tag in ("ul", "ol"):
            self.list_stack.append(tag)
            return
        if tag == "li":
            indent = "  " * max(0, len(self.list_stack) - 1)
            marker = "1." if self.list_stack[-1] == "ol" else "-"
            self.out.append(f"\n{indent}{marker} ")
            return
        if tag == "blockquote":
            self.out.append("\n\n> ")
            return
        if tag in ("strong", "b"):
            self.out.append("**")
            return
        if tag in ("em", "i"):
            self.out.append("*")
            return
        if tag == "hr":
            self.out.append("\n\n---\n\n")
            return
        if tag == "table":
            self.out.append("\n\n")
            return
        if tag == "tr":
            self.out.append("\n| ")
            return
        if tag in ("th", "td"):
            self.out.append(" | ")
            return

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self._skip():
            return
        if tag == "pre":
            self.in_pre = False
            self.out.append("\n```\n")
            return
        if tag == "code" and not self.in_pre:
            self.in_code = False
            self.out.append("`")
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.out.append("\n\n")
            return
        if tag == "a":
            self.in_a = False
            self.out.append(f"]({self.a_href})" if self.a_href else "]")
            self.a_href = None
            return
        if tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
            self.out.append("\n")
            return
        if tag == "blockquote":
            return
        if tag in ("strong", "b"):
            self.out.append("**")
            return
        if tag in ("em", "i"):
            self.out.append("*")
            return
        if tag in ("th", "td"):
            self.out.append(" |")
            return
        if tag == "table":
            self.out.append("\n")
            return

    def handle_data(self, data):
        if self._skip():
            return
        text = data
        if self.in_pre:
            self.out.append(text)
            return
        text = re.sub(r"[ \t]+", " ", text)
        self.out.append(text)


def strip_front_matter(text):
    """Drop a leading blockquote (used for local-archive metadata) after the H1.

    Heuristic: keep `# heading\n\n`, drop the contiguous blockquote block (with
    surrounding blank lines) that follows it, then resume.
    """
    lines = text.split("\n")
    h_idx = None
    for i, line in enumerate(lines):
        if line.startswith("# "):
            h_idx = i
            break
    if h_idx is None:
        return text
    j = h_idx + 1
    while j < len(lines) and not lines[j].strip():
        j += 1
    bq_start = j
    if j < len(lines) and lines[j].startswith(">"):
        while j < len(lines) and (lines[j].startswith(">") or not lines[j].strip()):
            j += 1
    if bq_start == j:
        return text
    new_lines = lines[:bq_start] + lines[j:]
    out, blanks = [], 0
    for line in new_lines:
        if not line.strip():
            blanks += 1
            if blanks <= 1:
                out.append(line)
        else:
            blanks = 0
            out.append(line)
    return "\n".join(out).strip() + "\n"


def extract_main(html_text):
    """Prefer <article>, then <main>, then <body>."""
    for tag in ("article", "main", "body"):
        m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", html_text, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1)
    return html_text


def main():
    if len(sys.argv) < 3:
        print("Usage: extract.py <input.html> <output.md> [--strip-front-matter]", file=sys.stderr)
        sys.exit(2)
    in_path, out_path = sys.argv[1], sys.argv[2]
    strip = "--strip-front-matter" in sys.argv
    with open(in_path, "r", encoding="utf-8") as f:
        html_text = f.read()
    parser = Extractor()
    parser.feed(extract_main(html_text))
    md = re.sub(r"\n{3,}", "\n\n", "".join(parser.out)).strip() + "\n"
    if strip:
        md = strip_front_matter(md)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
    title = next((ln[2:].strip() for ln in md.split("\n") if ln.startswith("# ")), "")
    print(f"wrote {out_path} ({len(md)} chars), title={title!r}")


if __name__ == "__main__":
    main()
