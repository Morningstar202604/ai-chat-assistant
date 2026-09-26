#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""单文件应用静态校验：AI对话助手.html

零第三方依赖（仅标准库）。校验内容：
  1. 文件存在、体积合理
  2. HTML 骨架完整（DOCTYPE / html / head / body / title / charset）
  3. 骨架标签成对闭合（div / section / ...；script、style 内容已剔除）
  4. <script> / <style> 开闭标签数量一致
  5. 若环境中有 node，则对每段内联 JS 执行语法检查（node --check）

在 CI 中由 .github/workflows/ci.yml 调用。
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "AI对话助手.html")

SKELETON_TAGS = ["div", "section", "main", "header", "footer", "aside", "form", "table"]

failures = []
total = 0


def check(ok, msg):
    global total
    total += 1
    print(("  [ok]   " if ok else "  [FAIL] ") + msg)
    if not ok:
        failures.append(msg)


def main():
    print("== 校验 %s ==" % os.path.relpath(APP, ROOT))

    if not os.path.isfile(APP):
        check(False, "文件存在")
        return 1
    size = os.path.getsize(APP)
    check(size > 50 * 1024, "文件体积 %.1f KB（单文件应用应自带全部样式与脚本）" % (size / 1024.0))

    with open(APP, encoding="utf-8") as f:
        html = f.read()

    # --- 骨架要素 ---
    low = html.lower()
    check(low.lstrip().startswith("<!doctype html>"), "以 <!DOCTYPE html> 开头")
    check(low.rstrip().endswith("</html>"), "以 </html> 收尾")
    for token, label in [("<html", "<html> 根元素"), ("<head>", "<head>"), ("<body", "<body>"),
                         ("<title>", "<title>"), ("charset", "charset 声明")]:
        check(token in low, "包含 %s" % label)
    check('lang="zh-cn"' in low, 'html lang="zh-CN"')

    # --- script / style 开闭配对 ---
    for tag in ("script", "style"):
        opens = len(re.findall(r"<%s\b" % tag, html, re.I))
        closes = len(re.findall(r"</%s>" % tag, html, re.I))
        check(opens == closes, "<%s> 开闭配对（%d/%d）" % (tag, opens, closes))

    # --- 剔除 script/style 内容后的骨架标签配对 ---
    skeleton = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S | re.I)
    skeleton = re.sub(r"<style\b[^>]*>.*?</style>", "", skeleton, flags=re.S | re.I)
    for tag in SKELETON_TAGS:
        opens = len(re.findall(r"<%s\b" % tag, skeleton, re.I))
        closes = len(re.findall(r"</%s>" % tag, skeleton, re.I))
        check(opens == closes, "<%s> 骨架配对（%d/%d）" % (tag, opens, closes))

    # --- 内联 JS 语法检查（可选：依赖 node） ---
    scripts = re.findall(r"<script\b[^>]*>(.*?)</script>", html, flags=re.S | re.I)
    node = shutil.which("node")
    if not node:
        print("  [skip] 未找到 node，跳过内联 JS 语法检查")
    else:
        tmp = tempfile.mkdtemp()
        for i, body in enumerate(scripts, 1):
            path = os.path.join(tmp, "inline_%d.js" % i)
            with open(path, "w", encoding="utf-8") as f:
                f.write(body)
            proc = subprocess.run([node, "--check", path], capture_output=True, text=True)
            detail = "" if proc.returncode == 0 else "\n" + proc.stderr.strip()[:500]
            check(proc.returncode == 0,
                  "内联脚本 #%d 语法（%d 行）%s" % (i, body.count("\n") + 1, detail))

    print("\n%s：共 %d 项检查，%d 项失败" % ("通过" if not failures else "未通过", total, len(failures)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())