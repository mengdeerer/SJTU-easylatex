#!/usr/bin/env python3
"""编译真实示例，检查中文提取、引用、可选依赖及关键失败路径。"""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "checks"


def run(command, *, success=True, expected=""):
    result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    if success and result.returncode:
        raise RuntimeError(f"命令失败：{command}\n{result.stdout[-8000:]}")
    if not success and (result.returncode == 0 or expected not in result.stdout):
        raise RuntimeError(f"未出现预期错误 {expected!r}：{command}\n{result.stdout[-8000:]}")
    return result.stdout


def fixture(name, source):
    path = OUT / f"{name}.tex"
    path.write_text(source, encoding="utf-8")
    return path


def document(body, options="", setup=""):
    return (r"\documentclass[12pt,a4paper,UTF8,fontset=none]{ctexart}" + "\n"
            + rf"\usepackage[{options}]{{easyR}}" + "\n" + setup + "\n"
            + r"\begin{document}" + "\n" + body + "\n" + r"\end{document}")


def compile_pdf(source, pdftotext):
    run(["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error",
         "-outdir=build/checks", str(source.relative_to(ROOT))])
    log = (OUT / f"{source.stem}.log").read_text(encoding="utf-8", errors="replace")
    for bad in ("Undefined control sequence", "No autoref name", "Missing character",
                "undefined references", "headheight is too small", "Overfull",
                "Unexpected value", "Label(s) may have changed", "LaTeX Font Warning"):
        if bad in log:
            raise RuntimeError(f"{source.name} 编译日志存在问题：{bad}")
    text = run([pdftotext, "-enc", "UTF-8", str(OUT / f"{source.stem}.pdf"), "-"])
    if "[?]" in text or re.search(r"[\u0f00-\u109f]", text):
        raise RuntimeError(f"{source.name} 存在未解析引用或中文乱码")
    return re.sub(r"\s+", "", text), text


def require(text, *phrases):
    for phrase in phrases:
        if phrase not in text:
            raise RuntimeError(f"PDF 文本缺少：{phrase}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdftotext", default="pdftotext")
    args = parser.parse_args()
    for executable in ("latexmk", "xelatex", "pdflatex", args.pdftotext):
        if not shutil.which(executable):
            raise RuntimeError(f"缺少依赖：{executable}；请按 README 的验证说明安装。")
    OUT.mkdir(parents=True, exist_ok=True)

    main_text, _ = compile_pdf(ROOT / "main.tex", args.pdftotext)
    require(main_text, "课程作业报告示例", "学号", "理论传输时间")
    # 默认启用全部功能；仍允许显式关闭，并且不加载已关闭的模块。
    minimal = fixture("minimal", document("精简模式正常。",
        options="code=false,theorems=false,boxes=false,subfigures=false,logo=false"))
    minimal_text, _ = compile_pdf(minimal, args.pdftotext)
    require(minimal_text, "精简模式正常")
    files = (OUT / "minimal.fls").read_text(encoding="utf-8", errors="replace")
    for package in ("listings.sty", "amsthm.sty", "tcolorbox.sty", "subcaption.sty"):
        if re.search(rf"[/\\]{re.escape(package)}(?:\s|$)", files):
            raise RuntimeError(f"显式关闭后仍加载了 {package}")

    features, _ = compile_pdf(ROOT / "examples/features.tex", args.pdftotext)
    require(features, "定理1.1", "引理1.2", "推论1.3", "命题1.4", "定义1.5", "例1.6",
            "计算理论传输时间", "这个文本框", "第一幅子图", "第二幅子图")

    info = fixture("metadata", document(
        r"\mytitle\section{章节}\subsection{小节}\label{sec:small}"
        r"\subsubsection{三级标题}\label{sec:tiny}"
        r"正文引用：\autoref{sec:small}、\autoref{sec:tiny}。",
        setup=r"\title{自定义标题检查}\author{测试作者}\date{指定日期}"
              r"\reportsetup{course={测试课程},assignment={第二次作业},student-id={123456}}"))
    info_text, _ = compile_pdf(info, args.pdftotext)
    require(info_text, "自定义标题检查", "测试作者", "指定日期", "学号：123456",
            "测试课程", "第二次作业", "节1.1", "节1.1.1")

    # 长框必须真的分到多页，且首尾内容都能保留。
    paragraphs = "\n\n".join(f"第{i}段。中文长文本框需要保留所有内容，并正确跨页。" * 3
                             for i in range(1, 45))
    longbox = fixture("longbox", document(
        r"\begin{reportbox}[title={跨页检查}]" + paragraphs + r"\end{reportbox}",
        setup=r"\reportsetup{course={跨页页眉检查}}"))
    box_text, raw_box = compile_pdf(longbox, args.pdftotext)
    require(box_text, "第1段", "第44段")
    if len([page for page in raw_box.split("\f") if page.strip()]) < 2:
        raise RuntimeError("长文本框未产生多个页面")
    for page in raw_box.split("\f"):
        if page.strip():
            require(re.sub(r"\s+", "", page), "跨页页眉检查")

    no_logo = fixture("nologo", document("无校徽模式正常。",
        options="logo=false,logopath=nonexistent-logo.pdf"))
    no_logo_text, _ = compile_pdf(no_logo, args.pdftotext)
    require(no_logo_text, "无校徽模式正常")

    custom = fixture("customfont", document("自定义字体模式正常。", options="font=custom",
        setup=r"\setCJKmainfont{NotoSerifSC-Regular.otf}[Path=fonts/]"))
    custom_text, _ = compile_pdf(custom, args.pdftotext)
    require(custom_text, "自定义字体模式正常")

    cases = [
        ("missingfont", document("test", options="fontpath=nonexistent-fonts/"),
         "Bundled regular font not found", "xelatex"),
        ("badfont", document("test", options="font=invalid"),
         "Unknown font mode", "xelatex"),
        ("disabledbox", document(r"\tbox{test}", options="boxes=false"),
         "Box support is disabled", "xelatex"),
        ("missinglogo", document("test", options="logopath=nonexistent-logo.pdf"),
         "Header logo not found", "xelatex"),
        ("wrongengine", document("test"), "XeTeX is required", "pdflatex"),
    ]
    for name, source, expected, engine in cases:
        path = fixture(name, source)
        run([engine, "-interaction=nonstopmode", "-halt-on-error",
             "-output-directory=build/checks", str(path.relative_to(ROOT))],
            success=False, expected=expected)
    print("通过：默认功能、显式关闭、中文提取、元数据、交叉引用、跨页页眉与文本框、自定义字体及 5 项失败路径。")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError) as error:
        print(f"验证失败：{error}", file=sys.stderr)
        sys.exit(1)
