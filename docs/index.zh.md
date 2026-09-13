# {{ brand }}：让 Fedora 属于你

{{ brandlink() }} 是一份非官方的社区指南，内容是 Fedora 无法分发的软件：多媒体
编解码器、NVIDIA 驱动、RPM Fusion 和 Flathub 这类第三方仓库，以及大多数桌面最终
都会用到的闭源应用。此外还有全新安装通常需要的那些修复。

## 这个站点为什么存在

根据 [Fedora 项目的使命][mission]，Fedora 只分发自由和开源软件。Red Hat 的法律
立场还排除了受专利限制以及不可再分发的代码。因此，桌面用户视为理所当然的一些东西
无法进入 Fedora：

- 受专利保护的多媒体编解码器（H.264、HEVC、AAC 等）
- NVIDIA 的专有驱动
- 专有固件和硬件启用二进制块
- 闭源应用：Steam、Discord、Chrome、Spotify

这些超出了项目的范围，所以相关文档只能放在别处。

## 面向的读者

在桌面上使用 Fedora、希望专有组件正常工作，并且希望在装好之后明白自己装了什么的
用户。

这些指南假定读者：

- 会打开终端并在命令行下操作
- 不怕执行命令，包括以 root 身份执行
- 在粘贴命令之前会先读一遍
- 想在这个过程中积累自己的 Fedora 知识

它们针对 x86_64 上当前受支持的 Fedora 版本：Workstation 和各个桌面 spin。原子化
变体（Silverblue、Kinoite）会在步骤不同的地方单独说明。

这些都不是必需的。原版 Fedora 安装本身就是完整且受支持的；这里的每一页都走出了
那个范围。

## 与 Fedora 项目无关

{{ brandlink() }} 是一个独立的社区项目，并非由 Fedora 项目或 Red Hat 制作、认可
或审核，“Fedora” 是 Red Hat, Inc. 的注册商标。官方文档请见
[docs.fedoraproject.org][docs]。

[mission]: https://docs.fedoraproject.org/zh_CN/project/
[docs]: https://docs.fedoraproject.org/
