# Case 501 — A citable preprint with a version DOI and generated numbers

**Date:** 2026-10-25 · **Direction:** research artifact · **Status:** published, DOI registered

**In one line:** A preprint with a permanent DOI, in English, open licence. The numbers in it are produced by a script, not typed by hand.

## Claim

A preprint of the lab bench ("Morphogenesis: an open, reproducible lab bench for emergent morphology in
neural cellular automata") is published on Zenodo as version 1.1.0, with a version DOI and a concept DOI,
in English, under CC BY 4.0, and its headline counts are produced by a script that reads the public
repository rather than by hand.

## Evidence

| what | link | proves |
|---|---|---|
| Version DOI | https://doi.org/10.5281/zenodo.23648667 | the preprint exists and resolves |
| Concept DOI | https://doi.org/10.5281/zenodo.23571609 | the stable identifier for all versions |
| Registered metadata | https://api.datacite.org/dois/10.5281/zenodo.23648667 | `state: findable`, `language: en`, type Preprint, license CC BY 4.0 |
| Author identifier | https://orcid.org/0009-0007-2996-3387 | the author record the DOI is bound to |
| Numbers | `tools/metrics.py` in the lab repository | the counts are generated, dated, and re-runnable |

Checked on 2026-10-25: DataCite returned `state: findable`, `language: en`, `resourceTypeGeneral: Preprint`,
`rightsIdentifier: cc-by-4.0`, creator `Vladimirov, Ilya`.

## Reproduce

```bash
curl -s https://api.datacite.org/dois/10.5281/zenodo.23648667 | jq '.data.attributes | {state, language, types, rightsList}'
# → state "findable", language "en", Preprint, cc-by-4.0
```

## Verdict

**Confirmed** — the record is registered, findable, in English, and the concept DOI resolves to the
latest version.

## Limits

- A DOI proves the document exists and is citable; it does not prove the science is right.
- The counts quoted in the record were taken at publication time and grow with the repository; the record
  is dated for that reason, and a later version may carry larger numbers.
- The preprint PDF is six pages: abstract, protocol, one results table, links. It is not a journal article
  and no peer review has taken place.
