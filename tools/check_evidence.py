#!/usr/bin/env python3
r"""check_evidence.py — проверяет, что доказательства в кейсах ЖИВЫЕ.

Кейс с мёртвой ссылкой хуже отсутствия кейса: он выглядит как доказательство, но им не является.
Скрипт проходит по всем ссылкам из cases/*/*.md и проверяет HTTP-статус. Запускается в CI на каждый
push: красный статус означает, что доказательство умерло.

Кроссплатформенность: на Windows бинарь называется curl.exe, на Linux/macOS — curl. Раньше здесь было
жёстко "curl.exe", и в CI все ссылки получали код 0 — проверка падала не на мёртвых ссылках, а на
отсутствии бинаря. Теперь бинарь ищется через shutil.which.

    403 считается «жив, но закрыт» (Cloudflare блокирует ботов, например у bscscan);
    с --strict 403 тоже считается ошибкой.

    python tools/check_evidence.py
    python tools/check_evidence.py --strict
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys

CURL = shutil.which("curl.exe") or shutil.which("curl") or "curl"
DEVNULL = "NUL" if os.name == "nt" else "/dev/null"
PROXY = os.environ.get("EVIDENCE_PROXY", "")  # в CI пусто: прокси там не нужен

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL_RE = re.compile(r"https?://[^\s)\]<>\"]+")


FENCE_RE = re.compile(r"```[\s\S]*?```")


def links() -> list[tuple[str, str]]:
    """Собирает ссылки-доказательства. Блоки кода пропускаются: там команды для запуска,
    а не публичные ссылки, и их доступность зависит от окружения, а не от честности кейса."""
    out: list[tuple[str, str]] = []
    for f in sorted(ROOT.glob("cases/*/*.md")):
        text = f.read_text(encoding="utf-8")
        text = FENCE_RE.sub(" ", text)
        for u in URL_RE.findall(text):
            out.append((str(f.relative_to(ROOT)), u.rstrip(".,;:`\"'")))
    return out


def _one(url: str, proxy: str | None) -> int:
    cmd = [CURL, "-s", "-o", DEVNULL, "-w", "%{http_code}", "-L", "--max-time", "25",
           "-A", "Mozilla/5.0 (compatible; gaduka-evidence-check)", url]
    if proxy:
        cmd[1:1] = ["-x", proxy]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=40, encoding="utf-8", errors="replace")
        return int((r.stdout or "0").strip() or 0)
    except Exception:
        return 0


def _head(url: str, proxy: str | None) -> int:
    cmd = [CURL, "-s", "-I", "-o", DEVNULL, "-w", "%{http_code}", "-L", "--max-time", "25",
           "-A", "Mozilla/5.0 (compatible; gaduka-evidence-check)", url]
    if proxy:
        cmd[1:1] = ["-x", proxy]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=40, encoding="utf-8", errors="replace")
        return int((r.stdout or "0").strip() or 0)
    except Exception:
        return 0


def check(url: str) -> int:
    """GET → при странном коде HEAD → при нуле повтор через прокси.
    Так DOI-редиректы (302→200) не считаются мёртвыми, а реальный 404 остаётся 404."""
    code = _one(url, None)
    if not (200 <= code < 400):
        alt = _head(url, None)
        if 200 <= alt < 400:
            code = alt
    if code == 0 and PROXY:
        code = _one(url, PROXY) or _head(url, PROXY)
    return code


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="считать 403 ошибкой")
    a = ap.parse_args()
    bad = 0
    all_links = links()
    for where, url in all_links:
        code = check(url)
        # 3xx — это редирект (DOI), 403 — «жив, но закрыт» (Cloudflare). Мёртвым считаем 4xx/5xx/0.
        ok = 200 <= code < 400 or (code == 403 and not a.strict)
        print(f"{'ok  ' if ok else 'DEAD'} {code:>3} {url}  ({where})")
        if not ok:
            bad += 1
    print(f"\nссылок: {len(all_links)}, мёртвых: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
