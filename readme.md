# SJTU-easylatex

用于中文课程小作业的 LaTeX 模板。默认使用 A4 纸、2.5 cm 页边距和简洁的标题、页眉页脚。
每次只需修改 `main.tex` 中的作业信息和正文，不必编辑 `easyR.sty`。

[查看示例 PDF](main.pdf)

## 开始使用

下载整个仓库，保留 `easyR.sty`、`fonts/` 和需要的图片资源。编译环境需要 **XeLaTeX**
和包含中文支持的 TeX Live / MacTeX / MiKTeX；不支持 pdfLaTeX。

在仓库根目录运行：

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir="build" "main.tex"
```

结果在 `build/main.pdf`。没有 `latexmk` 时，可以连续执行两次：

```sh
xelatex -interaction=nonstopmode -halt-on-error "main.tex"
xelatex -interaction=nonstopmode -halt-on-error "main.tex"
```

第二次编译用于更新编号、引用和书签。在 Overleaf 中上传整个项目，并将编译器设为 XeLaTeX。

## 填写作业信息

```tex
\documentclass[12pt,a4paper,UTF8,fontset=none]{ctexart}
\usepackage{easyR}

\title{多媒体压缩技术及其应用分析}
\author{姓名}
\reportsetup{
  course={网络多媒体技术},
  assignment={第一次作业},
  student-id={学号}
}
% \date{\today} % 默认不显示日期，需要时再设置

\begin{document}
\maketitle
\section{正文}
在这里写作业。
\end{document}
```

- `course` 和 `assignment` 分别显示在左、右页眉，建议各用简短名称。
- 学号为空时不显示“学号”字样；样式文件不保存姓名或学号。
- 标题和作者也会写入 PDF 文档信息。
- `\mytitle` 保留为 `\maketitle` 的别名，不再覆盖已填写的标题和作者。
- 默认标题为正文上方的紧凑标题块，不另设封面页。

## 常用内容

完整示例见 [main.tex](main.tex)。默认已支持数学公式、图片、三线表和可自动换行的表格。

```tex
\begin{equation}\label{eq:time}
  t = \frac{8S}{B}
\end{equation}
根据\autoref{eq:time}计算传输时间。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.3\linewidth]{figures/sjtu_logo_notitle.pdf}
  \caption{插图示例}\label{fig:logo}
\end{figure}
```

公式、图片、表格和章节均可用 `\label` 与 `\autoref` 引用。图片路径相对编译时的工作目录。
避免为微调版面大量插入 `\newpage` 或负值 `\vspace`，先调整图片大小与内容长度。

## 可选功能

默认不加载代码高亮、定理、文本框和子图的依赖。需要哪些就启用哪些：

```tex
\usepackage[code,theorems,boxes,subfigures]{easyR}
```

| 选项 | 功能 |
| --- | --- |
| `code` | 使用 `listings` 排版代码，如 `lstlisting[language=Python]` |
| `theorems` | `Theorem`、`Lemma`、`Corollary`、`Proposition`、`Definition`、`Example` 环境 |
| `boxes` | 可分页的 `reportbox` 环境，以及 `\tbox[选项]{内容}` |
| `subfigures` | 使用 `subcaption` 的 `subfigure` 环境和 `\subref` |

定理等环境按节共用编号，`\autoref` 会分别显示“定理”“引理”“定义”等名称。
文本框默认与当前正文等宽，例如：

```tex
\begin{reportbox}[title={说明}]
这里可以放多段文字；内容较长时自动跨页。
\end{reportbox}

\tbox[width=0.75\linewidth]{也可以指定文本框宽度。}
```

不要把需要跨页的文本框放进 `minipage` 或浮动体，否则外层环境仍会阻止分页。
完整示例见 [examples/features.tex](examples/features.tex)，从**仓库根目录**编译：

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir="build" "examples/features.tex"
```

## 中文字体

默认 `font=bundled` 使用 `fonts/` 中附带的 Noto Serif SC Regular / Bold，
避免依赖本机的宋体、仿宋等系统字体。两份源码字体约 23 MiB；输出 PDF 只嵌入用到的字形。
字体采用 SIL Open Font License 1.1，来源与许可证见 [fonts/README.md](fonts/README.md)。

不要单独复制 `.tex` 和 `.sty` 后遗漏字体。缺少字体时模板会明确报错，不会静默换成另一种字体。
如果字体存放在别处，可设置 `fontpath={路径/}`，路径末尾保留 `/`。

需要使用自己的字体时，明确选择 `font=custom`，并自行配置：

```tex
\documentclass[12pt,a4paper,UTF8,fontset=none]{ctexart}
\usepackage[font=custom]{easyR}
\setCJKmainfont{NotoSerifSC-Regular.otf}[
  Path=fonts/,
  BoldFont=NotoSerifSC-Bold.otf
]
```

自定义模式下模板不设置中文字体，也不承诺系统字体在其他机器或受限编译环境中可用。
若需要 `\fangsong`、`\kaishu` 等字体命令，也应自行配置对应字体。
判断中文是否正常时，除了查看 PDF，还应尝试搜索、复制姓名和正文。

## 调整版式

在 `\usepackage{easyR}` 之后覆盖所需设置，无需改动样式文件：

```tex
\geometry{margin=2.8cm}
\linespread{1.2}
\setlength{\parskip}{4pt}
\ctexset{section={beforeskip=14pt,afterskip=8pt}}
\hypersetup{urlcolor=black}
```

页眉默认按短课程名和作业名称设计；长页眉需要自行缩短或重新设置。
本模板只面向普通课程报告，未提供论文封面、作者单位和 `\thanks` 等论文标题功能。

## 从旧版迁移

1. 把原来写在 `easyR.sty` 中的标题和个人信息移到主文件，使用 `\title`、`\author`、`\reportsetup`。
2. 推荐将文档类选项写为 `[12pt,a4paper,UTF8,fontset=none]`，删去无须传给文档类的 `hyperref` 选项。
3. 用到定理、代码、文本框时，显式启用相应选项。旧的 `\mytitle` 和 `\tbox{...}` 写法仍保留。
4. 子图改用 `subcaption` 的环境语法，不能直接沿用旧 `subfigure` 包的 `\subfigure[...]` 命令。
5. 原来的 `pythonhighlight` 不再默认加载；Python 代码可以使用 `lstlisting[language=Python]`。
6. `float`、`multirow`、`makeidx` 等专用宏包按需在主文件中加载，旧稿使用 `[H]` 或 `\multirow` 时尤其注意。

## 验证与仓库文件

验证脚本需要 Python 3、XeLaTeX、pdfLaTeX、latexmk 和 Poppler 的 `pdftotext`，不依赖 Python 第三方包：

```sh
python3 "tests/check.py"
```

如果 `pdftotext` 不在 PATH 中，可以通过 `--pdftotext "/完整路径/pdftotext"` 指定。
检查覆盖默认示例、全部可选功能、中文提取、标题信息、定理引用、长框分页、自定义字体，
以及缺失字体、非法字体选项、未启用文本框和错误编译器的失败提示。
GitHub Actions 在推送和拉取请求中运行同一套检查，并保存示例 PDF。

`build/` 和编译中间文件均被 `.gitignore` 排除；仓库根目录的 `main.pdf` 是预览文件，
修改示例后应在检查通过时同步更新。`figures/` 保留原仓库的校徽资源。
