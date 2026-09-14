
import re
import json
import streamlit as st
from pypdf import PdfReader

# =========================================================
# PWCS RATE CARD — 1 JULY 2022
# =========================================================

RATE_CARD = {
    # Electric Scissor Lifts
    "Electric Scissor Lift 19ft": {"family":"Electric Scissor Lift","size":"19ft","daily":60.00,"daily_cpas":"1403","weekly":126.00,"weekly_cpas":"1404","transport":95.00,"transport_cpas":"2118"},
    "Electric Scissor Lift 20ft": {"family":"Electric Scissor Lift","size":"20ft","daily":60.00,"daily_cpas":"1405","weekly":126.00,"weekly_cpas":"1406","transport":95.00,"transport_cpas":"2118"},
    "Electric Scissor Lift 26ft": {"family":"Electric Scissor Lift","size":"26ft","daily":75.00,"daily_cpas":"1407","weekly":280.00,"weekly_cpas":"1408","transport":95.00,"transport_cpas":"2117"},
    "Electric Scissor Lift 32ft": {"family":"Electric Scissor Lift","size":"32ft","daily":180.00,"daily_cpas":None,"weekly":560.00,"weekly_cpas":None,"transport":180.00,"transport_cpas":None},
    "Electric Scissor Lift 40ft": {"family":"Electric Scissor Lift","size":"40ft","daily":250.00,"daily_cpas":None,"weekly":840.00,"weekly_cpas":None,"transport":220.00,"transport_cpas":None},

    # Diesel Scissor Lifts
    "Diesel Scissor Lift 26ft": {"family":"Diesel Scissor Lift","size":"26ft","daily":90.00,"daily_cpas":"1370","weekly":406.00,"weekly_cpas":"1371","transport":95.00,"transport_cpas":"2117"},
    "Diesel Scissor Lift 32ft": {"family":"Diesel Scissor Lift","size":"32ft","daily":190.00,"daily_cpas":None,"weekly":700.00,"weekly_cpas":None,"transport":180.00,"transport_cpas":None},
    "Diesel Scissor Lift 33ft": {"family":"Diesel Scissor Lift","size":"33ft","daily":95.00,"daily_cpas":"1362","weekly":455.00,"weekly_cpas":"1363","transport":95.00,"transport_cpas":"2117"},
    "Diesel Scissor Lift 40ft": {"family":"Diesel Scissor Lift","size":"40ft","daily":100.00,"daily_cpas":"1364","weekly":532.00,"weekly_cpas":"1365","transport":95.00,"transport_cpas":"2117"},
    "Diesel Scissor Lift 43ft": {"family":"Diesel Scissor Lift","size":"43ft","daily":110.00,"daily_cpas":"1366","weekly":595.00,"weekly_cpas":"1367","transport":95.00,"transport_cpas":"2117"},
    "Diesel Scissor Lift 50ft": {"family":"Diesel Scissor Lift","size":"50ft","daily":135.00,"daily_cpas":"1368","weekly":700.00,"weekly_cpas":"1369","transport":95.00,"transport_cpas":"2117"},
    "Diesel Scissor Lift 53ft": {"family":"Diesel Scissor Lift","size":"53ft","daily":280.00,"daily_cpas":None,"weekly":1260.00,"weekly_cpas":None,"transport":280.00,"transport_cpas":None},

    # Electric Knuckle Booms
    "Electric Knuckle Boom 30ft": {"family":"Electric Knuckle Boom","size":"30ft","daily":100.00,"daily_cpas":"1060","weekly":400.00,"weekly_cpas":"1061","transport":150.00,"transport_cpas":"1062"},
    "Electric Knuckle Boom 45ft": {"family":"Electric Knuckle Boom","size":"45ft","daily":260.00,"daily_cpas":None,"weekly":700.00,"weekly_cpas":None,"transport":280.00,"transport_cpas":None},
    "Star 10ft": {"family":"Electric Knuckle Boom","size":"10ft","daily":300.00,"daily_cpas":None,"weekly":980.00,"weekly_cpas":None,"transport":280.00,"transport_cpas":None},

    # Diesel Knuckle Booms
    "Diesel Knuckle Boom 34ft": {"family":"Articulating Boom Lift","size":"34ft","daily":115.00,"daily_cpas":"1606","weekly":497.00,"weekly_cpas":"1614","transport":155.00,"transport_cpas":"2113"},
    "Diesel Knuckle Boom 45ft": {"family":"Articulating Boom Lift","size":"45ft","daily":140.00,"daily_cpas":"1608","weekly":595.00,"weekly_cpas":"1615","transport":195.00,"transport_cpas":"2114"},
    "Diesel Knuckle Boom 60ft": {"family":"Articulating Boom Lift","size":"60ft","daily":170.00,"daily_cpas":"1609","weekly":910.00,"weekly_cpas":"1617","transport":195.00,"transport_cpas":"2114"},
    "Diesel Knuckle Boom 80ft": {"family":"Articulating Boom Lift","size":"80ft","daily":205.00,"daily_cpas":"1610","weekly":1365.00,"weekly_cpas":"1618","transport":230.00,"transport_cpas":"2116"},
    "Diesel Knuckle Boom 125ft": {"family":"Articulating Boom Lift","size":"125ft","daily":600.00,"daily_cpas":"1611","weekly":2590.00,"weekly_cpas":"1619","transport":280.00,"transport_cpas":"2115"},
    "Diesel Knuckle Boom 135ft": {"family":"Articulating Boom Lift","size":"135ft","daily":670.00,"daily_cpas":"1612","weekly":3220.00,"weekly_cpas":"1620","transport":280.00,"transport_cpas":"2115"},

    # Straight Stick Booms
    "Straight Stick Boom 42/45ft": {"family":"Straight Stick Boom","size":"42/45ft","daily":140.00,"daily_cpas":"2020","weekly":595.00,"weekly_cpas":"2025","transport":195.00,"transport_cpas":"2114"},
    "Straight Stick Boom 65/66ft": {"family":"Straight Stick Boom","size":"65/66ft","daily":170.00,"daily_cpas":"2021","weekly":910.00,"weekly_cpas":"2026","transport":195.00,"transport_cpas":"2114"},
    "Straight Stick Boom 85/86ft": {"family":"Straight Stick Boom","size":"85/86ft","daily":260.00,"daily_cpas":"2022","weekly":1365.00,"weekly_cpas":"2027","transport":230.00,"transport_cpas":"2116"},
    "Straight Stick Boom 120/125ft": {"family":"Straight Stick Boom","size":"120/125ft","daily":600.00,"daily_cpas":"2023","weekly":2590.00,"weekly_cpas":"2028","transport":280.00,"transport_cpas":"2115"},
    "Straight Stick Boom 135ft": {"family":"Straight Stick Boom","size":"135ft","daily":670.00,"daily_cpas":"2024","weekly":3220.00,"weekly_cpas":"2029","transport":280.00,"transport_cpas":"2115"},

    # Long Term / Permanent
    "LT Knuckle Boom 51ft": {"family":"Long Term Knuckle Boom","size":"51ft","daily":None,"daily_cpas":None,"weekly":679.00,"weekly_cpas":"2235","transport":195.00,"transport_cpas":"2114"},
    "LT Knuckle Boom 34ft": {"family":"Long Term Knuckle Boom","size":"34ft","daily":None,"daily_cpas":None,"weekly":455.00,"weekly_cpas":"1622","transport":195.00,"transport_cpas":"2114"},
    "LT Knuckle Boom 60ft": {"family":"Long Term Knuckle Boom","size":"60ft","daily":None,"daily_cpas":None,"weekly":700.00,"weekly_cpas":"1605","transport":230.00,"transport_cpas":"2116"},
}

