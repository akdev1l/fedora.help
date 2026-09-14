# Tooling

The rest of this site is written as manual steps. You read a command, decide
whether you want what it does, and run it. Some projects package the same
post-install work as a program instead: enable
[the third-party repositories](../repositories/index.md), install
[the codecs](../multimedia.md), set up [the NVIDIA driver](../nvidia/index.md),
write the usual modprobe options, all in one run.

This section catalogues those tools, so you can decide whether to use one in
place of working through the manual pages.

**All of it is third party.** None of these tools are produced, endorsed, or
reviewed by the Fedora Project, and none of them are maintained by this site.
Each page describes what the tool does at the version stated, where its work
overlaps the pages here, and what you take on by running it. The site's usual
position applies to the tool as much as to any command on any other page:
understand what it costs before you run it.

Each page is based on the tool's source. Where the source and the documentation
disagree, that is noted.

## The tools

- [Fedora Tricks](fedoratricks.md) — a Bash command-line tool that
  enables RPM Fusion, installs the multimedia stack, and sets up the NVIDIA
  driver. Distributed as an RPM from a [COPR](../repositories/copr.md).
