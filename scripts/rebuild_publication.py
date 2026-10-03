#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rebuild publication artifacts for 《至斬而止》:
1. 至斬而止_全書完稿.md (Full compiled manuscript)
2. 至斬而止_精裝閱讀版.html (Interactive HTML Reader)
"""

import os
import re

CHAPTER_METAS = [
    {
        "num": 1,
        "id": "ch01",
        "title": "第一章：硃批出閣",
        "countdown": "倒計時 63 天",
        "date": "光緒三十一年三月二十日",
        "summary": "",
    },
    {
        "num": 2,
        "id": "ch02",
        "title": "第二章：黑老鴰窩",
        "countdown": "倒計時 36 天",
        "date": "光緒三十一年四月十六日",
        "summary": "",
    },
    {
        "num": 3,
        "id": "ch03",
        "title": "第三章：招冊刮補",
        "countdown": "倒計時 28 天",
        "date": "光緒三十一年四月廿四日",
        "summary": "",
    },
    {
        "num": 4,
        "id": "ch04",
        "title": "第四章：客棧暗風",
        "countdown": "倒計時 26 天",
        "date": "光緒三十一年四月廿六日",
        "summary": "",
    },
    {
        "num": 5,
        "id": "ch05",
        "title": "第五章：茶肆暗盟",
        "countdown": "倒計時 20 天",
        "date": "光緒三十一年五月初二日",
        "summary": "",
    },
    {
        "num": 6,
        "id": "ch06",
        "title": "第六章：暗牢過堂",
        "countdown": "倒計時 14 天",
        "date": "光緒三十一年五月初八日",
        "summary": "",
    },
    {
        "num": 7,
        "id": "ch07",
        "title": "第七章：黑市摸排",
        "countdown": "倒計時 10 天",
        "date": "光緒三十一年五月十二日",
        "summary": "",
    },
    {
        "num": 8,
        "id": "ch08",
        "title": "第八章：隔絕之信",
        "countdown": "倒計時 1 天",
        "date": "光緒三十一年五月十四日至廿一日",
        "summary": "",
    },
    {
        "num": 9,
        "id": "ch09",
        "title": "第九章：至斬而止",
        "countdown": "倒計時 0 天",
        "date": "光緒三十一年五月二十二日",
        "summary": "",
    },
]

def load_chapters():
    chapters = []
    for meta in CHAPTER_METAS:
        filename = f"manuscript/chapter_{meta['num']:02d}.md"
        with open(filename, "r", encoding="utf-8") as f:
            raw_text = f.read().strip()
        
        # Strip leading # Title and ---
        lines = raw_text.splitlines()
        content_lines = []
        skip_header = True
        for line in lines:
            if skip_header:
                if line.startswith("# ") or line.strip() == "---":
                    continue
                else:
                    skip_header = False
            content_lines.append(line)
        clean_content = "\n".join(content_lines).strip()
        
        # Calculate character count (Chinese characters and alphanumeric, excluding spaces)
        chars = len([c for c in raw_text if not c.isspace()])
        
        chapters.append({
            "meta": meta,
            "filename": filename,
            "raw_text": raw_text,
            "content": clean_content,
            "chars": chars
        })
    return chapters

AFTERWORD = [
    "本書為虛構。趙連城、陸雲程、常六、胡文煥、花斑豹、烏勒春及其家人皆非歷史人物；如英、王憲臣的言行亦出於虛構。",
    "光緒三十一年三月二十日（西曆 1905 年 4 月 24 日），內閣奉上諭，准伍廷芳、沈家本所奏：「嗣後凡死罪至斬決而止」，凌遲、梟首、戮屍永遠刪除，原斬決各條改絞決，緣坐「除知情者仍治罪外，餘著悉予寬免」，刺字一併革除。第一章所引詔文即節錄自此上諭。「至斬而止」一語，亦出於原詔。",
    "史料中未見對已判決、已發遣親屬如何追溯清查的明確細則。小說據此虛構了一樁舊案無人負責的處置，不代表歷史上確有此事。",
]

def generate_markdown(chapters):
    md = []
    md.append("# 《至斬而止》\n")
    md.append("**全屍**\n")
    md.append("光緒三十一年，晚清司法歷史中篇小說\n")
    md.append("> 他用自己死後的身體，換一句女兒的下落。\n")
    md.append("---\n")
    md.append("## 目錄\n")
    for ch in chapters:
        md.append(f"{ch['meta']['num']}. {ch['meta']['title'].split('：',1)[1]}")
    md.append("\n---\n")
    for ch in chapters:
        m = ch["meta"]
        md.append(f"# {m['title']}\n")
        md.append(ch["content"])
        md.append("\n\n---\n\n")
    md.append("# 後記\n")
    for para in AFTERWORD:
        md.append(para + "\n")
    return "\n".join(md)

def markdown_to_html_body(content):
    lines = content.splitlines()
    html_parts = []
    
    in_quote = False
    quote_buf = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_quote:
                html_parts.append(f'<div class="clue-box">{"<br>".join(quote_buf)}</div>')
                in_quote = False
                quote_buf = []
            continue
        
        # Scene divider
        if stripped.startswith("### "):
            sec_name = stripped[4:].strip()
            html_parts.append(f'<div class="scene-divider"><span class="gemini-mark">❖ ❖ ❖</span></div>')
            html_parts.append(f'<h3 class="scene-number">§ {sec_name} §</h3>')
            continue
        elif stripped == "※":
            html_parts.append('<div class="scene-divider"><span class="gemini-mark">❖ ❖ ❖</span></div>')
            continue
        elif stripped == "---":
            continue
        
        # Blockquote
        if stripped.startswith(">"):
            in_quote = True
            quote_text = stripped[1:].strip()
            quote_buf.append(quote_text)
            continue
        else:
            if in_quote:
                html_parts.append(f'<div class="clue-box">{"<br>".join(quote_buf)}</div>')
                in_quote = False
                quote_buf = []
        
        # Paragraph with inline markdown formatting
        p_text = stripped
        # bold **text**
        p_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', p_text)
        # italic *text*
        p_text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', p_text)
        
        html_parts.append(f'<p>{p_text}</p>')
    
    if in_quote:
        html_parts.append(f'<div class="clue-box">{"<br>".join(quote_buf)}</div>')

    return "\n".join(html_parts)

def update_html(chapters, template_path="至斬而止_精裝閱讀版.html"):
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    total_chars = sum(ch["chars"] for ch in chapters)

    # 1. Update nav list
    nav_items = []
    for ch in chapters:
        m = ch["meta"]
        nav_items.append(f"""
            <li class="nav-item" data-target="{m['id']}">
                <a href="#{m['id']}">
                    <div class="nav-title">{m['title']}</div>
                    <div class="nav-meta">
                        <span class="meta-countdown">{m['countdown']}</span>
                        
                    </div>
                </a>
            </li>
        """)
    nav_html = "".join(nav_items)
    html = re.sub(r'<ul class="nav-list">.*?</ul>', f'<ul class="nav-list">{nav_html}</ul>', html, flags=re.DOTALL)

    # 2. Update front card info
    html = re.sub(r'\s*<p class="front-genre"[^>]*>.*?</p>', '', html)
    html = re.sub(r'<p class="front-subtitle">.*?</p>', '<p class="front-subtitle">全屍</p>\n                    <p class="front-genre" style="font-size:0.85rem;letter-spacing:0.2em;opacity:0.7;margin-top:0.6rem;">晚清司法歷史中篇小說</p>', html)
    html = re.sub(r'<div class="meta-col-val">\d[\d,]* 字.*?</div>', f'<div class="meta-col-val">全本</div>', html)
    html = re.sub(r'<div class="meta-col-val">v[\w.-]+</div>', '<div class="meta-col-val">v2.0-revised</div>', html)

    html = re.sub(r'<div class="front-quote">.*?</div>', '<div class="front-quote">他用自己死後的身體，換一句女兒的下落。</div>', html, count=1, flags=re.DOTALL)
    html = re.sub(r'<div class="meta-col-label">正文字數</div>\s*<div class="meta-col-val">[^<]*</div>', '<div class="meta-col-label">體裁</div>\n                            <div class="meta-col-val">歷史中篇</div>', html)

    # 3. Update chapter articles
    articles = []
    for ch in chapters:
        m = ch["meta"]
        body_html = markdown_to_html_body(ch["content"])
        art = f"""
            <article id="{m['id']}" class="chapter-card">
                <header class="chapter-header">
                    <div class="chapter-badge">
                        <span class="badge-seq">第 {m['num']} 卷</span>
                        <span class="badge-countdown">{m['countdown']}</span>
                        <span class="badge-date">{m['date']}</span>
                    </div>
                    <h2 class="chapter-main-heading">{m['title']}</h2>
                    
                    <div class="chapter-divider-line"></div>
                </header>
                <div class="chapter-body">
                    {body_html}
                </div>
            </article>
        """
        articles.append(art)
    
    all_articles_html = "\n".join(articles)

    # Replace articles section inside reader-container
    article_block_regex = r'(<!-- 各章節本文 -->).*?(<!-- 卷尾結語 -->)'
    html = re.sub(article_block_regex, f'\\1\n{all_articles_html}\n\\2', html, flags=re.DOTALL)

    # 4. Update epilogue section
    after_ps = "\n".join(f"                        <p>{p}</p>" for p in AFTERWORD)
    epilogue_html = f"""<!-- 卷尾結語 -->
                <section class="epilogue-card" id="epilogue">
                    <h2 class="epilogue-title">後記</h2>
                    <div class="epilogue-body">
{after_ps}
                    </div>
                    <div class="fin-seal">至斬而止</div>
                </section>
            </div>
        </main>
    </div>

    <!-- 浮動按鈕 -->"""
    html = re.sub(r'<!-- 卷尾結語 -->.*?<!-- 浮動按鈕 -->', epilogue_html, html, flags=re.DOTALL)

    return html

def main():
    chapters = load_chapters()
    total_chars = sum(ch["chars"] for ch in chapters)
    print(f"Loaded 9 chapters, total non-space characters: {total_chars:,}")
    
    # 1. Generate Markdown
    md_content = generate_markdown(chapters)
    with open("至斬而止_全書完稿.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("Updated 至斬而止_全書完稿.md successfully.")

    # 2. Update HTML Reader
    html_content = update_html(chapters)
    with open("至斬而止_精裝閱讀版.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Updated 至斬而止_精裝閱讀版.html successfully.")

if __name__ == "__main__":
    main()