FUEL_RATE = 2.80
FUEL_CPAS = "1477"
MISC_CPAS = "1760"

# =========================================================
# UTILITIES
# =========================================================

def norm_space(s):
    return re.sub(r"\s+", " ", (s or "")).strip()

def money(s):
    if s is None:
        return None
    try:
        return float(str(s).replace(",", ""))
    except Exception:
        return None

def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def first_match(pattern, text, flags=0):
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else None

def parse_header(text):
    invoice_date = first_match(r"Invoice Date\s+(\d{1,2}/\d{1,2}/\d{4})", text)
    hire_number = first_match(r"(HN/\d+)", text)
    pair = re.search(r"PO Number\s*\n(\d{10})\s*\n(\d+)", text)
    invoice_number = pair.group(1) if pair else None
    po_number = pair.group(2) if pair else None

    site = first_match(r"Site Address\s+(.+?)(?=\nItem Description)", text, re.S)
    if site:
        site = norm_space(site)

    subtotal = first_match(r"Sub Total:\s*([\d,]+\.\d{2})", text)
    if not subtotal:
        m = re.search(r"Sub Total:(.+?)GST Total:", text, re.S)
        if m:
            vals = re.findall(r"([\d,]+\.\d{2})", m.group(1))
            subtotal = vals[-1] if vals else None

    total = first_match(r"\$([\d,]+\.\d{2})\s+Any requests for credit", text, re.S)

    return {
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "po_work_order": po_number,
        "hire_number": hire_number,
        "site": site,
        "subtotal_ex_gst": money(subtotal),
        "invoice_total_inc_gst": money(total),
        "customer": "Port Waratah Coal Services CPAS",
    }

