# Prelint — capabilities and hackathon fit

*Mathieu’s preparation note · 28 September 2026*

## What it does

Prelint is a product-alignment reviewer for GitHub pull requests. It reads specifications, architecture decisions, API contracts, and other context, then checks a proposed code change for requirement violations, decision drift, business-logic mistakes, scope changes, and outdated documentation. Findings appear as comments on the relevant lines, with a review summary and GitHub check. It can review new commits on the same PR. Its MCP connection also lets AI agents search and record product decisions before coding. [Product overview](https://prelint.com/docs) · [Review details](https://prelint.com/docs/how-reviews-work) · [MCP](https://prelint.com/docs/mcp)

Prelint focuses on whether the implementation matches the agreed product intent. It does not replace tests, a code linter, type checking, or a security scanner. [Review scope](https://prelint.com/docs/how-reviews-work)

## Main usage

1. Connect the GitHub repository to Prelint.
2. Put the relevant product rules and decisions in repository Markdown or Prelint’s decision ledger.
3. Open a pull request. Prelint reviews the diff against that context and posts findings.
4. Resolve valid findings and review again when the PR changes.

The published price is **US$1 per completed PR review**; a completed review after new commits is charged separately. New organisations currently receive US$10 in free credits. [Pricing](https://prelint.com/pricing)

## My view for our hackathon

The idea is useful: code can run correctly yet miss the customer need or break an agreed business rule. For a larger project with many contributors and decisions spread across time, automatic checks and a shared decision history could save review effort.

For our **four-hour prototype**, I would **not set up Prelint**. We have three people, a small codebase, and a direct branch-merge workflow with no PRs. Its main review mechanism therefore does not fit our process, and setup plus repeated review would consume time better spent on integration and the demo. A focused AI review using the released brief, our Must-have acceptance criteria, and the actual code diff should cover the relevant product-alignment check. We still need to run the main user journey and a failure scenario ourselves.

## Our simpler alignment check

We can use Prelint's **method** without installing it. After selecting the MVP, write a few observable acceptance criteria from the brief and agreed Must-have scope. When the first end-to-end slice is integrated, or a meaningful scope or behaviour change raises doubt, compare the build with those criteria:

- Does every Must-have criterion have a working, visible result? Are business rules and challenge constraints respected?
- Do frontend, backend, and the demo story describe the same behaviour? Are errors, uncertainty, and customer approval handled where relevant?
- Has optional work displaced a Must-have, or does the pitch claim something we cannot demonstrate?

Mathieu can ask an AI reviewer to inspect the brief, criteria, decisions, and code diff for **concrete, evidence-backed mismatches**. The team then decides what to fix and runs the agreed normal and failure scenarios. This is a short product-alignment gate when useful, not a review on every commit.

**Decision:** We do not plan to use Prelint for this hackathon. Its absence will not weaken the prototype if we review the agreed requirements and run the demo checks ourselves.
