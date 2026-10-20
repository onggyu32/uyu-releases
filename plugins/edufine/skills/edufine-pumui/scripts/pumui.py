#!/usr/bin/env python3
"""견적 데이터(JSON) → 에듀파인 품의 제목·개요·품목내역·자동입력 데이터.

사용: python3 pumui.py input.json   (또는 표준입력)
"""
import json
import re
import sys

DIGITS = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
SMALL = ["천", "백", "십", ""]
BIG = ["", "만", "억", "조"]
COLORS = {"K": "검정", "C": "파랑", "M": "빨강", "Y": "노랑"}


def korean_amount(n):
    """1749000 -> 일백칠십사만구천 (공문서식: 일십·일백·일천)."""
    if n == 0:
        return "영"
    groups = []
    while n:
        groups.append(n % 10000)
        n //= 10000
    out = ""
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        if not g:
            continue
        s = str(g).zfill(4)
        for pos, ch in enumerate(s):
            d = int(ch)
            if d:
                out += DIGITS[d] + SMALL[pos]
        out += BIG[i]
    return out


def won(n):
    return f"{n:,}"


def auto_label(name):
    m = re.search(r"토너\s*([KCMY])$", name) or re.match(r"^([KCMY])\s*토너", name)
    if m:
        return COLORS[m.group(1)]
    m = re.match(r"^(.*?)\s*([KCMY])$", name)
    if m and m.group(1):
        return f"{m.group(1)}({COLORS[m.group(2)]})"
    return name


def build(data):
    items = data["items"]
    for it in items:
        it.setdefault("unit", "개")
        it.setdefault("spec", "")
        it["qty"] = int(it["qty"])
        it["price"] = int(it["price"])
        it["amount"] = it["qty"] * it["price"]
        if not it.get("label"):
            it["label"] = auto_label(it["name"])
    total = sum(it["amount"] for it in items)

    specs = {it["spec"] for it in items}
    if len(specs) == 1 and items[0]["spec"]:
        detail = items[0]["spec"] + ", " + ", ".join(
            f'{it["label"]} {it["qty"]}{it["unit"]}' for it in items)
    else:
        detail = ", ".join(
            f'{it["label"]}' + (f'({it["spec"]})' if it["spec"] else "") + f' {it["qty"]}{it["unit"]}'
            for it in items)

    groups = []  # (price, unit) 같은 품목은 묶어서 산출
    for it in items:
        key = (it["price"], it["unit"])
        for g in groups:
            if g[0] == key:
                g[1] += it["qty"]
                break
        else:
            groups.append([key, it["qty"]])
    calc = "+".join(f"{won(p)}원*{q}{u}" for (p, u), q in groups) + f"={won(total)}원."

    attachments = data.get("attachments") or ["지출품의서 1부", "견적서 1부"]
    if len(attachments) == 1:
        attach = f"붙임: {attachments[0]}.  끝."
    else:
        lines = [f"붙임: 1. {attachments[0]}"]
        for i, a in enumerate(attachments[1:], start=2):
            lines.append(f"      {i}. {a}")
        lines[-1] += ".  끝."
        attach = "\n".join(lines)

    title = data["subject"]
    overview = "\n".join([
        f" 1. 건명: {title}",
        f" 2. 위치: {data['location']}",
        f" 3. 내역: {detail}",
        f" 4. 금액: 금{won(total)}원(금{korean_amount(total)}원정)",
        f" 5. 산출내역: {calc}",
        f" 6. 구입처: {data['vendor']}",
        attach,
    ])
    rows = [{"name": it["name"], "spec": it["spec"], "qty": it["qty"], "unit": it["unit"],
             "price": it["price"], "amount": it["amount"]} for it in items]
    return {"title": title, "overview": overview, "items": rows, "total": total}


def main():
    src = open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin
    data = json.load(src)
    r = build(data)
    check = data.get("quoteTotal")
    print("[제목]")
    print(r["title"], f"  ({len(r['title'].encode())}/300 Byte)")
    print()
    print("[개요]")
    print(r["overview"])
    print(f"  ({len(r['overview'].encode())}/2000 Byte)")
    print()
    print("[품목내역]")
    print("순번\t내용\t규격\t수량\t단위\t예상단가\t예상금액")
    for i, it in enumerate(r["items"], 1):
        print(f'{i}\t{it["name"]}\t{it["spec"]}\t{it["qty"]}\t{it["unit"]}\t{won(it["price"])}\t{won(it["amount"])}')
    print(f"요구금액 합계: {won(r['total'])}원")
    if check is not None:
        mark = "일치" if int(check) == r["total"] else f"불일치! 견적서 합계 {won(int(check))}원"
        print(f"견적서 합계 검산: {mark}")
    print()
    print("[자동입력 데이터]")
    print(json.dumps(r, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
