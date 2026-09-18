---
title: "Foundry \"forge-std/Test.sol\" Not Found in VS Code: How to Troubleshoot It"
excerpt: "A red underline in VS Code doesn't always mean forge build actually fails — how to tell the difference and work through the real causes."
category: "foundry"
banner: "/images/banner-foundry-debug.svg"
metaLine: "Foundry Debugging Series · 2 of 5"
pubDate: 2026-09-13
stack: ["Foundry", "VS Code", "Solidity"]
---

Second in a short series on real problems I hit learning Foundry — see the [full series intro](/blog/foundry-forge-test-mt) for the rest.

## The error

While working on a Foundry project, VS Code underlined an import in red with this message:

```text
Source "/Users/cvalley/foundry-f26/foundry-fund-me-f26/lib/forge-std/src/Test.sol" not found:
File import callback not supported
solidity(6275)
```

This showed up in the editor even though I hadn't necessarily changed anything about the import itself — just a normal `import {Test} from "forge-std/Test.sol";` line.

## The first thing to check: is this a real error, or just the editor?

Before touching any config, the most useful diagnostic step is running the actual compiler and comparing it to what the editor claims:

```bash
forge build
```

If `forge build` compiles successfully while VS Code still shows a red underline, the problem is in the editor's Solidity language server, not in your actual project — Forge's own compiler is the ground truth, not the extension's inline diagnostics. I'm noting this explicitly because it's easy to assume a red underline means a broken project when it sometimes just means the extension hasn't picked up your project's import paths yet.

## Common real causes, in the order I'd check them

**1. `forge-std` isn't actually installed.** Check whether the dependency exists on disk:

```bash
ls lib/forge-std
```

If that directory is empty or missing, install it:

```bash
forge install foundry-rs/forge-std
```

**2. Remappings aren't configured, or aren't where the editor expects them.** Foundry resolves imports like `forge-std/Test.sol` using remappings — either an explicit `remappings.txt` file, or the `remappings` array in `foundry.toml`. You can print what Foundry itself is currently using:

```bash
forge remappings
```

If `forge build` succeeds, Forge is resolving the import correctly — which means any remaining red underline is specifically a VS Code / language-server configuration gap, not a project problem.

**3. The VS Code Solidity extension needs its own path configuration.** Depending on which Solidity extension is installed, it may need to be told explicitly where to find remappings or the project root, separately from Foundry's own config. This is worth checking in the extension's settings if step 1 and 2 both check out.

**4. Editor/language-server cache is stale.** Reloading the VS Code window (`Cmd/Ctrl+Shift+P` → "Reload Window") after installing a missing dependency or changing remappings clears a surprising number of phantom red underlines that don't reflect the current project state.

## What I won't claim

I want to be upfront about something: I don't have a single confirmed "this exact thing fixed it" story for this one the way I do for the `--mt` flag issue. The useful lesson is the diagnostic order — check `forge build` first, then dependency installation, then remappings, then the editor itself — rather than assuming any one specific cause. If you hit this exact error, work through those steps in order against your own project rather than assuming it's whichever cause is most commonly cited online.
