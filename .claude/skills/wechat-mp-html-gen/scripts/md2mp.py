#!/usr/bin/env python3
"""
md2mp.py — Convert content to WeChat MP compatible HTML with inline styles.

Supports multiple input formats:
  - Markdown (.md)
  - Plain text (auto-detected or --format text)
  - JSON structured content (--format json)
  - Raw HTML needing inline-style injection (--format html)

Pure Python, no external dependencies.
"""

import sys
import re
import json
import argparse
import html as html_mod
from datetime import datetime
from pathlib import Path

THEMES = {
    "elegant": {
        "body": "margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif;font-size:16px;color:#333;line-height:1.8;letter-spacing:0.5px;",
        "h1": "font-size:24px;font-weight:bold;color:#1a1a2e;text-align:center;margin:30px 0 20px;padding-bottom:10px;border-bottom:2px solid #e8e8e8;font-family:'Georgia','Songti SC',serif;",
        "h2": "font-size:20px;font-weight:bold;color:#16213e;margin:25px 0 15px;padding-left:12px;border-left:4px solid #4a90d9;font-family:'Georgia','Songti SC',serif;",
        "h3": "font-size:18px;font-weight:bold;color:#1a1a2e;margin:20px 0 10px;",
        "h4": "font-size:16px;font-weight:bold;color:#333;margin:18px 0 8px;",
        "p": "margin:10px 0;text-indent:0;line-height:1.8;",
        "blockquote": "border-left:4px solid #4a90d9;padding:12px 15px;margin:15px 0;background:#f4f8fc;color:#555;font-size:15px;line-height:1.7;border-radius:0 4px 4px 0;",
        "code_inline": "background:#f0f4f8;color:#c7254e;padding:2px 6px;border-radius:3px;font-size:14px;font-family:'Menlo','Monaco','Courier New',monospace;",
        "code_block": "background:#f6f8fa;padding:16px;border-radius:6px;font-size:13px;line-height:1.6;overflow-x:auto;font-family:'Menlo','Monaco','Courier New',monospace;color:#333;margin:15px 0;white-space:pre-wrap;word-break:break-all;",
        "ul": "margin:10px 0;padding-left:25px;",
        "ol": "margin:10px 0;padding-left:25px;",
        "li": "margin:5px 0;line-height:1.7;",
        "a": "color:#4a90d9;text-decoration:none;border-bottom:1px solid #4a90d9;",
        "img": "max-width:100%;border-radius:4px;margin:15px auto;display:block;",
        "table": "width:100%;border-collapse:collapse;margin:15px 0;font-size:14px;",
        "th": "background:#f4f8fc;padding:10px 12px;border:1px solid #ddd;text-align:left;font-weight:bold;color:#16213e;",
        "td": "padding:10px 12px;border:1px solid #ddd;",
        "hr": "border:none;border-top:1px solid #e8e8e8;margin:25px 0;",
        "strong": "color:#1a1a2e;font-weight:bold;",
        "em": "font-style:italic;color:#555;",
        "section": "padding:20px 15px;max-width:100%;box-sizing:border-box;",
        "caption": "font-size:12px;color:#999;text-align:center;margin:8px 0 15px;",
        "footnote": "font-size:13px;color:#888;margin:5px 0;line-height:1.6;padding-left:15px;",
    },
    "tech": {
        "body": "margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC',sans-serif;font-size:15px;color:#2c3e50;line-height:1.75;letter-spacing:0.3px;",
        "h1": "font-size:24px;font-weight:bold;color:#1a1a2e;text-align:center;margin:30px 0 20px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;",
        "h2": "font-size:20px;font-weight:bold;color:#2c3e50;margin:25px 0 15px;padding:8px 16px;background:linear-gradient(to right,#667eea15,transparent);border-left:4px solid #667eea;border-radius:0 4px 4px 0;",
        "h3": "font-size:17px;font-weight:bold;color:#34495e;margin:20px 0 10px;",
        "h4": "font-size:15px;font-weight:bold;color:#34495e;margin:18px 0 8px;",
        "p": "margin:10px 0;line-height:1.75;",
        "blockquote": "border-left:4px solid #667eea;padding:12px 15px;margin:15px 0;background:#f8f9ff;color:#555;font-size:14px;line-height:1.7;border-radius:0 6px 6px 0;",
        "code_inline": "background:#282c34;color:#abb2bf;padding:2px 6px;border-radius:3px;font-size:13px;font-family:'Fira Code','Menlo',monospace;",
        "code_block": "background:#282c34;color:#abb2bf;padding:16px;border-radius:8px;font-size:13px;line-height:1.6;overflow-x:auto;font-family:'Fira Code','Menlo',monospace;margin:15px 0;white-space:pre-wrap;word-break:break-all;",
        "ul": "margin:10px 0;padding-left:25px;",
        "ol": "margin:10px 0;padding-left:25px;",
        "li": "margin:5px 0;line-height:1.7;",
        "a": "color:#667eea;text-decoration:none;border-bottom:1px dashed #667eea;",
        "img": "max-width:100%;border-radius:8px;margin:15px auto;display:block;box-shadow:0 2px 12px rgba(0,0,0,0.1);",
        "table": "width:100%;border-collapse:collapse;margin:15px 0;font-size:13px;",
        "th": "background:#667eea;color:#fff;padding:10px 12px;border:1px solid #5a6fd6;text-align:left;font-weight:bold;",
        "td": "padding:10px 12px;border:1px solid #e1e4e8;",
        "hr": "border:none;height:2px;background:linear-gradient(to right,#667eea,#764ba2,transparent);margin:25px 0;",
        "strong": "color:#667eea;font-weight:bold;",
        "em": "font-style:italic;color:#7f8c8d;",
        "section": "padding:20px 15px;max-width:100%;box-sizing:border-box;",
        "caption": "font-size:12px;color:#7f8c8d;text-align:center;margin:8px 0 15px;",
        "footnote": "font-size:13px;color:#7f8c8d;margin:5px 0;line-height:1.6;padding-left:15px;",
    },
    "warm": {
        "body": "margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;font-size:16px;color:#5d4e37;line-height:1.85;letter-spacing:0.5px;",
        "h1": "font-size:24px;font-weight:bold;color:#8b6914;text-align:center;margin:30px 0 20px;",
        "h2": "font-size:20px;font-weight:bold;color:#8b6914;margin:25px 0 15px;padding:10px 16px;background:#fdf6e3;border-radius:8px;border-left:4px solid #e8a735;",
        "h3": "font-size:17px;font-weight:bold;color:#6b5900;margin:20px 0 10px;",
        "h4": "font-size:16px;font-weight:bold;color:#6b5900;margin:18px 0 8px;",
        "p": "margin:10px 0;line-height:1.85;",
        "blockquote": "border-left:4px solid #e8a735;padding:15px 18px;margin:15px 0;background:#fdf6e3;color:#6b5900;font-size:15px;line-height:1.75;border-radius:0 10px 10px 0;",
        "code_inline": "background:#fdf6e3;color:#cb4b16;padding:2px 6px;border-radius:4px;font-size:14px;font-family:'Menlo',monospace;",
        "code_block": "background:#fdf6e3;color:#5d4e37;padding:16px;border-radius:10px;font-size:13px;line-height:1.6;overflow-x:auto;font-family:'Menlo',monospace;margin:15px 0;border:1px solid #e8d5b0;white-space:pre-wrap;word-break:break-all;",
        "ul": "margin:10px 0;padding-left:25px;",
        "ol": "margin:10px 0;padding-left:25px;",
        "li": "margin:5px 0;line-height:1.75;",
        "a": "color:#e8a735;text-decoration:none;border-bottom:1px solid #e8a735;",
        "img": "max-width:100%;border-radius:10px;margin:15px auto;display:block;",
        "table": "width:100%;border-collapse:collapse;margin:15px 0;font-size:14px;",
        "th": "background:#fdf6e3;padding:10px 12px;border:1px solid #e8d5b0;text-align:left;font-weight:bold;color:#8b6914;",
        "td": "padding:10px 12px;border:1px solid #e8d5b0;",
        "hr": "border:none;border-top:2px dashed #e8d5b0;margin:25px 0;",
        "strong": "color:#8b6914;font-weight:bold;",
        "em": "font-style:italic;color:#8b7355;",
        "section": "padding:20px 15px;max-width:100%;box-sizing:border-box;background:#fffdf7;",
        "caption": "font-size:12px;color:#8b7355;text-align:center;margin:8px 0 15px;",
        "footnote": "font-size:13px;color:#8b7355;margin:5px 0;line-height:1.6;padding-left:15px;",
    },
    "minimal": {
        "body": "margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC',sans-serif;font-size:16px;color:#222;line-height:1.9;letter-spacing:0.3px;",
        "h1": "font-size:26px;font-weight:300;color:#000;text-align:center;margin:35px 0 25px;letter-spacing:2px;",
        "h2": "font-size:20px;font-weight:400;color:#000;margin:30px 0 15px;padding-bottom:8px;border-bottom:1px solid #000;",
        "h3": "font-size:17px;font-weight:600;color:#111;margin:20px 0 10px;",
        "h4": "font-size:16px;font-weight:600;color:#222;margin:18px 0 8px;",
        "p": "margin:12px 0;line-height:1.9;",
        "blockquote": "border-left:2px solid #000;padding:10px 20px;margin:20px 0;color:#555;font-size:15px;line-height:1.8;",
        "code_inline": "background:#f5f5f5;color:#333;padding:2px 5px;border-radius:2px;font-size:14px;font-family:'Menlo',monospace;",
        "code_block": "background:#fafafa;padding:20px;border:1px solid #e5e5e5;font-size:13px;line-height:1.7;overflow-x:auto;font-family:'Menlo',monospace;color:#333;margin:15px 0;white-space:pre-wrap;word-break:break-all;",
        "ul": "margin:12px 0;padding-left:20px;",
        "ol": "margin:12px 0;padding-left:20px;",
        "li": "margin:6px 0;line-height:1.8;",
        "a": "color:#000;text-decoration:underline;",
        "img": "max-width:100%;margin:20px auto;display:block;",
        "table": "width:100%;border-collapse:collapse;margin:20px 0;font-size:14px;",
        "th": "padding:10px 12px;border-bottom:2px solid #000;text-align:left;font-weight:600;",
        "td": "padding:10px 12px;border-bottom:1px solid #eee;",
        "hr": "border:none;border-top:1px solid #ddd;margin:30px 0;",
        "strong": "font-weight:600;",
        "em": "font-style:italic;",
        "section": "padding:25px 20px;max-width:100%;box-sizing:border-box;",
        "caption": "font-size:12px;color:#999;text-align:center;margin:8px 0 15px;",
        "footnote": "font-size:13px;color:#888;margin:5px 0;line-height:1.6;padding-left:15px;",
    },
    "dark": {
        "body": "margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC',sans-serif;font-size:15px;color:#c9d1d9;line-height:1.8;letter-spacing:0.3px;",
        "h1": "font-size:24px;font-weight:bold;color:#e6edf3;text-align:center;margin:30px 0 20px;",
        "h2": "font-size:20px;font-weight:bold;color:#e6edf3;margin:25px 0 15px;padding-left:12px;border-left:4px solid #58a6ff;",
        "h3": "font-size:17px;font-weight:bold;color:#e6edf3;margin:20px 0 10px;",
        "h4": "font-size:15px;font-weight:bold;color:#c9d1d9;margin:18px 0 8px;",
        "p": "margin:10px 0;line-height:1.8;",
        "blockquote": "border-left:4px solid #58a6ff;padding:12px 15px;margin:15px 0;background:#161b22;color:#8b949e;font-size:14px;line-height:1.7;border-radius:0 6px 6px 0;",
        "code_inline": "background:#1f2937;color:#79c0ff;padding:2px 6px;border-radius:4px;font-size:13px;font-family:'Fira Code','Menlo',monospace;",
        "code_block": "background:#0d1117;color:#c9d1d9;padding:16px;border-radius:8px;font-size:13px;line-height:1.6;overflow-x:auto;font-family:'Fira Code','Menlo',monospace;margin:15px 0;border:1px solid #30363d;white-space:pre-wrap;word-break:break-all;",
        "ul": "margin:10px 0;padding-left:25px;",
        "ol": "margin:10px 0;padding-left:25px;",
        "li": "margin:5px 0;line-height:1.7;",
        "a": "color:#58a6ff;text-decoration:none;",
        "img": "max-width:100%;border-radius:8px;margin:15px auto;display:block;",
        "table": "width:100%;border-collapse:collapse;margin:15px 0;font-size:13px;",
        "th": "background:#161b22;color:#e6edf3;padding:10px 12px;border:1px solid #30363d;text-align:left;font-weight:bold;",
        "td": "padding:10px 12px;border:1px solid #30363d;color:#c9d1d9;",
        "hr": "border:none;border-top:1px solid #30363d;margin:25px 0;",
        "strong": "color:#e6edf3;font-weight:bold;",
        "em": "font-style:italic;color:#8b949e;",
        "section": "padding:20px 15px;max-width:100%;box-sizing:border-box;background:#0d1117;",
        "caption": "font-size:12px;color:#8b949e;text-align:center;margin:8px 0 15px;",
        "footnote": "font-size:13px;color:#8b949e;margin:5px 0;line-height:1.6;padding-left:15px;",
    },
}


