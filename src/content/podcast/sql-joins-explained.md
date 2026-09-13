---
title: "SQL Joins Explained: INNER, LEFT, RIGHT and FULL JOIN"
shortDescription: "A clear, practical walkthrough of the four main SQL join types and when to actually use each one."
description: "Joins are the part of SQL that trip up even experienced developers once tables get more complex than a tutorial example. This episode covers INNER, LEFT, RIGHT, and FULL joins with concrete examples, plus the mental model that makes the difference between them click permanently instead of needing to be re-looked-up every time."
episodeNumber: 5
date: 2026-08-23
duration: "11 min"
featured: false
topics: ["SQL", "Databases", "Backend Development"]
inThisEpisode:
  - "The mental model: joins as combining rows, not tables"
  - "INNER JOIN — only matching rows"
  - "LEFT and RIGHT JOIN — keeping everything from one side"
  - "FULL JOIN — keeping everything from both sides"
  - "How to pick the right join without memorizing a chart"
timestamps:
  - { time: "00:00", label: "Introduction" }
  - { time: "01:10", label: "The mental model for joins" }
  - { time: "03:00", label: "INNER JOIN" }
  - { time: "05:20", label: "LEFT and RIGHT JOIN" }
  - { time: "08:00", label: "FULL JOIN" }
  - { time: "09:45", label: "Picking the right join in practice" }
resources:
  - { label: "My Campus Management project (Java + Oracle SQL)", url: "/projects" }
relatedArticles: []
relatedEpisodes: ["running-ojs-in-production"]
seoTitle: "SQL Joins Explained — INNER, LEFT, RIGHT and FULL JOIN with Examples"
seoDescription: "A practical explanation of INNER, LEFT, RIGHT, and FULL SQL joins, with a mental model that makes them easy to remember."
---

## Introduction

Joins are one of those SQL topics that feel clear in a tutorial with two tiny example tables, then get confusing the moment you're working with real schema. This episode is a practical walkthrough of the four main join types, aimed at making the difference between them stick permanently.

## The mental model for joins

Before the syntax, the mental model: a join doesn't combine *tables*, it combines *rows* based on a matching condition you specify, usually a shared key like a customer ID. Every join type is really just a different answer to the same question: "what happens to rows that don't have a match on the other side?"

## INNER JOIN

INNER JOIN is the strictest option: it only returns rows where the join condition matches on both sides. If a customer has no orders, that customer simply doesn't appear in the result at all. This is the right choice when you genuinely only care about complete pairs — for example, a report of orders that must, by definition, have both a customer and a product attached.

## LEFT and RIGHT JOIN

LEFT JOIN keeps every row from the left (first-listed) table, whether or not it has a match on the right — unmatched columns from the right table just come back as NULL. This is the join you reach for when the "no match" case is itself meaningful information: "show me every customer, and their most recent order if they have one" needs a LEFT JOIN, because a customer with zero orders is still a customer you want in the result.

RIGHT JOIN is the mirror image — keep everything from the right table instead. In practice, most people rarely use RIGHT JOIN directly; you can always rewrite it as a LEFT JOIN by swapping which table you list first, and most style guides prefer that for consistency.

## FULL JOIN

FULL JOIN keeps every row from both sides, matched where possible and NULL-padded where not. It's the least commonly needed of the four in typical application code, but it's the right tool when you're doing a reconciliation-style query — "show me every record from both systems, matched where they agree, so I can see what's missing from each side."

## Picking the right join in practice

Instead of memorizing a chart, ask one question: does a row with no match matter to what I'm trying to show? If no, INNER JOIN. If yes, and it matters for one specific side, LEFT JOIN with that table listed first. If it matters for both sides at once, FULL JOIN. That question resolves the choice faster than trying to recall which acronym does what.
