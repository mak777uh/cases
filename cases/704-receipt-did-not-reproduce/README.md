# Case 704 — We tried to reproduce our own receipt and it did not reproduce

**Date:** 2026-10-31 · **Direction:** self-verification of a grant artifact · **Status:** defect found, fixed, published

**In one line:** The Starknet Seed Grant application claims its receipt is reproducible by a stranger. We
became the stranger: installed the pinned toolchain, cloned the repository, ran it. Six cells passed and
the program output matched — but **7 of 8 file hashes did not match the receipt**, because git on Windows
checks files out with CRLF while the receipt was hashed with LF.

## Why this case exists

Every other case in this repository documents a claim about someone else's system. This one documents a
claim about **our own artifact**, checked the only way that counts: by trying to reproduce it from
scratch on a clean machine.

It is also the first time in this repository that a verification attempt produced a **defect in our own
work** rather than a refutation of someone else's.

## What was done

| step | result |
|---|---|
Downloaded **scarb v2.21.0** (Windows build, 64.5 MB, official release) | `scarb 2.21.0 (fbd5bd03d 2026-10-09)`, `cairo 2.21.0` — exactly what `RECEIPT.json` pins |
Cloned `github.com/mak777uh/verified-cells-cairo` from scratch | ok |
Ran `scarb execute --print-program-output` | **all six cells PASS**, program output `1346458451` — matched the receipt |
Compared sha256 of the eight files in `RECEIPT.json` | **7 matched, 1 did not** |

## The defect

`Scarb.toml`: receipt says `70ed4f0c88106bfb…`, the file hashes to `be2a412cc3da590b…`.

Cause — line endings. Git on Windows checks the file out with CRLF (14 of them); the receipt was computed
over the LF version:

```
raw (CRLF):  be2a412cc3da590bcffdbaf68a221f1b272764590db41d0cbfb3b6d0aab445ea
CRLF → LF:   70ed4f0c88106bfbd26d8978a349d9893b7a51c34cc6ee53c5ad714ea3475f58   ← matched the receipt
```

## Why it matters

**A receipt that does not reproduce for the person who cloned the repository is not a receipt.** That
property — "a stranger can re-run it" — is the single thing the Starknet application sells. Any reviewer
on Windows would have got a hash mismatch and concluded the files had been altered.

**The defect was invisible to reading.** `make_receipt.py` contained `p.read_bytes()` — a line that looks
correct and is correct on the platform where it was written. Only running it on a fresh clone surfaced
the problem.

## What was fixed

| change | detail |
|---|---|
`make_receipt.py` | hashes `p.read_bytes().replace(b"\r\n", b"\n")`, with a comment stating the date and the reason |
`.gitattributes` | added: `* text=auto eol=lf` plus explicit rules for `*.cairo`, `*.toml`, `*.lock`, `*.md`, `*.py`, `*.json` |
`RECEIPT.json` | regenerated — **8 of 8 hashes now match**, `verdict: PASS`, `statement_sha256: 3af70404ba71f894…` |

Verified after pushing: `RECEIPT.json` → HTTP 200, verdict PASS, 8 files; `.gitattributes` → HTTP 200.

## Then the milestone it was blocking

The application's milestone M1 promises each cell a `bound_to` of **(address, selector, block)**. That is
now in the receipt, built before the deadline rather than promised for it:

| field | value |
|---|---|
`bound_to.address` | `0x04718f5a0fc34cc1af16a1cdee98ffb20c31f5cd61d6ab07201858f4287c938d` (STRK token, Starknet mainnet) |
`bound_to.class_hash` | `0x2e77ee61d4df3d988ee1f42ea5442e913862cc82c2584d212ecda76666498fc` |
`bound_to.block_number` | 17,203,591 |
`models` | six cells, each with the function it models and that function's Starknet selector |
`upgrade` selector | `0x00f2f7c15cbe06c8d94597cd91fd7f3369eae842359235712def5584f8d270cd` |

The selector is `keccak256(name) & (2**250 − 1)` — it does not depend on the contract, so anyone who knows
the function name can recompute it and check ours without trusting us.

## What this does not claim

The `bound_to.note` says it plainly: address, class hash and block are what the chain returned at build
time; **this does not assert that the cell models that contract's bytecode**. That gap is exactly what
milestone M1's second half is meant to close, and pretending otherwise would repeat the mistake this case
is about.

## Reproduce

```bash
git clone https://github.com/mak777uh/verified-cells-cairo
# install scarb 2.21.0, then:
scarb execute --print-program-output     # six cells PASS, output 1346458451
python make_receipt.py                   # rewrites RECEIPT.json with matching hashes
```

## Lesson

**Verification of your own artifact is not a formality.** The line `p.read_bytes()` was correct and the
artifact was still wrong, because correctness depended on a platform detail nobody wrote down. The only
way to find it was to be the stranger the document promises.
