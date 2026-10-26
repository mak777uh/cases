# Case 101 — SD card file deletion in Specter DIY (open pull request)

**Date:** 2026-10-26 · **Direction:** code contribution · **Status:** pull request open, not merged

**In one line:** A hardware wallet's SD card could not delete files. I wrote the patch and its tests. The pull request is open.

## Claim

The SD host of Specter DIY could only read files: `*.psbt` and exported wallet descriptors could be
deleted only from a PC. We patched the host so the file picker can delete one file or wipe the card,
kept the picker open after a deletion instead of dropping to the main menu, added a best-effort secure
delete, and added 11 tests.

This is an **open pull request** — not a merge, and not a payment. It is labelled that way on purpose.

## Evidence

| what | link | proves |
|---|---|---|
| Pull request #447 | https://github.com/cryptoadvance/specter-diy/pull/447 | the patch exists, is public, and is against `master` |
| Patch diff | `git diff bec1ab1..42ab67e` in the branch `mak777uh:sd-card-delete-files` | exactly 3 files, +365/−8 |
| The defect | https://github.com/cryptoadvance/specter-diy/issues/359 | the issue this addresses, open since 2026-06-02 |
| Maintainer activity | `GET /repos/cryptoadvance/specter-diy/pulls?state=closed` | the project merges external PRs: 13 of the last 40 closed were merged, the newest on 2026-10-07 |
| Closing keyword | commit `42ab67e` body contains `Closes #359` | merging the PR closes the issue and satisfies the bounty's linkage |

## Reproduce

```bash
git clone https://github.com/mak777uh/specter-diy.git
cd specter-diy && git checkout sd-card-delete-files
git log -1 --format=%B          # contains "Closes #359"
git diff --stat bec1ab1..HEAD   # 3 files, +365/-8
# full native suite needs the embit and f469-disco submodules:
#   cd test && python3 run_native_tests.py
```

The new test file is `test/tests_native/test_sd_host_delete_files.py` (11 tests, fake GUI + real
filesystem). It was run through a local runner that fakes `sys.platform`, `pyb`, `lvgl`, `gui` and
`helpers`: `Ran 11 tests ... OK`. On unpatched code it fails at the import of the new constants.

## Verdict

**Confirmed** that the patch exists, applies cleanly to `bec1ab1`, and that the defect it fixes is real
and was reported by someone else. **Could not tell** whether it is accepted: no maintainer review yet
as of 2026-10-26 00:40 UTC.

## Limits

- Not merged, therefore not a shipped fix.
- Hardware behaviour (stm32 `os.fsync`, `r+b`, `os.stat()[6]`, MicroPython `write(buf, len)`) was not
  exercised on a device.
- The secure delete is best-effort: wear levelling and free space are not addressed, so it is not a
  forensic guarantee.
- Five other open PRs address the same issue; a maintainer may prefer one of them.
