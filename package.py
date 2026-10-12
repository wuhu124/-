# -*- coding: utf-8 -*-
"""
打包：把版本 A（清透玻璃版）与版本 B（模拟器版）合成一个交付 zip
=================================================================
运行顺序：python build.py  →  python build_v2.py  →  python package.py
"""

import os
import sys
import zipfile

from build import EXPS, WARN_JS

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
A_DIR = "版本A-清透玻璃版"
B_DIR = "版本B-模拟器版"
PKG = "化学实验数据处理系统_网页版_v2.0"
SOURCE_PKG = "实验计算_源码与可部署网页"


def log(text):
    sys.stdout.write(text + "\n")


README = """化学实验数据处理系统（网页版）
================================================

★ 最快上手（⚠ 必须先解压，不要在压缩包里直接双击）
------------------------------------------------
  第 1 步：右键这个压缩包  →  「全部解压 / Extract All」
  第 2 步：进入解压出来的文件夹
  第 3 步：双击最外层的「index.html」

  它会列出全部 5 个实验和两套界面，点哪一项就打开哪一项。
  不需要装任何软件、不需要联网、不需要启动服务器。

  ❌ 常见错误：在压缩包里直接双击 html。
     系统只会把「这一个文件」解到临时目录，其他文件没解出来，
     点页面里的链接就会报 ERR_FILE_NOT_FOUND（找不到文件）。

  💡 如果希望对方「点开就能用、不用解压」：
     那就单独发 all-in-one.html —— 它是单文件版（5 个实验都在里面），
     放在哪里、怎么打开都不会出错。

一、这个包里有两套界面，任选一套使用（也可以都留着）
------------------------------------------------
  版本A-清透玻璃版/
      浅色磨砂玻璃风格。视觉最"高级"，在超星的白底课程页里最融合。
  版本B-模拟器版/
      深蓝顶栏 + 参数滑块 + KPI 指标卡 + 标签页图表，
      参考 NovaSolver 模拟器页面版式，交互感更强。

  ★ 两套的计算逻辑完全相同，同一组数据算出的结果一字不差。
  ★ 两套都各有 5 个单实验页 + 1 个 all-in-one 合并版。
  ★ 向学生发布时，建议只用其中一套，避免混淆。

二、文件清单（以版本A为例，版本B结构相同）
------------------------------------------------
  index.html                    入口目录页
  exp1-mg-molar-mass.html       表 3-1  量气法测定镁的摩尔质量
  exp2-acetic-ka.html           表 3-2  pH 法测乙酸电离常数
  exp3-baso4-ksp.html           表 3-3  电导法测 BaSO4 溶度积
  exp4-kinetics-ea.html         表 3-4/3-5  反应速率·级数与活化能
  exp5-complex-k.html           表 3-5  配合物组成与稳定常数
  all-in-one.html               单文件合并版（一个页面切换 5 个实验）

三、技术特点（重要）
------------------------------------------------
  1. 全部为零依赖的单文件网页：CSS / JavaScript 全部内联，
     不引用任何 CDN、不需要装库、不需要服务器端程序、不需要联网。
  2. 计算全部在浏览器本地完成，学生数据不上传。
  3. 每个 html 都可以双击直接打开，也可以放到任意静态服务器。

四、线上部署与课堂使用
------------------------------------------------
  本系统是纯静态网页，计算在学生手机浏览器本地完成，不需要后端服务，
  学生输入的数据不会上传。

【GitHub Pages 自动部署】
  1. 将完整源码放入公开 GitHub 仓库。
  2. 在仓库 Settings → Pages 中，将部署来源设置为 GitHub Actions。
  3. 将源码推送到 main 分支；Actions 会自动生成并发布首页、版本 A
     和版本 B。若仓库默认分支不是 main，请同步修改工作流分支设置。
  4. 等待 Actions 部署成功，在 Pages 设置或部署任务中复制 HTTPS 首页链接，
     再把首页链接或具体实验链接添加到学习通。学生点击链接即可使用。

【手动静态托管】
  也可把压缩包解压，将最外层 index.html 与「版本A-清透玻璃版」、
  「版本B-模拟器版」两个完整文件夹一起上传到支持 HTTPS 的静态空间。
  不要只上传单个 HTML 文件。部署后，把首页或实验页 HTTPS 链接放进学习通。

  如果课程平台支持 iframe，再使用「嵌入代码.txt」里的代码；如果平台
  只允许添加链接，直接放 HTTPS 页面链接即可。

五、iframe 嵌入注意事项
------------------------------------------------
  1. 地址必须是 https（http 地址多数课程平台会拦截）。
  2. 服务器不要设置 X-Frame-Options: DENY。
  3. 建议高度：版本A 用 700，版本B 用 760；宽度写 100%。
  4. 网址后面加 ?embed=1 进入「嵌入模式」：
     隐藏页脚/顶栏、收紧留白，一屏放得下。

六、学生怎么用 / 怎么交作业
------------------------------------------------
  版本A：填数字 → 点「计算」→ 点「复制结果」或「下载 CSV」。
  版本B：拖滑块即时出结果 → 点「复制结果」或「下载 CSV」。

  ⚠ file:// 直接打开时浏览器不给剪贴板权限，此时请用
    「显示纯文本」按钮，把结果文本手动复制走。
    挂到 http/https 上则一切正常。

七、浏览器要求
------------------------------------------------
  Chrome / Edge 76+ ，Firefox 103+ ，Safari 9+ 。
  老浏览器上版本A 的毛玻璃会自动降级为半透明色块，功能不受影响。

八、本地预览
------------------------------------------------
  双击「本地预览.bat」，再在浏览器打开：
    http://localhost:8765/版本A-清透玻璃版/index.html
    http://localhost:8765/版本B-模拟器版/index.html
  （需要电脑上已装 Python 3；不需要安装任何第三方包）

================================================
"""