# =========================================================
# MACHINE NORMALISATION
# =========================================================

def size_from_text(text):
    vals = [int(x) for x in re.findall(r"(\d{2,3})\s*ft", text.lower())]
    if vals:
        return max(vals)
    # Also catch model strings like 1250AJP, Z135/70, GS2669RT
    model_hints = []
    low = text.lower()
    if "1250ajp" in low: model_hints.append(125)
    if "z135" in low: model_hints.append(135)
    if "gs2669" in low: model_hints.append(26)
    if "gs3369" in low: model_hints.append(33)
    if "gs4069" in low: model_hints.append(40)
    if "z34" in low: model_hints.append(34)
    if "z45" in low: model_hints.append(45)
    if "z60" in low: model_hints.append(60)
    if "z80" in low: model_hints.append(80)
    return max(model_hints) if model_hints else None

def identify_machine(raw_text):
    """
    Returns dict:
      category: RATE_CARD / MISC / FAMILY_ONLY / UNKNOWN
      normalized: normalized machine label
      family: equipment family
      size: int or None
      matched_key: RATE_CARD key or None
    """
    t = norm_space(raw_text)
    low = t.lower()
    size = size_from_text(t)

    # MISC categories
    if any(k in low for k in ["forklift", "telehandler", "rough terrain forklift"]):
        return {"category":"MISC","normalized":"MISC — Forklift/Telehandler","family":"Forklift/Telehandler","size":size,"matched_key":None}

    # PWCS invoice shorthand for diesel articulating/knuckle booms.
    # Examples: "34ft Diesel B", "45ft Diesel B", "125ft Diesel B".
    if re.search(r"\b(?:34|45|60|80|125|135)\s*ft\s+diesel\s+b\b", low):
        family = "Articulating Boom Lift"
        key = f"Diesel Knuckle Boom {size}ft" if size else None
        if key in RATE_CARD:
            return {"category":"RATE_CARD","normalized":key,"family":family,"size":size,"matched_key":key}

    # Generic family labels
    if "boom lift - a" in low or ("articulating" in low and size is None):
        return {"category":"FAMILY_ONLY","normalized":"Articulating Boom Lift — SIZE UNKNOWN","family":"Articulating Boom Lift","size":None,"matched_key":None}

    # Scissor lifts
    if "scissor" in low:
        if "diesel" in low or "rt" in low:
            family = "Diesel Scissor Lift"
            key = f"Diesel Scissor Lift {size}ft" if size else None
        else:
            family = "Electric Scissor Lift"
            key = f"Electric Scissor Lift {size}ft" if size else None
        if key in RATE_CARD:
            return {"category":"RATE_CARD","normalized":key,"family":family,"size":size,"matched_key":key}
        return {"category":"FAMILY_ONLY","normalized":f"{family} — SIZE UNKNOWN" if not size else f"{family} {size}ft — CHECK","family":family,"size":size,"matched_key":None}

    # Straight stick / telescopic
    if "straight" in low or "telescopic" in low:
        family = "Straight Stick Boom"
        key = None
        if size in (42,45): key = "Straight Stick Boom 42/45ft"
        elif size in (65,66): key = "Straight Stick Boom 65/66ft"
        elif size in (85,86): key = "Straight Stick Boom 85/86ft"
        elif size in (120,125): key = "Straight Stick Boom 120/125ft"
        elif size == 135: key = "Straight Stick Boom 135ft"
        if key:
            return {"category":"RATE_CARD","normalized":key,"family":family,"size":size,"matched_key":key}
        return {"category":"FAMILY_ONLY","normalized":"Straight Stick Boom — SIZE UNKNOWN","family":family,"size":size,"matched_key":None}

    # Articulating / knuckle booms
    if any(k in low for k in ["articulating", "knuckle", "boomlift", "boom lift", "z34", "z45", "z60", "z80", "z135", "1250ajp"]):
        family = "Articulating Boom Lift"
        if size:
            key = f"Diesel Knuckle Boom {size}ft"
            if key in RATE_CARD:
                return {"category":"RATE_CARD","normalized":key,"family":family,"size":size,"matched_key":key}
        label = f"Articulating Boom Lift {size}ft — NOT ON STANDARD RATE CARD" if size else "Articulating Boom Lift — SIZE UNKNOWN"
        return {"category":"FAMILY_ONLY","normalized":label,"family":family,"size":size,"matched_key":None}

    return {"category":"UNKNOWN","normalized":"UNRECOGNISED — CHECK MACHINE","family":None,"size":size,"matched_key":None}

# =========================================================
# PARSER
# =========================================================

