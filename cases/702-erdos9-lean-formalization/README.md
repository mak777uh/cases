# Case 702 — Erdős #9 in Lean: a proof that builds, on a platform that cannot take it

**Date:** 2026-10-30 · **Direction:** formalization / bounty attempt · **Status:** proof verified locally; submission blocked by the platform's own API

**In one line:** We assembled the published Lean formalization of Erdős problem #9, built it to a clean
`0 sorry / 0 non-standard axioms` state, and then found that the bounty platform's submission endpoint
returns 404 — so the proof exists and is checkable, but cannot be filed.

## Claim

The Erdős problem #9 (Erdős credits Schinzel) states that infinitely many odd integers are not of the form
`p + 2^k + 2^l`. The `formal-conjectures` repository carries the statement with a `sorry` **and an annotation
naming an existing Lean proof**:

```lean
@[category research solved, AMS 5 11, formal_proof using lean4 at
  "https://github.com/linrock/math-proofs/blob/de08009e.../erdos-9/Solution.lean#L25"]
theorem erdos_9.variants.infinite : Erdos9A.Infinite := by
  sorry
```

That annotation is the whole method: **the proof was not re-derived, it was located.** We fetched
`erdos-9/Proofs/Erdos9Unified435.lean` (124 KB), built it against our own mathlib, and confirmed the
statement holds with only the standard axioms.

## Evidence

| what | value | proves |
|---|---|---|
build result | `code 0`, 237 lines of output, **0 errors** | the file compiles under Lean 4.36.0-rc1 + mathlib |
`#print axioms Erdos9.erdos9A_infinite` | `[propext, Classical.choice, Quot.sound]` | only the three standard axioms; no `sorryAx` |
textual scan for `sorry` / `axiom` in 124 KB | **0 hits** | no hidden gaps |
gate (`env\ops\lean_proof_loop.py gate`) | `sorry: нет · нестандартные аксиомы: нет · ГЕЙТ ПРОЙДЕН` | the file passes the same gate we use for our own work |
platform submission API | `POST api.mathbounty.com/verify-and-sign` → **404** (also `/api/verify-and-sign`, `/verify`, `/submit`, `/api/submit`, `/api/verify`) | the platform's own frontend calls an endpoint that does not exist |
bounty contract `0xd35D606B9e54200F9eCe815A19b1B9f72D8f5d42` | code present **only on Sepolia** (4 438 bytes, 0.019 ETH); absent on Ethereum and Base | the reward lives on a testnet |
`isClaimed(9)` | `0` | the problem was still unclaimed when we checked |
`isClaimed(0)` | `1` | someone did complete the flow once, so the contract path is not dead |

## Reproduce

```bash
# 1. the annotation that points at the existing proof
curl -s https://raw.githubusercontent.com/google-deepmind/formal-conjectures/HEAD/FormalConjectures/ErdosProblems/9.lean | grep -A2 "formal_proof"

# 2. the proof itself
curl -sO https://raw.githubusercontent.com/linrock/math-proofs/de08009e59829727653bfa20b8d8f7ed1b1baf79/erdos-9/Proofs/Erdos9Unified435.lean

# 3. build it (needs Lean 4.36 + mathlib; ours took 244 s)
lake env lean Erdos9Unified435.lean

# 4. the platform's endpoint, as its own frontend calls it
curl -s -o /dev/null -w '%{http_code}\n' -X POST https://api.mathbounty.com/verify-and-sign
# → 404
```

## Verdict

**Confirmed:** the formal proof of Erdős #9 exists, builds cleanly, and uses only standard axioms. The
method that produced it — read the `formal_proof using lean4 at` annotation instead of searching for a
proof — turns "days of mathematics" into "hours of assembly", and that is the transferable result.

**Not confirmed:** that the bounty can be claimed. Three independent blockers, two outside our control:
the submission API returns 404, the faucet that would supply testnet gas rejects our IP range, and the
reward is denominated on Sepolia — test currency, not value.

## What this case does not claim

- that we wrote the proof. We did not; Linmiao Xu did, under Apache-2.0, and `formal-conjectures` already
  names it as the formal proof for this statement.
- that the platform is fraudulent. It may be unfinished rather than dishonest; the contract exists and one
  problem has been claimed.
- that the proof is worth $100. On Sepolia it is worth nothing in money, and its value here is as a
  reproducible artifact.

## Addendum (2026-10-30, 17:20) — the platform's API is dead from the browser too, and most "open" problems already have proofs

**The API is not merely returning 404 to us.** Its own frontend calls
`https://api.mathbounty.com/verify-and-sign`; running the same `fetch` from the page context on
`mathbounty.com` gives `TypeError: Failed to fetch`. The submission backend does not exist, so no proof can be
filed by anyone through the site.

**And the problems are not as open as the page suggests.** Cross-referencing the `formal-conjectures` files for
ten of the platform's OPEN problems against their `formal_proof using lean4 at` annotations:

| problem | formal proof already exists | where |
|---|---|---|
| #1 | yes | `tadamcz/erdos1` |
| #3 | yes | `openai/math` |
| #9 | yes | `linrock/math-proofs` (the one we built) |
| #10 | yes | `linrock/math-proofs` |
| #36 | yes | `linrock/math-proofs` |
| #189 | yes | `plby/lean-proofs` |
| #97, #137, #145, #188 | no | — |

**Six of ten "open" problems already have a Lean proof somewhere.** If the sample holds, roughly sixty of the
platform's 102 open problems are an assembly job rather than a mathematics job — which is the real, transferable
finding of this case, independent of whether the platform ever comes back.
