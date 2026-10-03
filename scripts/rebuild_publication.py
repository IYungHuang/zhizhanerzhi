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
        "summary": "刑部大堂沈家本力推新政，硃批免凌遲改斬決",
    },
    {
        "num": 2,
        "id": "ch02",
        "title": "第二章：黑老鴰窩",
        "countdown": "倒計時 36 天",
        "date": "光緒三十一年四月十六日",
        "summary": "刑部提牢南監，常六開價，趙連城以全屍換信號",
    },
    {
        "num": 3,
        "id": "ch03",
        "title": "第三章：招冊刮補",
        "countdown": "倒計時 28 天",
        "date": "光緒三十一年四月廿四日",
        "summary": "直隸清吏司刮補賊光，扣下李茂無印浮簽存根",
    },
    {
        "num": 4,
        "id": "ch04",
        "title": "第四章：客棧暗風",
        "countdown": "倒計時 26 天",
        "date": "光緒三十一年四月廿六日",
        "summary": "騾馬市截獲李茂，起獲咬痕斷簪，驚悉魏氏死訊",
    },
    {
        "num": 5,
        "id": "ch05",
        "title": "第五章：茶肆暗盟",
        "countdown": "倒計時 20 天",
        "date": "光緒三十一年五月初二日",
        "summary": "如英摔文焊死公門，竹簾對談沈家本兩難，茶棚結盟四十五兩籌資",
    },
    {
        "num": 6,
        "id": "ch06",
        "title": "第六章：暗牢過堂",
        "countdown": "倒計時 14 天",
        "date": "光緒三十一年五月初八日",
        "summary": "陸雲程夜探死牢，趙連城悔認濫殺栓子罪責，交代草垛藏女與長命鎖暗記",
    },
    {
        "num": 7,
        "id": "ch07",
        "title": "第七章：黑市摸排",
        "countdown": "倒計時 10 天",
        "date": "光緒三十一年五月十二日",
        "summary": "律例降維硬撬花斑豹暗帳，鎖定喜兒深陷良鄉八旗肅王府私莊",
    },
    {
        "num": 8,
        "id": "ch08",
        "title": "第八章：隔絕之信",
        "countdown": "倒計時 1 天",
        "date": "光緒三十一年五月廿一日",
        "summary": "菜市口黃沙鋪道，死牢歸還咬痕斷簪，知曉絕境立下全屍死誓",
    },
    {
        "num": 9,
        "id": "ch09",
        "title": "第九章：至斬而止",
        "countdown": "倒計時 0 天",
        "date": "光緒三十一年五月二十二日",
        "summary": "菜市口第一起免凌遲改斬決刑場，握簪伏誅，沈家本滴墨合卷，陸雲程焚簽碾灰自保妥協",
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

def generate_markdown(chapters):
    total_chars = sum(ch["chars"] for ch in chapters)
    
    md = []
    md.append("# 《至斬而止》\n")
    md.append("**副標題**：光緒三十一年晚清司法大變局歷史小說\n")
    md.append("> **核心主題**：\n> 「一紙廢除凌遲與緣坐的聖旨，保住了一個殺人兇手的完整皮囊；卻救不回兩個月前已依舊法賣入八旗私莊的九歲女兒。」\n>\n> 新政律條在朝堂之上熠熠生輝，而小民血淚在菜市口曬乾的黃沙間無聲乾涸。至斬而止。\n")
    md.append("---\n")
    md.append("## 卷首目錄與題解\n")
    md.append(f"- **作品體量**：全書九章完稿，共 {total_chars:,} 字（精編定本）")
    md.append("- **時代背景**：清光緒三十一年（西元1905年），沈家本主持修律、廢除凌遲與梟首之歷史轉折期")
    md.append("- **核心物證**：【TH-05 亡妻咬痕斷頭粗銀簪】、【TH-06 喜兒三項人身暗記（左肩月形青胎、耳後紅痣、底鏨「連」字長命鎖）】、【李茂過境浮簽存根】\n")
    md.append("### 目錄\n")
    for ch in chapters:
        m = ch["meta"]
        md.append(f"{m['num']}. **{m['title']}**（{m['countdown']} · {m['date']}）— *{m['summary']}*（約 {ch['chars']:,} 字）")
    md.append("\n---\n")
    md.append("## 主要人物譜\n")
    md.append("- **陸雲程**：刑部直隸清吏司六品主事，紹興律例師爺出身，性情冷峻沉著，恪守律法程序，內心深處橫亙良知天平。")
    md.append("- **趙連城**：直隸薊州鐵匠，因官紳強佔田界打死老父狂暴復仇連斃三人（含門房無辜小廝栓子）；身負重罪深陷刑部南監，以全屍換妻女音訊，立下冷酷死誓。")
    md.append("- **常六**：刑部提牢廳南監二十五年差撥老獄吏，精通黑市規費與「縫頭」行當，看透世態炎涼，在殘酷泥沼中暗存守信道義。")
    md.append("- **沈家本**：字子惇，大清修訂法律大臣、刑部右侍郎，近代法制變革領航者。身處保守派御史疆臣圍攻與各國治外法權的政治懸崖上，以宏觀變法為念，承擔歷史無奈。")
    md.append("- **如英**：刑部滿洲正紅旗侍郎，旗籍實權官僚，深諳官場平衡與火漆封卷之道，力阻公文外流。")
    md.append("- **王憲臣**：刑部直隸清吏司掌印郎中，老成持重，熟稔部務，力求文牘周全以避事端。")
    md.append("- **胡文煥**：直隸司老經承，如蠹魚般盤踞公事房三十年，暗中窺伺同僚把柄以求自保。")
    md.append("- **花斑豹**：天橋南下窪私牙總瓢把子，專門倒賣無籍人口、黑帳深鎖良鄉莊田。")
    md.append("- **魏氏**：趙連城亡妻，通州官道客棧絞腸痧暴斃前，拼死將喜兒塞入草垛，囑其咬死改稱逃荒孤兒，咬斷銀簪絕其呼號。")
    md.append("- **喜兒（大丫）**：趙連城九歲女兒，被私賣入良鄉三十里八旗肅王府私莊，改名大丫；以碎瓦割襖密縫長命鎖，誓死守護身分。")
    md.append("\n---\n\n")

    for ch in chapters:
        m = ch["meta"]
        md.append(f"# {m['title']}\n")
        md.append(f"> **【時間錨定】**：{m['date']}（{m['countdown']}）｜ **【本章主旨】**：{m['summary']}\n")
        md.append("---\n")
        md.append(ch["content"])
        md.append("\n\n---\n\n")
    
    # Afterword
    md.append("# 後記：至斬而止的歷史沉思\n")
    md.append("光緒三十一年三月二十日（西元1905年4月24日），清廷頒布由修訂法律大臣沈家本、伍廷芳聯名上奏之《刪除律例內重刑折》上諭，正式廢除凌遲、梟首、戮屍，重罪一律改為斬決與絞決；同時永久廢止連坐、緣坐及籍沒家產（除謀反大逆知情者仍治罪外），停罷刺字。\n")
    md.append("這是一場震古爍今的近代法律文明之巨變。\n")
    md.append("沈家本字子惇，面對張之洞、勞乃宣等封疆重臣與守舊派御史的洶湧圍攻，面對東交民巷列強以領事裁判權相威脅的內外交困，在晚清風雨飄搖之際，以宏大政治擔當為近代法治奠基。然而，在皇權特權與王府莊田密布的晚清泥沼中，新法的微光照亮了朝堂典章，卻照不穿八旗莊田的生土高牆。趙連城在菜市口伏誅，換得一具完整的皮囊；而他九歲的女兒喜兒，依舊深鎖在良鄉三十里外的鐵幕莊田裡。\n")
    md.append("《至斬而止》以「趙連城案」為虛構稜鏡，展現制度更迭之際宏觀法制文明推進與微觀個體命運間的深刻張力，非歷史實案之紀實。小民血淚與歷史車輪，至斬而止。\n")

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
                        <span class="meta-words">{ch['chars']:,} 字</span>
                    </div>
                </a>
            </li>
        """)
    nav_html = "".join(nav_items)
    html = re.sub(r'<ul class="nav-list">.*?</ul>', f'<ul class="nav-list">{nav_html}</ul>', html, flags=re.DOTALL)

    # 2. Update front card info
    html = re.sub(r'<p class="front-subtitle">.*?</p>', f'<p class="front-subtitle">晚清司法大變局歷史小說 · {total_chars:,}字典藏全本</p>', html)
    html = re.sub(r'<div class="meta-col-val">\d[\d,]* 字.*?</div>', f'<div class="meta-col-val">{total_chars:,} 字（精鍊典藏）</div>', html)
    html = re.sub(r'<div class="meta-col-val">v[\w.-]+</div>', '<div class="meta-col-val">v1.2-literary-masterpiece</div>', html)

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
                    <p class="chapter-summary">{m['summary']}</p>
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
    epilogue_html = """<!-- 卷尾結語 -->
                <section class="epilogue-card" id="epilogue">
                    <h2 class="epilogue-title">後記：至斬而止的歷史沉思</h2>
                    <div class="epilogue-body">
                        <p>光緒三十一年三月二十日（西元1905年4月24日），清廷頒布由修訂法律大臣沈家本、伍廷芳聯名上奏之《刪除律例內重刑折》上諭，正式廢除凌遲、梟首、戮屍，重罪一律改為斬決與絞決；同時永久廢止連坐、緣坐及籍沒家產（除謀反大逆知情者仍照舊例治罪外），停罷刺字。</p>
                        <p>這是一場震古爍今的近代法律文明之巨變。</p>
                        <p>沈家本字子惇，面對張之洞、勞乃宣等封疆重臣與守舊派御史的洶湧圍攻，面對東交民巷列強以領事裁判權相威脅的內外交困，在晚清風雨飄搖之際，以宏大政治擔當為近代法治奠基。然而，在皇權特權與王府莊田密布的晚清泥沼中，新法的微光照亮了朝堂典章，卻照不穿八旗莊田的生土高牆。趙連城在菜市口伏誅，換得一具完整的皮囊；而他九歲的女兒喜兒，依舊深鎖在良鄉三十里外的鐵幕莊田裡。</p>
                        <p>《至斬而止》以「趙連城案」為虛構稜鏡，展現制度更迭之際宏觀法制文明推進與微觀個體命運間的深刻張力，非歷史實案之紀實。小民血淚與歷史車輪，至斬而止。</p>
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