# Robust hire parser for Access invoice PDFs.
# pypdf often returns the visual columns in a scrambled token order such as:
# 1.0020/03/20251/03/2025NSW-13406 9,200.00Off HireZX135/70: ... 20 460.00
# This parser supports BOTH that real pypdf order and a normal left-to-right row.
def parse_hire_line(line):
    line = norm_space(line)

    # Pattern A — actual pypdf token order observed on Access invoices.
    scrambled = re.search(
        r"(?P<qty>\d+\.\d{2})"
        r"(?P<to>\d{1,2}/\d{1,2}/\d{4})"
        r"(?P<from>\d{1,2}/\d{1,2}/\d{4})"
        r"(?P<machine>[A-Z]{2,5}-?\d+)\s+"
        r"(?P<charge>[\d,]+\.\d{2})"
        r"(?P<status>Off Hire|On Hire)"
        r"(?P<desc>.+?)\s+"
        r"(?P<days>\d+)\s+"
        r"(?P<rate>[\d,]+\.\d{2})$",
        line,
        re.I,
    )

    # Pattern B — conventional invoice row order.
    conventional = re.search(
        r"(?P<machine>[A-Z]{2,5}-?\d+)\s+"
        r"(?P<desc>.+?)\s+"
        r"(?P<status>Off Hire|On Hire)\s*"
        r"(?P<from>\d{1,2}/\d{1,2}/\d{4})\s*"
        r"(?P<to>\d{1,2}/\d{1,2}/\d{4})\s+"
        r"(?P<qty>\d+(?:\.\d+)?)\s+"
        r"(?P<days>\d+)\s+"
        r"(?P<rate>[\d,]+\.\d{2})\s+"
        r"(?P<charge>[\d,]+\.\d{2})$",
        line,
        re.I,
    )

    m = scrambled or conventional
    if not m:
        return None

    raw_machine = norm_space(m.group("desc"))
    ident = identify_machine(raw_machine)

    return {
        "machine_no": m.group("machine").upper(),
        "charge_type": "Hire",
        "hire_machine_raw": raw_machine,
        "machine_normalized": ident["normalized"],
        "machine_category": ident["category"],
        "family": ident["family"],
        "size": ident["size"],
        "matched_key": ident["matched_key"],
        "quantity": money(m.group("qty")) or 1.0,
        "days": int(m.group("days")),
        "billed_rate": money(m.group("rate")),
        "billed_amount": money(m.group("charge")),
        "from_date": m.group("from"),
        "to_date": m.group("to"),
        "raw_invoice_line": line,
    }

def parse_numeric_tail(line):
    nums = re.findall(r"(?<![\w/])([\d,]+\.\d{1,2})(?![\w/])", line)
    if len(nums) >= 3:
        q, r, a = nums[-3:]
        return money(q), money(r), money(a)
    return None

def parse_invoice_lines(text):
    raw_lines = [norm_space(x) for x in text.splitlines() if x.strip()]
    rows = []
    order = 0
    hire_rows = []

    for idx, line in enumerate(raw_lines):
        h = parse_hire_line(line)
        if h:
            order += 1
            h["source_order"] = order
            rows.append(h)
            hire_rows.append(h)
            continue

        # Transport Levy — billable invoice line, retained for subtotal reconciliation.
        if re.search(r"\bTransport Levy\b", line, re.I):
            vals = parse_numeric_tail(line)
            if vals:
                order += 1
                q, r, a = vals
                rows.append({
                    "machine_no":None,
                    "charge_type":"Transport Levy",
                    "hire_machine_raw":None,
                    "machine_normalized":None,
                    "machine_category":None,
                    "family":None,
                    "size":None,
                    "matched_key":None,
                    "quantity":q,
                    "days":None,
                    "billed_rate":r,
                    "billed_amount":a,
                    "source_order":order,
                    "raw_invoice_line":line,
                })
                continue

        # Diesel
        if re.search(r"\bDiesel\b", line, re.I):
            vals = parse_numeric_tail(line)
            if vals:
                order += 1
                q, r, a = vals
                rows.append({
                    "machine_no": None,
                    "charge_type":"Diesel",
                    "hire_machine_raw":None,
                    "machine_normalized":None,
                    "machine_category":None,
                    "family":None,
                    "size":None,
                    "matched_key":None,
                    "quantity":q,
                    "days":None,
                    "billed_rate":r,
                    "billed_amount":a,
                    "source_order":order,
                    "raw_invoice_line":line,
                })
                continue

        # Delivery / Collection
        transport_type = None
        if re.search(r"\bDelivery\b", line, re.I):
            transport_type = "Delivery"
        elif re.search(r"\bCollection\b", line, re.I):
            transport_type = "Collection"

        if transport_type:
            vals = parse_numeric_tail(line)
            if vals:
                order += 1
                q, r, a = vals

                # find generic machine text from same line or next line
                machine_text = ""
                pre = re.split(r"\b(?:Delivery|Collection)\b", line, flags=re.I)[0]
                if pre and not pre.upper().startswith("TRANS"):
                    machine_text = pre

                if idx+1 < len(raw_lines):
                    nxt = raw_lines[idx+1]
                    if re.search(r"boom|lift|scissor|forklift|telehandler|straight|diesel", nxt, re.I):
                        machine_text = machine_text or nxt.lstrip("|").strip()

                ident = identify_machine(machine_text)

                rows.append({
                    "machine_no":None,
                    "charge_type":transport_type,
                    "hire_machine_raw":machine_text or None,
                    "machine_normalized":ident["normalized"],
                    "machine_category":ident["category"],
                    "family":ident["family"],
                    "size":ident["size"],
                    "matched_key":ident["matched_key"],
                    "quantity":q,
                    "days":None,
                    "billed_rate":r,
                    "billed_amount":a,
                    "source_order":order,
                    "raw_invoice_line":line,
                })

    # Link transport rows to hire rows where possible
    link_transports(rows, hire_rows)
    return ensure_in_lieu_field(row)s