SOURCE_README = """实验计算：源码与可部署网页
====================================

【最简单：直接部署网页】
  1. 打开「可直接上传的网站」文件夹。
  2. 把该文件夹里的 index.html、版本A-清透玻璃版、
     版本B-模拟器版，一起上传到支持 HTTPS 的静态网站空间。
  3. 发布后打开 index.html 对应的 HTTPS 链接测试，再把链接发给学生。
  不要只上传 index.html；它需要同目录下的两个版本文件夹。

【GitHub Pages 自动部署】
  「源码」文件夹内包含生成脚本和 .github/workflows/deploy-pages.yml。
  将「源码」文件夹内的所有内容放进一个公开 GitHub 仓库，仓库的
  Settings → Pages → Build and deployment → Source 选择 GitHub Actions，
  向 main 分支推送后会自动构建并部署。Actions 成功后，从 Pages 设置
  获取 HTTPS 链接。

【源码内容】
  build.py / build_v2.py：生成两套实验网页。
  package.py：生成网页包与本交接包。
  stage_pages.py：为 Pages 准备文件并检查站内链接。
  tests/：站点暂存与链接检查测试。
  .github/workflows/：自动部署配置。

全部计算在学生自己的浏览器中进行，不需要后端，也不会上传学生输入数据。
"""

PREVIEW_BAT = """@echo off
cd /d "%~dp0"
echo.
echo   化学实验数据处理系统 - 本地预览
echo.
echo   总入口          : http://localhost:8765/index.html
echo   版本 A（清透玻璃版）: http://localhost:8765/版本A-清透玻璃版/index.html
echo   版本 B（模拟器版）  : http://localhost:8765/版本B-模拟器版/index.html
echo.
echo   关闭本窗口即停止服务。
echo.
python -m http.server 8765
pause
"""


