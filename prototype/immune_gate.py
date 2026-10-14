#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GENOME — بوابة التناظر المناعي (نموذج أولي / محاكاة)

الدلالة المناعية الصحيحة:
  • الجيل الجذري (root): «جيل مرجعي» — لا يورث أحداً؛ ثغراته هي التي تُستخرج منها الأمصال.
  • أي جيل آخر: «الأمصال الوراثية» = الأمصال التي وُلدت في أسلافه الأقدمين (تحته فقط).
  • التناظر المناعي = نجاح الجيل في 100% من الأمصال الوراثية. أي فشل = «نسيان مناعي».

تدفّق البيانات: lineage.json + antibodies.json  →  فحص كل جيل  →  جواز مناعة موقّع.
ملاحظة: نتائج الفحص معطاة في ملف البيانات (محاكاة تعليمية)، وليست فحوصات أمنية حقيقية.
"""

import json
import hashlib
import datetime
from pathlib import Path

ROOT = Path(__file__).parent
FIXTURES = ROOT / "fixtures"
OUT = ROOT / "out"

GREEN, RED, YELLOW, DIM, RESET = "\033[92m", "\033[91m", "\033[93m", "\033[2m", "\033[0m"
BOLD = "\033[1m"


def load(name: str) -> dict:
    with open(FIXTURES / name, encoding="utf-8") as f:
        return json.load(f)


def ancestors(generations: list[dict], gen_id: str) -> set[str]:
    """كل أسلاف الجيل (بأي عمق) — بمن فيهم هو نفسه."""
    index = {g["id"]: g for g in generations}
    seen, stack = set(), [gen_id]
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(index[current].get("parents", []))
    return seen


def inherited_antibodies(generations, antibodies, gen_id: str) -> list[dict]:
    """الأمصال التي وُلدت في أسلاف أقدمين (لا في الجيل نفسه) ولها نتيجة فعلية عليه."""
    strict = ancestors(generations, gen_id) - {gen_id}
    return [
        ab for ab in antibodies
        if ab["born_in"] in strict and ab["results"].get(gen_id, "na") != "na"
    ]


def evaluate(generations, antibodies, gen_id: str) -> dict:
    target = next(g for g in generations if g["id"] == gen_id)
    is_root = not target.get("parents")
    inherited = inherited_antibodies(generations, antibodies, gen_id)
    born_here = [ab for ab in antibodies if ab["born_in"] == gen_id]

    findings, passed, failed = [], 0, 0
    for ab in inherited:
        res = ab["results"][gen_id]
        findings.append({"antibody_id": ab["id"], "result": res, "note": ab["title"]})
        if res == "pass":
            passed += 1
        else:
            failed += 1

    total = len(inherited)
    parity = None if is_root else (failed == 0)
    coverage = round(100.0 * passed / total, 1) if total else (None if is_root else 0.0)

    return {
        "artifact": {
            "name": "libgif-rs" if target["language"] == "rust" else "libgif",
            "version": "demo",
            "hash": "sha256:" + hashlib.sha256(gen_id.encode()).hexdigest(),
            "generation": gen_id,
            "language": target["language"],
        },
        "lineage": {
            "parents": target.get("parents", []),
            "operation": target["operation"],
            "depth": target["depth"],
        },
        "immunity": {
            "role": "reference" if is_root else "descendant",
            "antibodies_inherited": total,
            "passed": passed,
            "failed": failed,
            "skipped": 0,
            "immune_parity": parity,
            "inherited_coverage_pct": coverage,
            "new_antibodies": len(born_here),
            "findings": findings,
        },
        "_label": target["label"],
    }


def sign(passport: dict) -> str:
    """توقيع تجريبي: تجزئة على محتوى الجواز (في الإنتاج: Sigstore keyless)."""
    clean = {k: v for k, v in passport.items() if not k.startswith("_") and k != "attestation"}
    canonical = json.dumps(clean, sort_keys=True, ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


def print_report(passports: list[dict]):
    print()
    print(f"{BOLD}🧬 GENOME — تقرير التناظر المناعي (محاكاة){RESET}")
    print("═" * 72)
    for p in passports:
        imm = p["immunity"]
        print(f"\n{BOLD}الجيل {p['artifact']['generation']}: {p['_label']}{RESET}")
        print(f"  العملية: {p['lineage']['operation']}  |  العمق: {p['lineage']['depth']}")

        if imm["role"] == "reference":
            print(f"  {YELLOW}ℹ️  جيل مرجعي (لا أسلاف) — ثغراته الموثّقة تُصبح أمصالاً للأجيال القادمة{RESET}")
            print(f"  أمصال مستخرجة من هذا الجيل: {imm['new_antibodies']}")
        else:
            icon = (f"{GREEN}✅ تناظر مناعي محقّق{RESET}" if imm["immune_parity"]
                    else f"{RED}❌ نسيان مناعي — فقد {imm['failed']} من أمصال أسلافه{RESET}")
            print(f"  الأمصال الوراثية: {imm['antibodies_inherited']}  |  نجح: {imm['passed']}  |  فشل: {imm['failed']}")
            print(f"  التغطية الموروثة: {imm['inherited_coverage_pct']}%  |  أمصال جديدة تُضاف للأرشيف: {imm['new_antibodies']}")
            print(f"  الحالة: {icon}")

    last = passports[-1]["immunity"]
    print("\n" + "═" * 72)
    if last["immune_parity"]:
        print(f"{GREEN}{BOLD}🎯 الحكم: الجيل الأخير ورث كامل مناعة أسلافه — Immune Parity = VERIFIED{RESET}")
    else:
        print(f"{RED}{BOLD}🎯 الحكم: الجيل الأخير فقد {last['failed']} من أمصال أسلافه — نسيان مناعي!{RESET}")
    print(f"{DIM}   الجوازات الموقّعة كُتبت في: {OUT / 'passport.json'}{RESET}")


def main():
    lineage = load("lineage.json")
    antibodies = load("antibodies.json")["antibodies"]
    generations = lineage["generations"]

    passports = [evaluate(generations, antibodies, g["id"]) for g in generations]
    for p in passports:
        p["attestation"] = {
            "signed_by": "genome.dev (demo)",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "signature": sign(p),
            "transparency_log_index": 100000 + len(passports),
        }
        p["disclaimer"] = "دليل إجراءات اختبار موقّعة — ليس ضماناً بخلو الأرتي فاكت من الثغرات."

    OUT.mkdir(exist_ok=True)
    with open(OUT / "passport.json", "w", encoding="utf-8") as f:
        json.dump(passports, f, ensure_ascii=False, indent=2)

    print_report(passports)


if __name__ == "__main__":
    main()
