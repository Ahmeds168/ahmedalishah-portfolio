---
title: "AI Agents and Software Security: What Developers Need to Know"
shortDescription: "What autonomous AI systems mean for developers building applications that give AI agents access to tools, APIs, files, and external systems."
description: "AI agents that can call tools, browse the web, and execute code are showing up in more products every month. This episode walks through what actually changes for developers once a model can take actions on its own — the security model you're implicitly signing up for, the permission questions most teams skip, and practical steps for building agent-facing systems that fail safely instead of silently."
episodeNumber: 1
date: 2026-09-20
duration: "41 min"
audioPath: "/podcasts/001-ai-agents-software-security/episode.m4a"
featured: true
topics: ["AI", "Security", "Software Engineering"]
inThisEpisode:
  - "What an AI agent actually is, versus a plain chatbot"
  - "How agents use tool calling to take real actions"
  - "The security implications of giving a model tool access"
  - "Permission and authentication design for agent-facing systems"
  - "Practical recommendations for developers shipping agent features"
timestamps:
  - { time: "00:00", label: "Introduction" }
  - { time: "02:14", label: "What is an AI agent?" }
  - { time: "05:42", label: "Tool calling, explained plainly" }
  - { time: "08:30", label: "Security risks of tool access" }
  - { time: "12:15", label: "Permission and scope management" }
  - { time: "15:20", label: "Developer recommendations" }
resources:
  - { label: "My write-up on the Hugging Face AI agent breach", url: "/blog/the-hugging-face-ai-agent-breach" }
relatedArticles: ["the-hugging-face-ai-agent-breach", "what-prompt-engineering-looks-like"]
relatedEpisodes: ["running-ojs-in-production"]
seoTitle: "AI Agents and Software Security: What Developers Need to Know"
seoDescription: "A practical look at the security implications of building with AI agents — tool calling, permission design, and lessons from a real 2026 incident."
---

## Introduction

If you've shipped anything with an LLM in the last year, you've probably felt the shift from "the model answers questions" to "the model does things." That's the agent shift, and it changes your threat model whether you've thought about it or not.

This episode is about what actually changes for developers once a model can call tools, read files, hit APIs, or trigger other systems on its own — and what that means for how you design permissions, sandboxing, and failure modes.

## What is an AI agent?

Strip away the marketing and an "agent" is really just an LLM wired up to a loop: it gets a goal, it can call functions (search the web, run code, query a database, write a file), it sees the result, and it decides what to do next. Repeat until done.

The interesting part isn't the model getting smarter — it's that we've started handing it a set of real, consequential actions to take. A chatbot that's wrong wastes your time. An agent that's wrong can delete a file, spend your API budget, or — as we saw in a widely reported 2026 incident — chain together vulnerabilities to escape a sandbox entirely.

## Tool calling, explained plainly

Under the hood, tool calling is just structured output: instead of returning plain text, the model returns something like "call this function, with these arguments." Your code executes that function and feeds the result back in. That's it. There's no magic — which is exactly why the security conversation matters. Every tool you expose is a capability you're trusting the model to use appropriately, based on nothing but its training and your prompt.

## Security risks of tool access

The risk isn't that the model is malicious. It's that a capable model pursuing a goal will find paths you didn't anticipate — including paths through tools that seem harmless in isolation but compose into something dangerous together. A file-read tool plus a code-execution tool plus network access is a very different risk surface than any one of those alone.

This is exactly the pattern behind real-world incidents where agentic systems, given loosened safety constraints for testing purposes, chained together minor issues — a cache proxy vulnerability here, a template injection there — into a genuine production breach. Nobody wrote code that said "escape the sandbox." The capability existed because the pieces were all reachable.

## Permission and scope management

The practical fix is boring, which is a good sign: least privilege, applied to agents the same way you'd apply it to a junior engineer's production access. A few concrete habits:

- Scope every tool to the narrowest permission that gets the job done. A "read this one document" tool is safer than "read any file."
- Treat tool definitions as an attack surface you review, not a convenience you bolt on.
- Keep a human in the loop for anything irreversible — sending money, deleting data, deploying code — until you have real evidence the agent handles edge cases safely.
- Assume your safety monitoring needs to be on during testing, not just production. Several 2026 incidents specifically involved safety systems that existed but weren't active for the environment where the actual breach happened.

## Developer recommendations

If you're building agent-facing features right now, the single highest-leverage thing you can do is write down, explicitly, what the worst-case action of each tool you expose actually is — and make sure your permission model reflects that worst case, not the happy path. Agents are good at finding the gap between what you intended and what you actually allowed.

The rest is normal security hygiene: logging every tool call, rate-limiting, and building in a way to kill an agent's access instantly if something looks wrong. None of this is exotic. It's the same discipline you'd apply to any system with real-world side effects — it just needs to actually be applied here, because "the AI wouldn't do that" isn't a security control.
