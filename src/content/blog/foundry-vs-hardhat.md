---
title: "Foundry vs Hardhat in 2026: Which Should You Use for Solidity Development?"
excerpt: "Hardhat 3 now runs Foundry-style Solidity tests, and Foundry has reached 1.0. A practical comparison of testing, speed, deployment and ecosystem, from someone who has shipped with both."
category: "foundry"
banner: "/images/banner-foundry-vs-hardhat.svg"
metaLine: "Foundry & Tooling · A comparison from real projects"
pubDate: 2026-10-10
stack: ["Foundry", "Hardhat", "Solidity", "Ethereum"]
---

The first real decision in Solidity development isn't a language feature. It's the toolchain: Foundry or Hardhat. I've used both on real work. My [on-chain voting dApp](/projects/on-chain-voting-dapp) was built with Hardhat, which handled the local contract tests and the deployment script while ethers.js connected the contract to a React front end. Later I learned Foundry properly through Cyfrin's course and the FundMe project, and wrote up the problems I hit along the way in a [short debugging series](/blog/foundry-forge-test-mt).

For years the comparison was simple: Hardhat meant JavaScript, Foundry meant Solidity. That answer is now out of date. Hardhat 3 runs Solidity tests designed to be compatible with Foundry's, and Foundry reached its 1.0 release in February 2025. The two tools are closer than they have ever been, so the right choice depends less on philosophy and more on the project in front of you.

## The short answer

If you are learning Solidity, or your project is mostly contracts, start with **Foundry**. Writing tests in Solidity reinforces the language you are learning, and the tooling is fast.

If your project is a full-stack application with a TypeScript front end, deployment pipelines and integration tests that call the contracts the way the app does, **Hardhat 3** is a strong choice, and you no longer give up Solidity tests to use it.

The rest of this post explains why.

## The difference that used to settle it

Hardhat started as a JavaScript framework. You wrote tests, scripts and tasks in JavaScript or TypeScript, and Hardhat compiled and ran your contracts underneath. A typical Hardhat 2 test deployed a contract through ethers.js, called a function and asserted on the result with a JavaScript assertion library.

Foundry took the opposite position. Tests are Solidity contracts. A test function calls your contract directly and uses "cheatcodes" to control the environment: `vm.prank` to call as another address, `vm.warp` to move the block timestamp, `vm.expectRevert` to assert that a call fails. There is no JavaScript layer between the test and the contract.

That one decision shaped everything else. Foundry tests were faster and closer to the EVM. Hardhat tests were closer to how a real front end talks to a contract.

## What changed: Hardhat 3