def embed_snippets():
    lines = ["iframe 嵌入代码（把 https://你的域名/chemlab 换成你的实际网址）",
             "=" * 66, "",
             "■ 版本A（清透玻璃版）", "-" * 66]
    for e in EXPS:
        lines.append("【%s  %s】" % (e["tag"], e["name"]))
        lines.append('<iframe src="https://你的域名/chemlab/%s/%s.html?embed=1"\n'
                     '        width="100%%" height="700"\n'
                     '        style="border:none;border-radius:12px" loading="lazy"\n'
                     '        title="%s"></iframe>' % (A_DIR, e["file"], e["name"]))
        lines.append("")
    lines.append("【合并版（5 个实验合一）】")
    lines.append('<iframe src="https://你的域名/chemlab/%s/all-in-one.html?embed=1"\n'
                 '        width="100%%" height="800"\n'
                 '        style="border:none;border-radius:12px" loading="lazy"\n'
                 '        title="化学实验数据处理"></iframe>' % A_DIR)

    lines += ["", "", "■ 版本B（模拟器版）", "-" * 66]
    for e in EXPS:
        lines.append("【%s  %s】" % (e["tag"], e["name"]))
        lines.append('<iframe src="https://你的域名/chemlab/%s/%s.html?embed=1"\n'
                     '        width="100%%" height="760"\n'
                     '        style="border:none;border-radius:12px" loading="lazy"\n'
                     '        title="%s"></iframe>' % (B_DIR, e["file"], e["name"]))
        lines.append("")
    lines.append("【合并版（5 个实验合一）】")
    lines.append('<iframe src="https://你的域名/chemlab/%s/all-in-one.html?embed=1"\n'
                 '        width="100%%" height="820"\n'
                 '        style="border:none;border-radius:12px" loading="lazy"\n'
                 '        title="化学实验数据模拟器"></iframe>' % B_DIR)
    return "\n".join(lines)


