---
title: "Why I built a blockchain notary instead of another CRUD app"
excerpt: "On choosing Solidity over a database when the whole point is that nobody — including me — should be able to quietly edit the record."
category: "blockchain"
categoryLabel: "Blockchain & Cryptography"
categoryColor: "signal"
banner: "/images/banner-notary.svg"
metaLine: "Notes · Decentralized Document Notary"
order: 1
stack: ["Solidity", "React", "Supabase"]
codeSnippet:
  filename: "concept.sol"
  code: |
    function verifyHash(bytes32 storedHash, bytes32 fileHash)
        public view returns (bool) {
      // the chain only ever sees a hash, never the document
      return storedHash == fileHash;
    }
---

Most of the time, "store this document and remember when it was created" is a solved problem: a database row, a timestamp column, done. So why put a smart contract in front of it at all?

## The trust problem a database can't solve

A timestamp in a database is only as trustworthy as the people who control that database. If I run the database, I can edit the timestamp. If you run it, you can edit it. Notarization exists precisely because sometimes the parties involved don't fully trust each other, or don't trust a third party's server not to be quietly modified, hacked, or subpoenaed. A regular CRUD app can prove "a row says this," never "this couldn't have been changed."

A public blockchain flips that. Once a hash is written to Sepolia, changing it means rewriting history on a ledger that thousands of other nodes also hold a copy of. That's a fundamentally different guarantee than "trust my server."

## What actually goes on-chain (and what doesn't)

The document itself never touches the blockchain — that would be slow, expensive, and a privacy nightmare. Instead, the app hashes the document client-side and writes only the hash on-chain. The actual file lives in Cloudflare R2, with Supabase managing accounts and the mapping between a user, a file, and its hash. The chain's only job is to answer one question honestly: "did a hash matching this exact document exist at this block?"

## Why three different platforms

Vercel serves the frontend, Render runs a small backend service, and Sepolia handles the actual notarization logic. It would have been easier to cram everything into one deploy, but keeping "serve the UI," "handle app logic," and "provide immutability" as three genuinely separate concerns made each piece easier to reason about — and easier to swap out later if needed.

## The honest trade-off

This isn't free. Gas costs money, even on testnets that money is fake but the friction is real, and a public chain means the hash (though not the document) is technically visible to anyone. For a huge number of use cases, a signed database record with an audit log is genuinely fine. This project exists for the narrower slice of cases where "genuinely fine" isn't good enough — and it was a good excuse to actually feel that trade-off rather than just read about it.