# =========================================================
# TRANSPORT -> HIRE LINKING
# =========================================================

def link_transports(rows, hire_rows):
    for row in rows:
        if row["charge_type"] not in ("Delivery","Collection"):
            continue

        # MISC transport stays MISC if explicitly forklift/telehandler
        if row["machine_category"] == "MISC":
            continue

        candidates = []

        # If transport has known family/size, match exact machine
        if row.get("family"):
            for h in hire_rows:
                if h.get("family") == row["family"]:
                    if row.get("size") is None or h.get("size") == row.get("size"):
                        candidates.append(h)

        # Generic "Scissor Lift" / "Boom Lift - A": match family or unique hire
        if not candidates and row.get("family"):
            candidates = [h for h in hire_rows if h.get("family") == row.get("family")]

        # If only one hire machine on invoice, use it
        if not candidates and len(hire_rows) == 1:
            candidates = [hire_rows[0]]

        # If exactly one safe candidate, inherit everything including machine number.
        if len(candidates) == 1:
            h = candidates[0]
            row["machine_no"] = h["machine_no"]
            row["machine_normalized"] = h["machine_normalized"]
            row["machine_category"] = h["machine_category"]
            row["family"] = h["family"]
            row["size"] = h["size"]
            row["matched_key"] = h["matched_key"]
            row["linked_from_hire"] = True

        elif len(candidates) > 1:
            # NEW V3.2 RULE:
            # If multiple hire machines exist but ALL candidates are the same normalized
            # rate-card machine (same size/type), we can safely inherit the machine TYPE
            # for rate/CPAS validation even though we cannot know the exact asset number.
            matched_keys = {h.get("matched_key") for h in candidates if h.get("matched_key")}
            normalized = {h.get("machine_normalized") for h in candidates if h.get("machine_normalized")}
            families = {h.get("family") for h in candidates if h.get("family")}
            sizes = {h.get("size") for h in candidates if h.get("size") is not None}

            if len(matched_keys) == 1 and len(normalized) == 1:
                exemplar = candidates[0]
                row["machine_no"] = "MULTIPLE / NOT LINKED"
                row["machine_normalized"] = exemplar["machine_normalized"]
                row["machine_category"] = exemplar["machine_category"]
                row["family"] = exemplar["family"]
                row["size"] = exemplar["size"]
                row["matched_key"] = exemplar["matched_key"]
                row["linked_from_hire"] = True
                row["machine_link_status"] = "TYPE MATCHED — ASSET NOT LINKED"
            else:
                # Different sizes/types are present, so do not guess.
                row["linked_from_hire"] = False
                row["machine_link_status"] = "CHECK MACHINE LINK"

# =========================================================
# VALIDATION
# =========================================================

def family_transport_rates(family):
    vals = []
    for key, rc in RATE_CARD.items():
        if rc["family"] == family and rc["transport"] is not None:
            vals.append((key, rc["transport"], rc["transport_cpas"]))
    return vals

def nearest_transport_matches(family, billed):
    vals = family_transport_rates(family)
    if not vals:
        return []
    diffs = [(abs(rate-billed), key, rate, cpas) for key, rate, cpas in vals]
    best = min(x[0] for x in diffs)
    return [(key, rate, cpas) for d,key,rate,cpas in diffs if abs(d-best) < 0.01]

