#!/usr/bin/env python3
r"""check_evidence.py — проверяет, что доказательства в кейсах ЖИВЫЕ.

Зачем: кейс, в котором ссылка мертва, хуже отсутствия кейса — он выглядит как доказательство, но им не является.
Скрипт проходит по всем ссылкам из cases/*/README.md и cases/*/evidence.md и проверяет HTTP-статус.
Запуск в CI (GitHub Actions) на каждый push: красный статус означает, что доказательство умерло.

    python tools/check_evidence.py            # проверить всё
    python tools/check_evidence.py --strict   # падать и на 403 (иначе 403 считается «живой, но закрытой»)
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL_RE = re.compile(r"https?://[^\s)\]<>\"]+")


def links() -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for f in sorted(ROOT.glob("cases/*/*.md")):
        for u in URL_RE.findall(f.read_text(encoding="utf-8")):
            u = u.rstrip(".,;:")
            out.append((str(f.relative_to(ROOT)), u))
    return out


def check(url: str) -> int:
    try:
        r = subprocess.run(["curl.exe", "-s", "-o", "NUL", "-w", "%{http_code}", "-L",
                            "--max-time", "25", "-A", "gaduka-evidence-check", url],
                           capture_output=True, text=True, timeout=40, encoding="utf-8", errors="replace")
        return int((r.stdout or "0").strip() or 0)
    except Exception:
        return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    bad = 0
    for where, url in links():
        code = check(url)
        ok = code == 200 or (code == 403 and not a.strict)
        mark = "ok  " if ok else "DEAD"
        print(f"{mark} {code:>3} {url}  ({where})")
        if not ok:
            bad += 1
    print(f"\nссылок: {len(links())}, мёртвых: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
