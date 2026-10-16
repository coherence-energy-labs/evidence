# ONE_Q release candidate B: measured two-use coding gain on IBM Kingston

**Status: PUBLIC EXPERIMENTAL EVIDENCE REVIEW CANDIDATE. Not peer reviewed; no physical superactivation claimed.**

This standalone archive re-scores **both** hardware layouts from an October 2026 IBM Kingston experiment measuring the first two points of an effective flagged qubit channel's coding-fidelity curve. It is deliberately not a release of the private ONE_Q controller or channel synthesis engine.

Run (Python 3.10+, no packages):

    python verify_counts.py

Optional independent bootstrap (NumPy):

    python -m pip install numpy
    python bootstrap.py

## What is contained

* All **22 circuits x 4,000 unpostselected shots** of both experimental designs (88,000 per layout). The v1 negative result **is included**.
* The fixed two-qubit decoder's three small effect matrices needed to re-score the fully flagged branch. These are numerical decoder data, not private source code.
* Independent standard-library rescorer that recomputes every four-branch fidelity term and refuses tampered, incomplete, or structurally inconsistent records. Results do not depend on accepting the original analysis field.
* Source job IDs, physical qubit layouts and source Git blob object IDs. The corresponding private ONE_Q source records are not available to anonymous users, so these identifiers **do not** independently authenticate the IBM provider job.
* Two manuscripts: one hardware evidence note and one public reviewer checklist.

## Honest result

| Layout | One use $F_e$ | Two uses $F_e$ | Gain | Outcome |
|---|---:|---:|---:|---|
| [149,148,147], first trial | 0.6360713 | 0.6279297 | -0.0081416 | Failed preregistered gain test |
| [148,149,150], follow-up | 0.6349800 | 0.6611136 | +0.0261336 | Positive follow-up gain |

The original follow-up study reported a bootstrap 95% interval [0.0226918, 0.0296038] for the second gain. A *new*, independently seeded shot-level multinomial resampling in this package gives similar numbers. These intervals assume the described sampling process and may not account for drift/shared twirl errors.

**The 2-use protocol runs an *effective flagged channel* on a physical IBM processor**. It does NOT realize both abstract zero-capacity channels of the underlying Smith-Yard construction as independent, verified, physical CPTP maps. The fully erased flag branch uses mathematically prescribed measure/prepare decoding scored from reference counts; it is not a physical quantum decoder applied in that branch. This is NOT experimental superactivation. The first-vs-second layout contrast is observational, not a randomized causal test.

## What remains before scientific publication

1. Public authentication of IBM jobs or operator-attested raw receipts and freeze timestamps, without exposing credentials. The release contains self-consistent count records, not a provider signature.
2. Freeze/preregistration text and original compiled QPY/ISA circuit bytes with independent bit-order analysis. Current `prereg_sha256` is a pointer to **private** source.
3. Review effect-matrix rounding, channel-branch weights, bootstrap treatment of shared twirls and temporal/device drift.
4. Compare novelty claims against the published primary channel/coding literature, especially Parentin et al., arXiv:2604.27042 (2026).
5. Institutional or external researcher reruns both analysis and a preregistered independent hardware replication.

## Attribution

Research and data: Joshua Philbrick / Coherence Energy Labs. Published-paper antecedent: Marco Parentin, Bjarne Bergh, Nilanjana Datta, and Mark M. Wilde (2026), *Onset of superactivation of quantum capacity*. This is a distinct subsequent *hardware investigation of an effective channel*, not an original demonstration of asymptotic quantum-capacity superactivation.
