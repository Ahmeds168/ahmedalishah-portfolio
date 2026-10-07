---
title: "Why My Voting dApp Counts Wallets, Not People"
excerpt: "One line of Solidity stops anyone voting twice — from the same wallet. Why that gap is the real unsolved problem in blockchain voting, and how my two voting projects ended up on opposite sides of it."
category: "blockchain"
banner: "/images/banner-wallets-not-people.svg"
metaLine: "Blockchain · Lessons from building a voting dApp"
pubDate: 2026-10-06
stack: ["Solidity", "Hyperledger Fabric", "Identity", "Governance"]
---

There is one line in my voting contract that I am proud of, and one sentence about it that I have to be honest about.

The line is this:

```solidity
require(!hasVoted[msg.sender], "You have already voted");
```

It is the first thing my `vote()` function does. The contract keeps a `mapping(address => bool) public hasVoted`, and once an address has voted, that address can never vote again. Not through my interface, not through Etherscan, not through a script that calls the contract directly. The rule lives on-chain, so there is no way around it.

The sentence I have to be honest about is: **that guarantees one vote per wallet, not one vote per person.**

## Why the check belongs in the contract

When I built the [On-Chain Voting dApp](/projects/on-chain-voting-dapp), most of the work went into the front end. I wanted a ballot that looked like an official paper ballot rather than a crypto dashboard, so that someone who had never touched a wallet would still recognise what they were doing.

But the double-vote rule had to live in the contract, not the interface. A front-end check can always be bypassed. Anyone can open the browser console, call the contract with a library like ethers.js, or skip my website entirely and use a block explorer. If the only thing stopping a second vote was a disabled button, there would be nothing stopping a second vote.

So the contract enforces it. That part of the design is solid, and I would build it the same way again.

## What "already voted" actually means

The contract does not know who you are. It knows `msg.sender`, the address that signed the transaction.

On a public blockchain, an address costs nothing to create. A new wallet is a keypair generated on your own device in a second, with no registration, no email, and no identity check. On a test network like Sepolia, the ETH needed to pay for a vote comes free from a faucet.

So "you have already voted" really means "this address has already voted". Someone with two wallets can vote twice. Someone with a script can create a thousand wallets and vote a thousand times. The contract sees a thousand different voters, because as far as the chain is concerned, that is exactly what they are.

This has a name: a **Sybil attack**, where one person controls many identities to gain influence they should not have. It is not a bug in my contract. It is a property of any system that counts addresses, and it applies to every "one wallet, one vote" scheme, however well the contract is written.

## The alternative is worse in a different way

The usual way blockchains deal with this is to stop counting people altogether and count money instead. In **token-weighted voting**, one token equals one vote. Splitting your tokens across a thousand wallets gains you nothing, because your total voting power stays the same.

That closes the Sybil problem by replacing it with another one. Token-weighted voting is one-dollar-one-vote: whoever holds the most tokens holds the most power. For a protocol deciding how to spend its own treasury, that may be acceptable, since the people with the most at stake get the most say. For an election, it is the opposite of what an election is for.

So a public-chain voting system has two basic options, and neither is democratic. Count addresses, and anyone can manufacture votes. Count tokens, and the wealthy outvote everyone else.

## My two voting projects sit on opposite sides of this

This problem is not new to me, because I built two voting systems, years apart, on different kinds of blockchain.

My university final-year project was an [election system on Hyperledger Fabric](/projects). Fabric is a **permissioned** blockchain: only known, vetted participants can validate transactions. For an election, that was the point. There is an organisation behind every node, and identities are established before anyone takes part.

The voting dApp is the opposite. It runs on Ethereum's Sepolia test network, which is **permissionless**: anyone can create an address and take part, with no identity attached.

Building both made the trade-off concrete. The permissioned system knows who its participants are, but only because someone trusted decides who gets in, which reintroduces exactly the central authority a blockchain is supposed to remove. The permissionless system needs no gatekeeper, but it cannot tell one person with ten wallets from ten people. You do not get both for free.

## It is not only about counting

Writing this made me notice a second limitation in my own design.

On a public chain, every transaction is visible. When an address calls `vote()` with a candidate's ID, that choice is recorded permanently and anyone can read it. If you know someone's address, you can see how they voted.

My interface hides the vote counts until you have voted or until voting closes. That is a deliberate design choice, meant to stop people being nudged by seeing who is ahead. But it is a choice about the interface, not about the data. Anyone reading the contract directly can see the running totals at any time.

A real election needs a **secret ballot**. My contract provides the opposite: a permanent, public record of every choice tied to every address. That is fine for a community poll where transparency is the goal. It is a serious problem anywhere coercion or vote-buying is possible, because a voter can prove exactly how they voted to whoever is paying them.

## What happened when someone tried it for real

Blockchain voting has been used in an official U.S. election. In the 2018 midterms, West Virginia became the first state to let selected voters cast ballots on a phone through a proprietary app called Voatz, which claimed security through a permissioned blockchain, biometrics, and hardware-backed key storage.

In 2020, MIT researchers published [the first public security analysis of Voatz](https://www.usenix.org/conference/usenixsecurity20/presentation/specter), titled *The Ballot is Busted Before the Blockchain*. They reverse-engineered the Android app and found vulnerabilities that could let different kinds of attackers alter, stop, or expose a user's vote. They also concluded that the blockchain was unlikely to protect against those attacks, because the weaknesses sat in the app and the servers around it. Voatz disputed the findings, but a follow-up audit by the security firm Trail of Bits, which Voatz commissioned, confirmed the researchers' results.

The lesson I take from it matches my own small project. The blockchain part tends to be the strongest link. A tamper-proof ledger of votes is worth very little if the step before it — proving who is allowed to vote, and that they voted freely — is weak.

## How people are trying to close the gap

The missing piece has a name too: **proof of personhood**. The goal is to give each real human exactly one credential, without necessarily revealing who they are, so a contract can check "this address belongs to a unique person" instead of just "this address exists".

There are several approaches, and each makes a different trade:

- **Biometric** systems, such as World ID, verify uniqueness by scanning a person's iris. Strong guarantees, with serious privacy questions about collecting biometric data at scale.
- **Social graph** systems, such as BrightID, establish uniqueness through people vouching for each other. No biometrics, but dependent on the honesty of the network.
- **Credential aggregation**, such as Human Passport (formerly Gitcoin Passport), scores an address on accumulated proofs, like linked accounts and on-chain history. Easier to adopt, but a score rather than a guarantee.

None of them is a finished answer. Each one moves trust somewhere: to a device, to a community, or to the issuers of credentials. That is the honest summary of the problem. You can make wallets correspond to people, but only by trusting something outside the chain to say so.

## Where that leaves my dApp

If I extended the project, I would gate `vote()` behind a personhood check, so the contract asks a verifier whether an address belongs to a unique human before accepting its vote. The `hasVoted` mapping would stay exactly as it is. It would simply be protecting a more meaningful kind of address.

I would still not use it for a binding public election. The secret-ballot problem would remain, and solving it properly needs cryptography far beyond a single mapping and a `require` statement.

Where on-chain voting already works well is where its properties fit the job: community polls, DAO decisions, and votes where transparency is a feature rather than a risk, and where the voters are a group whose membership can be defined in advance.

That is what building this taught me. The contract was the easy part. The hard part was never on the chain at all — it is deciding who counts as a voter, and that is a question no smart contract can answer by itself.
