# Case 603 — 24 bounty tasks, triaged; none of them is free money

**Date:** 2026-10-29 · **Direction:** bounty triage · **Status:** closed — no submission

**In one line:** a board paying $50–$100 per Lean proof of a pinned Erdős statement was triaged end to end;
the honest result is that **no task is closed by automation**, and the first model-driven attempt failed to
produce a compiling proof.

## What the opportunity was

`zzzagents.com` pays **50–100 USDC** for a Lean 4 proof of a pinned declaration **or of its negation**,
checked by `#print axioms` against `{propext, Classical.choice, Quot.sound}`, with statements pinned to
`formal-conjectures@b82b08f` (Lean 4.33.1, Mathlib v4.33.1). The pool is 100 USDC; the first verified proof
per problem wins. Twenty-four tasks were listed.

## What was built to test it

The blocker was not the maths but the toolchain: the pinned dependency tree does not build out of the box on
this machine, and its `package.json`-equivalent pins two dependencies to branches whose GitHub repositories
are not publicly reachable. Working path found:

1. Lean **v4.33.1** toolchain downloaded directly (583 557 483 bytes; the `lake` downloader aborts mid-stream
   through the proxy, a resumed `curl` works) and installed into `~/.elan/toolchains/`.
2. `formal-conjectures@b82b08f` cloned; `mathlib v4.33.1` fetched as a **shallow clone at the tag** (99 MB in
   under a minute) rather than a full clone — the difference between minutes and hours.
3. Mathlib olean cache pulled by `lake update` (8 690 files, 6.3 GB); disk fell to **0.25 GB** and two unused
   Lean toolchains (4.34.1, 4.36.0-rc1) were deleted to recover 6.18 GB.
4. **All 18 task modules compiled**, exit 0.

## The measurement, and the two false positives it produced

The triage runs, per task, the battery `trivial → rfl → decide → norm_num → omega → simp → aesop → exact?`
against the **type extracted with `#check`** (the declaration is a proof term, not a type — `example : <decl>`
does not compile).

Two parser bugs produced false "successes" and both were caught by manual verification:

| symptom | cause | fix |
|---|---|---|
five tasks "closed by `omega`" | tactic line numbers computed by arithmetic instead of from the assembled file | line numbers taken from the actual file |
**all 24 tasks "closed by `exact?`"** | Lean reports unsolved goals on the **`example` line**, not the tactic line; the last tactic's `line+1` fell outside the file | match both the example line and the tactic line |

Verified independently: `exact?` on the false goal `(1:ℝ)+1 = 3` does fail with "could not close the goal",
so the tactic is honest — the parser was not.

## The result

**0 of 24 tasks are closed by any of the eight tactics.** A sample statement:

```lean
Erdos99.erdos_99 : sorry ↔ ∀ᶠ (n : ℕ) in Filter.atTop, ∀ (A : Finset (EuclideanSpace ℝ (Fin 2))),
  A.card = n → Erdos99.HasMinDist1 A → IsMinOn (fun B => Metric.diam ↑B) {B | B.card = n ∧
  Erdos99.HasMinDist1 B} A → ∃ p ∈ A, ∃ q ∈ A, ∃ r ∈ A, Erdos99.FormsEquilateralTriangle p q r
```

That is research mathematics, not a placeholder. The board's own note that one placeholder "elaborates to
True" is true of the placeholder, not of the statement: the type is `True ↔ P` where `P` is the real claim.

A free model (`poolside/laguna-s-2.1:free`) was then run in a "never give up" loop for 12 attempts on
`Erdos470.erdos_470.parts.ii`; every compiled attempt failed. Two attempts were lost to infrastructure, and
one of those turned out to be a **shared-channel bug**: two processes using the same model egress receive each
other's responses (a probe asking "say ok" returned another process's Lean code).

## What this case claims

- The environment is reproducible: toolchain, pinned Mathlib, 18 modules, all exit 0, commands recorded.
- The triage is wrong twice and both errors are documented with their fixes.
- No task on this board is reachable by off-the-shelf automation.

## What it does not claim

- That the tasks are unsolvable. They are solvable in principle; they are not solvable by a battery of
  tactics, and not by one free model in twelve attempts.
- That a better model would fail. DeepSeek V4 solved all 672 PutnamBench problems — but those are textbook
  problems with known answers, and the harness that did it ran for up to 78 hours per problem.

## Verdict

**Confirmed — 24 tasks triaged, 0 closed by automation, 1 free-model attempt failed to compile; no submission
was made and no money was spent.**