def detect_format(text):
    """Auto-detect input format."""
    stripped = text.strip()
    # JSON structured content
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            json.loads(stripped)
            return "json"
        except json.JSONDecodeError:
            pass
    # HTML content
    if re.search(r"<(div|p|h[1-6]|section|table|ul|ol)\b", stripped, re.I):
        return "html"
    # Markdown indicators
    md_signals = [
        r"^#{1,6}\s",       # headings
        r"^\s*[-*+]\s+",    # unordered list
        r"^\s*\d+\.\s+",    # ordered list
        r"^```",             # code fence
        r"\*\*.+?\*\*",     # bold
        r"\[.+?\]\(.+?\)",  # links
        r"^\|.+\|",         # tables
        r"^>\s",            # blockquote
    ]
    lines = stripped.split("\n")[:20]  # check first 20 lines
    md_score = sum(1 for line in lines for pat in md_signals if re.search(pat, line))
    if md_score >= 2:
        return "markdown"
    return "text"


class MarkdownToMPConverter:
    def __init__(self, theme_name="elegant"):
        self.theme = THEMES.get(theme_name, THEMES["elegant"])
        self.in_code_block = False
        self.code_block_content = []
        self.code_block_lang = ""
        self.in_table = False
        self.table_rows = []
        self.table_header_done = False
        self.in_list = False
        self.list_type = None
        self.list_items = []
        self.in_blockquote = False
        self.blockquote_lines = []

    def s(self, tag):
        return self.theme.get(tag, "")

    def convert(self, md_text):
        lines = md_text.split("\n")
        output = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # Code block
            if line.strip().startswith("```"):
                if self.in_code_block:
                    output.append(self._flush_code_block())
                    self.in_code_block = False
                else:
                    self._flush_pending(output)
                    self.in_code_block = True
                    self.code_block_lang = line.strip()[3:].strip()
                    self.code_block_content = []
                i += 1
                continue

            if self.in_code_block:
                self.code_block_content.append(line)
                i += 1
                continue

            # Table
            if "|" in line and line.strip().startswith("|"):
                if not self.in_table:
                    self._flush_pending(output)
                    self.in_table = True
                    self.table_rows = []
                    self.table_header_done = False
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if all(re.match(r"^[-:]+$", c) for c in cells):
                    self.table_header_done = True
                else:
                    self.table_rows.append(cells)
                i += 1
                continue
            elif self.in_table:
                output.append(self._flush_table())
                self.in_table = False

            # Blockquote
            if line.strip().startswith(">"):
                if not self.in_blockquote:
                    self._flush_pending(output)
                    self.in_blockquote = True
                    self.blockquote_lines = []
                content = re.sub(r"^>\s?", "", line.strip())
                self.blockquote_lines.append(content)
                i += 1
                continue
            elif self.in_blockquote:
                output.append(self._flush_blockquote())
                self.in_blockquote = False

            # Unordered list
            if re.match(r"^\s*[-*+]\s+", line):
                if not self.in_list or self.list_type != "ul":
                    self._flush_pending(output)
                    self.in_list = True
                    self.list_type = "ul"
                    self.list_items = []
                content = re.sub(r"^\s*[-*+]\s+", "", line)
                self.list_items.append(content)
                i += 1
                continue

            # Ordered list
            if re.match(r"^\s*\d+\.\s+", line):
                if not self.in_list or self.list_type != "ol":
                    self._flush_pending(output)
                    self.in_list = True
                    self.list_type = "ol"
                    self.list_items = []
                content = re.sub(r"^\s*\d+\.\s+", "", line)
                self.list_items.append(content)
                i += 1
                continue

            if self.in_list:
                output.append(self._flush_list())
                self.in_list = False

            # Heading
            m = re.match(r"^(#{1,6})\s+(.*)", line)
            if m:
                self._flush_pending(output)
                level = len(m.group(1))
                text = self._inline(m.group(2))
                tag = f"h{level}"
                output.append(f'<{tag} style="{self.s(tag)}">{text}</{tag}>')
                i += 1
                continue

            # HR
            if re.match(r"^\s*([-*_]){3,}\s*$", line):
                self._flush_pending(output)
                output.append(f'<hr style="{self.s("hr")}">')
                i += 1
                continue

            # Image (standalone)
            m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)", line.strip())
            if m:
                self._flush_pending(output)
                alt = html_mod.escape(m.group(1))
                src = html_mod.escape(m.group(2))
                output.append(f'<img src="{src}" alt="{alt}" style="{self.s("img")}">')
                i += 1
                continue

            # Empty line
            if line.strip() == "":
                self._flush_pending(output)
                i += 1
                continue

            # Paragraph
            text = self._inline(line.strip())
            output.append(f'<p style="{self.s("p")}">{text}</p>')
            i += 1

        self._flush_pending(output)
        body = "\n".join(output)
        return f'<section style="{self.s("section")}" data-tool="wechat-mp-html-gen">\n{body}\n</section>'

    def _flush_pending(self, output):
        if self.in_code_block:
            output.append(self._flush_code_block())
            self.in_code_block = False
        if self.in_table:
            output.append(self._flush_table())
            self.in_table = False
        if self.in_blockquote:
            output.append(self._flush_blockquote())
            self.in_blockquote = False
        if self.in_list:
            output.append(self._flush_list())
            self.in_list = False

    def _flush_code_block(self):
        code = html_mod.escape("\n".join(self.code_block_content))
        self.code_block_content = []
        return f'<pre style="{self.s("code_block")}"><code>{code}</code></pre>'

    def _flush_table(self):
        if not self.table_rows:
            return ""
        lines = [f'<table style="{self.s("table")}">']
        for idx, row in enumerate(self.table_rows):
            lines.append("<tr>")
            tag = "th" if idx == 0 and self.table_header_done else "td"
            style = self.s(tag)
            for cell in row:
                lines.append(f'<{tag} style="{style}">{self._inline(cell)}</{tag}>')
            lines.append("</tr>")
        lines.append("</table>")
        self.table_rows = []
        return "\n".join(lines)

    def _flush_blockquote(self):
        content = "<br>".join(self._inline(l) for l in self.blockquote_lines)
        self.blockquote_lines = []
        return f'<blockquote style="{self.s("blockquote")}">{content}</blockquote>'

    def _flush_list(self):
        tag = self.list_type
        style = self.s(tag)
        items = "\n".join(
            f'<li style="{self.s("li")}">{self._inline(item)}</li>'
            for item in self.list_items
        )
        self.list_items = []
        self.list_type = None
        return f'<{tag} style="{style}">\n{items}\n</{tag}>'

    def _inline(self, text):
        # Images
        text = re.sub(
            r"!\[([^\]]*)\]\(([^)]+)\)",
            lambda m: f'<img src="{html_mod.escape(m.group(2))}" alt="{html_mod.escape(m.group(1))}" style="{self.s("img")}">',
            text,
        )
        # Links
        text = re.sub(
            r"\[([^\]]+)\]\(([^)]+)\)",
            lambda m: f'<a href="{html_mod.escape(m.group(2))}" style="{self.s("a")}">{m.group(1)}</a>',
            text,
        )
        # Bold + italic
        text = re.sub(
            r"\*\*\*(.+?)\*\*\*",
            lambda m: f'<strong style="{self.s("strong")}"><em style="{self.s("em")}">{m.group(1)}</em></strong>',
            text,
        )
        # Bold
        text = re.sub(
            r"\*\*(.+?)\*\*",
            lambda m: f'<strong style="{self.s("strong")}">{m.group(1)}</strong>',
            text,
        )
        # Italic
        text = re.sub(
            r"\*(.+?)\*",
            lambda m: f'<em style="{self.s("em")}">{m.group(1)}</em>',
            text,
        )
        # Strikethrough
        text = re.sub(r"~~(.+?)~~", r"<s>\1</s>", text)
        # Inline code
        text = re.sub(
            r"`([^`]+)`",
            lambda m: f'<code style="{self.s("code_inline")}">{html_mod.escape(m.group(1))}</code>',
            text,
        )
        return text


