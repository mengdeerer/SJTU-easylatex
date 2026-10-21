# 中文字体

随附 Noto Serif SC（思源宋体风格的 Noto 简体中文子集）Regular 和 Bold，
来自 [Noto CJK 官方仓库](https://github.com/notofonts/noto-cjk/tree/main/Serif/SubsetOTF/SC)。
字体文件未做修改，使用 SIL Open Font License 1.1，完整许可证见 [LICENSE](LICENSE)。

- [NotoSerifSC-Regular.otf](https://raw.githubusercontent.com/notofonts/noto-cjk/main/Serif/SubsetOTF/SC/NotoSerifSC-Regular.otf)
- [NotoSerifSC-Bold.otf](https://raw.githubusercontent.com/notofonts/noto-cjk/main/Serif/SubsetOTF/SC/NotoSerifSC-Bold.otf)

两个字体文件合计约 23 MiB，供源码编译使用；输出 PDF 仅嵌入实际用到的字形。
模板使用同一组中文字体处理正文、标题和代码中的中文，不提供额外的仿宋或楷体。
需要其他字体时，使用 `font=custom` 并在主文件中自行配置。