Hardhat 3 removes most of that divide. The [Hardhat team describes](https://hardhat.org/docs/hardhat3/whats-new) "Foundry-compatible Solidity tests" that support unit, fuzz and invariant testing, while TypeScript tests remain available for integration work. Solidity test files use the same `.t.sol` naming, and many of the cheatcodes Foundry users know work as expected.

The compatibility isn't total. Hardhat's [Solidity test documentation](https://hardhat.org/docs/learn-more/solidity-tests) lists what is unsupported: scripting cheatcodes such as `startBroadcast`, fixture cheatcodes, and `getCode`. `testFail` tests also don't run by default, since Hardhat treats them as an anti-pattern in favour of `vm.expectRevert`. If you are moving a Foundry test suite across, those are the places to check.

Hardhat 3 also adds built-in Solidity coverage, ECMAScript modules by default, declarative configuration, and simulation of more than one network at a time, including first-class support for OP Mainnet. Underneath, the runtime was rebuilt in Rust, which the team presented at [Devcon 7](https://archive.devcon.org/devcon-7/hardhat-3-preview-overhauled-and-rust-powered/). After about nine months in beta, Hardhat 3 is now described as stable and production-ready, and Hardhat 2 reaches [end of life](https://hardhat.org/docs/reference/hardhat-2-end-of-life) by 1 June 2027 at the latest. Anyone starting a new Hardhat project today should start on version 3.

## What changed: Foundry 1.0

Foundry's 1.0 release, [announced by Paradigm](https://paradigm.xyz/2025/02/announcing-foundry-v1-0) on 13 February 2025, was about stability as much as features. It stabilised the APIs, made `foundryup` install stable releases by default, and introduced a release pipeline of nightly builds, release candidates and stable versions.

Paradigm's own benchmarks claim Forge compiles 2.1 to 5.2 times faster than Hardhat depending on caching, and that unit, fuzz and invariant tests run about twice as fast as in Foundry 0.2. Those are the maintainers' numbers on their chosen projects, so treat them as direction rather than a promise for your codebase.

## Side by side

| | Foundry | Hardhat 3 |
|---|---|---|
| Test language | Solidity | Solidity and TypeScript |
| Fuzz and invariant tests | Built in, mature | Built in, newer |
| Cheatcodes | Full set | Most of Foundry's, with listed exceptions |
| Deployment | `forge script`, written in Solidity | Hardhat Ignition, or TypeScript scripts |
| Local chain | Anvil | Built-in simulated networks, several at once |
| Installation | `foundryup` installs standalone binaries | npm package in your project |
| Extra tools | `cast` for chain calls, `chisel` for a Solidity REPL | Plugin system and the npm ecosystem |
| Coverage | `forge coverage` | `--coverage` flag, built in |

## Where Foundry still wins

**Speed and focus.** Foundry is a set of compiled binaries with no Node.js project around it. For contract-heavy work that keeps the loop short: edit, `forge test`, read the trace, repeat.

**The command-line toolkit.** Outside tests, `cast` lets you call a deployed contract, decode calldata or check a balance from the terminal. `anvil` gives you a local chain in one command, and `chisel` is useful for checking what a Solidity expression actually returns.

**Maturity of property testing.** Fuzz and invariant testing have been central to Foundry for years, and much of today's Solidity security course material and tooling is built around it. If your project's risk is in the contract logic, that ecosystem matters.

Foundry is not frictionless, though, especially when you are new. Most of my debugging series came from the gaps around the tool rather than the tool itself: [`forge: command not found` after installation on macOS](/blog/foundry-forge-command-not-found-macos), [VS Code failing to resolve `forge-std` imports](/blog/foundry-test-sol-not-found-vscode), and [Anvil accounts not showing their balance in MetaMask](/blog/anvil-metamask-balance-not-showing). None of these are Foundry bugs, but they are the kind of setup friction a beginner meets on day one.

## Where Hardhat still wins

**One language across the stack.** In my voting dApp the front end was React with ethers.js. With Hardhat, the deployment script and the tests sat in the same JavaScript tooling as the front end and shared the same compiled contract artifacts. Hardhat 3 generates typed artifacts by default, which makes that connection safer in TypeScript.

**Integration tests that look like your app.** Some behaviour is best tested the way a user triggers it: connect, sign, send a transaction, read an event. Hardhat's TypeScript tests make that natural, and in Hardhat 3 you can keep fast Solidity unit tests alongside them in the same project.

**Deployments as managed modules.** Hardhat Ignition describes deployments declaratively and tracks what has been deployed, which helps when a project has several contracts that depend on each other.

**Multichain simulation.** If you target an L2 such as OP Mainnet, simulating several chain types in one project is a genuine Hardhat 3 advantage.

## What developers actually use

The [Solidity Developer Survey 2025](https://soliditylang.org/blog/2026/04/15/solidity-developer-survey-2025-results/), with 1,095 respondents, found Foundry was the primary framework for 57% of developers, up from 51% the year before. Hardhat came second at 33% combined, split between Hardhat 3 at 18% and Hardhat 2 at 15%. Foundry leads and is growing, but a third of Solidity developers still work primarily in Hardhat, and many projects use both.

## How I'd choose

- **Learning Solidity, or doing Cyfrin or similar courses:** Foundry. You will be writing Solidity all day, including in your tests.
- **Auditing, security research or contract-only libraries:** Foundry, for its fuzzing, invariant testing and the tooling most security work assumes.
- **A full-stack dApp with a TypeScript front end:** Hardhat 3, with Solidity tests for the contracts and TypeScript tests for the integration.
- **An existing Hardhat 2 project:** plan the move to Hardhat 3 before the 2027 end of life rather than switching frameworks.
- **A team split between contract and front-end developers:** either works now, which is the real change. Pick the one your team will actually maintain.

## The bottom line

The old advice, "Foundry for Solidity people, Hardhat for JavaScript people", no longer describes the tools. Hardhat 3 writes Solidity tests, and Foundry is a stable 1.0 toolchain with the larger share of developers.

If you want one recommendation: learn Foundry first, because it makes you better at Solidity itself. Learn Hardhat 3 when you build a full application around your contracts. Being comfortable with both is the norm for working Solidity developers, not the exception.

If you're building something and want help with the contracts or the tooling around them, see my [Solidity and Foundry development service](/services/solidity-foundry-development), or browse more posts on [Foundry](/foundry) and [Solidity](/solidity).