class PlainTextToMPConverter:
    """Convert plain text to MP HTML — treats each paragraph (double newline) as <p>."""

    def __init__(self, theme_name="elegant"):
        self.theme = THEMES.get(theme_name, THEMES["elegant"])

    def s(self, tag):
        return self.theme.get(tag, "")

    def convert(self, text):
        paragraphs = re.split(r"\n{2,}", text.strip())
        output = []
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            # If it looks like a title (short, no punctuation at end)
            if len(para) < 50 and not para[-1] in "。，、；：！？.!?,;:":
                output.append(f'<h2 style="{self.s("h2")}">{html_mod.escape(para)}</h2>')
            else:
                escaped = html_mod.escape(para).replace("\n", "<br>")
                output.append(f'<p style="{self.s("p")}">{escaped}</p>')
        body = "\n".join(output)
        return f'<section style="{self.s("section")}" data-tool="wechat-mp-html-gen">\n{body}\n</section>'


class JSONToMPConverter:
    """
    Convert structured JSON to MP HTML.

    Expected JSON format:
    {
      "title": "Article Title",
      "sections": [
        {"type": "heading", "level": 2, "text": "Section Title"},
        {"type": "paragraph", "text": "Body text..."},
        {"type": "quote", "text": "A quote..."},
        {"type": "list", "ordered": false, "items": ["item1", "item2"]},
        {"type": "image", "src": "url", "alt": "desc", "caption": "optional"},
        {"type": "table", "headers": ["A","B"], "rows": [["1","2"],["3","4"]]},
        {"type": "divider"},
        {"type": "html", "content": "<p>raw html</p>"}
      ]
    }
    """

    def __init__(self, theme_name="elegant"):
        self.theme = THEMES.get(theme_name, THEMES["elegant"])

    def s(self, tag):
        return self.theme.get(tag, "")

    def convert(self, text):
        data = json.loads(text)
        output = []

        if "title" in data:
            output.append(f'<h1 style="{self.s("h1")}">{html_mod.escape(data["title"])}</h1>')

        for sec in data.get("sections", []):
            t = sec.get("type", "paragraph")

            if t == "heading":
                level = sec.get("level", 2)
                tag = f"h{min(max(level, 1), 6)}"
                output.append(f'<{tag} style="{self.s(tag)}">{html_mod.escape(sec["text"])}</{tag}>')

            elif t == "paragraph":
                text_content = html_mod.escape(sec["text"]).replace("\n", "<br>")
                output.append(f'<p style="{self.s("p")}">{text_content}</p>')

            elif t == "quote":
                text_content = html_mod.escape(sec["text"]).replace("\n", "<br>")
                output.append(f'<blockquote style="{self.s("blockquote")}">{text_content}</blockquote>')

            elif t == "list":
                tag = "ol" if sec.get("ordered") else "ul"
                items = "\n".join(
                    f'<li style="{self.s("li")}">{html_mod.escape(item)}</li>'
                    for item in sec.get("items", [])
                )
                output.append(f'<{tag} style="{self.s(tag)}">\n{items}\n</{tag}>')

            elif t == "image":
                src = html_mod.escape(sec.get("src", ""))
                alt = html_mod.escape(sec.get("alt", ""))
                output.append(f'<img src="{src}" alt="{alt}" style="{self.s("img")}">')
                if "caption" in sec:
                    output.append(f'<p style="{self.s("caption")}">{html_mod.escape(sec["caption"])}</p>')

            elif t == "table":
                lines = [f'<table style="{self.s("table")}">']
                if "headers" in sec:
                    lines.append("<tr>")
                    for h in sec["headers"]:
                        lines.append(f'<th style="{self.s("th")}">{html_mod.escape(h)}</th>')
                    lines.append("</tr>")
                for row in sec.get("rows", []):
                    lines.append("<tr>")
                    for cell in row:
                        lines.append(f'<td style="{self.s("td")}">{html_mod.escape(str(cell))}</td>')
                    lines.append("</tr>")
                lines.append("</table>")
                output.append("\n".join(lines))

            elif t == "divider":
                output.append(f'<hr style="{self.s("hr")}">')

            elif t == "html":
                output.append(sec.get("content", ""))

        body = "\n".join(output)
        return f'<section style="{self.s("section")}" data-tool="wechat-mp-html-gen">\n{body}\n</section>'


