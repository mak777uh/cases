# Case 601 — A statement-scope review that ended "not confirmed"

**Date:** 2026-10-23 · **Direction:** bug hunt (research claim) · **Status:** published in a public issue thread

**In one line:** A paper's sentence compared with its formal (machine-checked) version. They do not say the same thing. Verdict: not confirmed.

## Claim

A published claim (Run-129 / C4, bounded overshoot) was compared line by line against its Lean
formalisation. The two do not say the same thing: the Lean statement adds a two-sided boundedness
hypothesis that the prose does not contain. The maintainer of the repository agreed that the scope
distinction is real. Nothing was paid, and no payment was claimed.

## Evidence

| what | link | proves |
|---|---|---|
| Issue thread | https://github.com/jdhart81/viridis-canon/issues/121 | the review, the pinned source locations, and the maintainer's reply |
| The maintainer's agreement | reply dated 2026-10-22 in the same thread | "the scope distinction is real" |
| Our follow-up | comment dated 2026-10-23 | the open question: is the finding eligible for the bounty |

## Reproduce

1. Open the issue above and read the first comment: it names the paper's sentence, the Lean declaration,
   and the extra hypothesis.
2. Compare with the pinned file and line in the repository at the commit named in that comment.
3. The verdict is in the comment itself: **not confirmed** — the formal statement is stronger than the
   prose claim, so the formal result does not transfer to the paper's claim as written.

## Verdict

**Not confirmed** — with reasons, and the maintainer concurred on the scope distinction. This case is
published as "not confirmed" because that is what the evidence supports; it is worth the same as a
confirmed finding, and it is the honest form of the result.

## Limits

- We checked the statement, not the mathematics of the paper as a whole.
- The question of eligibility for the project's bounty is unresolved; the maintainer has not answered
  whether this counts, and we did not press for a payment.
- No counterexample is offered here — only a scope mismatch between a claim and its formalisation.
