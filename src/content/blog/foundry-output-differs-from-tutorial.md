---
title: "Why Your Foundry Test Output Looks Different From a Course Video"
excerpt: "A passing test with different-looking terminal output isn't a sign something's wrong — what actually causes the formatting to shift."
category: "blockchain"
categoryLabel: "Blockchain & Cryptography"
categoryColor: "signal"
banner: "/images/banner-foundry-debug.svg"
metaLine: "Foundry Debugging Series · 5 of 5"
pubDate: 2026-09-13
order: 9
stack: ["Foundry", "Forge"]
---

Last in a short series on real problems I hit learning Foundry — see the [full series intro](/blog/foundry-forge-test-mt) for the rest.

## The moment that causes doubt

I ran a test against a Sepolia fork:

```bash
forge test --mt testPriceFeedVersionIsAccurate -vvv --fork-url $SEPOLIA_RPC_URL
```

And got a clean pass:

```text
[PASS] testPriceFeedVersionIsAccurate() (gas: 14523)
```

The test passed. The assertion was correct. And I still second-guessed myself, because the surrounding terminal output — spacing, extra lines, exact wording — didn't look identical to what I'd seen in Patrick Collins' course video.

That gap between "the test passed" and "it doesn't look like the video" is worth pulling apart, because the two things aren't actually connected.

## What `[PASS]` actually verifies

A `[PASS]` result means every assertion inside that test function evaluated true, and the function didn't revert unexpectedly. It says nothing about terminal formatting, log layout, or which extra lines Forge decides to print around the result — those are cosmetic, controlled by Forge's own version and your verbosity flags, not by whether your contract logic is correct.

## Where the actual differences come from

A handful of things reliably change Forge's terminal output between when a course was recorded and whenever you happen to be following along:

- **Forge version.** Foundry ships frequently. Output formatting, summary lines, and even default behaviors have changed across versions — a video recorded against an older release can look meaningfully different from the same command today.
- **Verbosity level.** `-v` through `-vvvvv` each show progressively more detail. If a tutorial used a different verbosity flag than you did — or the instructor's default settings differ from yours — the amount of visible output will differ even for an identical test result.
- **Gas reporting format.** How gas usage is displayed alongside test results has changed across Foundry versions.
- **Solidity compiler version.** A different `solc` version can change compile-time messages even when the actual test behavior is identical.
- **Fork configuration and RPC provider.** Forking from a different RPC endpoint, or at a different block, can surface provider-specific log lines that have nothing to do with your contract.

## The actual lesson

The thing that matters is whether your assertions pass and whether the contract logic being tested is correct — not whether your terminal's exact spacing and line count matches a video recorded at some earlier point against some earlier Foundry release. Tutorials are a snapshot of a tool at a specific moment; a fast-moving CLI tool's cosmetic output is one of the most likely things to drift, and drifting is not the same as breaking.
