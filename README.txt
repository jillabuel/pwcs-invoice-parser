PWCS Invoice Parser Prototype V3.2

Small transport-linking patch on top of V3.1.

NEW RULE:
- If a generic transport line (e.g. Boom Lift - A) has multiple possible hire rows,
  but every matching hire row is the SAME normalized machine size/type,
  the parser inherits that machine TYPE for rate + CPAS validation.
- It does NOT invent the exact asset number.
- Machine No displays: MULTIPLE / NOT LINKED
- If the transport rate matches that machine's PWCS rate card, Validation = PASS
  and Recommended Action = No action required.
- If multiple different sizes/types are present, it remains CHECK MACHINE LINK.

Expected for invoice 1000659527:
- Both hire rows = Diesel Knuckle Boom 135ft
- Collection = Diesel Knuckle Boom 135ft
- Machine No = MULTIPLE / NOT LINKED
- Billed transport = $280
- Expected transport = $280
- CPAS = 2115
- Variance = $0
- Validation = PASS
- Collection should disappear from Exceptions / Reviews

Install:
1. Extract ZIP
2. Copy app.py into your existing working PWCS_PDF_Parser_Prototype_V1 folder
3. Replace old app.py
4. Ctrl+C in Command Prompt
5. Run:
   .venv\Scripts\python.exe -m streamlit run app.py
6. Confirm heading says PWCS Invoice Parser Prototype — V3.2