def find_in_lieu_hire_match(row):
    """
    Detect an actual supplied machine that is not on the standard PWCS rate-card
    size but is billed at a valid smaller machine rate in the same family.

    Returns a unique smaller-machine match where possible.
    """
    actual_size = row.get("size")
    family = row.get("family")
    billed_rate = row.get("billed_rate")
    billed_amount = row.get("billed_amount")
    days = row.get("days")

    if family != "Articulating Boom Lift" or actual_size is None:
        return None

    candidates = []
    for key, rc in RATE_CARD.items():
        if rc.get("family") != family:
            continue

        m = re.search(r"(\d{2,3})ft$", key)
        if not m:
            continue
        candidate_size = int(m.group(1))
        if candidate_size >= actual_size:
            continue

        # Match either the displayed weekly/daily rate or the actual prorated amount.
        for basis, rate, cpas in (
            ("daily", rc.get("daily"), rc.get("daily_cpas")),
            ("weekly", rc.get("weekly"), rc.get("weekly_cpas")),
        ):
            if rate is None:
                continue

            rate_match = billed_rate is not None and abs(billed_rate - rate) < 0.01
            amount_match = False
            expected_amount = None

            if days is not None:
                if basis == "daily":
                    expected_amount = round(rate * days, 2)
                else:
                    expected_amount = round((rate / 7.0) * days, 2)

                if billed_amount is not None and abs(billed_amount - expected_amount) < 0.01:
                    amount_match = True

            if rate_match or amount_match:
                candidates.append({
                    "key": key,
                    "size": candidate_size,
                    "basis": basis,
                    "rate": rate,
                    "cpas": cpas,
                    "expected_amount": expected_amount,
                })

    # Prefer exact displayed-rate matches, then the closest smaller size.
    if not candidates:
        return None

    exact_rate = [c for c in candidates if billed_rate is not None and abs(c["rate"] - billed_rate) < 0.01]
    pool = exact_rate or candidates
    pool.sort(key=lambda c: c["size"], reverse=True)

    # Only return a confident top match.
    top = pool[0]
    same_top = [c for c in pool if c["size"] == top["size"] and c["basis"] == top["basis"]]
    return top if len(same_top) == 1 else top


def validate_hire(row):
    out = {}
    cat = row.get("machine_category")
    key = row.get("matched_key")
    billed_rate = row.get("billed_rate")
    billed_amount = row.get("billed_amount")
    days = row.get("days")

    if cat == "MISC":
        out.update({
            "expected_rate": None,
            "expected_amount": None,
            "variance_ex_gst": None,
            "expected_cpas": MISC_CPAS,
            "validation_result":"MISC RATE CHECK REQUIRED",
            "recommended_action":"Validate approved MISC hire rate.",
        })
        return out

    if not key or key not in RATE_CARD:
        in_lieu = find_in_lieu_hire_match(row)
        if in_lieu:
            expected_amount = in_lieu.get("expected_amount")
            variance = None
            if expected_amount is not None and billed_amount is not None:
                variance = round(billed_amount - expected_amount, 2)

            smaller_label = in_lieu["key"]
            out.update({
                "expected_rate":in_lieu["rate"],
                "expected_amount":expected_amount,
                "variance_ex_gst":variance,
                "expected_cpas":in_lieu["cpas"],
                "in_lieu_cpas":in_lieu["cpas"],
                "validation_result":f"IN LIEU — MATCHES {smaller_label}",
                "recommended_action":(
                    f"Actual supplied machine is {row.get('size')}ft, but billing matches "
                    f"{smaller_label}. Use CPAS {in_lieu['cpas']} for the approved in-lieu billing "
                    f"and confirm the substitution; do not credit automatically."
                ),
            })
            return out

        out.update({
            "expected_rate":None,
            "expected_amount":None,
            "variance_ex_gst":None,
            "expected_cpas":None,
            "validation_result":"CHECK MACHINE SIZE",
            "recommended_action":"Confirm machine size before hire-rate validation.",
        })
        return out

    rc = RATE_CARD[key]
    daily = rc["daily"]
    weekly = rc["weekly"]

    # infer expected billing basis from billed rate if available
    expected_rate = None
    expected_amount = None
    expected_cpas = None
    result = "HIRE RATE REVIEW"
    action = "Review hire rate against PWCS contract."

    if billed_rate is not None:
        if daily is not None and abs(billed_rate-daily) < 0.01:
            expected_rate = daily
            expected_cpas = rc["daily_cpas"]
            expected_amount = round(daily * (days or 1), 2)
        elif weekly is not None and abs(billed_rate-weekly) < 0.01:
            expected_rate = weekly
            expected_cpas = rc["weekly_cpas"]
            if days:
                expected_amount = round((weekly/7.0)*days, 2)
        else:
            # Determine expected rate from days
            if days is not None:
                if days <= 6 and daily is not None:
                    expected_rate = daily
                    expected_cpas = rc["daily_cpas"]
                    expected_amount = round(daily * days, 2)
                elif weekly is not None:
                    expected_rate = weekly
                    expected_cpas = rc["weekly_cpas"]
                    expected_amount = round((weekly/7.0)*days, 2)

        if expected_amount is not None and billed_amount is not None:
            var = round(billed_amount - expected_amount, 2)
            if abs(var) < 0.01:
                result = "PASS"
                action = "No action required."
            elif var > 0:
                result = "CREDIT REQUIRED"
                action = f"Credit required: ${var:.2f} ex GST."
            else:
                result = "UNDERBILLED — REVIEW"
                action = f"Underbilled by ${abs(var):.2f} ex GST."
        else:
            var = None
    else:
        # Still populate expected rate from days so user can compare
        if days is not None:
            if days <= 6 and daily is not None:
                expected_rate = daily
                expected_cpas = rc["daily_cpas"]
            elif weekly is not None:
                expected_rate = weekly
                expected_cpas = rc["weekly_cpas"]
        var = None
        result = "RATE CAPTURE REQUIRED"
        action = "Billed hire rate/amount was not captured; check source line."

    out.update({
        "expected_rate":expected_rate,
        "expected_amount":expected_amount,
        "variance_ex_gst":var,
        "expected_cpas":expected_cpas,
        "validation_result":result,
        "recommended_action":action,
    })
    return out