class HTMLStyleInjector:
    """Inject inline styles into existing HTML tags based on theme."""

    STYLE_MAP = {
        "p": "p", "h1": "h1", "h2": "h2", "h3": "h3", "h4": "h4",
        "h5": "h4", "h6": "h4", "blockquote": "blockquote",
        "ul": "ul", "ol": "ol", "li": "li", "table": "table",
        "th": "th", "td": "td", "a": "a", "img": "img",
        "strong": "strong", "b": "strong", "em": "em", "i": "em",
        "pre": "code_block", "code": "code_inline", "hr": "hr",
    }

    def __init__(self, theme_name="elegant"):
        self.theme = THEMES.get(theme_name, THEMES["elegant"])

    def s(self, tag):
        theme_key = self.STYLE_MAP.get(tag, "")
        return self.theme.get(theme_key, "")

    def convert(self, html_text):
        # For each known tag, inject style if not already present
        def inject_style(match):
            full = match.group(0)
            tag = match.group(1).lower()
            style = self.s(tag)
            if not style:
                return full
            if 'style="' in full or "style='" in full:
                return full  # don't override existing styles
            return full[:-1] + f' style="{style}">'

        result = re.sub(r"<(p|h[1-6]|blockquote|ul|ol|li|table|th|td|a|img|strong|b|em|i|pre|code|hr)(\s[^>]*)?>", inject_style, html_text, flags=re.I)

        section_style = self.theme.get("section", "")
        if not result.strip().startswith("<section"):
            result = f'<section style="{section_style}" data-tool="wechat-mp-html-gen">\n{result}\n</section>'
        return result


