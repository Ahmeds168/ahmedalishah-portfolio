---
title: "Modernizing a university's journal system: lessons from running OJS in production"
excerpt: "What two years of administering Open Journal Systems for a real department actually looks like day to day."
category: "systems"
categoryLabel: "Systems & Infrastructure"
categoryColor: "#5B8CFF"
banner: "/images/banner-ojs.svg"
metaLine: "Notes · Software Development Intern, Sukkur IBA University"
order: 2
stack: ["OJS", "Sysadmin"]
---

Open Journal Systems (OJS) is the piece of software that quietly runs a huge share of the world's academic journals — including several at Sukkur IBA University's Department of Electrical Engineering, which I administered and upgraded during my time as a Software Development Intern. It's not glamorous work, but it taught me more about running production software for real users than any greenfield project has.

## Upgrades are the scary part, not new features

Building a new feature is fun because if it breaks, it just doesn't ship. Upgrading a system that editors, reviewers, and authors already depend on is a different kind of pressure — a botched upgrade doesn't just fail quietly, it breaks an active submission cycle for real academics with real deadlines. Most of the actual skill in this role was in staging upgrades carefully, testing plugin compatibility beforehand, and having a rollback plan that I genuinely expected never to need but always kept ready anyway.

## Office automation is undervalued

A meaningful chunk of my time went into automating recurring office workflows that had nothing to do with OJS directly — the unglamorous documentation and process work that eats a department's time in small, repeated cuts. None of it is resume-flashy, but it's the kind of work that compounds: an hour saved on a recurring task once is fine, saved every week for two years is a real chunk of someone's working life back.

## Owning the whole website, not just a feature

Being responsible for the entire department website administration — not just "the frontend" or "the CMS" — meant genuinely owning uptime, content updates, and whatever broke on a given day, regardless of whether it was originally "my" code. That end-to-end ownership is a different muscle than shipping a scoped feature in a sprint, and it's one I think more developers should build early, even if it's less exciting than greenfield work.
