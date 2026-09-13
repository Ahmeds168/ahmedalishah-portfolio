---
title: "Defensive Engineering of the FundMe Contract: Reentrancy, Access Control, and Price Feed Safety"
shortDescription: "A defensive-engineering walkthrough of FundMe, the canonical Solidity teaching contract — and the patterns that turn a working contract into a safe one."
description: "FundMe — a crowdfunding contract that accepts ETH pegged to a USD minimum via a Chainlink price feed — is one of the most widely used teaching contracts in Solidity education. This episode goes past 'does it work' into 'is it safe': the checks-effects-interactions pattern, why custom errors beat require strings, access control with onlyOwner, price feed staleness checks, and the pull-over-push withdrawal pattern, with a look at how each of these gets tested in Foundry."
episodeNumber: 6
date: 2026-09-13
duration: "16 min"
featured: false
audioPath: "/podcasts/006-defensive-engineering-fundme/episode.m4a"
topics: ["Blockchain", "Solidity", "Security", "Foundry"]
inThisEpisode:
  - "What FundMe is and why it's a common Solidity teaching contract"
  - "The checks-effects-interactions pattern and why ordering matters"
  - "Custom errors versus require strings"
  - "Access control with onlyOwner, done defensively"
  - "Chainlink price feed staleness checks"
  - "Pull-over-push: why withdrawals shouldn't push funds automatically"
timestamps:
  - { time: "00:00", label: "Introduction" }
  - { time: "01:50", label: "What FundMe actually does" }
  - { time: "04:15", label: "Checks-effects-interactions" }
  - { time: "07:20", label: "Custom errors vs. require strings" }
  - { time: "09:45", label: "Access control with onlyOwner" }
  - { time: "12:10", label: "Price feed staleness checks" }
  - { time: "14:00", label: "Pull-over-push withdrawals" }
resources:
  - { label: "Chainlink Price Feeds documentation", url: "https://docs.chain.link/data-feeds" }
  - { label: "My On-Chain Voting dApp (similar defensive patterns)", url: "/projects" }
relatedArticles: ["why-i-built-a-blockchain-notary"]
relatedEpisodes: ["foundry-vs-hardhat", "how-foundry-testing-works"]
seoTitle: "Defensive Engineering of the FundMe Contract — Solidity Security Patterns"
seoDescription: "A defensive-engineering breakdown of the FundMe contract: reentrancy protection, custom errors, access control, and Chainlink price feed safety."
---

## Introduction

FundMe shows up in more Solidity courses than almost any other example contract, mine included — it's simple enough to teach in an afternoon, but it touches nearly every pattern you actually need in production: external calls, price oracles, access control, and fund handling. This episode isn't about how FundMe works — it's about the difference between a version that works in a demo and a version you'd trust with real money.

## What FundMe actually does

FundMe is a crowdfunding contract: anyone can send ETH, as long as the USD-equivalent value of that ETH meets a minimum funding amount. The USD conversion comes from a Chainlink price feed — an oracle that reports the current ETH/USD price on-chain. The contract owner can withdraw the accumulated funds. That's the entire feature set. The interesting engineering lives entirely in how carefully each of those three pieces — receiving funds, reading a price, and withdrawing — gets handled.

## Checks-effects-interactions

This is the pattern most reentrancy bugs come down to violating. The rule: check your conditions first, update your own contract's state second, and only *then* make any external call — sending ETH, calling another contract, anything that hands control to code you don't own. If you send ETH before updating your internal accounting, a malicious recipient contract can call back into your function mid-execution and drain funds before your state ever reflects the first withdrawal.

In FundMe's withdraw function, that means: zero out the funder's balance and reset the funders array *before* the actual ETH transfer happens, never after. It's a small ordering change with an outsized security consequence.

## Custom errors versus require strings

Older Solidity leaned on `require(condition, "error message")`. Custom errors — declared once and referenced by name — cost noticeably less gas, because the revert reason is encoded as a selector instead of a full string stored in the transaction. They also read better at the call site: `if (msg.sender != owner) revert FundMe__NotOwner();` documents the failure mode as clearly as a require string, without the runtime cost. For any contract where gas actually matters — which is most of them — this is close to a free win.

## Access control with onlyOwner

The `onlyOwner` modifier is simple in concept and easy to get subtly wrong in practice. The defensive version stores the owner as an `immutable` variable set once in the constructor, rather than a mutable one that could theoretically be reassigned through an overlooked function. It also fails loudly with a custom error rather than a generic revert, which matters when you're debugging a failed transaction later and need to know exactly why it failed.

## Price feed staleness checks

This is the part people skip most often. A Chainlink price feed isn't guaranteed to update every block — if the underlying network has an issue, or the feed's heartbeat interval hasn't elapsed, you can read a price that's technically valid but hours old. A defensive implementation checks the timestamp returned alongside the price and reverts if it's older than the feed's expected heartbeat, rather than silently trusting a possibly stale number to gate how much ETH someone needs to send.

## Pull-over-push withdrawals

The naive version of "let the owner withdraw funds" pushes ETH out automatically as part of some other function. The defensive version separates "the owner is allowed to withdraw" from "the ETH transfer actually happens," and requires the owner to explicitly call a withdraw function themselves — a pull, not a push. This matters because push-based transfers to a contract address can fail silently or be exploited depending on the recipient's fallback logic; a pull pattern puts the recipient in control of when and how they receive funds, which removes an entire class of failure modes from the sender's side.

None of these patterns are exotic. What makes FundMe worth revisiting even after you've written it once is that every one of these five decisions is invisible when the contract is working correctly — and each one is exactly the line that separates a tutorial contract from one you'd actually deploy.
