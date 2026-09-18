---
title: "Imported an Anvil Account Into MetaMask but Can't See the 10,000 ETH?"
excerpt: "The private key imports fine. The balance is real. MetaMask is just pointed at the wrong network — here's the actual fix."
category: "foundry"
banner: "/images/banner-foundry-debug.svg"
metaLine: "Foundry Debugging Series · 4 of 5"
pubDate: 2026-09-13
stack: ["Foundry", "Anvil", "MetaMask"]
---

Fourth in a short series on real problems I hit learning Foundry — see the [full series intro](/blog/foundry-forge-test-mt) for the rest.

## The symptom

I started a local Anvil chain, which prints out a set of pre-funded test accounts with large ETH balances. I imported the private key for one of those accounts into MetaMask — and the balance I expected wasn't there.

The private key import itself worked correctly. The confusing part is that a *successful* import can still show a balance of zero, for a reason that has nothing to do with the key.

## The actual cause

Anvil is a local, throwaway blockchain — it isn't Ethereum mainnet, and it isn't Sepolia. The 10,000 test ETH an Anvil account holds only exists *on that specific local chain*, running on your own machine. Importing the private key into MetaMask makes that account available inside MetaMask — but MetaMask still shows whatever network it's currently switched to. If MetaMask is set to Ethereum Mainnet or Sepolia, it will correctly show a balance of 0 for that account, because on those networks, that address genuinely has never received anything.

The key was never the problem. The network selector was.

## The fix: add Anvil as a custom network in MetaMask

Anvil's default local endpoint and chain ID, per Foundry's own documentation:

- RPC URL: `http://127.0.0.1:8545`
- Chain ID: `31337`

In MetaMask: **Add a network → Add a network manually**, then enter:

- Network name: something like `Anvil Local` (this label is just for you)
- New RPC URL: `http://127.0.0.1:8545`
- Chain ID: `31337`
- Currency symbol: `ETH`

Once that network exists, switch MetaMask to it. The imported account should now show its real Anvil balance — because MetaMask is finally asking the right chain.

## Worth confirming against your own terminal

Anvil prints its actual RPC address and chain ID when it starts, and those defaults can be overridden with flags like `--port` or `--chain-id`. Before assuming `8545`/`31337`, it's worth glancing at your own running Anvil terminal output to confirm you're using the values it's actually reporting, rather than trusting a default that might have been overridden.

## One more thing worth knowing

Anvil's local chain state resets when you restart it (unless you've explicitly configured persistence). If you stop and restart Anvil, previously deployed contracts and any transactions from the old session are gone — including, for testing purposes, that no longer matters, since the whole point of a local chain is that it's disposable. Test ETH has no real monetary value on any network; it exists purely so you can send transactions without spending real funds.
