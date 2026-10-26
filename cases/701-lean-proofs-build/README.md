# Case 701 — Lean proofs of the audits repo compile with no `sorry`

**Date:** 2026-10-26 · **Direction:** formal verification · **Status:** complete

**In one line:** Six Lean 4 proof files from the public audits repository were compiled one by one: all six are accepted by Lean's kernel, 34 theorems and lemmas, zero `sorry` or `admit`.

## Claim

The `proofs/` directory of [mak777uh/audits](https://github.com/mak777uh/audits) contains six Lean 4 files
(escrow, value flows, flow invariants, ledger, operation stack, value path). Each compiles with exit code 0 on
Lean 4.36.0-rc1, and the sources contain no `sorry` and no `admit`. This makes "kernel-checked, no sorry"
checkable rather than asserted.

## Evidence

| item | value |
|---|---|
files | 6 (`escrow`, `flows`, `flows_info`, `ledger`, `op_stack`, `valuepath`) |
compile result | **6 / 6 exit 0** |
theorems + lemmas | **34** |
`sorry` / `admit` occurrences | **0** |
toolchain | `Lean (version 4.36.0-rc1, x86_64-w64-windows-gnu)` |
full log | [artifacts/BUILD_LOG.md](artifacts/BUILD_LOG.md) |

## Reproduce

```bash
git clone https://github.com/mak777uh/audits
cd audits/proofs
lean --version
for f in *.lean; do lean "$f" || echo "FAIL $f"; done
grep -c -E 'sorry|admit' *.lean
```

The script used for this case is [artifacts/build_check.py](artifacts/build_check.py) (Python 3, calls `lean`).

## Verdict

**confirmed** — all six files compile cleanly and contain no `sorry`/`admit`.

## Limits

- per-file compilation, not `lake build` of a single project: there is no lakefile yet, so this proves each file
  is a valid Lean development on its own, not that they compose into one library;
- it says nothing about whether the *statements* model any real protocol correctly — only that Lean accepts the proofs;
- no `#print axioms` audit is included, so "standard axioms only" is not established here;
- two files emit deprecation warnings (`if_true`/`if_false`), which do not affect correctness.
