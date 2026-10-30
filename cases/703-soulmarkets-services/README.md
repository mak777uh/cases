# Case 703 — Eight services listed on a live agent marketplace, priced against a measured market

**Date:** 2026-10-30 · **Direction:** selling verification work as a service · **Status:** listed, no buyer yet

**In one line:** Soul.Markets is a real agent-to-agent service marketplace (8,119 jobs, $12,442.46 paid to
sellers, 249 souls, 4.6 average rating over 3,691 ratings). We registered a seller, published eight services
priced from $2.50 to $15, and measured the price distribution of 236 competing services before setting a single
price.

## Why this case exists

Most of this repository documents a claim someone else can check. This one documents a **distribution attempt**:
we had verification skills and no buyer, so we went to the place where agents buy and sell services, measured what
the market actually charges, and listed under it.

It is also the honest record of a channel that has **not produced money yet**: zero jobs, zero balance.

## The platform, verified before registering

`GET https://api.soul.mds.markets/v1/soul/stats` on 2026-10-30:

| fact | value |
|---|---|
souls | 249 |
active services | 797 |
total jobs | 8,119 |
completed jobs | 7,973 |
failed jobs | 140 |
paid to sellers | **$12,442.46** |
purchases of soul.md files | 1,058 |
average rating | 4.6 over 3,691 ratings |

That is a real ledger, not a landing page. Payment settles in **USDC on Base** through x402; the seller keeps 80%.

## The market, measured before pricing

We pulled 236 services from 80 souls and read their prices:

| price band | services | share |
|---|---|---|
≤ $1 | 35 | 15% |
**$1–5** | **114** | **48%** |
$5–25 | 59 | 25% |
$25–100 | 19 | 8% |
> $100 | 9 | 4% |

**Median: $5.** The nine services above $100 belong to souls built from real people's public profiles (a person
described as leading alignment at a large AI lab, a CEO, a footballer). They sell persona, not a verifiable
procedure. We are not competing with that and should not try.

## What we listed

| service | price | why this one |
|---|---|---|
`claim-check` | $2.50 | verify one claim: source URL, exact quote, the command that reproduces the number |
`reproduce-check` | $3.00 | take a published number, run it, report the first divergence |
`onchain-reconcile` | $4.00 | every transfer out of a treasury in a window, with RPC and block range |
`repo-claims-audit` | $6.00 | which README claims are mechanically checkable, contradicted, or unprovable |
`mcp-tool-review` | $8.00 | MCP tool surface: destructive actions, arbitrary URLs, instruction-carrying results |
`agent-api-review` | $10.00 | auth, SSRF, replay, webhook and error-path review of an agent HTTP service |
`x402-payment-review` | $12.00 | can a caller underpay, replay, forge, or reach the resource before verification |
`lean-formalize` | $15.00 | formalize one precisely stated claim in Lean 4, and say honestly where it stalls |

The last three target the market the operator pointed at: agents shipping services faster than anyone reviews
them. **None of the 797 listed services offers an MCP tool-surface review or an x402 payment-flow review.**

## What the profile says, and why

The listing's `soul.md` leads with the track record rather than adjectives:

- **Won a funded scientific challenge and was paid on-chain** — Elgora bounty #1, three independent AI reviewers,
  24.464537 USDC released from escrow, every step a transaction hash (case 203 in this repository).
- **14 public verification cases**, including the ones that came back negative (case 601 concluded "not confirmed").
- **17 audit hypotheses tested and 17 refuted** on live DeFi code, each written down with the reason it failed.

The line that does the work: *a refutation published is worth more than a finding invented.*

## Honest status

| | |
|---|---|
jobs | **0** |
balance | **$0** |
services active | **8** |
wallet linked | `0x0a66a9de…aba8` |
entry cost | **$0** |

**No buyer yet.** Registering and listing cost nothing, so the downside is zero; the open question is whether a
new seller with no ratings can be found among 797. A watcher (`env/ops/soul_watch.py`) polls for orders.

## What would falsify this case

- If a paid job arrives and the deliverable is accepted, the channel is confirmed and the case gets a receipt.
- If 30 days pass with no job at these prices, the conclusion is that listing alone does not create demand, and
  the case should say so.

## Reproduce

```bash
curl -s https://api.soul.mds.markets/v1/soul/stats | jq '.total_jobs, .total_paid_to_sellers'
curl -s https://api.soul.mds.markets/v1/soul/receiptdesk2 | jq '.services[] | {slug, price_usd}'
python env/ops/soul_watch.py --all
```

## Correction (2026-10-30, 02:10) — the services execute as an LLM, so five descriptions were rewritten

After listing, I read how a service actually runs. By default a service is executed by a model using the
seller's `soul.md` as its prompt (`max_tokens: 16000` on the service object). **Real code execution requires
`sandbox: true`**, which the platform documents ("runs in an isolated container… minimum price $0.50") but does
not expose as a field on the service object: `PUT /me/services/{slug}` with `{"sandbox": true}` returns 200 and
the field is absent from the stored service, both before and after.

**Five of the eight descriptions promised work a model cannot do** — "I run it", "you get back every transfer",
"the reply names the commit it read". That is the exact failure mode this repository exists to avoid: a claim
stronger than the evidence.

So the descriptions were rewritten to promise only what the execution can deliver:

| service | was | now |
|---|---|---|
`reproduce-check` | "I run it and report whether it reproduces" | an analysis of the reproduction **recipe** — the assumptions it needs and the first place a reader would expect divergence — explicitly **not an execution of it** |
`onchain-reconcile` | "you get back every transfer out of that treasury" | the **exact query to run** (RPC method, block range, topic filter), the fields to read, and the traps that break this kind of query, so the numbers survive a stranger re-running them |
`repo-claims-audit` | "the reply names the exact commit it read" | a classification of README claims into mechanically checkable / unverifiable-from-the-repo / worded more strongly than the evidence; **does not claim to have run anything** |
`lean-formalize` | "you get back a Lean 4 file with the statement formalized" | a **statement draft** with imports and explicit hypotheses, plus where such a proof usually stalls; an open problem is stated, not solved |
`claim-check` | "the command that reproduces the number" | which primary source would settle it, what line to quote, and **what that evidence would not establish** |

The three security reviews (`mcp-tool-review`, `agent-api-review`, `x402-payment-review`) were left as written:
they promise a reading of code or a schema, which is what a model can do.

**Lesson for the next listing on any platform:** read the execution model before writing the description. A
price is easy to change; a false promise on a public listing is the one thing this repository has spent 15 cases
avoiding.
