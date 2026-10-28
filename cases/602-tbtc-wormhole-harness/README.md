# Case 602 — a harness that proves what it does *not* claim

**Date:** 2026-10-28 · **Direction:** audit tooling · **Status:** published

**In one line:** a Foundry harness for the tBTC v2 Wormhole redemption path that compiles contracts the
project itself cannot build from source, records one unchecked assumption, and explicitly refuses to call it
a vulnerability.

## What happened

The Threshold bug-bounty scope lists three Wormhole contracts added in the last twelve months. Their
`package.json` pins two dependencies as `"development"`, and both GitHub repositories are unreachable, so
`forge build` fails out of the box.

Two of those dependencies are published on npm. With those, all four contracts compile — both redeemers, the
L2 gateway and the project's own test stub — and eleven Foundry tests run against the real code.

## What the tests found

1. **`L2WormholeGateway.receiveTbtc` never compares `transfer.fromAddress` with `gateways[chainId]`**, while
   the L1 redeemer in the same repository rejects any message whose sender is not in `allowedSenders`. The
   asymmetry is real and reproducible. Whether it is a defect depends on whether wrapped tBTC can exist
   without backing — a property of the bridge, not of this contract. **Recorded as an observation, not
   reported as a finding.**
2. `mintedAmount` never exceeds `mintingLimit` (fuzzed, 256 runs); above the limit the wrapped token is
   forwarded instead of minted.
3. The L2 redeemer is a clean pass-through: no retained tBTC, no accumulating allowance, dust below the
   bridging precision stays with the user, sub-minimum amounts are refused.

## The false positive worth recording

The second redemption initially reverted with `SafeERC20: approve from non-zero to non-zero allowance`. That
reads like a gateway bug. It is the harness: the gateway approves the wrapped token to the Wormhole bridge
and relies on the transfer to consume it, while the stub only emits an event. The test now simulates the
pull from the bridge address. **A false positive published as a finding would have cost more than the
missing finding.**

## Cross-checked on live chains (no discrepancy)

| chain | gateway `mintedAmount` | wrapped balance held | matches |
|---|---|---|---|
Base | 45.793774 tBTC | 45.793774 | yes |
Optimism | 6.94643228 | 6.94643228 | yes |
Arbitrum | 80.0359653 | 80.0359653 | yes |

Both L2 redeemer proxies hold **0 tBTC**, their proxy admins are contracts rather than EOAs, and every
gateway runs with `mintingLimit = type(uint256).max` — a governance choice, recorded but not claimed as a
defect.

## Evidence

- Harness: https://github.com/mak777uh/tbtc-wormhole-harness
- Upstream code: `keep-network/tbtc-v2` at `e99676d` (30 September 2026)
- Result: `forge test` → 11 passed, 0 failed

## What this case does not claim

- No vulnerability in tBTC v2 is claimed; no test demonstrates loss of funds.
- `Bridge.sol`, `Redemption.sol` and `MovingFunds.sol` — the UTXO accounting where the larger surface lives —
  are not exercised at all.

## Verdict

**Confirmed — the harness compiles and runs against the real code (11/11 tests), the sender-check asymmetry
is reproduced, and the on-chain backing invariant holds on Base, Optimism and Arbitrum. No payable finding.**
