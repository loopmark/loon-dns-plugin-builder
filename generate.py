#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import urllib.request
from datetime import datetime, timezone

# 覆盖更大（推荐）：China_Domain.list
SOURCE = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Loon/China/China_Domain.list"
# 如果你想先小规模测试，可以改成：
# SOURCE = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Loon/ChinaTest/ChinaTest_Domain.list"

ALIDOH = "https://dns.alidns.com/dns-query"
OUT = "China_AliDoH.plugin"

OUTPUT_BARE_AND_WILDCARD = True  # True：同时输出 domain 和 *.domain（更稳，体积更大）

SUPPORTED_PREFIXES = ("DOMAIN,", "DOMAIN-SUFFIX,", "HOST,", "DOMAIN-KEYWORD,")
DOMAIN_RE = re.compile(r"^(?=.{1,253}$)(?!-)([a-z0-9-]{1,63}\.)+[a-z]{2,63}$")

def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")

def normalize_domain(s: str) -> str:
    s = s.strip().lower()
    return s.lstrip(".")

def is_domain(s: str) -> bool:
    if "*" in s or "/" in s or " " in s:
        return False
    return DOMAIN_RE.match(s) is not None

def parse_line(line: str):
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    for p in SUPPORTED_PREFIXES:
        if line.startswith(p):
            parts = line.split(",")
            if len(parts) >= 2:
                cand = normalize_domain(parts[1])
                if is_domain(cand):
                    return cand
            return None

    cand = normalize_domain(line)
    if is_domain(cand):
        return cand

    return None

def main():
    text = fetch(SOURCE)
    domains = set()

    for raw in text.splitlines():
        d = parse_line(raw)
        if d:
            domains.add(d)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    header = f"""#!name= China Domains -> Ali DoH
#!desc= Auto-generated from blackmatrix7 list; force these domains to resolve via Ali DoH
#!homepage= {SOURCE}
#!updated= {now}

[Host]
"""
    lines = [header]
    for d in sorted(domains):
        if OUTPUT_BARE_AND_WILDCARD:
            lines.append(f"{d} = server:{ALIDOH}\n")
            lines.append(f"*.{d} = server:{ALIDOH}\n")
        else:
            lines.append(f"*.{d} = server:{ALIDOH}\n")

    with open(OUT, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Generated {OUT} with {len(domains)} domains.")

if __name__ == "__main__":
    main()
