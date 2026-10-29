# Case 604 — Rocket Pool slice 2: four statements, and the one that failed first

**Date:** 2026-10-29 · **Direction:** grant evidence · **Status:** closed — evidence published, no money moved

**In one line:** the second slice of the rETH invariant witness adds four statements about the deposit pool and
the exchange rate; one of them failed because the model behind it was wrong, which is the reason to trust the
other three.

## Why a second slice at all

The grant application (`dao.rocketpool.net/t/4070`, post #10) promises milestones M1–M4. M1 — mint, burn,
exchange rate — was already green on five forks. A milestone list is a promise; a second working slice is
evidence that the cadence is real. It also tests whether the method generalises beyond the one path it was
built for.

## The four statements

File: `test/DepositPoolInvariants.t.sol`. Addresses are **not hardcoded** — they are derived from
`RocketStorage.getAddress(keccak256("contract.address" + name))`, so the harness documents where each contract
comes from and cannot silently drift from the deployment.

| statement | value at block 26 294 800 | what it rules out |
|---|---|---|
| deposit pool balance ≤ declared maximum | 16.34 ETH vs 6 000 000 ETH cap | the pool holding more than its own cap |
| network total ETH ≥ pool balance | 362 610 ETH vs 16.34 ETH | the pool accounting for ETH absent from the network total |
| `getExcessBalance()` ≤ `getBalance()` | — | excess being an independent counter rather than a subset |
| rETH rate within 0.1% of network-total / supply | — | the rate being read from a different source |

Runs: block **26 294 800** and block **26 290 581**, both **4/4 passed**.

## The statement that failed, and why that is the point

The rate check was first written against `RocketTokenRETH.getTotalCollateral()`. That call returned
**2 645 ETH**, while `getExchangeRate()` was **1.1746** and `totalSupply()` was **308 566 rETH**. For a
collateral figure that is arithmetically impossible: a 1.17 rate over 308 566 rETH requires ≈ 362 600 ETH of
collateral.

The correct source is `RocketNetworkBalances.getTotalETHBalance()` — **362 610 ETH**. With that, the identity
holds within 0.0455%, which is exactly the size of the drift you expect between a daily oracle update and a
live `totalSupply()`.

Three lessons, all of them the same lesson:

1. A test that validates *our reading of a contract* must be able to fail. This one did.
2. The tolerance (0.1%) is not slack — it encodes the oracle cadence. Writing strict equality would have been
   a stronger-looking and false claim.
3. The failure was not a protocol finding. Publishing it as one would have been the error this repository
   exists to prevent.

## Receipt

`tools/witness_receipt.py --block 26294800` now covers **eleven statements** (7 from slice 1 + 4 from slice 2):
**11/11 passed**, `forge_exit_code: 0`, `signed: false`.
`tools/verify_receipt.py receipts/26294800.json --rerun` recomputes the input digests and re-runs the suite:
the set and statuses match exactly. The verifier also prints what it cannot establish — block provenance
without a signature — rather than implying it.

## What this case claims

- Four new statements hold on two pinned blocks, and the harness derives its contract addresses from storage.
- One of the four was wrong on the first attempt, the error is documented, and the correction is in the file's
  comments for the next reader.
- The receipt covers all eleven statements and is independently re-runnable.

## What it does not claim

- Nothing here is a theorem. These are `test`, not `proof`; no Lean model has been checked for these paths.
- Coverage stops at the deposit pool and the rate source. Minipool distribution, node-operator collateral,
  withdrawal queues and bridge paths are not covered — that is milestone M3 and it is written into
  `NOT-CLAIMED.md`.
- A green suite on two blocks says nothing about blocks it was not run on.

## Verdict

**Confirmed — 4 statements, 4/4 on two blocks, 11/11 in the receipt; one statement initially failed on a wrong
collateral source and the model was corrected before it passed.**