MASTER = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>化学实验数据处理系统 · 网页版</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:"Microsoft YaHei UI","Microsoft YaHei","PingFang SC",system-ui,
       -apple-system,"Segoe UI",sans-serif;background:#f1f5f9;color:#0f172a;
       padding:34px 20px 50px;-webkit-font-smoothing:antialiased}
  .wrap{max-width:1060px;margin:0 auto}
  .top{background:linear-gradient(118deg,#132a63,#1d4ed8 58%,#0891b2);color:#fff;
       border-radius:18px;padding:30px 34px;box-shadow:0 12px 34px rgba(15,23,42,.18)}
  .top .pill{display:inline-block;font-size:11px;font-weight:800;color:#0c2f6b;
             background:#bfdbfe;border-radius:999px;padding:4px 13px;margin-bottom:14px}
  .top h1{font-size:27px;font-weight:800;letter-spacing:.3px}
  .top p{margin-top:10px;font-size:13.5px;line-height:1.8;color:#dbeafe;max-width:780px}
  .tip{margin-top:16px;font-size:12.5px;line-height:1.8;color:#e0f2fe;
       background:rgba(255,255,255,.12);border-radius:10px;padding:11px 14px}
  .cols{display:grid;grid-template-columns:1fr;gap:18px;margin-top:20px}
  @media (min-width:820px){.cols{grid-template-columns:1fr 1fr}}
  .card{background:#fff;border:1px solid #e2e8f0;border-radius:16px;padding:20px 22px;
        box-shadow:0 1px 3px rgba(15,23,42,.05)}
  .card h2{font-size:15px;font-weight:800;margin-bottom:4px}
  .card .sub{font-size:11.5px;color:#94a3b8;line-height:1.7;margin-bottom:15px}
  .row{display:flex;align-items:center;gap:11px;text-decoration:none;color:inherit;
       padding:10px 12px;border-radius:10px;border:1px solid transparent;transition:all .14s}
  .row:hover{background:#f8fafc;border-color:#dbeafe;transform:translateX(3px)}
  .row .t{flex:none;font-size:10.5px;font-weight:800;color:#0891b2;
          background:#ecfeff;border-radius:6px;padding:3px 8px;min-width:64px;text-align:center}
  .row .n{font-size:13.5px;font-weight:600}
  .row.all .t{color:#1d4ed8;background:#eff6ff}
  .row.all .n{color:#1d4ed8;font-weight:800}
  .foot{margin-top:22px;font-size:12px;color:#94a3b8;line-height:1.9}
  code{font-family:Consolas,monospace;background:#f1f5f9;border-radius:5px;
       padding:1px 6px;font-size:12px;color:#0f172a}
</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <span class="pill">网页版 · 零依赖</span>
    <h1>化学实验数据处理系统</h1>
    <p>5 个实验的数据处理工具，每页都可以单独打开、单独嵌入课程平台。
       所有计算都在浏览器本地完成，不联网、不上传数据。</p>
    <div class="tip">👆 直接点下面的任意一项即可打开（无需安装任何软件、无需启动服务器）</div>
  </div>

  <div class="cols">
    <section class="card">
      <h2>版本 A · 清透玻璃版</h2>
      <p class="sub">浅色磨砂玻璃风格，在课程平台的白底页面里最融合</p>
      @@A@@
    </section>
    <section class="card">
      <h2>版本 B · 模拟器版</h2>
      <p class="sub">深蓝顶栏 + 参数滑块 + 指标卡，拖动即时出结果</p>
      @@B@@
    </section>
  </div>

  <p class="foot">
    · 两版计算逻辑完全相同，同一组数据结果一字不差，向学生发布时建议只用其中一版。<br>
    · 要嵌入课程平台时：先看 <code>部署说明.txt</code>，iframe 代码在 <code>嵌入代码.txt</code> 里直接复制。<br>
    · 想在本机用 http:// 方式预览（更接近线上环境）：双击 <code>本地预览.bat</code>。
  </p>
</div>
@@WARN@@
</body>
</html>
"""


def master_index():
    def rows(folder):
        out = []
        for e in EXPS:
            out.append('<a class="row" href="%s/%s.html">'
                       '<span class="t">%s</span><span class="n">%s</span></a>'
                       % (folder, e["file"], e["tag"], e["name"]))
        out.append('<a class="row all" href="%s/all-in-one.html">'
                   '<span class="t">合并版</span>'
                   '<span class="n">5 个实验合一 · 一个页面切换</span></a>' % folder)
        return "\n      ".join(out)

    return (MASTER
            .replace("@@A@@", rows(A_DIR))
            .replace("@@B@@", rows(B_DIR))
            .replace("@@WARN@@", WARN_JS))


def main():
    for name, d in (("版本A", "A"), ("版本B", "B")):
        p = os.path.join(BUILD, d)
        if not os.path.isdir(p) or not os.listdir(p):
            log("缺少 build/%s，请先运行 build.py / build_v2.py" % d)
            return

    with open(os.path.join(BUILD, "index.html"), "w", encoding="utf-8") as f:
        f.write(master_index())
    with open(os.path.join(BUILD, "部署说明.txt"), "w", encoding="utf-8") as f:
        f.write(README)
    with open(os.path.join(BUILD, "嵌入代码.txt"), "w", encoding="utf-8") as f:
        f.write(embed_snippets())
    with open(os.path.join(BUILD, "本地预览.bat"), "w", encoding="gbk") as f:
        f.write(PREVIEW_BAT)
    log("  生成 index.html（总入口）")
    log("  生成 部署说明.txt / 嵌入代码.txt / 本地预览.bat")

    zip_path = os.path.join(HERE, PKG + ".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in ("index.html", "部署说明.txt", "嵌入代码.txt", "本地预览.bat"):
            z.write(os.path.join(BUILD, name), PKG + "/" + name)
        for d, folder in (("A", A_DIR), ("B", B_DIR)):
            base = os.path.join(BUILD, d)
            for fname in sorted(os.listdir(base)):
                z.write(os.path.join(base, fname), PKG + "/" + folder + "/" + fname)
    log("  打包 " + os.path.basename(zip_path) + "  (%.1f KB)"
        % (os.path.getsize(zip_path) / 1024.0))

    source_zip_path = os.path.join(HERE, SOURCE_PKG + ".zip")
    source_files = (
        ".gitignore",
        "README.md",
        "build.py",
        "build_v2.py",
        "make.bat",
        "package.py",
        "serve.bat",
        "stage_pages.py",
        os.path.join("tests", "test_stage_pages.py"),
        os.path.join(".github", "workflows", "deploy-pages.yml"),
    )
    with zipfile.ZipFile(source_zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(SOURCE_PKG + "/请先看-部署说明.txt", SOURCE_README)
        for name in source_files:
            z.write(os.path.join(HERE, name), SOURCE_PKG + "/源码/" + name)
        z.write(os.path.join(BUILD, "index.html"),
                SOURCE_PKG + "/可直接上传的网站/index.html")
        for d, folder in (("A", A_DIR), ("B", B_DIR)):
            base = os.path.join(BUILD, d)
            for fname in sorted(os.listdir(base)):
                z.write(os.path.join(base, fname),
                        SOURCE_PKG + "/可直接上传的网站/" + folder + "/" + fname)
    log("  打包 " + os.path.basename(source_zip_path) + "  (%.1f KB)"
        % (os.path.getsize(source_zip_path) / 1024.0))
    log("完成。")


if __name__ == "__main__":
    main()
