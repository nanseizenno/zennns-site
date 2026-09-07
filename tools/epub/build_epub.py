#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
CSS = ROOT / "tools" / "epub" / "epub.css"
DIST = ROOT / "dist"

SITE_HOSTS = {"zennns.com", "www.zennns.com"}

LANG_CONFIG = {
    "jp": {
        "book_title": "TPCA / PCN 状態遷移前制御体系｜公開技術資料集",
        "author": "全野南政 / Nansei Zenno",
        "lang": "ja-JP",
        "filename_prefix": "TPCA_PCN_JP",
    },
    "zh": {
        "book_title": "TPCA / PCN 状态迁移前置控制体系｜公开技术资料集",
        "author": "全野南政 / Nansei Zenno",
        "lang": "zh-CN",
        "filename_prefix": "TPCA_PCN_ZH",
    },
}

# EPUB 内での大まかな章順
SECTION_ORDER = {
    "": 0,
    "about": 10,
    "questions": 20,
    "concepts": 30,
    "cases": 40,
    "whitepaper": 50,
    "notes": 60,
}

FRONT_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.S)
MD_LINK_RE = re.compile(r'(!?)\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
HTML_A_RE = re.compile(r'<a\s+([^>]*?)href=["\']([^"\']+)["\']([^>]*)>', re.I)
HTML_IMG_RE = re.compile(r'<img\s+([^>]*?)src=["\']([^"\']+)["\']([^>]*)>', re.I)

# {{< diagram src="..." alt="..." >}} ... {{< /diagram >}}
PAIR_DIAGRAM_RE = re.compile(
    r'\{\{<\s*diagram\s+([^>]*)>\}\}(.*?)\{\{<\s*/diagram\s*>\}\}',
    re.I | re.S,
)
SINGLE_DIAGRAM_RE = re.compile(r'\{\{<\s*diagram\s+([^>]*)>\}\}', re.I)
ATTR_RE = re.compile(r'([\w-]+)\s*=\s*"([^"]*)"')

# Interactive shortcodes cannot work inside EPUB.
INTERACTIVE_PAIR_RE = re.compile(
    r'\{\{<\s*(pcn-animation|production-dx-animation)[^>]*>\}\}.*?\{\{<\s*/\1\s*>\}\}',
    re.I | re.S,
)
INTERACTIVE_SINGLE_RE = re.compile(
    r'\{\{<\s*(pcn-animation|production-dx-animation)[^>]*>\}\}',
    re.I,
)
ANY_SHORTCODE_RE = re.compile(r'\{\{[<%].*?[>%]\}\}', re.S)


@dataclass
class Page:
    path: Path
    meta: dict
    body: str
    title: str
    route: str
    anchor: str
    section: str
    weight: int


def read_markdown(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8-sig")
    m = FRONT_RE.match(text)
    if not m:
        return {}, text

    raw = m.group(1)
    body = text[m.end():]
    try:
        meta = yaml.safe_load(raw) or {}
    except Exception:
        meta = {}
    return meta, body


def language_file(path: Path, lang: str) -> bool:
    return path.name.endswith(f".{lang}.md")


def stripped_stem(path: Path, lang: str) -> str:
    name = path.name
    suffix = f".{lang}.md"
    return name[:-len(suffix)] if name.endswith(suffix) else path.stem


def derive_route(path: Path, lang: str, meta: dict) -> str:
    # Explicit Hugo URL takes precedence.
    explicit = meta.get("url")
    if isinstance(explicit, str) and explicit.strip():
        parsed = urlparse(explicit.strip())
        p = parsed.path or explicit.strip()
        if not p.startswith("/"):
            p = "/" + p
        return normalize_route(p)

    rel = path.relative_to(CONTENT)
    parts = list(rel.parts)
    stem = stripped_stem(path, lang)
    parts = parts[:-1]

    route_parts = [lang]
    route_parts.extend(parts)

    if stem not in {"_index", "index"}:
        slug = meta.get("slug")
        route_parts.append(str(slug).strip("/") if slug else stem)

    return normalize_route("/" + "/".join(x.strip("/") for x in route_parts if x) + "/")


def normalize_route(route: str) -> str:
    parsed = urlparse(route)
    p = parsed.path or "/"
    if not p.startswith("/"):
        p = "/" + p
    # Hugo content pages use directory-like URLs.
    if "." not in Path(p).name and not p.endswith("/"):
        p += "/"
    p = re.sub(r"/{2,}", "/", p)
    return p


def anchor_from_route(route: str) -> str:
    s = route.strip("/") or "home"
    s = re.sub(r"[^0-9A-Za-z_-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-").lower()
    return "page-" + (s or "home")


def section_name(path: Path) -> str:
    rel = path.relative_to(CONTENT)
    return rel.parts[0] if len(rel.parts) > 1 else ""


def title_from(meta: dict, path: Path, lang: str) -> str:
    title = meta.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()
    stem = stripped_stem(path, lang)
    return stem if stem not in {"_index", "index"} else path.parent.name or "Home"


def should_include(meta: dict, body: str) -> bool:
    if bool(meta.get("draft", False)):
        return False
    if meta.get("epub") is False or meta.get("epub_exclude") is True:
        return False
    # Skip placeholder language pages that only contain empty front matter.
    if len(re.sub(r"\s+", "", body)) < 10:
        return False
    return True


def discover_pages(lang: str) -> list[Page]:
    pages: list[Page] = []
    for path in CONTENT.rglob(f"*.{lang}.md"):
        meta, body = read_markdown(path)
        if not should_include(meta, body):
            continue
        route = derive_route(path, lang, meta)
        section = section_name(path)
        try:
            weight = int(meta.get("weight", 9999))
        except Exception:
            weight = 9999

        pages.append(
            Page(
                path=path,
                meta=meta,
                body=body,
                title=title_from(meta, path, lang),
                route=route,
                anchor=anchor_from_route(route),
                section=section,
                weight=weight,
            )
        )

    # Section landing page first, then Hugo weight, then path.
    def sort_key(p: Page):
        stem = stripped_stem(p.path, lang)
        is_index = 0 if stem in {"_index", "index"} else 1
        return (
            SECTION_ORDER.get(p.section, 90),
            p.section,
            is_index,
            p.weight,
            str(p.path.relative_to(CONTENT)).lower(),
        )

    pages.sort(key=sort_key)

    # If two source files unexpectedly map to the same public route,
    # prefer the one with more body content.
    dedup: dict[str, Page] = {}
    for p in pages:
        old = dedup.get(p.route)
        if old is None or len(p.body) > len(old.body):
            dedup[p.route] = p

    final = list(dedup.values())
    final.sort(key=sort_key)
    return final


def attrs(raw: str) -> dict[str, str]:
    return dict(ATTR_RE.findall(raw))


def static_resource(target: str) -> str:
    if target.startswith(("http://", "https://", "data:", "#", "mailto:", "tel:")):
        return target

    if target.startswith("/"):
        p = STATIC / target.lstrip("/")
        if p.exists():
            return p.resolve().as_posix()

    return target


def convert_shortcodes(text: str) -> str:
    def diagram_pair(m: re.Match) -> str:
        a = attrs(m.group(1))
        src = a.get("src", "")
        alt = a.get("alt", "") or a.get("title", "") or "diagram"
        caption = re.sub(r"\s+", " ", m.group(2)).strip()
        if not src:
            return caption
        img = f"![{alt}]({src})"
        return img + (f"\n\n*{caption}*" if caption else "")

    def diagram_single(m: re.Match) -> str:
        a = attrs(m.group(1))
        src = a.get("src", "")
        alt = a.get("alt", "") or a.get("title", "") or "diagram"
        return f"![{alt}]({src})" if src else ""

    text = PAIR_DIAGRAM_RE.sub(diagram_pair, text)
    text = SINGLE_DIAGRAM_RE.sub(diagram_single, text)

    # JS/animation shortcodes are removed in an offline EPUB.
    text = INTERACTIVE_PAIR_RE.sub("", text)
    text = INTERACTIVE_SINGLE_RE.sub("", text)

    # Remove any remaining Hugo shortcode tokens rather than exposing raw syntax.
    text = ANY_SHORTCODE_RE.sub("", text)
    return text


def site_route_from_target(target: str) -> str | None:
    parsed = urlparse(target)

    if parsed.scheme in {"http", "https"}:
        if parsed.netloc.lower() not in SITE_HOSTS:
            return None
        return normalize_route(parsed.path or "/")

    if target.startswith("/"):
        # Static resources are not page links.
        if target.startswith(("/images/", "/img/", "/assets/", "/uploads/", "/files/")):
            return None
        return normalize_route(target)

    return None


def rewrite_links(text: str, route_to_anchor: dict[str, str]) -> str:
    def md(m: re.Match) -> str:
        bang, label, target = m.groups()

        if bang == "!":
            return f"![{label}]({static_resource(target)})"

        route = site_route_from_target(target)
        if route and route in route_to_anchor:
            return f"[{label}](#{route_to_anchor[route]})"
        return m.group(0)

    text = MD_LINK_RE.sub(md, text)

    def html_a(m: re.Match) -> str:
        before, target, after = m.groups()
        route = site_route_from_target(target)
        if route and route in route_to_anchor:
            target = "#" + route_to_anchor[route]
        return f'<a {before}href="{html.escape(target, quote=True)}"{after}>'

    text = HTML_A_RE.sub(html_a, text)

    def html_img(m: re.Match) -> str:
        before, target, after = m.groups()
        target = static_resource(target)
        return f'<img {before}src="{html.escape(target, quote=True)}"{after}>'

    return HTML_IMG_RE.sub(html_img, text)


def build_one(lang: str) -> Path:
    cfg = LANG_CONFIG[lang]
    pages = discover_pages(lang)
    if not pages:
        raise RuntimeError(f"No .{lang}.md pages found under content/")

    route_to_anchor = {p.route: p.anchor for p in pages}
    chapters: list[str] = []

    for p in pages:
        body = convert_shortcodes(p.body)
        body = rewrite_links(body, route_to_anchor).strip()

        # Front matter title becomes the EPUB chapter title.
        chapter = f'# {p.title} {{#{p.anchor}}}\n\n{body}'
        chapters.append(chapter)

    combined = "\n\n\\newpage\n\n".join(chapters) + "\n"

    DIST.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    out = DIST / f"{cfg['filename_prefix']}_{stamp}.epub"

    with tempfile.TemporaryDirectory(prefix=f"epub_{lang}_") as td:
        md = Path(td) / f"book_{lang}.md"
        md.write_text(combined, encoding="utf-8")

        cmd = [
            "pandoc",
            str(md),
            "--from=gfm+raw_html",
            "--to=epub3",
            "--toc",
            "--toc-depth=2",
            "--metadata", f"title={cfg['book_title']}",
            "--metadata", f"author={cfg['author']}",
            "--metadata", f"lang={cfg['lang']}",
            "--css", str(CSS),
            "--resource-path", os.pathsep.join(
                [str(ROOT), str(STATIC), str(CONTENT)]
            ),
            "-o", str(out),
        ]
        subprocess.run(cmd, check=True)

    print(f"[{lang}] {len(pages)} pages -> {out}")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["jp", "zh", "both"], default="both")
    args = parser.parse_args()

    if not shutil.which("pandoc"):
        print("ERROR: pandoc not found", file=sys.stderr)
        return 1

    langs = ["jp", "zh"] if args.lang == "both" else [args.lang]
    for lang in langs:
        build_one(lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
