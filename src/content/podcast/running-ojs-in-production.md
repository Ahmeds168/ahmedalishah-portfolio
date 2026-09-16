---
title: "Running Open Journal Systems in Production: Lessons From Real-World OJS Administration"
shortDescription: "Lessons learned from maintaining, securing, upgrading, and troubleshooting a production OJS installation."
description: "Open Journal Systems quietly runs a huge share of the world's academic publishing, but almost nobody talks about what it actually takes to keep an installation healthy over time. Drawing on real administration experience at a university department, this episode covers upgrade discipline, plugin compatibility, and the unglamorous automation work that ends up mattering most."
episodeNumber: 2
date: 2026-09-13
duration: "14 min"
featured: false
topics: ["OJS", "Web Administration", "Security", "DevOps"]
inThisEpisode:
  - "What Open Journal Systems is and why it's everywhere in academic publishing"
  - "Why upgrades are riskier than new feature work"
  - "Plugin compatibility as a recurring failure point"
  - "Building a rollback plan you hope to never use"
  - "Where office automation quietly pays for itself"
timestamps:
  - { time: "00:00", label: "Introduction" }
  - { time: "01:45", label: "What OJS is, for the unfamiliar" }
  - { time: "04:10", label: "Why upgrades are the scary part" }
  - { time: "07:30", label: "Plugin compatibility testing" }
  - { time: "10:05", label: "Rollback planning" }
  - { time: "12:00", label: "Office automation that compounds" }
resources:
  - { label: "My full write-up on this topic", url: "/blog/modernizing-a-university-journal-system" }
  - { label: "Open Journal Systems (official project)", url: "https://pkp.sfu.ca/ojs/" }
relatedArticles: ["modernizing-a-university-journal-system", "upgrade-ojs-3504-to-3505-safely"]
relatedEpisodes: ["ai-agents-software-security"]
seoTitle: "Running Open Journal Systems in Production — Real Administration Lessons"
seoDescription: "Practical lessons from administering a production OJS installation: upgrade risk, plugin compatibility, rollback planning, and office automation."
---

## Introduction

Open Journal Systems is one of those pieces of software that runs an enormous share of the world's academic journals while almost nobody outside the field has heard of it. I administered and upgraded an OJS installation for a university's Electrical Engineering department, and this episode is about what that work actually looks like — not the feature list, the day-to-day maintenance reality.

## What OJS is, for the unfamiliar

OJS is open-source journal management software: submission handling, peer review workflows, publishing, archiving. If a small or mid-sized academic journal exists, there's a decent chance it's running on OJS somewhere. It's mature, widely deployed, and — like most mature software with a long deployment tail — carries real operational weight once it's actually serving people.

## Why upgrades are the scary part

New features are low-stakes to build: if something's wrong, it just doesn't ship. Upgrading a system that editors, reviewers, and authors already depend on is a completely different kind of pressure. A botched upgrade doesn't fail quietly — it breaks an active submission cycle for real academics working against real deadlines.

Most of the actual skill in this kind of role isn't writing code. It's staging upgrades carefully: testing in an environment that mirrors production, checking plugin compatibility before touching anything live, and treating every version bump as a project with its own risk assessment rather than a routine chore.

## Plugin compatibility testing

OJS installations tend to accumulate plugins over years — for DOI registration, specific citation formats, institutional integrations. Every one of those is a dependency that might not survive a core upgrade cleanly. Before any real upgrade, the discipline is: inventory every plugin in use, check each one's compatibility with the target version, and test the combination somewhere that isn't production. It's not exciting work, but skipping it is how a routine upgrade turns into an outage.

## Rollback planning

Every upgrade needs a rollback plan you genuinely expect never to use, but keep ready anyway. That means a real database backup taken immediately before the upgrade starts, a documented sequence for reverting both the application and the data, and — critically — actually testing that the rollback works before you need it under pressure. A rollback plan you haven't tested is a hope, not a plan.

## Office automation that compounds

A meaningful chunk of time in this kind of role goes into automating recurring office workflows that have nothing to do with OJS directly — the documentation and process work that eats a department's time in small, repeated cuts. None of it is resume-flashy. But an hour saved on a recurring task once is a nice bonus; the same hour saved every week for two years is a real chunk of someone's working life handed back to them. That compounding effect is easy to underestimate and, in my experience, is where a lot of the actual value of this kind of role ends up living.
