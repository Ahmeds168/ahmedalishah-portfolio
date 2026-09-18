---
title: "Foundry Installed but \"forge\" Command Not Found on macOS"
excerpt: "Foundry's installer and the actual forge/cast/anvil binaries are two separate steps — what to check when the command still isn't found."
category: "foundry"
banner: "/images/banner-foundry-debug.svg"
metaLine: "Foundry Debugging Series · 3 of 5"
pubDate: 2026-09-13
stack: ["Foundry", "macOS", "PATH"]
---

Third in a short series on real problems I hit learning Foundry — see the [full series intro](/blog/foundry-forge-test-mt) for the rest.

## The symptom

Early in setting up Foundry on macOS, I had Foundry-related files under `~/.foundry` and `~/.foundry/bin` — including `foundryup`, the tool that actually installs the Foundry binaries — but `forge` still wasn't available as a command in the terminal.

This is a setup/PATH issue, not a Foundry bug: `foundryup` installing successfully and the individual tools (`forge`, `cast`, `anvil`, `chisel`) being on your `PATH` are two different steps.

## Checking what's actually installed and where

Before changing anything, it's worth confirming what's actually on disk versus what your shell can currently see:

```bash
ls ~/.foundry/bin
which forge
echo $PATH
```

If `ls ~/.foundry/bin` shows `forge`, `cast`, `anvil`, and `chisel` present, but `which forge` comes back empty, the binaries exist — your shell just doesn't know to look in that directory.

## The install flow, in the right order

Foundry's official install path is:

```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

The first command installs `foundryup` itself. Running `foundryup` afterward is a separate, required step — it's what actually downloads and installs `forge`, `cast`, `anvil`, and `chisel` into `~/.foundry/bin`. Skipping the second step, or running it in a terminal session that hasn't reloaded its shell config, is the most common reason the tools show up on disk but not on `PATH`.

## Fixing the PATH itself

`foundryup` normally adds `~/.foundry/bin` to your `PATH` by updating your shell's profile file (`~/.zshrc` on modern macOS, since zsh is the default shell; `~/.bash_profile` or `~/.bashrc` if you're using bash). If that line didn't get added — or was added to a profile file your current shell session isn't actually reading — you can add it manually:

```bash
echo 'export PATH="$HOME/.foundry/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Then verify each tool is actually reachable:

```bash
forge --version
cast --version
anvil --version
```

## Why this looks like a Foundry problem but isn't

The confusing part is that everything about the *install* can look successful — `foundryup` runs, files appear under `~/.foundry` — while the terminal still can't find the commands. That gap is entirely about shell configuration (which profile file your shell reads, and whether you've opened a new terminal session since it changed) rather than anything wrong with Foundry itself.
