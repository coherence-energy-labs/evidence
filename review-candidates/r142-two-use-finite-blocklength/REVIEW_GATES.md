# Referee requirements for candidate A

The following are independently separable gates; a failed gate must block a corresponding claim.

| Gate | Evidence currently shipped | Status |
|---|---|---|
| A1: branch-level two-use fidelity and closed formula | stdlib `verify_closed.py`, exact rational arithmetic | PASS (within declared effective channel) |
| A2: closed-form threshold d=22 and monotonic extension | stdlib exact integer square-root enclosures | PASS |
| A3: finite-dimensional Choi PSD/TP/PPT and off-boundary rejection | independent NumPy script d=2..5 | PASS, **finite dims only** |
| A4: all-d PPT partial-transpose spectrum from two independent proofs | algebraic statement from private R142; public finite-dimensional examples | PENDING external proof |
| A5: exact local pre/postprocessing produces the flagged qubit channel at all d | private R142 mathematical derivation; separate small-d tests not bundled | PENDING independent referee |
| A6: explicit CPTP decoding instruments for every flag outcome | branch-level derivation; full maps not in minimal package | PENDING external proof |
| A7: independent rigorous optimized-code witness at d20,21 | private summaries only; **not** shipped | BLOCKED; not claimed |
| A8: exhaustive current prior-art review with intellectual property clearance | dated selective literature notes | PENDING |
| A9: unrelated hardware or engineering claims | none | NOT CLAIMED |

**Do not publicize “two-use superactivation proven” as an unqualified statement until A4-A6 are independently passed.**