def validate_transport(row):
    cat = row.get("machine_category")
    key = row.get("matched_key")
    billed = row.get("billed_amount")
    billed_rate = row.get("billed_rate")

    if cat == "MISC":
        return {
            "expected_rate":None,
            "expected_amount":None,
            "variance_ex_gst":None,
            "expected_cpas":MISC_CPAS,
            "validation_result":"MISC RATE CHECK REQUIRED",
            "recommended_action":"Validate approved MISC transport rate.",
        }

    # Family known but size unknown
    if cat == "FAMILY_ONLY" or not key:
        family = row.get("family")
        if family:
            valid_rates = sorted(set(rate for _,rate,_ in family_transport_rates(family)))
            if billed_rate in valid_rates:
                matches = [(k,r,c) for k,r,c in family_transport_rates(family) if abs(r-billed_rate)<0.01]
                labels = ", ".join(k for k,_,_ in matches)
                cpas = matches[0][2] if len(set(x[2] for x in matches)) == 1 else "CHECK MACHINE SIZE"
                return {
                    "expected_rate":billed_rate,
                    "expected_amount":round((row.get("quantity") or 1)*billed_rate,2),
                    "variance_ex_gst":0.0,
                    "expected_cpas":cpas,
                    "validation_result":"RATE MATCH FOUND — CHECK MACHINE SIZE",
                    "recommended_action":f"Rate matches {labels}; confirm machine size before upload.",
                }
            near = nearest_transport_matches(family, billed_rate)
            near_txt = ", ".join(f"{k} ${r:.2f}" for k,r,_ in near) if near else "none"
            return {
                "expected_rate":None,
                "expected_amount":None,
                "variance_ex_gst":None,
                "expected_cpas":"CHECK MACHINE SIZE",
                "validation_result":"CREDIT REQUIRED + CHECK MACHINE SIZE",
                "recommended_action":f"Billed transport ${billed_rate:.2f} matches no valid {family} rate. Nearest: {near_txt}. Confirm size to calculate exact credit.",
            }

        return {
            "expected_rate":None,"expected_amount":None,"variance_ex_gst":None,
            "expected_cpas":"CHECK MACHINE","validation_result":"CHECK MACHINE",
            "recommended_action":"Confirm machine before transport validation."
        }

    rc = RATE_CARD[key]
    expected_rate = rc["transport"]
    expected_amount = round((row.get("quantity") or 1)*expected_rate, 2)
    variance = round((billed or 0)-expected_amount, 2)
    if abs(variance) < 0.01:
        result = "PASS"
        action = "No action required."
    elif variance > 0:
        result = "CREDIT REQUIRED"
        action = f"Credit required: ${variance:.2f} ex GST."
    else:
        result = "UNDERBILLED — REVIEW"
        action = f"Underbilled by ${abs(variance):.2f} ex GST."

    return {
        "expected_rate":expected_rate,
        "expected_amount":expected_amount,
        "variance_ex_gst":variance,
        "expected_cpas":rc["transport_cpas"],
        "validation_result":result,
        "recommended_action":action,
    }

def ensure_in_lieu_field(result):
    if "in_lieu_cpas" not in result:
        result["in_lieu_cpas"] = None
    return result


