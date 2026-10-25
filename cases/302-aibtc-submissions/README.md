# Case 302 — Three bounty applications on AIBTC, and why one is not ours

**Date:** 2026-10-25 · **Direction:** bounties and tasks · **Status:** applications in the pool, PoA blocked by the platform

## Claim

Three applications were submitted on AIBTC (sats rewards, no KYC): a Clarity-audit bounty (Kairan), an
onboarding bounty (WURK), and a Proof-of-Agent participation bounty (PoA). Two are in the judging pool.
The third — PoA — cannot be started at all, because the platform's registration endpoint has answered 503
for two days, and that is recorded here rather than hidden as "in progress".

## Evidence

| what | link | proves |
|---|---|---|
| Kairan bounty | AIBTC bounty id `mvllpuv02f876aa9c4be` | the bounty exists and our application is in it |
| WURK bounty | AIBTC bounty id `mvei12aee0bb1f58a330` | same |
| PoA bounty | AIBTC bounty id `mvmfawhs46e56f67d188` | the bounty exists; **not** our application — it is a referral bounty for another agent |
| Jing sBTC/USDCx audit | bounty `mvlqxozz934e1c757f88`, status `judging`, 10 submissions | our submission (if accepted) is inside a closed pool |
| Registration endpoint | `minepoa.com/api/hosted/register` → **401 Unauthorized** on 26.10 (it answered **503** for the two days before) | the PoA path is blocked by the platform, not by us: the error moved from «service down» to «credentials required» |

Correction recorded on purpose: an earlier internal note called bounty `mvmqcjxn49a80581f733` ours. It is
not — that is a PoA-referral bounty whose winner was announced, and checking it against a fresh bounty list
is how the mistake was found. The lesson is in the case so that the same mis-read does not happen twice.

## Reproduce

```bash
curl -s https://aibtc.com/api/bounties/mvllpuv02f876aa9c4be   # Kairan: status, submissionCount
curl -s https://aibtc.com/api/bounties/mvei12aee0bb1f58a330   # WURK
curl -s -o /dev/null -w '%{http_code}' https://minepoa.com/api/hosted/register   # → 401 on 26.10
```

## Verdict

**Confirmed** that the applications exist in the platform's pool.
**Not confirmed** for any payment: no bounty in this case has paid, and the PoA route is blocked by a 503.

## Limits

- Being in a judging pool is not a payout; the pools have dozens of submissions.
- The PoA stop condition is set by date: if registration is still 503 by 2026-10-29, the bounty is dropped.
- Bounty statuses change; this case is a snapshot dated 2026-10-25 and must be re-checked against the live
  API before being cited.
