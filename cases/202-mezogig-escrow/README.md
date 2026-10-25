# Case 202 — MUSD escrow deployed on Mezo testnet, verified, and reasoned about

**Date:** 2026-10-23 · **Direction:** on-chain verification · **Status:** deployed to testnet, submitted to a grant round

## Claim

A milestone escrow in MUSD was written, tested and deployed to the Mezo testnet. It releases funds on
delivery, splits to an arbiter path on dispute, and has an explicit client-silence path so funds cannot sit
forever. The contract source is published and Sourcify returns an exact match. Twelve invariants about it
are stated in Lean 4 and kernel-checked, with a coverage matrix that says which of them are proved, which
are only tested, and which are not covered at all.

## Evidence

| what | link | proves |
|---|---|---|
| Deployed contract | `0x247b313d0eD3C532B16c7E5f9eA760272361600F` on Mezo testnet | the escrow exists on a live chain |
| Source match | https://sourcify.dev/server/v2/contract/31611/0x247b313d0eD3C532B16c7E5f9eA760272361600F | Sourcify answers `exact_match` for creation and runtime, verified 2026-10-19T16:45:17Z |
| Test suite | `90 tests`, 100% statement coverage in the repository | the behaviour is exercised, not just described |
| Invariants | Lean 4 models under `formal/`, 12 theorems | the safety claims are machine-checked, not prose |
| Submission | AKINDO "Build with MUSD and MEZO" round | the work was entered into the grant round |

## Reproduce

```bash
# contract
curl -s -X POST "$MEZO_RPC" -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"eth_getCode","params":["0x247b313d0eD3C532B16c7E5f9eA760272361600F","latest"]}'
# → non-empty bytecode means the address is a contract, not an EOA

# source match
curl -s "https://sourcify.dev/server/v2/contract/31611/0x247b313d0eD3C532B16c7E5f9eA760272361600F"
# → {"match":"exact_match","chainId":"31611",...}
```

## Verdict

**Confirmed** that a contract is deployed at that address and that its source matches exactly.
**Could not tell** whether it is useful to anyone else: it is a testnet deployment with no users, and no
funds of value have moved through it.

## Limits

- Testnet only. Nothing here proves mainnet safety, and no audit firm has reviewed it.
- "100% statement coverage" is coverage of statements executed by tests, not coverage of the threat
  surface. Reentrancy, oracle manipulation and griefing are only covered where a theorem says so.
- The twelve Lean theorems cover the escrow's own accounting rules, not the token contract it holds.
- The grant round has not decided; a submission is not an award.