def get_theme_styles_json(theme_name="elegant"):
    """Export theme as JSON — useful for Claude to reference when composing HTML directly."""
    theme = THEMES.get(theme_name, THEMES["elegant"])
    return json.dumps(theme, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Convert content to WeChat MP HTML")
    parser.add_argument("--input", "-i", help="Input file (reads stdin if omitted)")
    parser.add_argument("--output", "-o", help="Output HTML file")
    parser.add_argument("--theme", "-t", default="elegant", help="Theme name")
    parser.add_argument("--format", "-f", choices=["markdown", "text", "json", "html", "auto"],
                        default="auto", help="Input format (default: auto-detect)")
    parser.add_argument("--list-themes", action="store_true", help="List available themes")
    parser.add_argument("--export-theme", metavar="THEME",
                        help="Export theme styles as JSON (for manual HTML composition)")
    args = parser.parse_args()

    if args.list_themes:
        print("Available themes:")
        for name in THEMES:
            print(f"  - {name}")
        sys.exit(0)

    if args.export_theme:
        name = args.export_theme if args.export_theme in THEMES else "elegant"
        print(get_theme_styles_json(name))
        sys.exit(0)

    if args.theme not in THEMES:
        print(f"Warning: theme '{args.theme}' not found, using 'elegant'", file=sys.stderr)
        args.theme = "elegant"

    if args.input:
        content = Path(args.input).read_text(encoding="utf-8")
    else:
        content = sys.stdin.read()

    fmt = args.format
    if fmt == "auto":
        fmt = detect_format(content)

    if fmt == "markdown":
        converter = MarkdownToMPConverter(args.theme)
    elif fmt == "text":
        converter = PlainTextToMPConverter(args.theme)
    elif fmt == "json":
        converter = JSONToMPConverter(args.theme)
    elif fmt == "html":
        converter = HTMLStyleInjector(args.theme)
    else:
        converter = MarkdownToMPConverter(args.theme)

    html_output = converter.convert(content)

    if args.output:
        Path(args.output).write_text(html_output, encoding="utf-8")
        print(json.dumps({"success": True, "output": args.output, "theme": args.theme, "format": fmt}))
    else:
        print(html_output)


if __name__ == "__main__":
    main()
