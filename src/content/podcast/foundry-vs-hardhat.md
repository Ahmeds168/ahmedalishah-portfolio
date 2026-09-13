---
title: "Foundry vs Hardhat: Which Ethereum Development Framework Should You Learn?"
shortDescription: "A practical comparison of Ethereum development workflows, testing, scripting, and developer experience."
description: "Foundry and Hardhat are the two dominant toolchains for Solidity development, and they take genuinely different approaches — Solidity-native tests versus a JavaScript-based workflow. This episode compares them on the things that actually matter day to day: test speed, scripting ergonomics, and how each fits into a real smart contract project."
episodeNumber: 3
date: 2026-09-06
duration: "12 min"
featured: false
topics: ["Blockchain", "Ethereum", "Solidity", "Foundry"]
inThisEpisode:
  - "The core philosophical difference between Foundry and Hardhat"
  - "Why writing tests in Solidity changes how you test"
  - "Where Hardhat's JavaScript ecosystem still has an edge"
  - "Deployment scripting in both frameworks"
  - "A practical recommendation for which to learn first"
timestamps:
  - { time: "00:00", label: "Introduction" }
  - { time: "01:30", label: "The core philosophical difference" }
  - { time: "04:20", label: "Testing in Solidity vs. JavaScript" }
  - { time: "07:15", label: "Where Hardhat's ecosystem still wins" }
  - { time: "09:40", label: "Deployment scripting compared" }
  - { time: "11:00", label: "Which one should you learn first?" }
resources:
  - { label: "Foundry Book (official docs)", url: "https://book.getfoundry.sh/" }
  - { label: "Hardhat (official docs)", url: "https://hardhat.org/" }
  - { label: "My On-Chain Voting dApp project", url: "/projects" }
relatedArticles: ["why-i-built-a-blockchain-notary", "foundry-forge-test-mt"]
relatedEpisodes: ["how-foundry-testing-works"]
seoTitle: "Foundry vs Hardhat — A Practical Ethereum Development Comparison"
seoDescription: "Comparing Foundry and Hardhat on testing speed, scripting, and developer experience, based on real smart contract project work."
---

## Introduction

If you're starting Solidity development today, the first real decision you'll make isn't a language feature — it's which toolchain to learn: Foundry or Hardhat. Both are mature, both are widely used, and they solve the same problem with genuinely different philosophies. This episode is a practical comparison based on having used both across real projects, not a marketing rundown.

## The core philosophical difference

Hardhat is a JavaScript-based framework: you write your tests, scripts, and tooling in TypeScript or JavaScript, and Hardhat orchestrates compiling and running your Solidity contracts underneath that layer. Foundry flips this — you write your tests in Solidity itself, running on a purpose-built EVM test runner called Forge.

That one decision cascades into almost every other difference between them.

## Testing in Solidity vs. JavaScript

Writing tests in the same language as your contracts has a real advantage: you're not context-switching between Solidity for the logic and JavaScript for the tests, and you get direct access to Solidity-level features like cheat codes for manipulating block time, account balances, or call context mid-test. Foundry's test runner is also compiled and extremely fast — a full test suite that takes real time under Hardhat often runs near-instantly under Forge.

The trade-off is that Solidity is a less expressive scripting language than JavaScript for anything outside the EVM itself — parsing complex fixtures or hitting external APIs during test setup is more natural in a Hardhat/JS test.

## Where Hardhat's ecosystem still wins

Hardhat has been around longer and has a correspondingly larger plugin ecosystem — coverage tooling, gas reporting, and integrations with various frontend and deployment pipelines tend to be more mature or more numerous. If your project leans heavily on JavaScript tooling elsewhere (a Next.js frontend, existing Node scripts), staying in one language end-to-end is a real ergonomic win that Hardhat naturally supports.

## Deployment scripting compared

Both frameworks support scripted deployments, but the flavor differs the same way testing does: Foundry scripts are written in Solidity and executed through Forge, giving you direct access to the same cheat codes and types you use in tests. Hardhat scripts are JavaScript, which makes them easier to wire into existing CI/CD systems or external services that already speak JavaScript.

## Which one should you learn first?

My honest recommendation: start with Foundry if you're learning Solidity from scratch, specifically because writing tests in Solidity reinforces the language itself rather than splitting your attention. Learn Hardhat once you're working on a project that has real JavaScript-side requirements — a frontend integration, an existing Node toolchain, or plugins that only exist in that ecosystem. Most serious Solidity developers end up comfortable with both; the choice is really about which one fits the specific project in front of you.
