---
title: "How Foundry Testing Works: Forge, Anvil and Smart Contract Testing Explained"
shortDescription: "A closer look at Forge and Anvil — how Foundry's test runner and local EVM node actually work together."
description: "Foundry is more than one tool — Forge handles testing and building, Anvil gives you a local Ethereum node, and Cast lets you interact with chains from the command line. This episode breaks down how these pieces fit together, what fuzz testing actually buys you, and how to structure a smart contract test suite that catches real bugs."
episodeNumber: 4
date: 2026-08-30
duration: "13 min"
featured: false
topics: ["Foundry", "Solidity", "Ethereum", "Testing"]
inThisEpisode:
  - "What Forge, Anvil, and Cast each actually do"
  - "Writing your first Solidity test"
  - "What fuzz testing catches that example-based tests miss"
  - "Using cheat codes to manipulate test conditions"
  - "Structuring a test suite for a real contract"
timestamps:
  - { time: "00:00", label: "Introduction" }
  - { time: "01:20", label: "Forge, Anvil, and Cast explained" }
  - { time: "03:45", label: "Writing your first test" }
  - { time: "06:30", label: "Fuzz testing, explained" }
  - { time: "09:15", label: "Cheat codes in practice" }
  - { time: "11:30", label: "Structuring a real test suite" }
resources:
  - { label: "Foundry Book — Forge testing reference", url: "https://book.getfoundry.sh/forge/tests" }
  - { label: "My On-Chain Voting dApp (built and tested with Foundry-style tooling)", url: "/projects" }
relatedArticles: ["why-i-built-a-blockchain-notary"]
relatedEpisodes: ["foundry-vs-hardhat"]
seoTitle: "How Foundry Testing Works — Forge, Anvil, and Fuzz Testing Explained"
seoDescription: "A practical explanation of Foundry's Forge test runner, Anvil local node, and fuzz testing for Solidity smart contracts."
---

## Introduction

Foundry isn't one tool — it's a small toolkit, and understanding what each piece does makes the whole thing click. This episode walks through Forge, Anvil, and Cast, then goes deeper into the part that actually catches bugs: how to write tests that go beyond the happy path.

## Forge, Anvil, and Cast explained

Forge is the core: it compiles your contracts and runs your test suite, written in Solidity. Anvil is a local Ethereum node — think of it as a disposable blockchain you spin up instantly for local development and testing, with instant transactions and no real gas cost. Cast is a command-line tool for talking to any Ethereum node: sending transactions, calling contract functions, decoding calldata, all from your terminal without writing a script.

Together, they cover the full local development loop: write a contract, test it with Forge, run it against a live-feeling chain with Anvil, and poke at it manually with Cast.

## Writing your first test

A Foundry test is a Solidity contract that inherits from Forge's `Test` base contract, with test functions prefixed `test`. You deploy your contract in a `setUp()` function that runs before every test, then write normal Solidity function calls asserting on the results. It reads like ordinary Solidity because it is ordinary Solidity — there's no separate testing DSL to learn.

## Fuzz testing, explained

This is the feature that changes how you think about test coverage. Instead of writing one test with one specific input, you write a test function that takes parameters, and Forge automatically generates hundreds of randomized inputs to run against it — hunting for the edge case that breaks your assumption. An example-based test might check that transferring 100 tokens works. A fuzz test checks that transferring *any* amount, including edge values like zero or the maximum uint256, doesn't break your invariants. It's the difference between confirming what you already expected and actually looking for what you didn't.

## Cheat codes in practice

Foundry exposes "cheat codes" — special functions that let a test manipulate the EVM environment in ways that wouldn't be possible on a real chain: jumping the block timestamp forward to test a time lock, impersonating a specific address to test access control, or forcing a revert to check your error handling. These make it possible to test time-dependent or permission-dependent logic deterministically, without waiting for real time to pass or controlling real private keys.

## Structuring a real test suite

For a real contract, I structure tests in three layers: unit tests for individual functions in isolation, integration tests that exercise the actual sequence of calls a real user would make, and fuzz tests specifically on anything involving amounts, indexes, or arithmetic — the places where edge cases hide. The goal isn't test count, it's coverage of behavior you'd actually be embarrassed to get wrong in production.
