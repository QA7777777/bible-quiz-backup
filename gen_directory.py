#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a link-only directory page (titles -> ORIGINAL site URLs).
No quiz content is stored or served here - navigation only."""
import html
import json
import os

WORKDIR = "/home/ubuntu/quizmig"
OUT = os.path.join(WORKDIR, "directory-only")
DATA = os.path.join(WORKDIR, "quizzes.json")
SOURCE = "http://sq.zhsw777.com/plugin.php?id=hejin_wxyx&model=test&tid="

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#F4F5F9;color:#3B4A68;line-height:1.75;
font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei","Noto Sans SC",sans-serif}
a{color:#5E72E4;text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:820px;margin:0 auto;padding:18px 16px 60px}
.banner{background:linear-gradient(135deg,#5E72E4,#8965E0);border-radius:12px;color:#fff;
padding:32px 30px;margin:20px 0 10px;box-shadow:0 4px 6px rgba(50,50,93,.11),0 1px 3px rgba(0,0,0,.08)}
.banner h1{font-size:28px;font-weight:900;margin:0 0 6px;color:#fff}
.banner p{margin:0;opacity:.92;font-size:15px}
.note{background:#FFF8E6;border:1px solid #F0E0A0;border-radius:10px;padding:12px 16px;
font-size:14px;color:#7A6A2F;margin:14px 0}
.sec{font-size:22px;font-weight:700;margin:26px 0 8px;color:#32325D}
details.book{border:1px solid #E3E6EA;border-radius:10px;margin:8px 0;background:#fff}
details.book summary{padding:12px 16px;cursor:pointer;font-size:16px;font-weight:600;list-style:none}
details.book summary::before{content:'\\25B8 ';color:#aaa}
details.book[open] summary::before{content:'\\25BE '}
details.book ul{margin:0;padding:4px 16px 12px 34px}
details.book li{margin:5px 0}
.foot{color:#8B94A8;font-size:13px;margin-top:30px;text-align:center}
"""


def esc(s):
    return html.escape(s or "", quote=True)


def main():
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)

    counts = {}
    for q in data:
        key = (q["section"], q["book"])
        counts[key] = counts.get(key, 0) + 1

    parts = ["""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>圣经测题目录 · 导航</title>
<style>""" + CSS + """</style>
</head>
<body>
<div class="wrap">
<div class="banner"><h1>圣经测题目录</h1><p>导航页 · 点击条目跳转到原站阅读作答</p></div>
<div class="note">本页仅为目录导航，所有测题内容均保存在原站。点击任意条目将跳转到原站对应页面；如原站无法访问，则条目暂不可用。</div>"""]

    cur_sec = None
    cur_book = None
    for q in data:
        if q["section"] != cur_sec:
            parts.append(f'<div class="sec">{esc(q["section"])}</div>')
            cur_sec = q["section"]
            cur_book = None
        if (q["section"], q["book"]) != cur_book:
            if cur_book is not None:
                parts.append("</ul></details>")
            n = counts[(q["section"], q["book"])]
            parts.append(f'<details class="book"><summary>{esc(q["book"])}（{n}）</summary><ul>')
            cur_book = (q["section"], q["book"])
        url = SOURCE + str(q["tid"])
        parts.append(f'<li><a href="{esc(url)}" target="_blank" rel="noopener">{esc(q["title"])}</a></li>')
    parts.append("</ul></details>")
    parts.append("""<div class="foot">本页仅为目录导航，不含任何测题内容 · 内容版权归原作者所有，请访问原站支持</div>
</div>
</body>
</html>""")

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print("link-only directory -> %s/index.html (%d entries)" % (OUT, len(data)))


if __name__ == "__main__":
    main()
