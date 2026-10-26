# Cases

Public record of verification work: what was done, what proves it, what the result was, and how to
reproduce it.

Most repositories show results. This one shows **the checking**: three transactions compared field by field,
a patch against deployed code, a paper sentence compared with its formal version. Where the answer was
"could not tell", it says so.

## Three finished examples

| case | what was checked | result |
|---|---|---|
| [201](cases/201-flapjax-payout-verification/) | Three FLAPJAX payouts: sender, recipient, amount, token, block | **confirmed**, 12 of 12 fields matched |
| [101](cases/101-specter-sd-delete/) | A patch for Specter DIY (SD-card file deletion): does it apply, is the defect real | **confirmed** patch exists; acceptance unknown, PR is open |
| [601](cases/601-statement-scope-review/) | A paper's claim compared with its Lean formalisation | **not confirmed**: the formal statement is stronger than the prose |

More in [REGISTRY.md](REGISTRY.md) (generated from the folders, so it cannot drift).

## How a case is organised

```
cases/NNN-slug/
├── README.md   # claim, evidence, reproduce, verdict, limits
└── evidence.md # optional: links with what each one proves
```

Five short sections, always in the same order:

1. **Claim**: what was done, plain sentences.
2. **Evidence**: a table of links or tx hashes, and what each one proves.
3. **Reproduce**: the exact commands.
4. **Verdict**: `confirmed`, `not confirmed`, or `could not tell`.
5. **Limits**: what this case does not establish.

## Rules

- Every claim needs a public link, a transaction hash, or a pinned commit. Otherwise it is an opinion.
- Numbers come from a script and carry a date. A stale count is a wrong count.
- "Not confirmed, here is why" counts the same as "confirmed". Both are published.

## Repo description for the sidebar

> Public record of verification work: claim, evidence, verdict (including "not confirmed"), and the commands to reproduce it.

---

На русском: здесь лежат разборы, а не витрина. В каждой папке один разбор: что проверяли, чем
подтверждается (хеш транзакции, коммит, ссылка), что получилось и как это повторить. Реестр в
REGISTRY.md собирается из папок автоматически.
