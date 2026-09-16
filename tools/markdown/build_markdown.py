#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

# Allow importing the existing EPUB builder.
sys.path.insert(0, str(ROOT))

from tools.epub.build_epub import (  # noqa: E402
    LANG_CONFIG,
    convert_shortcodes,
    discover_pages,
)

DIST = ROOT / "dist"
SITE_BASE = "https://zennns.com"


# ---------------------------------------------------------
# Public bundle settings
# ---------------------------------------------------------

SECTION_TITLES = {
    "zh": {
        "": "首页",
        "about": "关于",
        "questions": "工程问题",
        "concepts": "核心概念",
        "cases": "应用案例",
        "whitepaper": "白皮书",
        "notes": "技术札记",
    },
    "jp": {
        "": "ホーム",
        "about": "About",
        "questions": "エンジニアリング課題",
        "concepts": "基本概念",
        "cases": "応用事例",
        "whitepaper": "ホワイトペーパー",
        "notes": "技術ノート",
    },
}

INTRO = {
    "zh": (
        "本文件汇总 zennns.com 当前公开的中文技术内容，"
        "用于离线阅读、技术交流与资料保存。\n\n"
        "部分内部工程实现、具体参数及未公开技术内容不包含在本文件中。"
        "各文章的最新版本以网站公开页面为准。"
    ),
    "jp": (
        "本ファイルは、zennns.com で現在公開している日本語の技術コンテンツを、"
        "オフラインでの閲覧、技術交流および資料保存を目的としてまとめたものです。\n\n"
        "内部の実装詳細、具体的なパラメータおよび未公開の技術内容は含みません。"
        "各記事の最新版は公開サイトを参照してください。"
    ),
}


# ---------------------------------------------------------
# Markdown processing
# ---------------------------------------------------------

MD_LINK_RE = re.compile(
    r'(!?)\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)'
)

HTML_SRC_RE = re.compile(
    r'(<img\s+[^>]*?src=["\'])(/[^"\']+)(["\'])',
    re.I,
)

FIRST_H1_RE = re.compile(
    r"\A\s*#\s+(.+?)\s*(?:\n+|\Z)"
)


def absolute_site_links(text: str) -> str:
    """
    Convert root-relative website links and image paths to absolute
    zennns.com URLs so that the generated Markdown also works offline
    or outside the Hugo repository.
    """

    def md_replace(m: re.Match) -> str:
        bang, label, target = m.groups()

        if target.startswith("/"):
            target = SITE_BASE + target

        return f"{bang}[{label}]({target})"

    text = MD_LINK_RE.sub(md_replace, text)

    text = HTML_SRC_RE.sub(
        lambda m: (
            m.group(1)
            + SITE_BASE
            + m.group(2)
            + m.group(3)
        ),
        text,
    )

    return text


def strip_duplicate_h1(body: str, title: str) -> str:
    """
    If the source article already begins with the same H1 as its
    front-matter title, remove it because the bundle generates its
    own article heading.
    """

    m = FIRST_H1_RE.match(body)

    if not m:
        return body

    heading = re.sub(r"\s+", " ", m.group(1)).strip()
    clean_title = re.sub(r"\s+", " ", title).strip()

    if heading == clean_title:
        return body[m.end():].lstrip()

    return body


def page_source_url(route: str) -> str:
    return SITE_BASE + route


# ---------------------------------------------------------
# Build
# ---------------------------------------------------------

def build_one(lang: str) -> Path:

    cfg = LANG_CONFIG[lang]

    # Reuse exactly the same discovery / draft filtering /
    # section ordering logic as Build EPUB.
    pages = discover_pages(lang)

    if not pages:
        raise RuntimeError(
            f"No .{lang}.md pages found under content/"
        )

    today = date.today().isoformat()

    lines: list[str] = [
        "---",
        f'title: "{cfg["book_title"]}"',
        f'author: "{cfg["author"]}"',
        f'language: "{lang}"',
        f'generated: "{today}"',
        'site: "https://zennns.com"',
        "---",
        "",
        f'# {cfg["book_title"]}',
        "",
        INTRO[lang],
        "",
        "---",
        "",
    ]

    current_section: str | None = None
    section_titles = SECTION_TITLES[lang]

    for page in pages:

        # ---------------------------------------------
        # Section heading
        # ---------------------------------------------

        if page.section != current_section:

            current_section = page.section

            section_title = section_titles.get(
                page.section,
                page.section or "Contents",
            )

            lines.extend(
                [
                    f"# {section_title}",
                    "",
                ]
            )

        # ---------------------------------------------
        # Article body
        # ---------------------------------------------

        body = convert_shortcodes(page.body)

        body = strip_duplicate_h1(
            body,
            page.title,
        )

        body = absolute_site_links(body).strip()

        lines.extend(
            [
                f"## {page.title}",
                "",
                f"> Source: {page_source_url(page.route)}",
                "",
                body,
                "",
                "---",
                "",
            ]
        )

    # -------------------------------------------------
    # Output
    # -------------------------------------------------

    DIST.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = DIST / (
        f"{cfg['filename_prefix']}"
        f"_Public_Contents_"
        f"{today}.md"
    )

    output.write_text(
        "\n".join(lines).rstrip() + "\n",
        encoding="utf-8",
    )

    print(
        f"[{lang}] "
        f"{len(pages)} pages -> "
        f"{output}"
    )

    return output


# ---------------------------------------------------------
# CLI
# ---------------------------------------------------------

def main() -> int:

    parser = argparse.ArgumentParser(
        description=(
            "Build public Markdown bundles "
            "from Hugo content"
        )
    )

    parser.add_argument(
        "--lang",
        choices=[
            "jp",
            "zh",
            "both",
        ],
        default="both",
    )

    args = parser.parse_args()

    langs = (
        ["jp", "zh"]
        if args.lang == "both"
        else [args.lang]
    )

    for lang in langs:
        build_one(lang)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