def validate_row(row):
    if row["charge_type"] == "Diesel":
        exp = round((row["quantity"] or 0)*FUEL_RATE,2)
        var = round((row["billed_amount"] or 0)-exp,2)
        return {
            **row,
            "expected_rate":FUEL_RATE,
            "expected_amount":exp,
            "variance_ex_gst":var,
            "expected_cpas":FUEL_CPAS,
            "validation_result":"PASS" if abs(var)<0.01 else ("CREDIT REQUIRED" if var>0 else "UNDERBILLED — REVIEW"),
            "recommended_action":"No action required." if abs(var)<0.01 else (f"Credit required: ${var:.2f} ex GST." if var>0 else f"Underbilled by ${abs(var):.2f} ex GST.")
        }

    if row["charge_type"] == "Transport Levy":
        return {
            **row,
            "expected_rate":None,
            "expected_amount":None,
            "variance_ex_gst":None,
            "expected_cpas":None,
            "validation_result":"REVIEW — UNSUPPORTED CHARGE",
            "recommended_action":"Check supporting agreement/approval for transport levy.",
        })

    if row["charge_type"] == "Hire":
        return ensure_in_lieu_field({**row, **validate_hire(row)})

    if row["charge_type"] in ("Delivery","Collection"):
        return ensure_in_lieu_field({**row, **validate_transport(row)})

    return row

def reconcile(header, rows):
    subtotal = header.get("subtotal_ex_gst")
    extracted = round(sum((r.get("billed_amount") or 0) for r in rows),2)
    diff = None if subtotal is None else round(subtotal-extracted,2)
    return {
        "extracted_total":extracted,
        "subtotal":subtotal,
        "difference":diff,
        "status":"PASS" if diff is not None and abs(diff)<0.01 else "PARSING INCOMPLETE"
    }

def overall_status(rows, recon):
    if recon["status"] != "PASS":
        return "PARSING INCOMPLETE — DO NOT VALIDATE"
    statuses = [r.get("validation_result","") for r in rows]
    if any("CREDIT REQUIRED" in s for s in statuses):
        return "CREDIT REQUIRED"
    if any(any(x in s for x in ["CHECK","REVIEW","MISC","RATE CAPTURE"]) for s in statuses):
        return "REVIEW REQUIRED"
    return "VALIDATED — READY"

# =========================================================
# UI
# =========================================================

st.set_page_config(page_title="PWCS Invoice Parser Prototype — V3.4", layout="wide")
st.title("PWCS Invoice Parser Prototype — V3.4")
st.caption("V3.4: adds explicit CPAS visibility for in-lieu machines, including the matched smaller-machine CPAS code.")

uploaded = st.file_uploader("Upload PWCS invoice PDF", type=["pdf"])

if uploaded:
    text = extract_text(uploaded)
    header = parse_header(text)
    parsed = parse_invoice_lines(text)
    validated = [validate_row(r) for r in parsed]
    recon = reconcile(header, validated)
    status = overall_status(validated, recon)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Invoice", header.get("invoice_number") or "—")
    c2.metric("Lines Extracted", len(validated))
    c3.metric("Extracted Total", f"${recon['extracted_total']:,.2f}")
    c4.metric("Invoice Subtotal", f"${recon['subtotal']:,.2f}" if recon['subtotal'] is not None else "—")

    if recon["status"] == "PASS":
        st.success("✅ RECONCILIATION PASS — extracted lines equal invoice subtotal.")
    else:
        diff = recon["difference"]
        st.error(f"🔴 PARSING INCOMPLETE — ${abs(diff):,.2f} unaccounted for." if diff is not None else "🔴 PARSING INCOMPLETE")

    st.subheader(f"Overall Status: {status}")

    st.subheader("Invoice Header")
    st.json(header)

    st.subheader(f"Invoice Lines — {len(validated)} lines in PDF order")

    display_cols = [
        "machine_no",
        "charge_type",
        "hire_machine_raw",
        "machine_normalized",
        "quantity",
        "days",
        "billed_rate",
        "billed_amount",
        "expected_rate",
        "expected_amount",
        "variance_ex_gst",
        "expected_cpas",
        "in_lieu_cpas",
        "validation_result",
        "recommended_action",
    ]

    st.dataframe(
        [{k:r.get(k) for k in display_cols} for r in validated],
        use_container_width=True,
        hide_index=True,
    )

    exceptions = [r for r in validated if r.get("validation_result") not in ("PASS",)]
    st.subheader(f"Exceptions / Reviews — {len(exceptions)}")
    st.dataframe(
        [{k:r.get(k) for k in display_cols} for r in exceptions],
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download structured JSON",
        json.dumps({
            "header":header,
            "reconciliation":recon,
            "overall_status":status,
            "lines":validated,
        }, indent=2),
        file_name=f"PWCS_{header.get('invoice_number') or 'invoice'}_v3.json",
        mime="application/json",
    )

    with st.expander("Raw PDF text"):
        st.text(text)
