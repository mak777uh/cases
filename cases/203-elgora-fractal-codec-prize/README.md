# Case 203 — A bounty we entered, won, and got paid for

**Date:** 2026-10-27 (settled) · **Direction:** paid scientific challenge · **Status:** **awarded and paid on-chain**

**In one line:** Elgora bounty #1 — "build a coding-efficient, parallel fractal image codec" — was judged by
three independent AI reviewers in our favour, and the prize **24.464537 USDC** was released from escrow to our
wallet, then forwarded to the operator. Every step is a transaction with a hash.

## Why this case exists

Most cases in this repository document a claim that someone else could check. This one documents a claim that
resolved: the challenge was funded on-chain, judged, and paid. It is the reference point for what the rest of
the work is trying to reach, and it is also the honest baseline — one win out of two attempts in that round.

| fact | value |
|---|---|
challenge | [`elgora.ai/bounties/1`](https://elgora.ai/bounties/1) — funded scientific challenge, "Awarded" |
what was asked | a self-contained fractal (PIFS) image codec for 8-bit grayscale and RGB; bitstreams judged on quality at **fixed byte budgets** |
participants | multiple; our solver wallet `0xAE04394FB67dDd0E217a729c3E2484Ac4687fE20` |
judging | three independent AI Guardians — Dark Tang, Rare Mussel, Loud Abalone — **all three awarded to us** |
escrow → settlement | `27.182818` USDC escrow, guardian fee `2.718281`, **settlement `24.464537` USDC** |
result | **won**, then claimed, then transferred to the operator's wallet |

## What was built

A Python + NumPy codec (internally "FRC2"), delivered as bitstreams plus a full format specification and a
results table:

| component | approach |
|---|---|
| transform | orthonormalised (mean-removed) affine map, 8 isometries |
| partitioning | quadtree blocks 32 → 4 |
| domain coding | offset from the "home" cell |
| entropy coder | adaptive binary **range coder** with per-syntax contexts |
| optimisation | Lagrangian **RD-optimisation**, rate control by λ bisection — byte budget used **99.3–100 %** |
| post-processing | refinement on the decoded attractor + normative deblocking filter |
| colour | **YCbCr 4:2:0**, channel weights derived for RGB-PSNR |
| performance | multi-threaded domain–range search (1 and 4 threads) |
| artifacts | **36 bitstreams**, format spec, report, `results.csv`, sources |

## Results

- Mean gain over JPEG: **+1.83 dB**, with the acceptance threshold at **−1.00 dB**.
- By class: natural **+2.36**, texture **+0.90**, high-res **+2.13**, text **+1.03** dB.
- Decoding from initial images of all-0 and all-255 produced **identical** output (difference 0).
- Bit accounting matched file size **exactly** on all bitstreams.

## Evidence (all on Base, public)

| step | transaction | block |
|---|---|---|
| submission of bounty #1 | `0x32615fe95ef78e4049bf84a2cef7451c01d7b20a47687eb845aae38626f5913d` | 52643564 |
| contract published the verdict (`status: awarded`, winner = our wallet) | `0x2ce3285eca6dc550d4b128a9d1ddbb15392d21bce9c589b172fe6cf55248a327` | 53147544 |
| claim by our wallet — **24.464537 USDC** | `0xb84eab8b472b3557ecc58dd24c3a8da471c69dbdd4ca4d42d74f1d34f2f4ae50` | 53150232 |
| transfer of the prize to the operator's wallet | `0x375ee9a85875aae281715abf0f71dcbb7040c0891f4b7e6a69ee237ac9b0f862` | 53150256 |

Balances after the transfer: our wallet `0.000000` USDC, operator's wallet **28.707099** USDC
(24.464537 prize + 0.4047 that was already sitting there). Gas for both operations ≈ **$0.0006**.

## Uncomfortable part, kept on purpose

Bounty **#0** in the same round — a different challenge, 42.69 USDC — was **not** won: one Guardian judged
that no valid submissions existed, the other chose another participant. The lesson recorded at the time:
a funded challenge can pay one participant and reject the rest, and the entry cost is time, not money.

## Reproducing this case

Nothing here needs our infrastructure: open the four transactions above in BaseScan, read the verdict page,
and compare the numbers. The codec sources and `results.csv` were delivered through the platform's submission;
they are not stored in this repository, so the runnable artifact here is the **chain record**, not the code.

**Status:** closed — paid.
